#include <QtTest/QtTest>
#include <vector>
#include "../src/persistence/SaveManager.h"
#include "../src/models/Player.h"
#include "../src/game/factories/ItemFactory.h"
#include "../src/models/Skill.h"
#include <vector>

class TestPersistence : public QObject
{
    Q_OBJECT

private slots:
    void testSaveLoadGame();
    void testSaveToSlot();
    void testLoadFromSlot();
    void testDeleteSlot();
    void testGetSaveSlots();
    void testSlotBoundaries();
    void testSlotOverwrite();
    void testEmptySlotLoad();
    void testCharacterClassSerialization();
    void testSkillSerialization();
    void testEquipmentSerialization();
    void cleanup();

private:
    void cleanupTestSlots();
};

void TestPersistence::cleanupTestSlots()
{
    SaveManager saveManager;
    for (int i = 1; i <= 10; ++i) {
        saveManager.deleteSaveSlot(i);
    }
}

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

void TestPersistence::testSaveToSlot()
{
    SaveManager saveManager;
    Player *player = new Player("SlotTest", "Warrior");
    player->gold = 1000;
    player->level = 10;

    // Test saving to slot
    QVERIFY(saveManager.saveToSlot(player, 1));

    // Verify slot info
    SaveSlotInfo info = saveManager.getSlotInfo(1);
    QVERIFY(info.exists);
    QCOMPARE(info.characterName, QString("SlotTest"));
    QCOMPARE(info.level, 10);

    delete player;
}

void TestPersistence::testLoadFromSlot()
{
    SaveManager saveManager;
    Player *player = new Player("LoadTest", "Mage");
    player->gold = 2000;
    player->level = 15;

    // Save to slot
    QVERIFY(saveManager.saveToSlot(player, 2));

    // Load from slot
    Player *loaded = saveManager.loadFromSlot(2);
    QVERIFY(loaded != nullptr);
    QCOMPARE(loaded->name, QString("LoadTest"));
    QCOMPARE(loaded->characterClass, QString("Mage"));
    QCOMPARE(loaded->gold, 2000);
    QCOMPARE(loaded->level, 15);

    delete player;
    delete loaded;
}

void TestPersistence::testDeleteSlot()
{
    SaveManager saveManager;
    Player *player = new Player("DeleteTest");

    // Save to slot
    QVERIFY(saveManager.saveToSlot(player, 3));
    QVERIFY(saveManager.getSlotInfo(3).exists);

    // Delete slot
    QVERIFY(saveManager.deleteSaveSlot(3));
    SaveSlotInfo info = saveManager.getSlotInfo(3);
    QVERIFY(!info.exists);

    delete player;
}

void TestPersistence::testGetSaveSlots()
{
    SaveManager saveManager;

    // Create saves in multiple slots
    Player *p1 = new Player("Player1", "Warrior");
    Player *p2 = new Player("Player2", "Mage");
    Player *p3 = new Player("Player3", "Rogue");

    saveManager.saveToSlot(p1, 1);
    saveManager.saveToSlot(p2, 5);
    saveManager.saveToSlot(p3, 10);

    // Get all slots
    auto save_slots = saveManager.getSaveSlots();
    QCOMPARE((int)save_slots.size(), 10);

    // Verify specific slots
    QVERIFY(save_slots[0].exists);
    QCOMPARE(save_slots[0].characterName, QString("Player1"));
    QVERIFY(save_slots[4].exists);
    QCOMPARE(save_slots[4].characterName, QString("Player2"));
    QVERIFY(save_slots[9].exists);
    QCOMPARE(save_slots[9].characterName, QString("Player3"));

    // Verify empty slots
    QVERIFY(!save_slots[1].exists);
    QVERIFY(!save_slots[2].exists);

    delete p1;
    delete p2;
    delete p3;
}

void TestPersistence::testSlotBoundaries()
{
    SaveManager saveManager;
    Player *player = new Player("BoundaryTest");

    // Test invalid slot numbers
    QVERIFY(!saveManager.saveToSlot(player, 0));
    QVERIFY(!saveManager.saveToSlot(player, -1));
    QVERIFY(!saveManager.saveToSlot(player, 11));
    QVERIFY(!saveManager.saveToSlot(player, 100));

    // Test valid boundaries
    QVERIFY(saveManager.saveToSlot(player, 1));
    QVERIFY(saveManager.saveToSlot(player, 10));

    delete player;
}

