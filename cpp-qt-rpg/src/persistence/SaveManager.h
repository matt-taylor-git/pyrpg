#ifndef SAVEMANAGER_H
#define SAVEMANAGER_H

#include <QString>

class Player;

class SaveManager
{
public:
    SaveManager();
    bool saveGame(Player *player, const QString &filePath);
    Player* loadGame(const QString &filePath);
};

#endif // SAVEMANAGER_H
