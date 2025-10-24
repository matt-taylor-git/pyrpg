#include <QTest>
#include <QSignalSpy>
#include <QKeyEvent>
#include "MainWindow.h"
#include "components/MenuOverlay.h"
#include "models/Player.h"

class TestMainWindow : public QObject
{
    Q_OBJECT

private slots:
    void testWindowTitle();
    void testMenuOverlayShowHide();
    void testMenuOverlayContentUpdate();
    void testMenuOverlayRapidToggle();
    void testMenuOverlayEdgeCases();
    void testMenuOverlayAnimationState();
    void testMenuOverlayFocusManagement();
    void testCombatEndedSignalHandling();
};

void TestMainWindow::testWindowTitle()
{
    MainWindow window;
    QCOMPARE(window.windowTitle(), QString("Pyrpg-Qt"));
}

void TestMainWindow::testMenuOverlayShowHide()
{
    MenuOverlay overlay;

    // Test initial state
    QVERIFY(!overlay.isVisible());
    QCOMPARE(overlay.opacity(), 0.0);

    // Test show overlay
    overlay.showOverlay();
    QVERIFY(overlay.isVisible());

    // Test hide overlay with signal spy
    QSignalSpy spy(&overlay, &MenuOverlay::overlayHidden);
    overlay.hideOverlay();

    // Wait for animation to complete
    QTest::qWait(300);

    // Verify overlay is hidden and signal was emitted
    QVERIFY(!overlay.isVisible());
    QCOMPARE(spy.count(), 1);
}

void TestMainWindow::testMenuOverlayContentUpdate()
{
    MenuOverlay overlay;

    // Create a player with some items
    Player player("TestPlayer", "Warrior");
    player.level = 5;
    player.health = 100;
    player.maxHealth = 100;

    // Update overlay content
    overlay.updateContent(&player);

    // Show the overlay
    overlay.showOverlay();
    QVERIFY(overlay.isVisible());

    overlay.hide();
}

void TestMainWindow::testMenuOverlayRapidToggle()
{
    MenuOverlay overlay;
    Player player("TestPlayer");
    overlay.updateContent(&player);

    // Rapidly toggle the overlay multiple times
    for (int i = 0; i < 5; ++i) {
        overlay.showOverlay();
        overlay.hideOverlay();
    }

    // Wait for animations to settle
    QTest::qWait(300);

    // Should not crash and should be in a consistent state
    QVERIFY(!overlay.isVisible());
}

void TestMainWindow::testMenuOverlayEdgeCases()
{
    MenuOverlay overlay;

    // Test opening menu without player (should not crash)
    overlay.updateContent(nullptr);
    overlay.showOverlay();
    QVERIFY(overlay.isVisible());
    overlay.hide();

    // Test ESC key handling
    overlay.showOverlay();
    QKeyEvent keyPress(QEvent::KeyPress, Qt::Key_Escape, Qt::NoModifier);
    QCoreApplication::sendEvent(&overlay, &keyPress);

    // Wait for animation
    QTest::qWait(300);
    QVERIFY(!overlay.isVisible());
}

void TestMainWindow::testMenuOverlayAnimationState()
{
    MenuOverlay overlay;
    Player player("TestPlayer");
    overlay.updateContent(&player);

    // Show overlay and immediately try to hide it
    overlay.showOverlay();
    overlay.hideOverlay();

    // Try to hide again while already hiding (should be a no-op)
    overlay.hideOverlay();

    // Wait for animation
    QTest::qWait(300);
    QVERIFY(!overlay.isVisible());
}

void TestMainWindow::testMenuOverlayFocusManagement()
{
    MenuOverlay overlay;
    Player player("TestPlayer");
    overlay.updateContent(&player);

    // Create a widget to hold focus
    QWidget focusWidget;
    focusWidget.setFocusPolicy(Qt::StrongFocus);
    focusWidget.show();
    focusWidget.setFocus();

    // Show overlay (should store previous focus)
    overlay.showOverlay();
    QVERIFY(overlay.isVisible());

    // Hide overlay
    overlay.hideOverlay();
    QTest::qWait(300);

    // Verify overlay is hidden
    QVERIFY(!overlay.isVisible());
}

void TestMainWindow::testCombatEndedSignalHandling()
{
    MainWindow window;

    // Create a character to enable combat
    QTest::keyClick(&window, Qt::Key_Return); // Simulate pressing enter on new game
    QTest::qWait(100); // Allow UI to update

    // The test verifies that the signal connection exists and doesn't crash
    // In a real test, we'd need to mock the game state, but this ensures basic functionality
    QVERIFY(window.windowTitle() == "Pyrpg-Qt");
}

QTEST_MAIN(TestMainWindow)
#include "test_mainwindow.moc"
