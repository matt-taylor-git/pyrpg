#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class QStackedWidget;
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

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void handleCharacterCreation(const QString &name);
    void handleExploreClicked();
    void handleRestClicked();
    void handleQuitClicked();
    void handleAttackClicked();
    void handleSkillClicked();
    void handleItemClicked();
    void handleStatsClicked();
    void handleRunClicked();
    void handleViewStatsClicked();

private:
    QStackedWidget *stackedWidget;
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
};

#endif // MAINWINDOW_H
