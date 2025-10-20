#ifndef GAME_H
#define GAME_H

#include "../models/Player.h"
#include "../models/Monster.h"
#include <QObject>

class Game : public QObject
{
    Q_OBJECT

public:
    explicit Game(QObject *parent = nullptr);
    void newGame(const QString &playerName);
    Player* getPlayer();

private:
    Player *player;

private:
    // This will hold the main game state logic
};

#endif // GAME_H
