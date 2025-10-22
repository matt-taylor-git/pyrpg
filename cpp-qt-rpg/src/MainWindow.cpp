#include "MainWindow.h"
#include "views/MainMenu.h"
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
#include "components/SkillSelectionDialog.h"
#include "components/CombatItemDialog.h"
#include "components/CombatResultDialog.h"
#include "models/Player.h"
#include "models/Monster.h"
#include "models/Skill.h"
#include "models/Item.h"
#include <QStackedWidget>
#include <QWidget>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Pyrpg-Qt");
    resize(800, 600);

    stackedWidget = new QStackedWidget(this);
    setCentralWidget(stackedWidget);

    // Main Menu
    m_mainMenu = new MainMenu();
    connect(m_mainMenu, &MainMenu::newGameRequested, this, &MainWindow::handleMainMenuNewGame);
    connect(m_mainMenu, &MainMenu::loadGameRequested, this, &MainWindow::handleMainMenuLoadGame);
    connect(m_mainMenu, &MainMenu::exitRequested, this, &MainWindow::handleMainMenuExit);
    stackedWidget->addWidget(m_mainMenu);

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
    connect(m_adventurePage, &AdventurePage::inventoryClicked, this, &MainWindow::handleInventoryClicked);
    connect(m_adventurePage, &AdventurePage::shopClicked, this, &MainWindow::handleShopClicked);
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
    connect(m_inventoryPage, &InventoryPage::backRequested, this, &MainWindow::handleInventoryBack);
    stackedWidget->addWidget(m_inventoryPage);

    // Monster Stats Page
    m_monsterStatsPage = new MonsterStatsPage();
    connect(m_monsterStatsPage, &MonsterStatsPage::backRequested, this, &MainWindow::handleMonsterStatsBack);
    stackedWidget->addWidget(m_monsterStatsPage);

    // Save Load Page
    m_saveLoadPage = new SaveLoadPage();
    connect(m_saveLoadPage, &SaveLoadPage::quickSaveRequested, this, &MainWindow::handleQuickSave);
    connect(m_saveLoadPage, &SaveLoadPage::quickLoadRequested, this, &MainWindow::handleQuickLoad);
    connect(m_saveLoadPage, &SaveLoadPage::saveToFileRequested, this, &MainWindow::handleSaveToFile);
    connect(m_saveLoadPage, &SaveLoadPage::loadFromFileRequested, this, &MainWindow::handleLoadFromFile);
    connect(m_saveLoadPage, &SaveLoadPage::newSaveRequested, this, &MainWindow::handleNewSave);
    connect(m_saveLoadPage, &SaveLoadPage::backRequested, this, &MainWindow::handleSaveLoadBack);
    stackedWidget->addWidget(m_saveLoadPage);

    // Shop Page
    m_shopPage = new ShopPage();
    connect(m_shopPage, &ShopPage::leaveRequested, this, &MainWindow::handleShopLeave);
    stackedWidget->addWidget(m_shopPage);

    // Stats Page
    m_statsPage = new StatsPage();
    connect(m_statsPage, &StatsPage::backRequested, this, &MainWindow::handleStatsBack);
    stackedWidget->addWidget(m_statsPage);

    // Set the initial view
    stackedWidget->setCurrentWidget(m_mainMenu);

    m_game = new Game();
}

void MainWindow::handleCharacterCreation(const QString &name, const QString &characterClass)
{
    m_game->newGame(name, characterClass);
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleExploreClicked()
{
m_game->startCombat();
    m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), "");
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleRestClicked()
{
    // Rest to restore health/mana
    Player *player = m_game->getPlayer();
    if (player) {
        player->health = player->maxHealth;
        player->mana = player->maxMana;
        QMessageBox::information(this, "Rest", "You rest and restore your health and mana!");
    }
}

void MainWindow::handleInventoryClicked()
{
    m_inventoryPage->updateInventory(m_game->getPlayer());
    stackedWidget->setCurrentWidget(m_inventoryPage);
}

void MainWindow::handleShopClicked()
{
    m_shopPage->updateShop(m_game->getPlayer());
    stackedWidget->setCurrentWidget(m_shopPage);
}

void MainWindow::handleQuitClicked()
{
    close();
}

void MainWindow::handleAttackClicked()
{
    int oldLevel = m_game->getPlayer()->level;
    QString log = m_game->playerAttack();
    m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), log);

    if (m_game->isCombatOver()) {
        handleCombatEnd(oldLevel);
    } else {
        // Monster turn
        QString monsterLog = m_game->monsterAttack();
        m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), monsterLog);

        if (m_game->isCombatOver()) {
            handleCombatEnd(oldLevel);
        }
    }
}

void MainWindow::handleSkillClicked()
{
    // Open skill selection dialog
    SkillSelectionDialog dialog(m_game->getPlayer(), this);
    if (dialog.exec() == QDialog::Accepted) {
        Skill *selectedSkill = dialog.getSelectedSkill();
        if (selectedSkill) {
            int oldLevel = m_game->getPlayer()->level;
            QString log = m_game->playerUseSkill(selectedSkill);
            m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), log);

            if (m_game->isCombatOver()) {
                handleCombatEnd(oldLevel);
            } else {
                // Monster turn
                QString monsterLog = m_game->monsterAttack();
                m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), monsterLog);

                if (m_game->isCombatOver()) {
                    handleCombatEnd(oldLevel);
                }
            }
        }
    }
}

void MainWindow::handleItemClicked()
{
    // Open combat item dialog
    CombatItemDialog dialog(m_game->getPlayer(), this);
    if (dialog.exec() == QDialog::Accepted) {
        Item *selectedItem = dialog.getSelectedItem();
        if (selectedItem) {
            QString log = m_game->playerUseItem(selectedItem);
            m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), log);
            // Item use doesn't end player's turn, no monster attack
        }
    }
}

void MainWindow::handleStatsClicked()
{
    // Show player stats, not monster stats
    m_statsPage->updateStats(m_game->getPlayer());
    stackedWidget->setCurrentWidget(m_statsPage);
}

void MainWindow::handleCombatEnd(int oldLevel)
{
    m_game->endCombat();
    bool victory = m_game->getCombatResult() == "Victory";

    if (victory) {
        Monster *monster = m_game->getCurrentMonster();
        bool leveledUp = m_game->getPlayer()->level > oldLevel;

        // Show combat result dialog
        CombatResultDialog resultDialog(
            true,
            monster ? monster->expReward : 0,
            monster ? monster->goldReward : 0,
            "",  // Loot message will be in combat log
            leveledUp,
            this
        );
        resultDialog.exec();
    } else {
        // Defeat
        CombatResultDialog resultDialog(false, 0, 0, "", false, this);
        resultDialog.exec();
    }

    stackedWidget->setCurrentWidget(m_adventurePage);
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
    stackedWidget->setCurrentWidget(m_newGameView);
}

void MainWindow::handleMainMenuNewGame()
{
    stackedWidget->setCurrentWidget(m_newGameView);
}

void MainWindow::handleMainMenuLoadGame()
{
    stackedWidget->setCurrentWidget(m_saveLoadPage);
}

void MainWindow::handleMainMenuExit()
{
    close();
}

void MainWindow::handleInventoryBack()
{
    // Back to adventure page
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleShopLeave()
{
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleStatsBack()
{
    stackedWidget->setCurrentWidget(m_adventurePage);
}

void MainWindow::handleMonsterStatsBack()
{
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleSaveLoadBack()
{
    stackedWidget->setCurrentWidget(m_mainMenu);
}

MainWindow::~MainWindow()
{
}
