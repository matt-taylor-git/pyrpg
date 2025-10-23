#include "AdventurePage.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QPushButton>
#include <QFont>
#include <QFrame>

AdventurePage::AdventurePage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void AdventurePage::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL, Theme::SPACING_XL, Theme::SPACING_XL);
    mainLayout->setSpacing(Theme::SPACING_XL);

    // Title section
    QLabel *titleLabel = new QLabel("Adventure Awaits");
    QFont titleFont;
    titleFont.setPointSize(28);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setStyleSheet(QString("color: %1;").arg(Theme::PRIMARY.name()));
    titleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(titleLabel);

    QLabel *subtitleLabel = new QLabel("Choose your next action");
    QFont subtitleFont;
    subtitleFont.setPointSize(14);
    subtitleLabel->setFont(subtitleFont);
    subtitleLabel->setStyleSheet(QString("color: %1; margin-bottom: %2px;").arg(Theme::MUTED_FOREGROUND.name()).arg(Theme::SPACING_MD));
    subtitleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(subtitleLabel);

    // Main content container
    QWidget *contentWidget = new QWidget();
    QVBoxLayout *contentLayout = new QVBoxLayout(contentWidget);
    contentLayout->setSpacing(Theme::SPACING_LG);
    contentLayout->setContentsMargins(0, 0, 0, 0);

    // Primary Actions Card
    QFrame *primaryCard = createCardFrame("Primary Actions");
    QGridLayout *primaryGrid = new QGridLayout();
    primaryGrid->setSpacing(Theme::SPACING_MD);
    primaryGrid->setContentsMargins(Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD);

    m_exploreButton = createActionButton("🏞️ Explore", "Venture into the unknown and find enemies", true);
    connect(m_exploreButton, &QPushButton::clicked, this, &AdventurePage::exploreClicked);

    m_restButton = createActionButton("😴 Rest", "Recover health and mana", false);
    connect(m_restButton, &QPushButton::clicked, this, &AdventurePage::restClicked);

    primaryGrid->addWidget(m_exploreButton, 0, 0);
    primaryGrid->addWidget(m_restButton, 0, 1);

    primaryCard->layout()->addItem(primaryGrid);
    contentLayout->addWidget(primaryCard);

    // Character Management Card
    QFrame *characterCard = createCardFrame("Character Management");
    QGridLayout *characterGrid = new QGridLayout();
    characterGrid->setSpacing(Theme::SPACING_MD);
    characterGrid->setContentsMargins(Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD);

    QPushButton* inventoryButton = createActionButton("🎒 Inventory", "View and manage your items", false);
    connect(inventoryButton, &QPushButton::clicked, this, &AdventurePage::inventoryClicked);

    QPushButton* viewStatsButton = createActionButton("📊 View Stats", "Check your character statistics", false);
    connect(viewStatsButton, &QPushButton::clicked, this, &AdventurePage::viewStatsClicked);

    characterGrid->addWidget(inventoryButton, 0, 0);
    characterGrid->addWidget(viewStatsButton, 0, 1);

    characterCard->layout()->addItem(characterGrid);
    contentLayout->addWidget(characterCard);

    // Other Actions Card
    QFrame *otherCard = createCardFrame("Other Actions");
    QGridLayout *otherGrid = new QGridLayout();
    otherGrid->setSpacing(Theme::SPACING_MD);
    otherGrid->setContentsMargins(Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD, Theme::SPACING_MD);

    QPushButton* shopButton = createActionButton("🏪 Shop", "Buy and sell items", false);
    connect(shopButton, &QPushButton::clicked, this, &AdventurePage::shopClicked);

    m_quitButton = createActionButton("🚪 Quit Game", "Exit to main menu", false);
    m_quitButton->setObjectName("destructive");
    connect(m_quitButton, &QPushButton::clicked, this, &AdventurePage::quitClicked);

    otherGrid->addWidget(shopButton, 0, 0);
    otherGrid->addWidget(m_quitButton, 0, 1);

    otherCard->layout()->addItem(otherGrid);
    contentLayout->addWidget(otherCard);

    mainLayout->addWidget(contentWidget);
    mainLayout->addStretch();
}

QFrame* AdventurePage::createCardFrame(const QString &title)
{
    QFrame *card = new QFrame();
    card->setStyleSheet(QString(
        "QFrame { "
        "background-color: %1; "
        "border: %2px solid %3; "
        "border-radius: %4px; "
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER_WIDTH_THIN)
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_LG));

    QVBoxLayout *cardLayout = new QVBoxLayout(card);
    cardLayout->setSpacing(Theme::SPACING_SM);
    cardLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG);

    QLabel *cardTitle = new QLabel(title);
    QFont titleFont;
    titleFont.setPointSize(16);
    titleFont.setWeight(Theme::FONT_WEIGHT_SEMIBOLD);
    cardTitle->setFont(titleFont);
    cardTitle->setStyleSheet(QString("color: %1; margin-bottom: %2px;")
                                 .arg(Theme::ACCENT.name())
                                 .arg(Theme::SPACING_SM));
    cardLayout->addWidget(cardTitle);

    return card;
}

QPushButton* AdventurePage::createActionButton(const QString &text, const QString &tooltip, bool isPrimary)
{
    QPushButton *button = new QPushButton(text);
    button->setToolTip(tooltip);
    button->setMinimumHeight(80);
    button->setMinimumWidth(200);

    if (isPrimary) {
        button->setObjectName("primary");
    }

    QFont buttonFont;
    buttonFont.setPointSize(14);
    buttonFont.setWeight(Theme::FONT_WEIGHT_MEDIUM);
    button->setFont(buttonFont);

    return button;
}