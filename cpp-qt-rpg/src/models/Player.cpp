#include "Player.h"

Player::Player(const QString &name)
    : Character(name, 1, 100, 100), // Base stats for a new player
      mana(50),
      maxMana(50),
      strength(12),
      dexterity(10),
      intelligence(8),
      vitality(10),
      gold(100),
      experience(0),
      experienceToLevel(100),
      skillPoints(0),
      statPoints(0)
{
    // Initialize equipment with nullptrs
    equipment["weapon"] = nullptr;
    equipment["armor"] = nullptr;
    equipment["accessory"] = nullptr;
}

QDataStream &operator<<(QDataStream &out, const Player &p)
{
    // Serialize base class
    out << static_cast<const Character&>(p);
    // Serialize Player members
    out << p.mana << p.maxMana << p.strength << p.dexterity << p.intelligence << p.vitality;
    out << p.gold << p.experience << p.experienceToLevel << p.skillPoints << p.statPoints;

    // Serialize equipment: only non-null items
    QMap<QString, Item> eq;
    for (auto it = p.equipment.begin(); it != p.equipment.end(); ++it) {
        if (it.value() != nullptr) {
            eq[it.key()] = *it.value();
        }
    }
    out << eq;

    // Serialize inventory
    QList<Item> inv;
    for (Item* item : p.inventory) {
        if (item != nullptr) {
            inv.append(*item);
        }
    }
    out << inv;

    return out;
}

QDataStream &operator>>(QDataStream &in, Player &p)
{
    // Deserialize base class
    in >> static_cast<Character&>(p);
    // Deserialize Player members
    in >> p.mana >> p.maxMana >> p.strength >> p.dexterity >> p.intelligence >> p.vitality;
    in >> p.gold >> p.experience >> p.experienceToLevel >> p.skillPoints >> p.statPoints;

    // Deserialize equipment
    QMap<QString, Item> eq;
    in >> eq;
    for (auto it = eq.begin(); it != eq.end(); ++it) {
        p.equipment[it.key()] = new Item(it.value());
    }
    // Ensure slots are initialized if not present
    if (!p.equipment.contains("weapon")) p.equipment["weapon"] = nullptr;
    if (!p.equipment.contains("armor")) p.equipment["armor"] = nullptr;
    if (!p.equipment.contains("accessory")) p.equipment["accessory"] = nullptr;

    // Deserialize inventory
    QList<Item> inv;
    in >> inv;
    for (const Item &item : inv) {
        p.inventory.append(new Item(item));
    }

    return in;
}
