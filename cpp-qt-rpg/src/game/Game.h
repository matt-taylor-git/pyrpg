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
    bool saveGame(const QString &filePath);
    bool loadGame(const QString &filePath);

private:
    Player *player;
    SaveManager saveManager;

private:
    // This will hold the main game state logic
};

#endif // GAME_H
