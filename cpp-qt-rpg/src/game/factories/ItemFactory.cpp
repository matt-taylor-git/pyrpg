#include "ItemFactory.h"
#include <QRandomGenerator>

Item* ItemFactory::generateRandomItem(int enemyLevel)
{
    // This is a simplified port. A more robust system would use data files.
    QStringList itemTypes = {"weapon", "armor", "accessory", "consumable"};
    QString itemType = itemTypes.at(QRandomGenerator::global()->bounded(itemTypes.size()));

    if (itemType == "consumable") {
        QList<Item*> consumables;
        consumables.append(new Item("Health Potion", "consumable", "common", "", 0, 0, "heal", 50, 25));
        consumables.append(new Item("Mana Potion", "consumable", "common", "", 0, 0, "restore_mana", 30, 20));
        return consumables.at(QRandomGenerator::global()->bounded(consumables.size()));
    }

    // Simplified logic for equipment generation
    QString name = "Random Item";
    QString rarity = "common";
    int value = 10 * enemyLevel;

    if (itemType == "weapon") {
        name = "Random Sword";
        int attackBonus = 5 + enemyLevel;
        return new Item(name, "weapon", rarity, "weapon", attackBonus, 0, "", 0, value);
    }
    if (itemType == "armor") {
        name = "Random Armor";
        int defenseBonus = 3 + enemyLevel;
        return new Item(name, "armor", rarity, "armor", 0, defenseBonus, "", 0, value);
    }
    if (itemType == "accessory") {
        name = "Random Ring";
        int bonus = 2 + enemyLevel;
        return new Item(name, "accessory", rarity, "accessory", bonus, bonus, "", 0, value);
    }

    return new Item("Junk", "junk", "common"); // Fallback
}

QMap<QString, Item*> ItemFactory::getShopItems()
{
    QMap<QString, Item*> items;
    items.insert("Health Potion", new Item("Health Potion", "consumable", "common", "", 0, 0, "heal", 50, 25, "Restores 50 HP"));
    items.insert("Mana Potion", new Item("Mana Potion", "consumable", "common", "", 0, 0, "restore_mana", 30, 20, "Restores 30 MP"));
    items.insert("Iron Sword", new Item("Iron Sword", "weapon", "common", "weapon", 8, 0, "", 0, 75, "+8 Attack Power"));
    items.insert("Leather Armor", new Item("Leather Armor", "armor", "common", "armor", 0, 5, "", 0, 60, "+5 Defense"));
    return items;
}
