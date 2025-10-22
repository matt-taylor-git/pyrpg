#include "InventoryPage.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QScrollArea>
#include <QGridLayout>
#include <QPushButton>

InventoryPage::InventoryPage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void InventoryPage::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG);
    mainLayout->setSpacing(Theme::SPACING_LG);

    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *title = new QLabel("Inventory");
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
    m_inventoryGridLayout = new QGridLayout(scrollContent);
    scrollArea->setWidget(scrollContent);
    mainLayout->addWidget(scrollArea);

    // Back button
    m_backButton = new QPushButton("⬅️ Back");
    m_backButton->setMinimumHeight(40);
    connect(m_backButton, &QPushButton::clicked, this, &InventoryPage::backRequested);
    mainLayout->addWidget(m_backButton, 0, Qt::AlignCenter);

    // Placeholder for empty inventory
    QLabel *emptyLabel = new QLabel("Your inventory is empty.");
    emptyLabel->setAlignment(Qt::AlignCenter);
    m_inventoryGridLayout->addWidget(emptyLabel, 0, 0, 1, 4);
}