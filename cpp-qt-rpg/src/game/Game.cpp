#include "Game.h"

Game::Game(QObject *parent)
    : QObject(parent), player(nullptr)
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
