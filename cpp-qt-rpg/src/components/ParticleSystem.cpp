#include "ParticleSystem.h"
#include <QEasingCurve>
#include <QDebug>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <QFontMetrics>
#include <QGraphicsOpacityEffect>

// Initialize random seed once
namespace {
    struct RandomInitializer {
        RandomInitializer() { std::srand(std::time(0)); }
    } initializer;
}

// --- Particle Implementation ---

Particle::Particle(QWidget *parent, const QString &particleType, const QString &color)
    : QLabel(parent),
      m_opacityEffect(new QGraphicsOpacityEffect(this))
{
    // The parent is passed from ParticleSystem::createBurst
    setParent(parent);
    setAttribute(Qt::WA_TranslucentBackground);
    setFixedSize(16, 16);
    setGraphicsEffect(m_opacityEffect); // Apply the opacity effect

    QString text;
    if (particleType == "star") text = "⭐";
    else if (particleType == "spark") text = "✨";
    else if (particleType == "coin") text = "💰";
    else if (particleType == "heart") text = "💚";
    else text = "•";

    setText(text);
    setStyleSheet(QString("color: %1; font-size: 12px; font-weight: bold;").arg(color));
    show();
}

Particle::~Particle()
{
    qDeleteAll(m_animations);
    m_animations.clear();
}

void Particle::animate(const QPoint &startPos, const QPoint &endPos, int duration)
{
    move(startPos);

    // Position animation
    QPropertyAnimation *anim = new QPropertyAnimation(this, "pos", this); // Use "pos" property
    anim->setStartValue(startPos);

    // Add some randomness to end position
    QPoint variance(std::rand() % 21 - 10, std::rand() % 21 - 10); // -10 to 10
    anim->setEndValue(endPos + variance);

    anim->setDuration(duration);
    anim->setEasingCurve(QEasingCurve::OutExpo);

    // Fade out animation (Targeting QGraphicsOpacityEffect's opacity property)
    QPropertyAnimation *fadeAnim = new QPropertyAnimation(m_opacityEffect, "opacity", this);
    fadeAnim->setStartValue(1.0);
    fadeAnim->setEndValue(0.0);
    fadeAnim->setDuration(static_cast<int>(duration * 0.7));
    fadeAnim->setEasingCurve(QEasingCurve::InQuad);

    // Connect to delete the particle when fade is finished
    connect(fadeAnim, &QPropertyAnimation::finished, this, &Particle::deleteLater);

    anim->start();
    fadeAnim->start();

    m_animations.append(anim);
    m_animations.append(fadeAnim);
}

// --- ParticleSystem Implementation ---

ParticleSystem::ParticleSystem(QWidget *parent)
    : QWidget(parent)
{
    // The particle system should be transparent and cover the area where effects happen
    setAttribute(Qt::WA_TranslucentBackground);
    // We rely on the parent to set the geometry.
}

void ParticleSystem::createBurst(const QPoint &centerPos, int particleCount, const QString &particleType, const QString &color)
{
    for (int i = 0; i < particleCount; ++i) {
        Particle *particle = new Particle(this, particleType, color);

        // Calculate position in circle
        double angle = (static_cast<double>(i) / particleCount) * 2 * M_PI;
        int radius = std::rand() % 51 + 30; // 30 to 80
        int endX = centerPos.x() + static_cast<int>(std::cos(angle) * radius);
        int endY = centerPos.y() + static_cast<int>(std::sin(angle) * radius);

        QPoint startPos = centerPos - QPoint(8, 8); // Center the particle
        QPoint endPos(endX, endY);

        int duration = std::rand() % 401 + 800; // 800 to 1200
        particle->animate(startPos, endPos, duration);
        m_particles.append(particle);
    }

    // Clean up after animation completes
    QTimer::singleShot(1500, this, &ParticleSystem::cleanup);
}

void ParticleSystem::cleanup()
{
    // The particles delete themselves via deleteLater().
    // We just clear the list of pointers and emit the signal.
    m_particles.clear();
    emit animationFinished();
}

