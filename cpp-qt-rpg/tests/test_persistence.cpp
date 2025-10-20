#include <QtTest/QtTest>
#include "../src/persistence/SaveManager.h"
#include "../src/models/Player.h"
#include "../src/game/factories/ItemFactory.h"

class TestPersistence : public QObject
{
    Q_OBJECT

private slots:
    void testSaveLoadGame();
};

void TestPersistence::testSaveLoadGame()
{
    // Setup
    Player *originalPlayer = new Player("TestHero");
    originalPlayer->gold = 500;
    originalPlayer->level = 5;
    originalPlayer->inventory.append(ItemFactory::createItem("Iron Sword"));

    SaveManager saveManager;
    const QString saveFilePath = "test_save.dat";

    // Save the game
    bool saveSuccess = saveManager.saveGame(originalPlayer, saveFilePath);
    QVERIFY(saveSuccess);

    // Load the game
    Player *loadedPlayer = saveManager.loadGame(saveFilePath);
    QVERIFY(loadedPlayer != nullptr);

    // Verify data
    QCOMPARE(loadedPlayer->name, originalPlayer->name);
    QCOMPARE(loadedPlayer->gold, originalPlayer->gold);
    QCOMPARE(loadedPlayer->level, originalPlayer->level);
    QCOMPARE(loadedPlayer->inventory.size(), originalPlayer->inventory.size());
    QCOMPARE(loadedPlayer->inventory.first()->name, originalPlayer->inventory.first()->name);

    // Cleanup
    delete originalPlayer;
    delete loadedPlayer;
    QFile::remove(saveFilePath);
}

QTEST_MAIN(TestPersistence)
#include "test_persistence.moc"
