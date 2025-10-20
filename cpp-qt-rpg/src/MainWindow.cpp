#include "MainWindow.h"
#include "views/NewGameView.h"
#include "views/CharacterCustomizationPage.h"
#include "views/AdventurePage.h"
#include "views/CombatPage.h"
#include "views/InventoryPage.h"
#include "views/MonsterStatsPage.h"
#include "views/SaveLoadPage.h"
#include "views/ShopPage.h"
#include "views/StatsPage.h"
#include "game/Game.h"
#include <QStackedWidget>
#include <QWidget>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Pyrpg-Qt");
    resize(800, 600);

    stackedWidget = new QStackedWidget(this);
    setCentralWidget(stackedWidget);

    // Main Menu View (placeholder)
    QWidget *mainMenuView = new QWidget();
    mainMenuView->setStyleSheet("background-color: #333;");
    stackedWidget->addWidget(mainMenuView);

    // New Game View
    m_newGameView = new NewGameView();
    connect(m_newGameView, &NewGameView::characterCreated, this, &MainWindow::handleCharacterCreation);
    stackedWidget->addWidget(m_newGameView);

    // Character Customization Page
    m_characterCustomizationPage = new CharacterCustomizationPage();
    stackedWidget->addWidget(m_characterCustomizationPage);

    // Adventure Page
    m_adventurePage = new AdventurePage();
    connect(m_adventurePage, &AdventurePage::exploreClicked, this, &MainWindow::handleExploreClicked);
    connect(m_adventurePage, &AdventurePage::restClicked, this, &MainWindow::handleRestClicked);
    connect(m_adventurePage, &AdventurePage::quitClicked, this, &MainWindow::handleQuitClicked);
    connect(m_adventurePage, &AdventurePage::viewStatsClicked, this, &MainWindow::handleViewStatsClicked);
    stackedWidget->addWidget(m_adventurePage);

    // Combat Page
    m_combatPage = new CombatPage();
    connect(m_combatPage, &CombatPage::attackClicked, this, &MainWindow::handleAttackClicked);
    connect(m_combatPage, &CombatPage::skillClicked, this, &MainWindow::handleSkillClicked);
    connect(m_combatPage, &CombatPage::itemClicked, this, &MainWindow::handleItemClicked);
    connect(m_combatPage, &CombatPage::statsClicked, this, &MainWindow::handleStatsClicked);
    connect(m_combatPage, &CombatPage::runClicked, this, &MainWindow::handleRunClicked);
    stackedWidget->addWidget(m_combatPage);

    // Inventory Page
    m_inventoryPage = new InventoryPage();
    stackedWidget->addWidget(m_inventoryPage);

    // Monster Stats Page
    m_monsterStatsPage = new MonsterStatsPage();
    stackedWidget->addWidget(m_monsterStatsPage);

    // Save Load Page
    m_saveLoadPage = new SaveLoadPage();
    connect(m_saveLoadPage, &SaveLoadPage::quickSaveRequested, this, &MainWindow::handleQuickSave);
    connect(m_saveLoadPage, &SaveLoadPage::quickLoadRequested, this, &MainWindow::handleQuickLoad);
    connect(m_saveLoadPage, &SaveLoadPage::saveToFileRequested, this, &MainWindow::handleSaveToFile);
    connect(m_saveLoadPage, &SaveLoadPage::loadFromFileRequested, this, &MainWindow::handleLoadFromFile);
    connect(m_saveLoadPage, &SaveLoadPage::newSaveRequested, this, &MainWindow::handleNewSave);
    stackedWidget->addWidget(m_saveLoadPage);

    // Shop Page
    m_shopPage = new ShopPage();
    stackedWidget->addWidget(m_shopPage);

    // Stats Page
    m_statsPage = new StatsPage();
    stackedWidget->addWidget(m_statsPage);

    // Set the initial view
    stackedWidget->setCurrentWidget(m_statsPage);

    m_game = new Game();
}

void MainWindow::handleCharacterCreation(const QString &name)
{
    m_game->newGame(name);
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleExploreClicked()
{
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleRestClicked()
{
    // Placeholder: Go to shop for now
    stackedWidget->setCurrentWidget(m_shopPage);
}

void MainWindow::handleQuitClicked()
{
    close();
}

void MainWindow::handleAttackClicked()
{
    stackedWidget->setCurrentWidget(m_inventoryPage);
}

void MainWindow::handleSkillClicked()
{
    stackedWidget->setCurrentWidget(m_inventoryPage);
}

void MainWindow::handleItemClicked()
{
    stackedWidget->setCurrentWidget(m_inventoryPage);
}

void MainWindow::handleStatsClicked()
{
    stackedWidget->setCurrentWidget(m_monsterStatsPage);
}

void MainWindow::handleRunClicked()
{
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleViewStatsClicked()
{
    m_statsPage->updateStats(m_game->getPlayer());
    stackedWidget->setCurrentWidget(m_statsPage);
}

void MainWindow::handleQuickSave()
{
    // For quick save, use a default file path, e.g., quicksave.dat
    QString filePath = "quicksave.dat";
    if (m_game->saveGame(filePath)) {
        // Optionally show success message
    }
}

void MainWindow::handleQuickLoad()
{
    QString filePath = "quicksave.dat";
    if (m_game->loadGame(filePath)) {
        // After loading, perhaps update UI or go to adventure page
        stackedWidget->setCurrentWidget(m_adventurePage);
    }
}

void MainWindow::handleSaveToFile(const QString &filePath)
{
    if (m_game->saveGame(filePath)) {
        // Optionally show success message
    }
}

void MainWindow::handleLoadFromFile(const QString &filePath)
{
    if (m_game->loadGame(filePath)) {
        stackedWidget->setCurrentWidget(m_adventurePage);
    }
}

void MainWindow::handleNewSave()
{
    // Perhaps start a new game or something, but for now, maybe go to new game view
    stackedWidget->setCurrentWidget(m_newGameView);
}

MainWindow::~MainWindow()
{
}
