#ifndef COMBATPAGE_H
#define COMBATPAGE_H

#include <QWidget>

class QLabel;
class QProgressBar;
class QPushButton;
class QTextEdit;

class CombatPage : public QWidget
{
    Q_OBJECT
public:
    explicit CombatPage(QWidget *parent = nullptr);

signals:
    void attackClicked();
    void skillClicked();
    void itemClicked();
    void statsClicked();
    void runClicked();

private:
    void setupUi();
    QWidget* createArenaCard();
    QWidget* createLogCard();

    // Arena widgets
    QLabel *m_heroSpriteLabel;
    QLabel *m_enemySpriteLabel;
    QProgressBar *m_heroHealthBar;
    QProgressBar *m_enemyHealthBar;
    QPushButton *m_attackButton;
    QPushButton *m_skillButton;
    QPushButton *m_itemButton;
    QPushButton *m_statsButton;
    QPushButton *m_runButton;

    // Log widgets
    QTextEdit *m_battleLog;
};

#endif // COMBATPAGE_H
