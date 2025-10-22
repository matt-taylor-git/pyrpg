#include "ShopPage.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QScrollArea>
#include <QGridLayout>
#include <QPushButton>

ShopPage::ShopPage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void ShopPage::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG);
    mainLayout->setSpacing(Theme::SPACING_LG);

    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *title = new QLabel("Merchant Shop");
    title->setStyleSheet("font-size: 18px; font-weight: bold;");
    m_goldLabel = new QLabel("Gold: 0");
    m_goldLabel->setStyleSheet("font-size: 16px; font-weight: bold; color: #e5c07b;");
    headerLayout->addWidget(title);
    headerLayout->addStretch();
    headerLayout->addWidget(m_goldLabel);
    mainLayout->addLayout(headerLayout);

    QScrollArea *scrollArea = new QScrollArea();
    scrollArea->setWidgetResizable(true);
    QWidget *scrollContent = new QWidget();
    m_shopGridLayout = new QGridLayout(scrollContent);
    scrollArea->setWidget(scrollContent);
    mainLayout->addWidget(scrollArea);

    // Placeholder for shop items
    QLabel *emptyLabel = new QLabel("The shop is currently empty.");
    emptyLabel->setAlignment(Qt::AlignCenter);
    m_shopGridLayout->addWidget(emptyLabel, 0, 0, 1, 4);

    QHBoxLayout *buttonLayout = new QHBoxLayout();
    m_sellButton = new QPushButton("Sell Items");
    m_leaveButton = new QPushButton("Leave Shop");
    connect(m_leaveButton, &QPushButton::clicked, this, &ShopPage::leaveRequested);
    buttonLayout->addStretch();
    buttonLayout->addWidget(m_sellButton);
    buttonLayout->addWidget(m_leaveButton);
    mainLayout->addLayout(buttonLayout);
}