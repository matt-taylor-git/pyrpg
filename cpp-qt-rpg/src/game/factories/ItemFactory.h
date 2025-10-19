#ifndef ITEMFACTORY_H
#define ITEMFACTORY_H

#include "models/Item.h"
#include <QList>
#include <QMap>

class ItemFactory
{
public:
    static Item* generateRandomItem(int enemyLevel);
    static QMap<QString, Item*> getShopItems();
};

#endif // ITEMFACTORY_H
