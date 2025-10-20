#include "CombatPage.h"
#include "../theme/Theme.h"
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QProgressBar>
#include <QPushButton>
#include <QTextEdit>
#include <QFrame>
#include <QFont>

CombatPage::CombatPage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void CombatPage::setupUi()
{
    QHBoxLayout *mainLayout = new QHBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG);
    mainLayout->setSpacing(Theme::SPACING_LG);

    QWidget *arenaCard = createArenaCard();
    mainLayout->addWidget(arenaCard, 2);

    QWidget *logCard = createLogCard();
    mainLayout->addWidget(logCard, 1);
}

QWidget* CombatPage::createArenaCard()
{
    QFrame *card = new QFrame();
    card->setStyleSheet(QString("background-color: %1; border-radius: %2px;").arg(Theme::CARD.name()).arg(Theme::BORDER_RADIUS_MD));
    QVBoxLayout *layout = new QVBoxLayout(card);

    QLabel *title = new QLabel("⚔️ Battle Arena");
    QFont titleFont;
    titleFont.setPointSize(18);
    titleFont.setBold(true);
    title->setFont(titleFont);
    title->setStyleSheet(QString("color: %1; margin-bottom: %2px;").arg(Theme::PRIMARY.name()).arg(Theme::SPACING_SM));
    layout->addWidget(title);

    QFrame *spritesContainer = new QFrame();
    spritesContainer->setFrameShape(QFrame::Box);
    spritesContainer->setStyleSheet(QString(
        "QFrame { border: 2px solid %1; border-radius: %2px; background-color: %3; padding: %4px; }"
    ).arg(Theme::BORDER.name()).arg(Theme::BORDER_RADIUS_MD).arg(Theme::CARD.name()).arg(Theme::SPACING_MD));
    QHBoxLayout *spritesLayout = new QHBoxLayout(spritesContainer);
    spritesLayout->setSpacing(Theme::SPACING_MD);

    m_heroSpriteLabel = new QLabel("🛡️ HERO");
    m_heroSpriteLabel->setAlignment(Qt::AlignCenter);
    m_heroSpriteLabel->setMinimumSize(80, 80);
    m_enemySpriteLabel = new QLabel("👹 ENEMY");
    m_enemySpriteLabel->setAlignment(Qt::AlignCenter);
    m_enemySpriteLabel->setMinimumSize(80, 80);

    spritesLayout->addWidget(m_heroSpriteLabel);
    spritesLayout->addWidget(new QLabel("⚔️"));
    spritesLayout->addWidget(m_enemySpriteLabel);
    layout->addWidget(spritesContainer);

    m_heroHealthBar = new QProgressBar();
    m_heroHealthBar->setRange(0, 100);
    m_heroHealthBar->setValue(100);
    m_heroHealthBar->setTextVisible(true);
    m_heroHealthBar->setFormat("100 / 100 HP");
    layout->addWidget(new QLabel("❤️ Hero Health"));
    layout->addWidget(m_heroHealthBar);

    m_enemyHealthBar = new QProgressBar();
    m_enemyHealthBar->setRange(0, 100);
    m_enemyHealthBar->setValue(100);
    m_enemyHealthBar->setTextVisible(true);
    m_enemyHealthBar->setFormat("100 / 100 HP");
    layout->addWidget(new QLabel("💀 Enemy Health"));
    layout->addWidget(m_enemyHealthBar);

    QGridLayout *actionsLayout = new QGridLayout();
    actionsLayout->setSpacing(Theme::SPACING_SM);
    m_attackButton = new QPushButton("⚔️ Attack");
    connect(m_attackButton, &QPushButton::clicked, this, &CombatPage::attackClicked);
    m_skillButton = new QPushButton("✨ Use Skill");
    connect(m_skillButton, &QPushButton::clicked, this, &CombatPage::skillClicked);
    m_itemButton = new QPushButton("🧪 Use Item");
    connect(m_itemButton, &QPushButton::clicked, this, &CombatPage::itemClicked);
    m_statsButton = new QPushButton("📖 View Stats");
    connect(m_statsButton, &QPushButton::clicked, this, &CombatPage::statsClicked);
    m_runButton = new QPushButton("🏃 Run");
    connect(m_runButton, &QPushButton::clicked, this, &CombatPage::runClicked);
    actionsLayout->addWidget(m_attackButton, 0, 0);
    actionsLayout->addWidget(m_skillButton, 0, 1);
    actionsLayout->addWidget(m_itemButton, 1, 0);
    actionsLayout->addWidget(m_statsButton, 1, 1);
    actionsLayout->addWidget(m_runButton, 2, 0, 1, 2);
    layout->addLayout(actionsLayout);

    return card;
}

QWidget* CombatPage::createLogCard()
{
    QFrame *card = new QFrame();
    card->setStyleSheet(QString("background-color: %1; border-radius: %2px;").arg(Theme::CARD.name()).arg(Theme::BORDER_RADIUS_MD));
    QVBoxLayout *layout = new QVBoxLayout(card);

    QLabel *title = new QLabel("📜 Battle Log");
    QFont titleFont;
    titleFont.setPointSize(18);
    titleFont.setBold(true);
    title->setFont(titleFont);
    title->setStyleSheet(QString("color: %1; margin-bottom: %2px;").arg(Theme::PRIMARY.name()).arg(Theme::SPACING_SM));
    layout->addWidget(title);

    m_battleLog = new QTextEdit();
    m_battleLog->setReadOnly(true);
    m_battleLog->setText("A wild enemy appears!\nPrepare for battle!");
    layout->addWidget(m_battleLog);

    return card;
}