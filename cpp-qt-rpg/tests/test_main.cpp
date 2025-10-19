#include <QTest>
#include "../src/MainWindow.h"

class TestMainWindow : public QObject
{
    Q_OBJECT

private slots:
    void testWindowTitle();
};

void TestMainWindow::testWindowTitle()
{
    MainWindow window;
    QCOMPARE(window.windowTitle(), QString("Pyrpg-Qt"));
}

QTEST_MAIN(TestMainWindow)
#include "test_main.moc"
