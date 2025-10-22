#include "AdventurePage.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QFont>

AdventurePage::AdventurePage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void AdventurePage::setupUi()
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL, Theme::SPACING_XL, Theme::SPACING_XL);
    layout->setSpacing(Theme::SPACING_LG);
    layout->setAlignment(Qt::AlignCenter);

    QLabel *titleLabel = new QLabel("Adventure awaits...");
    QFont titleFont;
    titleFont.setPointSize(24);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setStyleSheet(QString("color: %1; margin-bottom: %2px;").arg(Theme::FOREGROUND.name()).arg(Theme::SPACING_MD));
    layout->addWidget(titleLabel, 0, Qt::AlignCenter);

    QWidget *buttonContainer = new QWidget();
    QVBoxLayout *buttonLayout = new QVBoxLayout(buttonContainer);
    buttonLayout->setSpacing(Theme::SPACING_MD);
    buttonLayout->setAlignment(Qt::AlignCenter);

    m_exploreButton = new QPushButton("🏞️ Explore");
    connect(m_exploreButton, &QPushButton::clicked, this, &AdventurePage::exploreClicked);
    m_exploreButton->setMinimumHeight(60);
    m_restButton = new QPushButton("😴 Rest");
    connect(m_restButton, &QPushButton::clicked, this, &AdventurePage::restClicked);
    m_restButton->setMinimumHeight(60);
    m_quitButton = new QPushButton("🚪 Quit Game");
    connect(m_quitButton, &QPushButton::clicked, this, &AdventurePage::quitClicked);
    m_quitButton->setMinimumHeight(60);

    QPushButton* viewStatsButton = new QPushButton("📊 View Stats");
    connect(viewStatsButton, &QPushButton::clicked, this, &AdventurePage::viewStatsClicked);
    viewStatsButton->setMinimumHeight(60);

    QPushButton* inventoryButton = new QPushButton("🎒 Inventory");
    connect(inventoryButton, &QPushButton::clicked, this, &AdventurePage::inventoryClicked);
    inventoryButton->setMinimumHeight(60);

    QPushButton* shopButton = new QPushButton("🏪 Shop");
    connect(shopButton, &QPushButton::clicked, this, &AdventurePage::shopClicked);
    shopButton->setMinimumHeight(60);

    buttonLayout->addWidget(m_exploreButton);
    buttonLayout->addWidget(m_restButton);
    buttonLayout->addWidget(inventoryButton);
    buttonLayout->addWidget(shopButton);
    buttonLayout->addWidget(viewStatsButton);
    buttonLayout->addWidget(m_quitButton);

    layout->addWidget(buttonContainer);
}