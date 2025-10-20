#include "SaveManager.h"
#include "../models/Player.h"
#include "../game/factories/ItemFactory.h"
#include <QFile>
#include <QDataStream>
#include <QDebug>

SaveManager::SaveManager()
{
}

bool SaveManager::saveGame(Player *player, const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Could not open file for writing:" << filePath;
        return false;
    }

    QDataStream out(&file);
    out.setVersion(QDataStream::Qt_6_0);
    out << *player;

    file.close();
    return true;
}

Player* SaveManager::loadGame(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Could not open file for reading:" << filePath;
        return nullptr;
    }

    QDataStream in(&file);
    in.setVersion(QDataStream::Qt_6_0);

    Player *player = new Player(""); // Create a dummy player
    in >> *player;

    file.close();
    return player;
}
