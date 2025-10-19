#include <QTest>
#include "models/Player.h"
#include "models/Monster.h"
#include "game/factories/ItemFactory.h"

class TestModels : public QObject
{
    Q_OBJECT

private slots:
    void testPlayerCreation();
    void testMonsterCreation();
    void testItemFactory();
};

void TestModels::testPlayerCreation()
{
    Player player("Hero");
    QCOMPARE(player.name, QString("Hero"));
    QCOMPARE(player.level, 1);
    QCOMPARE(player.health, 100);
    QCOMPARE(player.gold, 100);
}

void TestModels::testMonsterCreation()
{
    Monster monster("Goblin", 5);
    QCOMPARE(monster.name, QString("Goblin"));
    QCOMPARE(monster.level, 5);
    QVERIFY(monster.health > 50);
}

void TestModels::testItemFactory()
{
    QMap<QString, Item*> shopItems = ItemFactory::getShopItems();
    QVERIFY(shopItems.contains("Health Potion"));
    QCOMPARE(shopItems["Health Potion"]->value, 25);
    qDeleteAll(shopItems);
}

QTEST_MAIN(TestModels)
#include "test_models.moc"
