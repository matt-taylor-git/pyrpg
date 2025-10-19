#include "Item.h"

Item::Item(const QString &name, const QString &itemType, const QString &rarity, 
           const QString &slot, int attackBonus, int defenseBonus, 
           const QString &effect, int power, int value, const QString &description)
    : name(name), itemType(itemType), rarity(rarity), slot(slot), 
      attackBonus(attackBonus), defenseBonus(defenseBonus), effect(effect), 
      power(power), value(value), description(description)
{
}
