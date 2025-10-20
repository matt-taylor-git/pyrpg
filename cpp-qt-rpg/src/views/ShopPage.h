#ifndef SHOPPAGE_H
#define SHOPPAGE_H

#include <QWidget>

class QLabel;
class QGridLayout;
class QPushButton;

class ShopPage : public QWidget
{
    Q_OBJECT
public:
    explicit ShopPage(QWidget *parent = nullptr);

private:
    void setupUi();

    QLabel *m_goldLabel;
    QGridLayout *m_shopGridLayout;
    QPushButton *m_sellButton;
    QPushButton *m_leaveButton;
};

#endif // SHOPPAGE_H