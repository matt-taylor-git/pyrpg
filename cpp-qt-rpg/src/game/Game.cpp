#include "Game.h"

Game::Game(QObject *parent)
: QObject(parent), player(nullptr), currentMonster(nullptr), combatActive(false)
{
}

void Game::newGame(const QString &playerName)
{
    // Clean up old player object if it exists
    if (player) {
        delete player;
    }
    player = new Player(playerName);
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

// Combat
void Game::startCombat()
{
    // Create a simple monster
    if (currentMonster) {
        delete currentMonster;
    }
    currentMonster = new Monster("Goblin", 1, "goblin");
    combatActive = true;
    combatLog = "Combat started! A Goblin appears.";
}

QString Game::playerAttack()
{
    if (!combatActive || !currentMonster) return "";

    int damage = player->strength; // Simple damage
    currentMonster->health -= damage;
    combatLog = QString("You attack for %1 damage!").arg(damage);

    if (currentMonster->health <= 0) {
        combatActive = false;
        combatLog += " Monster defeated!";
    }

    return combatLog;
}

QString Game::monsterAttack()
{
    if (!combatActive || !currentMonster) return "";

    int damage = currentMonster->level * 5; // Simple
    player->health -= damage;
    combatLog = QString("Monster attacks for %1 damage!").arg(damage);

    if (player->health <= 0) {
        combatActive = false;
        combatLog += " You are defeated!";
    }

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
