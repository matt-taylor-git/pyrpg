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
