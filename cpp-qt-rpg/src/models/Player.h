#ifndef PLAYER_H
#define PLAYER_H

#include "Character.h"
#include "Item.h"
#include "Skill.h"
#include <QList>
#include <QMap>

class Player : public Character
{
public:
    explicit Player(const QString &name);

    int mana;
    int maxMana;
    int strength;
    int dexterity;
    int intelligence;
    int vitality;

    QMap<QString, Item*> equipment;
    QList<Item*> inventory;
    int gold;

    int experience;
    int experienceToLevel;
    int skillPoints;
    int statPoints;
};

#endif // PLAYER_H
