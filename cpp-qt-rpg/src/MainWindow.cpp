#include "MainWindow.h"
#include <QStackedWidget>
#include <QWidget>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Pyrpg-Qt");
    resize(800, 600);

    stackedWidget = new QStackedWidget(this);
    setCentralWidget(stackedWidget);

    // Placeholder views
    QWidget *mainMenuView = new QWidget();
    mainMenuView->setStyleSheet("background-color: #333;");
    stackedWidget->addWidget(mainMenuView);

    QWidget *characterCreationView = new QWidget();
    characterCreationView->setStyleSheet("background-color: #444;");
    stackedWidget->addWidget(characterCreationView);

    QWidget *adventureView = new QWidget();
    adventureView->setStyleSheet("background-color: #555;");
    stackedWidget->addWidget(adventureView);

    // Set the initial view
    stackedWidget->setCurrentWidget(mainMenuView);
}

MainWindow::~MainWindow()
{
}
