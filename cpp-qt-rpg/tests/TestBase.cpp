#include "TestBase.h"
#include <QDebug>

// Include model headers
#include "models/Item.h"
#include "models/Skill.h"

Player* TestBase::createTestPlayer(const QString& name,
                                 const QString& characterClass,
                                 int level,
                                 int gold)
{
    Player* player = new Player(name, characterClass);
    player->level = level;
    player->gold = gold;
    player->health = player->maxHealth; // Ensure full health

    addToCleanup(player);
    return player;
}

Monster* TestBase::createTestMonster(const QString& name,
                                   int level,
                                   int health)
{
    Monster* monster = new Monster(name, level);
    monster->health = health;
    monster->maxHealth = health;

    addToCleanup(monster);
    return monster;
}

Game* TestBase::createTestGame(const QString& playerName,
                              const QString& characterClass)
{
    Game* game = new Game(nullptr);
    game->newGame(playerName, characterClass);

    addToCleanup(game);
    return game;
}

Item* TestBase::createTestItem(const QString& itemName)
{
    Item* item = ItemFactory::createItem(itemName);
    if (item) {
        addToCleanup(item);
    }
    return item;
}

void TestBase::addToCleanup(void* obj)
{
    if (obj && !testObjects.contains(obj)) {
        testObjects.append(obj);
    }
}

void TestBase::cleanupTestObjects()
{
    for (void* obj : testObjects) {
        delete obj;
    }
    testObjects.clear();
}

void TestBase::cleanup()
{
    cleanupTestObjects();
}
