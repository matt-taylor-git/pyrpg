#include "CombatResultDialog.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QFont>

CombatResultDialog::CombatResultDialog(bool victory, int expGained, int goldGained,
                                       const QString &lootMessage, bool leveledUp,
                                       QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle(victory ? "Victory!" : "Defeat");
    setMinimumWidth(400);
    setupUi(victory, expGained, goldGained, lootMessage, leveledUp);
}

void CombatResultDialog::setupUi(bool victory, int expGained, int goldGained,
                                  const QString &lootMessage, bool leveledUp)
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(Theme::SPACING_LG);
    mainLayout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL,
                                   Theme::SPACING_XL, Theme::SPACING_XL);

    // Title
    QLabel *titleLabel = new QLabel(victory ? "🎉 VICTORY! 🎉" : "💀 DEFEAT 💀");
    QFont titleFont;
    titleFont.setPointSize(24);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    titleLabel->setStyleSheet(QString("color: %1; margin-bottom: 20px;")
                                  .arg(victory ? Theme::ACCENT.name() : Theme::DESTRUCTIVE.name()));
    mainLayout->addWidget(titleLabel);

    if (victory) {
        // Level up notification
        if (leveledUp) {
            QLabel *levelUpLabel = new QLabel("⭐ LEVEL UP! ⭐");
            QFont levelUpFont;
            levelUpFont.setPointSize(20);
            levelUpFont.setBold(true);
            levelUpLabel->setFont(levelUpFont);
            levelUpLabel->setAlignment(Qt::AlignCenter);
            levelUpLabel->setStyleSheet(QString("color: %1; background-color: %2; "
                                                "padding: 15px; border-radius: 8px; margin: 10px;")
                                           .arg(Theme::PRIMARY_FOREGROUND.name())
                                           .arg(Theme::PRIMARY.name()));
            mainLayout->addWidget(levelUpLabel);
        }

        // Rewards section
        QLabel *rewardsTitle = new QLabel("Rewards:");
        rewardsTitle->setStyleSheet("font-size: 16px; font-weight: bold;");
        mainLayout->addWidget(rewardsTitle);

        QString rewardsText;
        if (expGained > 0) {
            rewardsText += QString("📈 Experience: +%1 XP\n").arg(expGained);
        }
        if (goldGained > 0) {
            rewardsText += QString("💰 Gold: +%1\n").arg(goldGained);
        }
        if (!lootMessage.isEmpty()) {
            rewardsText += QString("🎁 %1\n").arg(lootMessage);
        }

        QLabel *rewardsLabel = new QLabel(rewardsText);
        rewardsLabel->setStyleSheet(QString(
            "color: %1; "
            "background-color: %2; "
            "padding: 15px; "
            "border-radius: 8px; "
            "border: 2px solid %3;"
        ).arg(Theme::FOREGROUND.name())
         .arg(Theme::CARD.name())
         .arg(Theme::BORDER.name()));
        mainLayout->addWidget(rewardsLabel);
    } else {
        // Defeat message
        QLabel *defeatMsg = new QLabel("You have been defeated...\nBut you can try again!");
        defeatMsg->setAlignment(Qt::AlignCenter);
        defeatMsg->setStyleSheet(QString("color: %1; font-size: 14px; margin: 20px;")
                                    .arg(Theme::FOREGROUND.name()));
        mainLayout->addWidget(defeatMsg);
    }

    // Continue button
    QPushButton *continueButton = new QPushButton(victory ? "Continue" : "Return to Adventure");
    continueButton->setMinimumHeight(50);
    continueButton->setStyleSheet(QString(
        "QPushButton {"
        "    background-color: %1;"
        "    color: %2;"
        "    font-size: 16px;"
        "    font-weight: bold;"
        "    border-radius: 8px;"
        "}"
        "QPushButton:hover { background-color: %3; }"
    ).arg(victory ? Theme::ACCENT.name() : Theme::PRIMARY.name())
     .arg(Theme::PRIMARY_FOREGROUND.name())
     .arg(victory ? Theme::ACCENT.lighter(110).name() : Theme::PRIMARY.lighter(110).name()));
    connect(continueButton, &QPushButton::clicked, this, &QDialog::accept);
    mainLayout->addWidget(continueButton);
}
