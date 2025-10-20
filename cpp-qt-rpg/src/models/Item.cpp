#include "Item.h"

Item::Item()
    : name(""), itemType(""), rarity("common"), slot(""),
      attackBonus(0), defenseBonus(0), effect(""), power(0), value(0), description("")
{
}

Item::Item(const QString &name, const QString &itemType, const QString &rarity,
           const QString &slot, int attackBonus, int defenseBonus,
           const QString &effect, int power, int value, const QString &description)
    : name(name), itemType(itemType), rarity(rarity), slot(slot),
      attackBonus(attackBonus), defenseBonus(defenseBonus), effect(effect),
      power(power), value(value), description(description)
{
}

QDataStream &operator<<(QDataStream &out, const Item &item)
{
    out << item.name << item.itemType << item.rarity << item.slot
        << item.attackBonus << item.defenseBonus << item.effect
        << item.power << item.value << item.description;
    return out;
}

QDataStream &operator>>(QDataStream &in, Item &item)
{
    in >> item.name >> item.itemType >> item.rarity >> item.slot
       >> item.attackBonus >> item.defenseBonus >> item.effect
       >> item.power >> item.value >> item.description;
    return in;
}

