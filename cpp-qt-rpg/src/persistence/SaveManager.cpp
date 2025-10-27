#include "SaveManager.h"
#include "../models/Player.h"
#include "../game/factories/ItemFactory.h"
#include <QFile>
#include <QDataStream>
#include <QDebug>
#include <QDir>
#include <QFileInfo>
#include <QStandardPaths>

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

QString SaveManager::getSavesDirectory() const
{
    QString dataDir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    return dataDir + "/saves";
}

bool SaveManager::ensureSavesDirectoryExists() const
{
    QDir dir;
    QString savesPath = getSavesDirectory();
    if (!dir.exists(savesPath)) {
        return dir.mkpath(savesPath);
    }
    return true;
}

QString SaveManager::getSlotFilePath(int slotNumber) const
{
    return getSavesDirectory() + QString("/save_slot_%1.dat").arg(slotNumber);
}

SaveSlotInfo SaveManager::getSlotInfo(int slotNumber) const
{
    SaveSlotInfo info;
    info.slotNumber = slotNumber;
    info.filePath = getSlotFilePath(slotNumber);
    info.exists = false;

    QFileInfo fileInfo(info.filePath);
    if (!fileInfo.exists()) {
        return info;
    }

    info.exists = true;
    info.saveTime = fileInfo.lastModified();

    // Try to read basic player info without loading the full player
    Player *player = loadGame(info.filePath);
    if (player) {
        info.characterName = player->getName();
        info.level = player->getLevel();
        delete player;
    }

    return info;
}

QList<SaveSlotInfo> SaveManager::getSaveSlots() const
{
    QList<SaveSlotInfo> slots;
    for (int i = 1; i <= MAX_SAVE_SLOTS; ++i) {
        slots.append(getSlotInfo(i));
    }
    return slots;
}

bool SaveManager::saveToSlot(Player *player, int slotNumber)
{
    if (slotNumber < 1 || slotNumber > MAX_SAVE_SLOTS) {
        qWarning() << "Invalid slot number:" << slotNumber;
        return false;
    }

    if (!ensureSavesDirectoryExists()) {
        qWarning() << "Failed to create saves directory";
        return false;
    }

    QString filePath = getSlotFilePath(slotNumber);
    return saveGame(player, filePath);
}

Player* SaveManager::loadFromSlot(int slotNumber)
{
    if (slotNumber < 1 || slotNumber > MAX_SAVE_SLOTS) {
        qWarning() << "Invalid slot number:" << slotNumber;
        return nullptr;
    }

    QString filePath = getSlotFilePath(slotNumber);
    return loadGame(filePath);
}

bool SaveManager::deleteSaveSlot(int slotNumber)
{
    if (slotNumber < 1 || slotNumber > MAX_SAVE_SLOTS) {
        qWarning() << "Invalid slot number:" << slotNumber;
        return false;
    }

    QString filePath = getSlotFilePath(slotNumber);
    QFile file(filePath);

    if (!file.exists()) {
        return true; // Already deleted
    }

    return file.remove();
}
