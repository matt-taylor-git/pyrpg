#include "MainWindow.h"
#include "views/MainMenu.h"
#include "views/NewGameView.h"
#include "views/CharacterCustomizationPage.h"

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
#include "components/MenuOverlay.h"
#include "models/Player.h"
#include "models/Monster.h"
#include "models/Skill.h"
#include "models/Item.h"
#include <QStackedWidget>
#include <QWidget>
#include <QMessageBox>
#include <QKeyEvent>
#include <QResizeEvent>

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

    // Combat Page (now serves as main game hub)
    m_combatPage = new CombatPage();
    connect(m_combatPage, &CombatPage::exploreClicked, this, &MainWindow::handleExploreClicked);
    connect(m_combatPage, &CombatPage::restClicked, this, &MainWindow::handleRestClicked);
    connect(m_combatPage, &CombatPage::attackClicked, this, &MainWindow::handleAttackClicked);
    connect(m_combatPage, &CombatPage::skillClicked, this, &MainWindow::handleSkillClicked);
    connect(m_combatPage, &CombatPage::itemClicked, this, &MainWindow::handleItemClicked);
    connect(m_combatPage, &CombatPage::statsClicked, this, &MainWindow::handleStatsClicked);
    connect(m_combatPage, &CombatPage::runClicked, this, &MainWindow::handleRunClicked);
    connect(m_combatPage, &CombatPage::menuClicked, this, &MainWindow::handleMenuButtonClicked);
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
    connect(m_saveLoadPage, &SaveLoadPage::saveToSlotRequested, this, &MainWindow::handleSaveToSlot);
    connect(m_saveLoadPage, &SaveLoadPage::loadFromSlotRequested, this, &MainWindow::handleLoadFromSlot);
    connect(m_saveLoadPage, &SaveLoadPage::deleteSlotRequested, this, &MainWindow::handleDeleteSlot);
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
    connect(m_game, &Game::combatEnded, this, &MainWindow::handleCombatEnded);

    // Menu Overlay (floating overlay, not in stacked widget)
    m_menuOverlay = new MenuOverlay(this);
    m_menuOverlay->setGeometry(0, 0, width(), height());
    connect(m_menuOverlay, &MenuOverlay::saveRequested, this, &MainWindow::handleQuickSave);
    connect(m_menuOverlay, &MenuOverlay::loadRequested, this, &MainWindow::handleQuickLoad);
    connect(m_menuOverlay, &MenuOverlay::quitRequested, this, &MainWindow::handleQuitClicked);
    m_menuOverlay->hide();
}

void MainWindow::handleCharacterCreation(const QString &name, const QString &characterClass)
{
    m_game->newGame(name, characterClass);
    // Start in non-combat mode on the main game hub (CombatPage)
    m_combatPage->setCombatMode(false);
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleExploreClicked()
{
    m_game->startCombat();
    m_combatPage->setCombatMode(true);
    m_combatPage->setCombatActive(true);
    m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), "");
    // Already on CombatPage, just ensure it's visible
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

