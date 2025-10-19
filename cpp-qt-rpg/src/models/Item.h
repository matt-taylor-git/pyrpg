#ifndef ITEM_H
#define ITEM_H

#include <QString>

class Item
{
public:
    Item(const QString &name, const QString &itemType, const QString &rarity = "common", 
         const QString &slot = "", int attackBonus = 0, int defenseBonus = 0, 
         const QString &effect = "", int power = 0, int value = 0, const QString &description = "");

    QString name;
    QString itemType;
    QString rarity;
    QString slot;
    int attackBonus;
    int defenseBonus;
    QString effect;
    int power;
    int value;
    QString description;
};

#endif // ITEM_H
