#ifndef INVENTORYPAGE_H
#define INVENTORYPAGE_H

#include <QWidget>

class QLabel;
class QGridLayout;

class InventoryPage : public QWidget
{
    Q_OBJECT
public:
    explicit InventoryPage(QWidget *parent = nullptr);

private:
    void setupUi();

    QLabel *m_goldLabel;
    QGridLayout *m_inventoryGridLayout;
};

#endif // INVENTORYPAGE_H