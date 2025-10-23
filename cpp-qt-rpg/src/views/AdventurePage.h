#ifndef ADVENTUREPAGE_H
#define ADVENTUREPAGE_H

#include <QWidget>

class QPushButton;
class QFrame;

class AdventurePage : public QWidget
{
    Q_OBJECT
public:
    explicit AdventurePage(QWidget *parent = nullptr);

signals:
    void exploreClicked();
    void restClicked();
    void quitClicked();
    void viewStatsClicked();
    void inventoryClicked();
    void shopClicked();
    void menuButtonClicked();

private:
    void setupUi();
    QFrame* createCardFrame(const QString &title);
    QPushButton* createActionButton(const QString &text, const QString &tooltip, bool isPrimary);

    QPushButton *m_exploreButton;
    QPushButton *m_restButton;
    QPushButton *m_quitButton;
    QPushButton *m_inventoryButton;
    QPushButton *m_viewStatsButton;
    QPushButton *m_shopButton;
    QPushButton *m_menuButton;
};

#endif // ADVENTUREPAGE_H
