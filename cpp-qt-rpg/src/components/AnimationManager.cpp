#include "AnimationManager.h"
#include "../views/CombatPage.h"
#include <QPropertyAnimation>
#include <QSequentialAnimationGroup>
#include <QPauseAnimation>
#include <QLabel>
#include <QEasingCurve>

AnimationManager::AnimationManager(CombatPage *combatPage, QObject *parent)
    : QObject(parent), m_combatPage(combatPage)
{
}

void AnimationManager::playPlayerAttackAnimation()
{
    QLabel* heroSprite = m_combatPage->getHeroSpriteLabel();
    QLabel* enemySprite = m_combatPage->getEnemySpriteLabel();

    if (!heroSprite || !enemySprite) {
        emit animationFinished();
        return;
    }

    QPoint startPos = heroSprite->pos();
    QPoint endPos = enemySprite->pos();

    QSequentialAnimationGroup *group = new QSequentialAnimationGroup(this);

    // Animation to move to the enemy
    QPropertyAnimation *attackAnimation = new QPropertyAnimation(heroSprite, "pos");
    attackAnimation->setDuration(300);
    attackAnimation->setStartValue(startPos);
    attackAnimation->setEndValue(endPos);
    attackAnimation->setEasingCurve(QEasingCurve::InOutQuad);

    // Animation to return to the original position
    QPropertyAnimation *returnAnimation = new QPropertyAnimation(heroSprite, "pos");
    returnAnimation->setDuration(300);
    returnAnimation->setStartValue(endPos);
    returnAnimation->setEndValue(startPos);
    returnAnimation->setEasingCurve(QEasingCurve::InOutQuad);

    group->addAnimation(attackAnimation);
    group->addPause(100);
    group->addAnimation(returnAnimation);

    connect(group, &QSequentialAnimationGroup::finished, this, &AnimationManager::animationFinished);
    connect(group, &QSequentialAnimationGroup::finished, group, &QSequentialAnimationGroup::deleteLater);

    group->start();
}

void AnimationManager::playDamageAnimation(QLabel* target)
{
    // Placeholder for now, just emit the signal.
    emit animationFinished();
}
