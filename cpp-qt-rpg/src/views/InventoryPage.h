#ifndef INVENTORYPAGE_H
#define INVENTORYPAGE_H

#include <QWidget>

class QLabel;
class QGridLayout;
class QPushButton;

class InventoryPage : public QWidget
{
    Q_OBJECT
public:
    explicit InventoryPage(QWidget *parent = nullptr);

signals:
    void backRequested();

private:
    void setupUi();

    QLabel *m_goldLabel;
    QGridLayout *m_inventoryGridLayout;
    QPushButton *m_backButton;
};

#endif // INVENTORYPAGE_H