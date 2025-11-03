#ifndef MONSTERFACTORY_H
#define MONSTERFACTORY_H

#include "models/Monster.h"
#include "models/FinalBoss.h"
#include <QString>

class MonsterFactory
{
public:
    static Monster* createMonster(const QString &monsterType, int playerLevel);
    static Monster* createRandomMonster(int playerLevel);
    static Monster* createBoss(int playerLevel);
    static FinalBoss* createFinalBoss(int playerLevel);
};

#endif // MONSTERFACTORY_H
