#ifndef INVENTORYPAGE_H
#define INVENTORYPAGE_H

#include <QWidget>

class QLabel;
class QGridLayout;
class QPushButton;
class QFrame;
class Player;
class Item;

class InventoryPage : public QWidget
{
    Q_OBJECT
public:
    explicit InventoryPage(QWidget *parent = nullptr);
    void updateInventory(Player *player);

signals:
    void backRequested();
    void itemEquipped(Item *item);
    void itemUsed(Item *item);

private slots:
    void handleItemClicked(Item *item);

private:
    void setupUi();
    void clearInventory();
    QWidget* createItemCard(Item *item);
    QWidget* createEquipmentPanel(Player *player);

    Player *m_currentPlayer;
    QLabel *m_goldLabel;
    QGridLayout *m_inventoryGridLayout;
    QFrame *m_equipmentPanel;
    QLabel *m_weaponSlot;
    QLabel *m_armorSlot;
    QLabel *m_accessorySlot;
};

#endif // INVENTORYPAGE_H