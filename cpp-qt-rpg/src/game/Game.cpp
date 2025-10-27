#include "Game.h"
#include "factories/MonsterFactory.h"
#include "factories/SkillFactory.h"
#include "factories/ItemFactory.h"
#include <QRandomGenerator>

Game::Game(QObject *parent)
: QObject(parent), player(nullptr), currentMonster(nullptr), combatActive(false)
{
}

void Game::newGame(const QString &playerName, const QString &characterClass)
{
    // Clean up old player object if it exists
    if (player) {
        delete player;
    }
    player = new Player(playerName, characterClass);

    // Give starting skills
    QList<Skill*> startingSkills = SkillFactory::getStartingSkills(characterClass);
    for (Skill* skill : startingSkills) {
        player->learnSkill(skill);
    }
}

Player* Game::getPlayer()
{
return player;
}

Monster* Game::getCurrentMonster()
{
    return currentMonster;
}

bool Game::saveGame(const QString &filePath)
{
    if (!player) return false;
    return saveManager.saveGame(player, filePath);
}

bool Game::loadGame(const QString &filePath)
{
Player *loadedPlayer = saveManager.loadGame(filePath);
if (!loadedPlayer) return false;
if (player) {
delete player;
}
player = loadedPlayer;
return true;
}

bool Game::saveToSlot(int slotNumber)
{
    if (!player) return false;
    return saveManager.saveToSlot(player, slotNumber);
}

bool Game::loadFromSlot(int slotNumber)
{
    Player *loadedPlayer = saveManager.loadFromSlot(slotNumber);
    if (!loadedPlayer) return false;
    if (player) {
        delete player;
    }
    player = loadedPlayer;
    return true;
}

bool Game::deleteSlot(int slotNumber)
{
    return saveManager.deleteSaveSlot(slotNumber);
}

// Combat
void Game::startCombat()
{
    // Create a random monster based on player level
    if (currentMonster) {
        delete currentMonster;
    }
    currentMonster = MonsterFactory::createRandomMonster(player->level);
    combatActive = true;
    combatLog = QString("Combat started! A %1 (Level %2) appears!").arg(currentMonster->name).arg(currentMonster->level);
}

QString Game::playerAttack()
{
    if (!combatActive || !currentMonster || !player) return "";

    bool critical = rollCritical(player->dexterity);
    int baseDamage = player->getTotalAttack();
    int damage = calculateDamage(baseDamage, player->level, currentMonster->defense, critical);

    currentMonster->health -= damage;

    if (critical) {
        combatLog = QString("**CRITICAL HIT!** You strike for %1 damage!").arg(damage);
    } else {
        combatLog = QString("You attack for %1 damage!").arg(damage);
    }

    if (currentMonster->health <= 0) {
        currentMonster->health = 0;
        combatLog += QString(" %1 defeated!").arg(currentMonster->name);
    }

    checkCombatEndAfterAction();
    return combatLog;
}

QString Game::playerUseSkill(Skill* skill)
{
    if (!combatActive || !currentMonster || !player || !skill) return "";

    // Check mana
    if (player->mana < skill->manaCost) {
        return "Not enough mana!";
    }

    player->mana -= skill->manaCost;

    if (skill->skillType == "physical") {
        bool critical = rollCritical(player->dexterity);
        int baseDamage = player->getTotalAttack() + skill->damage;
        int damage = calculateDamage(baseDamage, player->level, currentMonster->defense, critical);
        currentMonster->health -= damage;

        if (critical) {
            combatLog = QString("**CRITICAL!** %1 deals %2 damage!").arg(skill->name).arg(damage);
        } else {
            combatLog = QString("%1 deals %2 damage!").arg(skill->name).arg(damage);
        }
    }
    else if (skill->skillType == "magic") {
        int baseDamage = (player->intelligence * 2) + skill->damage;
        int damage = calculateDamage(baseDamage, player->level, currentMonster->defense / 2); // Magic ignores some defense
        currentMonster->health -= damage;
        combatLog = QString("%1 hits for %2 magic damage!").arg(skill->name).arg(damage);
    }
    else if (skill->skillType == "buff") {
        combatLog = QString("You use %1! (Effect lasts 3 turns)").arg(skill->name);
        // TODO: Implement buff system properly when status effects are added
    }

    if (currentMonster->health <= 0) {
        currentMonster->health = 0;
        combatLog += QString(" %1 defeated!").arg(currentMonster->name);
    }

    checkCombatEndAfterAction();
    return combatLog;
}

