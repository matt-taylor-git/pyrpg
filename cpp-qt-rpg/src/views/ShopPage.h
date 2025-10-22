#ifndef SHOPPAGE_H
#define SHOPPAGE_H

#include <QWidget>

class QLabel;
class QGridLayout;
class QPushButton;
class Player;
class Item;

class ShopPage : public QWidget
{
    Q_OBJECT
public:
    explicit ShopPage(QWidget *parent = nullptr);

    void updateShop(Player *player);

signals:
    void leaveRequested();
    void itemPurchased(Item *item);

private:
    void setupUi();
    void clearShop();
    QWidget* createShopItemCard(Item *item, int price);
    void handleBuyClicked(Item *item, int price);

    QLabel *m_goldLabel;
    QGridLayout *m_shopGridLayout;
    QPushButton *m_sellButton;
    QPushButton *m_leaveButton;
    Player *m_currentPlayer;
};

#endif // SHOPPAGE_H