void MainWindow::handleQuitClicked()
{
    // Add confirmation dialog to prevent accidental exits
    QMessageBox::StandardButton reply = QMessageBox::question(
        this,
        "Quit Game",
        "Are you sure you want to quit? Any unsaved progress will be lost.",
        QMessageBox::Yes | QMessageBox::No
    );

    if (reply == QMessageBox::Yes) {
        close();
    }
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
    // Legacy method - combat is already ended by the signal handler
    // This method is kept for backward compatibility but should be removed
    m_combatPage->setCombatMode(false);
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleCombatEnded(bool playerWon)
{
    // Disable combat buttons since combat has ended
    m_combatPage->setCombatActive(false);

    // For now, don't check leveling - rewards are already given
    bool leveledUp = false;

    // Show combat result dialog
    if (playerWon) {
        Monster *monster = m_game->getCurrentMonster();
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

    // Return to non-combat mode on the main game hub
    m_combatPage->setCombatMode(false);
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleRunClicked()
{
    m_combatPage->setCombatMode(false);
    stackedWidget->setCurrentWidget(m_combatPage);
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
        m_combatPage->setCombatMode(false);
        stackedWidget->setCurrentWidget(m_combatPage);
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
        m_combatPage->setCombatMode(false);
        stackedWidget->setCurrentWidget(m_combatPage);
    }
}

void MainWindow::handleNewSave()
{
    stackedWidget->setCurrentWidget(m_newGameView);
}

void MainWindow::handleSaveToSlot(int slotNumber)
{
    if (m_game->saveToSlot(slotNumber)) {
        m_saveLoadPage->refreshSaveSlots();
        // Optionally show success message
    }
}

void MainWindow::handleLoadFromSlot(int slotNumber)
{
    if (m_game->loadFromSlot(slotNumber)) {
        m_combatPage->setCombatMode(false);
        stackedWidget->setCurrentWidget(m_combatPage);
    }
}

void MainWindow::handleDeleteSlot(int slotNumber)
{
    if (m_game->deleteSlot(slotNumber)) {
        m_saveLoadPage->refreshSaveSlots();
    }
}

void MainWindow::handleMainMenuNewGame()
{
    stackedWidget->setCurrentWidget(m_newGameView);
}

void MainWindow::handleMainMenuLoadGame()
{
    m_saveLoadPage->refreshSaveSlots();
    stackedWidget->setCurrentWidget(m_saveLoadPage);
}

void MainWindow::handleMainMenuExit()
{
    close();
}

void MainWindow::handleInventoryBack()
{
    // Back to combat page, preserving combat state
    bool inCombat = (m_game->getCurrentMonster() != nullptr && !m_game->isCombatOver());
    m_combatPage->setCombatMode(inCombat);
    if (inCombat) {
        m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), "");
    }
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleShopLeave()
{
    m_combatPage->setCombatMode(false);
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleStatsBack()
{
    // Back to combat page, preserving combat state
    bool inCombat = (m_game->getCurrentMonster() != nullptr && !m_game->isCombatOver());
    m_combatPage->setCombatMode(inCombat);
    if (inCombat) {
        m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), "");
    }
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleMonsterStatsBack()
{
    // Back to combat page, preserving combat state
    bool inCombat = (m_game->getCurrentMonster() != nullptr && !m_game->isCombatOver());
    m_combatPage->setCombatMode(inCombat);
    if (inCombat) {
        m_combatPage->updateCombatState(m_game->getPlayer(), m_game->getCurrentMonster(), "");
    }
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleSaveLoadBack()
{
    stackedWidget->setCurrentWidget(m_mainMenu);
}

void MainWindow::handleMenuButtonClicked()
{
    // Show menu overlay from CombatPage (only when player exists)
    // Add defensive checks to ensure we're in an appropriate state
    if (!m_game || !m_game->getPlayer() || !m_menuOverlay) {
        return;
    }

    // Verify we're on the correct widget (CombatPage) before showing menu
    QWidget *currentWidget = stackedWidget->currentWidget();
    if (!currentWidget || currentWidget != m_combatPage) {
        return;
    }

    m_menuOverlay->updateContent(m_game->getPlayer());
    m_menuOverlay->showOverlay();
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    // Only handle ESC if we're on the adventure page or combat page (in-game)
    if (event->key() == Qt::Key_Escape && m_menuOverlay) {
        QWidget *currentWidget = stackedWidget->currentWidget();

        // Check if menu overlay is visible
        if (m_menuOverlay->isVisible()) {
            m_menuOverlay->hideOverlay();
            event->accept();
            return;
        }

        // Show menu if we're in-game (on combat page) and player exists
        if (currentWidget == m_combatPage && m_game && m_game->getPlayer()) {
            m_menuOverlay->updateContent(m_game->getPlayer());
            m_menuOverlay->showOverlay();
            event->accept();
            return;
        }
    }

    QMainWindow::keyPressEvent(event);
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    QMainWindow::resizeEvent(event);

    // Keep menu overlay sized to match the window
    if (m_menuOverlay) {
        m_menuOverlay->setGeometry(0, 0, width(), height());
    }
}

MainWindow::~MainWindow()
{
}