QString Game::playerUseItem(Item* item)
{
    if (!combatActive || !player || !item) return "";

    if (item->effect == "heal") {
        int oldHealth = player->health;
        player->useItem(item);
        int healed = player->health - oldHealth;
        return QString("Used %1! Restored %2 HP.").arg(item->name).arg(healed);
    }
    else if (item->effect == "restore_mana") {
        int oldMana = player->mana;
        player->useItem(item);
        int restored = player->mana - oldMana;
        return QString("Used %1! Restored %2 MP.").arg(item->name).arg(restored);
    }

    return "Item has no effect in combat.";
}

QString Game::monsterAttack()
{
    if (!combatActive || !currentMonster || !player) return "";

    int baseDamage = currentMonster->attack;
    int damage = calculateDamage(baseDamage, currentMonster->level, player->getTotalDefense());

    player->health -= damage;

    combatLog = QString("%1 attacks for %2 damage!").arg(currentMonster->name).arg(damage);

    if (player->health <= 0) {
        player->health = 0;
        combatLog += " You are defeated!";
    }

    checkCombatEndAfterAction();
    return combatLog;
}

bool Game::isCombatOver()
{
    return !combatActive;
}

QString Game::getCombatResult()
{
    if (!player || !currentMonster) return "";

    if (player->health <= 0) {
        return "Defeat";
    } else if (currentMonster->health <= 0) {
        return "Victory";
    }
    return "Ongoing";
}

void Game::endCombat()
{
    if (!combatActive) return;

    combatActive = false;

    // If player won, give rewards
    if (currentMonster && currentMonster->health <= 0 && player && player->health > 0) {
        giveCombatRewards();
    }
}

int Game::calculateDamage(int baseDamage, int attackerLevel, int defenderDefense, bool isCritical)
{
    // Base formula: damage = baseDamage * levelMultiplier - defense
    double levelMultiplier = 1.0 + (attackerLevel * 0.1);
    int damage = static_cast<int>(baseDamage * levelMultiplier) - defenderDefense;

    // Apply critical multiplier
    if (isCritical) {
        damage = static_cast<int>(damage * 1.75);
    }

    // Minimum damage is 1
    if (damage < 1) damage = 1;

    // Add some variance (±10%)
    int variance = QRandomGenerator::global()->bounded(damage / 5) - (damage / 10);
    damage += variance;

    return damage > 0 ? damage : 1;
}

bool Game::rollCritical(int dexterity)
{
    // Base crit chance: 5% + (dexterity * 0.5%)
    int critChance = 5 + (dexterity / 2);
    if (critChance > 50) critChance = 50; // Cap at 50%

    int roll = QRandomGenerator::global()->bounded(100);
    return roll < critChance;
}

void Game::giveCombatRewards()
{
    if (!player || !currentMonster) return;

    // Give experience
    int expGained = currentMonster->expReward;
    player->gainExperience(expGained);

    // Give gold
    int goldGained = currentMonster->goldReward;
    player->gold += goldGained;

    // Random loot drop (30% chance)
    int lootRoll = QRandomGenerator::global()->bounded(100);
    if (lootRoll < 30) {
        Item* loot = ItemFactory::generateRandomItem(currentMonster->level);
        if (loot) {
            player->inventory.append(loot);
            combatLog += QString("\nFound loot: %1!").arg(loot->name);
        }
    }

    combatLog += QString("\nGained %1 EXP and %2 gold!").arg(expGained).arg(goldGained);
}
void Game::checkCombatEndAfterAction()
{
    if (!combatActive) return;

    bool playerWon = (currentMonster && currentMonster->health <= 0);
    bool playerLost = (player && player->health <= 0);

    if (playerWon || playerLost) {
        endCombat();
        emit combatEnded(playerWon);
    }
}
