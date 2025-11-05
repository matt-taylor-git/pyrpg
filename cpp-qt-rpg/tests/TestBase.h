#pragma once

#include <QObject>
#include <QList>
#include <QString>
#include "models/Player.h"
#include "models/Monster.h"
#include "game/Game.h"
#include "game/factories/ItemFactory.h"
#include "game/factories/MonsterFactory.h"

/**
 * Base class for all test classes providing common functionality
 * for creating test objects and managing cleanup.
 */
class TestBase : public QObject
{
    Q_OBJECT

protected:
    // Test object creation helpers
    Player* createTestPlayer(const QString& name = "TestPlayer",
                           const QString& characterClass = "Warrior",
                           int level = 1,
                           int gold = 100);

    Monster* createTestMonster(const QString& name = "TestMonster",
                             int level = 1,
                             int health = 50);

    Game* createTestGame(const QString& playerName = "TestPlayer",
                        const QString& characterClass = "Warrior");

    Item* createTestItem(const QString& itemName);

    // Memory management
    QList<void*> testObjects;

    // Cleanup helpers
    void addToCleanup(void* obj);
    void cleanupTestObjects();

private slots:
    void cleanup();
};
