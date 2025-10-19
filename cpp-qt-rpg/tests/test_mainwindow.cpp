#include <QTest>
#include "MainWindow.h"

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
#include "test_mainwindow.moc"
