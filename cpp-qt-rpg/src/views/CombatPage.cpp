#include "CombatPage.h"
#include "../theme/Theme.h"
#include "../models/Player.h"
#include "../models/Monster.h"
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
    m_heroSpriteLabel->setMinimumSize(100, 100);
    m_enemySpriteLabel = new QLabel("👹 ENEMY");
    m_enemySpriteLabel->setAlignment(Qt::AlignCenter);
    m_enemySpriteLabel->setMinimumSize(100, 100);

    spritesLayout->addWidget(m_heroSpriteLabel);
    spritesLayout->addWidget(new QLabel("⚔️"));
    spritesLayout->addWidget(m_enemySpriteLabel);
    layout->addWidget(spritesContainer);

    // Monster name/level display
    m_monsterNameLabel = new QLabel("Unknown Monster");
    m_monsterNameLabel->setAlignment(Qt::AlignCenter);
    m_monsterNameLabel->setStyleSheet(QString("font-size: 16px; font-weight: bold; color: %1;").arg(Theme::FOREGROUND.name()));
    layout->addWidget(m_monsterNameLabel);

    // Hero stats
    layout->addWidget(new QLabel("❤️ Hero Health"));
    m_heroHealthBar = new QProgressBar();
    m_heroHealthBar->setRange(0, 100);
    m_heroHealthBar->setValue(100);
    m_heroHealthBar->setTextVisible(true);
    m_heroHealthBar->setFormat("100 / 100 HP");
    m_heroHealthBar->setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #dc3545; }");
    layout->addWidget(m_heroHealthBar);

    layout->addWidget(new QLabel("💙 Hero Mana"));
    m_heroManaBar = new QProgressBar();
    m_heroManaBar->setRange(0, 100);
    m_heroManaBar->setValue(100);
    m_heroManaBar->setTextVisible(true);
    m_heroManaBar->setFormat("100 / 100 MP");
    m_heroManaBar->setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #3b82f6; }");
    layout->addWidget(m_heroManaBar);

    // Enemy stats
    layout->addWidget(new QLabel("💀 Enemy Health"));
    m_enemyHealthBar = new QProgressBar();
    m_enemyHealthBar->setRange(0, 100);
    m_enemyHealthBar->setValue(100);
    m_enemyHealthBar->setTextVisible(true);
    m_enemyHealthBar->setFormat("100 / 100 HP");
    m_enemyHealthBar->setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #ef4444; }");
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

void CombatPage::updateCombatState(Player *player, Monster *monster, const QString &log)
{
    if (player) {
        m_heroHealthBar->setMaximum(player->maxHealth);
        m_heroHealthBar->setValue(player->health);
        m_heroHealthBar->setFormat(QString("%1 / %2 HP").arg(player->health).arg(player->maxHealth));

        m_heroManaBar->setMaximum(player->maxMana);
        m_heroManaBar->setValue(player->mana);
        m_heroManaBar->setFormat(QString("%1 / %2 MP").arg(player->mana).arg(player->maxMana));

        // Try to load character sprite
        QString spritePath = QString(":/assets/%1.png").arg(player->characterClass.toLower());
        QPixmap sprite(spritePath);
        if (!sprite.isNull()) {
            m_heroSpriteLabel->setPixmap(sprite.scaled(100, 100, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        }
    }
    if (monster) {
        m_enemyHealthBar->setMaximum(monster->maxHealth);
        m_enemyHealthBar->setValue(monster->health);
        m_enemyHealthBar->setFormat(QString("%1 / %2 HP").arg(monster->health).arg(monster->maxHealth));

        // Update monster name and level
        m_monsterNameLabel->setText(QString("%1 (Level %2)").arg(monster->name).arg(monster->level));

        // Try to load monster sprite based on enemyType
        QString spritePath = QString(":/assets/%1.png").arg(monster->enemyType);
        QPixmap sprite(spritePath);
        if (!sprite.isNull()) {
            m_enemySpriteLabel->setPixmap(sprite.scaled(100, 100, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        }
    }
    if (!log.isEmpty()) {
        m_battleLog->append(log);
    }
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