void ParticleSystem::victoryExplosion(const QPoint &centerPos)
{
    createBurst(centerPos, 8, "star", "#e5c07b");
    QTimer::singleShot(200, [this, centerPos] {
        createBurst(centerPos, 6, "spark", "#98c379");
    });
}

void ParticleSystem::healingBurst(const QPoint &centerPos)
{
    createBurst(centerPos, 10, "heart", "#27ae60");
}

void ParticleSystem::levelUpBurst(const QPoint &centerPos)
{
    createBurst(centerPos, 15, "star", "#c678dd");
}

void ParticleSystem::goldRewardBurst(const QPoint &centerPos)
{
    createBurst(centerPos, 8, "coin", "#e5c07b");
}

// --- AchievementSystem Implementation ---

AchievementSystem::AchievementSystem(QWidget *parentWidget)
    : QObject(parentWidget),
      m_parent(parentWidget),
      m_particleSystem(new ParticleSystem(parentWidget))
{
    // The particle system should be the same size as the parent to cover the area
    m_particleSystem->setGeometry(parentWidget->rect());
    m_particleSystem->show();
    // We need to ensure the particle system resizes with the parent
    // This is usually done by setting a layout on the parent, but since we don't have access
    // to the parent's layout, we'll connect to the parent's resize event if possible,
    // or rely on the user to set the geometry correctly. For now, we'll assume the parent
    // is a fixed size or the user will handle the resize.

    connect(m_particleSystem, &ParticleSystem::animationFinished, this, &AchievementSystem::onParticlesFinished);
}

void AchievementSystem::triggerAchievement(const QString &achievementType, const QPoint &position)
{
    if (achievementType == "victory") {
        m_particleSystem->victoryExplosion(position);
        showAchievementText("Victory!", position, "#98c379");
    } else if (achievementType == "level_up") {
        m_particleSystem->levelUpBurst(position);
        showAchievementText("Level Up!", position, "#c678dd");
    } else if (achievementType == "critical_hit") {
        m_particleSystem->createBurst(position, 6, "spark", "#e74c3c");
        showAchievementText("Critical!", position, "#e74c3c");
    } else if (achievementType == "healing") {
        m_particleSystem->healingBurst(position);
        showAchievementText("Healed!", position, "#27ae60");
    }
}

void AchievementSystem::showAchievementText(const QString &text, const QPoint &position, const QString &color)
{
    QLabel *label = new QLabel(text, m_parent);
    label->setStyleSheet(QString(R"(
        color: %1;
        font-size: 16px;
        font-weight: bold;
        background: rgba(0, 0, 0, 0);
        border: none;
    )").arg(color));

    // Position above the effect
    QFontMetrics fm(label->font());
    QPoint textPos = position - QPoint(fm.horizontalAdvance(text) / 2, 50);
    label->move(textPos);
    label->show();

    // Animate text floating up and fading
    QPropertyAnimation *anim = new QPropertyAnimation(label, "pos", this);
    anim->setStartValue(textPos);
    anim->setEndValue(textPos - QPoint(0, 30));
    anim->setDuration(2000);
    anim->setEasingCurve(QEasingCurve::OutQuad);

    QPropertyAnimation *fadeAnim = new QPropertyAnimation(label, "windowOpacity", this);
    fadeAnim->setStartValue(1.0);
    fadeAnim->setEndValue(0.0);
    fadeAnim->setDuration(2000);

    // Connect to delete the label when fade is finished
    connect(fadeAnim, &QPropertyAnimation::finished, label, &QLabel::deleteLater);

    anim->start();
    fadeAnim->start();

    // Store references to prevent garbage collection
    m_textAnimations.append(anim);
    m_textAnimations.append(fadeAnim);
}

void AchievementSystem::onParticlesFinished()
{
    // Clean up finished text animations
    for (int i = m_textAnimations.size() - 1; i >= 0; --i) {
        QPropertyAnimation *anim = m_textAnimations.at(i);
        if (anim->state() == QAbstractAnimation::Stopped) {
            // The animation is a child of AchievementSystem (this), so it will be deleted
            // when AchievementSystem is deleted. We don't need to delete it here, just remove the pointer.
            m_textAnimations.removeAt(i);
        }
    }
}
