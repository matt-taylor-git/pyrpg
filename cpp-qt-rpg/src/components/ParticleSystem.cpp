#include "ParticleSystem.h"
#include <QEasingCurve>
#include <QDebug>
#include <cmath>
#include <random>
#include <QFontMetrics>
#include <QGraphicsOpacityEffect>

// Particle constants
namespace ParticleConstants {
    constexpr int PARTICLE_SIZE = 16;
    constexpr int MIN_DURATION_MS = 800;
    constexpr int MAX_DURATION_MS = 1200;
    constexpr int MIN_RADIUS = 30;
    constexpr int MAX_RADIUS = 80;
    constexpr int POSITION_VARIANCE = 10;
    constexpr int PARTICLE_HALF_SIZE = PARTICLE_SIZE / 2;
    constexpr double FADE_DURATION_RATIO = 0.7;
    constexpr int VICTORY_SECOND_BURST_DELAY_MS = 200;
    constexpr int TEXT_FLOAT_DISTANCE = 30;
    constexpr int TEXT_ANIMATION_DURATION_MS = 2000;
    constexpr int TEXT_VERTICAL_OFFSET = 50;
    constexpr int MAX_PARTICLES_PER_BURST = 100;
    constexpr int ATTACK_IMPACT_DELAY_MS = 300;
}

// Thread-safe random number generator
namespace {
    std::random_device rd;
    std::mt19937 gen(rd());

    int randomInt(int min, int max) {
        std::uniform_int_distribution<> dis(min, max);
        return dis(gen);
    }
}

// --- Particle Implementation ---

Particle::Particle(QWidget *parent, const QString &particleType, const QString &color)
    : QLabel(parent),
      m_opacityEffect(new QGraphicsOpacityEffect(this))
{
    // The parent is passed from ParticleSystem::createBurst
    setParent(parent);
    setAttribute(Qt::WA_TranslucentBackground);
    setFixedSize(ParticleConstants::PARTICLE_SIZE, ParticleConstants::PARTICLE_SIZE);
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
    // Animations are managed by Qt's parent-child ownership and will be
    // deleted automatically. We don't need to manually delete them here.
    // Just clear the list to avoid dangling pointers.
    m_animations.clear();
}

void Particle::animate(const QPoint &startPos, const QPoint &endPos, int duration)
{
    move(startPos);

    // Position animation (no parent set - managed by m_animations list)
    QPropertyAnimation *anim = new QPropertyAnimation(this, "pos");
    anim->setStartValue(startPos);

    // Add some randomness to end position
    QPoint variance(randomInt(-ParticleConstants::POSITION_VARIANCE, ParticleConstants::POSITION_VARIANCE),
                    randomInt(-ParticleConstants::POSITION_VARIANCE, ParticleConstants::POSITION_VARIANCE));
    anim->setEndValue(endPos + variance);

    anim->setDuration(duration);
    anim->setEasingCurve(QEasingCurve::OutExpo);

    // Fade out animation (no parent set - managed by m_animations list)
    QPropertyAnimation *fadeAnim = new QPropertyAnimation(m_opacityEffect, "opacity");
    fadeAnim->setStartValue(1.0);
    fadeAnim->setEndValue(0.0);
    fadeAnim->setDuration(static_cast<int>(duration * ParticleConstants::FADE_DURATION_RATIO));
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
    : QWidget(parent),
      m_activeParticleCount(0),
      m_emitSignalWhenComplete(false)
{
    // The particle system should be transparent and cover the area where effects happen
    setAttribute(Qt::WA_TranslucentBackground);
    // We rely on the parent to set the geometry.
}

void ParticleSystem::createBurst(const QPoint &centerPos, int particleCount, const QString &particleType, const QString &color, bool emitSignal)
{
    // Input validation
    if (particleCount <= 0) {
        qWarning() << "ParticleSystem::createBurst: particleCount must be positive, got" << particleCount;
        return;
    }

    if (particleCount > ParticleConstants::MAX_PARTICLES_PER_BURST) {
        qWarning() << "ParticleSystem::createBurst: particleCount" << particleCount
                   << "exceeds maximum" << ParticleConstants::MAX_PARTICLES_PER_BURST
                   << ", clamping to maximum";
        particleCount = ParticleConstants::MAX_PARTICLES_PER_BURST;
    }

    if (emitSignal) {
        m_emitSignalWhenComplete = true;
    }

    for (int i = 0; i < particleCount; ++i) {
        Particle *particle = new Particle(this, particleType, color);

        // Track when particles are destroyed
        connect(particle, &QObject::destroyed, this, &ParticleSystem::onParticleDestroyed);
        m_activeParticleCount++;

        // Calculate position in circle
        double angle = (static_cast<double>(i) / particleCount) * 2 * M_PI;
        int radius = randomInt(ParticleConstants::MIN_RADIUS, ParticleConstants::MAX_RADIUS);
        int endX = centerPos.x() + static_cast<int>(std::cos(angle) * radius);
        int endY = centerPos.y() + static_cast<int>(std::sin(angle) * radius);

        QPoint startPos = centerPos - QPoint(ParticleConstants::PARTICLE_HALF_SIZE, ParticleConstants::PARTICLE_HALF_SIZE);
        QPoint endPos(endX, endY);

        int duration = randomInt(ParticleConstants::MIN_DURATION_MS, ParticleConstants::MAX_DURATION_MS);
        particle->animate(startPos, endPos, duration);
        m_particles.append(particle);
    }
}

void ParticleSystem::onParticleDestroyed()
{
    m_activeParticleCount--;

    // When all particles are destroyed, clean up and emit signal if needed
    if (m_activeParticleCount == 0) {
        m_particles.clear();
        if (m_emitSignalWhenComplete) {
            m_emitSignalWhenComplete = false;
            emit animationFinished();
        }
    }
}

void ParticleSystem::victoryExplosion(const QPoint &centerPos)
{
    // First burst doesn't emit signal
    createBurst(centerPos, 8, "star", "#e5c07b", false);
    // Second burst will emit signal when all particles from both bursts are done
    QTimer::singleShot(ParticleConstants::VICTORY_SECOND_BURST_DELAY_MS, [this, centerPos] {
        createBurst(centerPos, 6, "spark", "#98c379", true);
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

    // Create opacity effect for proper fading
    QGraphicsOpacityEffect *opacityEffect = new QGraphicsOpacityEffect(label);
    label->setGraphicsEffect(opacityEffect);

    // Position above the effect
    QFontMetrics fm(label->font());
    QPoint textPos = position - QPoint(fm.horizontalAdvance(text) / 2, ParticleConstants::TEXT_VERTICAL_OFFSET);
    label->move(textPos);
    label->show();

    // Animate text floating up and fading
    QPropertyAnimation *anim = new QPropertyAnimation(label, "pos", this);
    anim->setStartValue(textPos);
    anim->setEndValue(textPos - QPoint(0, ParticleConstants::TEXT_FLOAT_DISTANCE));
    anim->setDuration(ParticleConstants::TEXT_ANIMATION_DURATION_MS);
    anim->setEasingCurve(QEasingCurve::OutQuad);

    QPropertyAnimation *fadeAnim = new QPropertyAnimation(opacityEffect, "opacity", this);
    fadeAnim->setStartValue(1.0);
    fadeAnim->setEndValue(0.0);
    fadeAnim->setDuration(ParticleConstants::TEXT_ANIMATION_DURATION_MS);

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
