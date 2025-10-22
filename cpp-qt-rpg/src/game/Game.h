#ifndef GAME_H
#define GAME_H

#include "../models/Player.h"
#include "../models/Monster.h"
#include "../models/Skill.h"
#include "../persistence/SaveManager.h"
#include <QObject>

class Game : public QObject
{
Q_OBJECT

public:
explicit Game(QObject *parent = nullptr);
void newGame(const QString &playerName, const QString &characterClass = "Hero");
Player* getPlayer();
Monster* getCurrentMonster();
bool saveGame(const QString &filePath);
    bool loadGame(const QString &filePath);

// Combat
void startCombat();
    QString playerAttack();
    QString playerUseSkill(Skill* skill);
    QString playerUseItem(Item* item);
    QString monsterAttack();
bool isCombatOver();
    QString getCombatResult();
    void endCombat();

private:
    Player *player;
    Monster *currentMonster;
    bool combatActive;
    QString combatLog;
    SaveManager saveManager;

    // Combat helpers
    int calculateDamage(int baseDamage, int attackerLevel, int defenderDefense, bool isCritical = false);
    bool rollCritical(int dexterity);
    void giveCombatRewards();
};

#endif // GAME_H
