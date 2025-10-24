#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class QStackedWidget;
class MainMenu;
class NewGameView;
class CharacterCustomizationPage;
class AdventurePage;
class CombatPage;
class InventoryPage;
class MonsterStatsPage;
class SaveLoadPage;
class ShopPage;
class StatsPage;
class Game;
class MenuOverlay;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void handleCharacterCreation(const QString &name, const QString &characterClass);
    void handleExploreClicked();
    void handleRestClicked();
    void handleQuitClicked();
    void handleAttackClicked();
    void handleSkillClicked();
    void handleItemClicked();
    void handleStatsClicked();
    void handleRunClicked();
    void handleViewStatsClicked();
    void handleQuickSave();
    void handleQuickLoad();
    void handleSaveToFile(const QString &filePath);
    void handleLoadFromFile(const QString &filePath);
    void handleNewSave();
    void handleMainMenuNewGame();
    void handleMainMenuLoadGame();
    void handleMainMenuExit();
    void handleInventoryBack();
    void handleShopLeave();
    void handleStatsBack();
    void handleMonsterStatsBack();
    void handleSaveLoadBack();
    void handleCombatEnd(int oldLevel);
    void handleCombatEnded(bool playerWon);
    void handleInventoryClicked();
    void handleShopClicked();
    void handleMenuButtonClicked();

protected:
    void keyPressEvent(QKeyEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

private:
    QStackedWidget *stackedWidget;
    MainMenu *m_mainMenu;
    NewGameView *m_newGameView;
    CharacterCustomizationPage *m_characterCustomizationPage;
    AdventurePage *m_adventurePage;
    CombatPage *m_combatPage;
    InventoryPage *m_inventoryPage;
    MonsterStatsPage *m_monsterStatsPage;
    SaveLoadPage *m_saveLoadPage;
    ShopPage *m_shopPage;
    StatsPage *m_statsPage;
    Game *m_game;
    MenuOverlay *m_menuOverlay;
};

#endif // MAINWINDOW_H
