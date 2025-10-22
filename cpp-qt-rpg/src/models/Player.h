#ifndef PLAYER_H
#define PLAYER_H

#include "Character.h"
#include "Item.h"
#include "Skill.h"
#include <QList>
#include <QMap>
#include <QDataStream>

class Player : public Character
{
public:
    explicit Player(const QString &name, const QString &characterClass = "Hero");

    int mana;
    int maxMana;
    int strength;
    int dexterity;
    int intelligence;
    int vitality;

    QString characterClass;
    QList<Skill*> skills;

    QMap<QString, Item*> equipment;
    QList<Item*> inventory;
    int gold;

    int experience;
    int experienceToLevel;
    int skillPoints;
    int statPoints;

    // Skill management
    void learnSkill(Skill* skill);
    bool hasSkill(const QString &skillName) const;
    Skill* getSkill(const QString &skillName) const;

    // Item management
    bool equipItem(Item* item);
    bool unequipItem(const QString &slot);
    bool useItem(Item* item);

    // Stat management
    void gainExperience(int amount);
    void levelUp();
    int getTotalAttack() const;
    int getTotalDefense() const;

    friend QDataStream &operator<<(QDataStream &out, const Player &p);
    friend QDataStream &operator>>(QDataStream &in, Player &p);
};

#endif // PLAYER_H
