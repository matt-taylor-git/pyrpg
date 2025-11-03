#include "StoryManager.h"
#include "factories/StoryEventFactory.h"
#include <QDebug>

StoryManager::StoryManager(Player* player, QObject* parent)
    : QObject(parent)
    , m_player(player)
{
}

StoryManager::~StoryManager()
{
    // Events are managed by factory static cache, don't delete them here
    m_allEvents.clear();
    m_eventMap.clear();
}

void StoryManager::loadEvents()
{
    QList<StoryEvent*> events = StoryEventFactory::getAllEvents();
    for (StoryEvent* event : events) {
        if (event) {
            m_eventMap[event->eventId] = event;
            m_allEvents.append(event);
        }
    }
    qDebug() << "Loaded" << m_allEvents.size() << "story events";
}

void StoryManager::checkEventTriggers()
{
    for (StoryEvent* event : m_allEvents) {
        if (event->triggerType == "level_reached") {
            int requiredLevel = event->triggerId.toInt();
            if (m_player->level >= requiredLevel) {
                triggerEvent(event->eventId);
            }
        }
    }
}

void StoryManager::triggerEvent(const QString &eventId)
{
    StoryEvent* event = m_eventMap.value(eventId, nullptr);
    if (!event) {
        qWarning() << "Story event not found:" << eventId;
        return;
    }

    // Check if already viewed
    if (m_player->hasViewedEvent(eventId)) {
        qDebug() << "Story event already viewed:" << eventId;
        return;
    }

    // Check prerequisites
    for (const QString &prereq : event->prerequisites) {
        if (prereq.startsWith("quest_")) {
            QString questId = prereq.mid(6);  // Remove "quest_" prefix
            Quest* quest = m_player->getQuest(questId);
            if (!quest || !quest->isComplete()) {
                qDebug() << "Event prerequisite not met:" << prereq;
                return;
            }
        } else if (prereq.startsWith("level_")) {
            int requiredLevel = prereq.mid(6).toInt();
            if (m_player->level < requiredLevel) {
                qDebug() << "Event requires level" << requiredLevel;
                return;
            }
        }
    }

    // Emit event (copy event data for UI)
    emit eventTriggered(*event);

    // Mark as viewed
    m_player->markEventViewed(eventId);
}

void StoryManager::onQuestStarted(const QString &questId)
{
    for (StoryEvent* event : m_allEvents) {
        if (event->triggerType == "quest_start" && event->triggerId == questId) {
            triggerEvent(event->eventId);
        }
    }
}

void StoryManager::onQuestCompleted(const QString &questId)
{
    for (StoryEvent* event : m_allEvents) {
        if (event->triggerType == "quest_complete" && event->triggerId == questId) {
            triggerEvent(event->eventId);
        }
    }
}

void StoryManager::onLevelReached(int level)
{
    checkEventTriggers();
}
