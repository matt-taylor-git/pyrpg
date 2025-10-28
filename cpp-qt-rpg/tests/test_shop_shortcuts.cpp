#include <QTest>
#include <QSignalSpy>
#include "../src/views/ShopPage.h"
#include "../src/models/Player.h"

class TestShopShortcuts : public QObject
{
    Q_OBJECT

private slots:
    void testESCKeyLeavesShop();
    // TODO: Add more tests for arrow navigation when implemented
};

void TestShopShortcuts::testESCKeyLeavesShop()
{
    ShopPage page;
    Player player("Test");
    page.updateShop(&player);

    QSignalSpy spy(&page, &ShopPage::leaveRequested);

    // Simulate ESC key
    QKeyEvent keyPress(QEvent::KeyPress, Qt::Key_Escape, Qt::NoModifier);
    QCoreApplication::sendEvent(&page, &keyPress);

    QCOMPARE(spy.count(), 1);
}

QTEST_MAIN(TestShopShortcuts)
#include "test_shop_shortcuts.moc"
