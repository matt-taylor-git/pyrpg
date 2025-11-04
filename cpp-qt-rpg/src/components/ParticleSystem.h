#ifndef PARTICLESYSTEM_H
#define PARTICLESYSTEM_H

#include <QWidget>
#include <QLabel>
#include <QPropertyAnimation>
#include <QPoint>
#include <QList>
#include <QTimer>
#include <QObject>
#include <QGraphicsOpacityEffect> // Added for fading

// Particle animation constants
namespace ParticleConstants {
    constexpr int ATTACK_IMPACT_DELAY_MS = 300;
    constexpr int COMBAT_RESULT_DELAY_MS = 200;
    constexpr int LEVEL_UP_DELAY_MS = 500;
}

// --- Particle Class ---
class Particle : public QLabel
{
    Q_OBJECT
    // Removed Q_PROPERTY for pos and windowOpacity, relying on QWidget::pos and QGraphicsOpacityEffect

public:
    explicit Particle(QWidget *parent = nullptr, const QString &particleType = "star", const QString &color = "#dc3545");
    ~Particle() override;

    void animate(const QPoint &startPos, const QPoint &endPos, int duration = 1000);

private:
    QList<QPropertyAnimation*> m_animations;
    QGraphicsOpacityEffect *m_opacityEffect; // New member for fading
};

// --- ParticleSystem Class ---
class ParticleSystem : public QWidget
{
    Q_OBJECT

signals:
    void animationFinished();

public:
    explicit ParticleSystem(QWidget *parent = nullptr);

    void createBurst(const QPoint &centerPos, int particleCount = 12, const QString &particleType = "star", const QString &color = "#dc3545", bool emitSignal = true);
    void victoryExplosion(const QPoint &centerPos);
    void healingBurst(const QPoint &centerPos);
    void levelUpBurst(const QPoint &centerPos);
    void goldRewardBurst(const QPoint &centerPos);

private slots:
    void onParticleDestroyed();

private:
    QList<Particle*> m_particles;
    int m_activeParticleCount;
    bool m_emitSignalWhenComplete;
};

// --- AchievementSystem Class ---
class AchievementSystem : public QObject
{
    Q_OBJECT

public:
    explicit AchievementSystem(QWidget *parentWidget);
    ~AchievementSystem() override = default;

    void triggerAchievement(const QString &achievementType, const QPoint &position);

private slots:
    void onParticlesFinished();

private:
    void showAchievementText(const QString &text, const QPoint &position, const QString &color);

    QWidget *m_parent;
    ParticleSystem *m_particleSystem;
    QList<QPropertyAnimation*> m_textAnimations;
};

#endif // PARTICLESYSTEM_H