void TestPersistence::testSlotOverwrite()
{
    SaveManager saveManager;
    Player *player1 = new Player("Original", "Warrior");
    player1->gold = 100;

    Player *player2 = new Player("Overwrite", "Mage");
    player2->gold = 500;

    // Save first player
    QVERIFY(saveManager.saveToSlot(player1, 4));
    SaveSlotInfo info1 = saveManager.getSlotInfo(4);
    QCOMPARE(info1.characterName, QString("Original"));

    // Overwrite with second player
    QVERIFY(saveManager.saveToSlot(player2, 4));
    SaveSlotInfo info2 = saveManager.getSlotInfo(4);
    QCOMPARE(info2.characterName, QString("Overwrite"));

    // Verify loaded data is from second player
    Player *loaded = saveManager.loadFromSlot(4);
    QVERIFY(loaded != nullptr);
    QCOMPARE(loaded->name, QString("Overwrite"));
    QCOMPARE(loaded->gold, 500);

    delete player1;
    delete player2;
    delete loaded;
}

void TestPersistence::testEmptySlotLoad()
{
    SaveManager saveManager;

    // Ensure slot is empty
    saveManager.deleteSaveSlot(7);

    // Try to load from empty slot
    Player *loaded = saveManager.loadFromSlot(7);
    QVERIFY(loaded == nullptr);
}

void TestPersistence::testCharacterClassSerialization()
{
    SaveManager saveManager;

    // Test each character class
    QStringList classes = {"Warrior", "Mage", "Rogue"};
    int slot = 1;

    for (const QString &className : classes) {
        Player *player = new Player("TestChar", className);
        QVERIFY(saveManager.saveToSlot(player, slot));

        Player *loaded = saveManager.loadFromSlot(slot);
        QVERIFY(loaded != nullptr);
        QCOMPARE(loaded->characterClass, className);

        delete player;
        delete loaded;
        slot++;
    }
}

void TestPersistence::testSkillSerialization()
{
    SaveManager saveManager;
    Player *player = new Player("SkillTest");

    // Add skills
    Skill *skill1 = new Skill("Fireball", "magic", 50, 20, "A powerful fire spell");
    Skill *skill2 = new Skill("Sword Slash", "physical", 30, 10, "A basic sword attack");
    player->learnSkill(skill1);
    player->learnSkill(skill2);

    // Save and load
    QVERIFY(saveManager.saveToSlot(player, 8));
    Player *loaded = saveManager.loadFromSlot(8);

    // Verify skills
    QVERIFY(loaded != nullptr);
    QCOMPARE(loaded->skills.size(), 2);
    QVERIFY(loaded->hasSkill("Fireball"));
    QVERIFY(loaded->hasSkill("Sword Slash"));

    Skill *loadedSkill = loaded->getSkill("Fireball");
    QVERIFY(loadedSkill != nullptr);
    QCOMPARE(loadedSkill->damage, 50);
    QCOMPARE(loadedSkill->manaCost, 20);

    delete player;
    delete loaded;
}

void TestPersistence::testEquipmentSerialization()
{
    SaveManager saveManager;
    Player *player = new Player("EquipTest");

    // Equip items
    Item *weapon = ItemFactory::createItem("Iron Sword");
    Item *armor = ItemFactory::createItem("Leather Armor");
    player->equipItem(weapon);
    player->equipItem(armor);

    // Save and load
    QVERIFY(saveManager.saveToSlot(player, 9));
    Player *loaded = saveManager.loadFromSlot(9);

    // Verify equipment
    QVERIFY(loaded != nullptr);
    QVERIFY(loaded->equipment.contains("weapon"));
    QVERIFY(loaded->equipment["weapon"] != nullptr);
    QCOMPARE(loaded->equipment["weapon"]->name, QString("Iron Sword"));

    QVERIFY(loaded->equipment.contains("armor"));
    QVERIFY(loaded->equipment["armor"] != nullptr);
    QCOMPARE(loaded->equipment["armor"]->name, QString("Leather Armor"));

    delete player;
    delete loaded;
}

void TestPersistence::cleanup()
{
    cleanupTestSlots();
}

QTEST_MAIN(TestPersistence)
#include "test_persistence.moc"
