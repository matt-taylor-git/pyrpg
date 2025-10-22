#ifndef GAME_H
#define GAME_H

#include "../models/Player.h"
#include "../models/Monster.h"
#include "../persistence/SaveManager.h"
#include <QObject>

class Game : public QObject
{
Q_OBJECT

public:
explicit Game(QObject *parent = nullptr);
void newGame(const QString &playerName);
Player* getPlayer();
Monster* getCurrentMonster();
bool saveGame(const QString &filePath);
    bool loadGame(const QString &filePath);

// Combat
void startCombat();
    QString playerAttack();
    QString monsterAttack();
bool isCombatOver();
    QString getCombatResult();

private:
    Player *player;
    Monster *currentMonster;
    bool combatActive;
    QString combatLog;
    SaveManager saveManager;

private:
    // This will hold the main game state logic
};

#endif // GAME_H
