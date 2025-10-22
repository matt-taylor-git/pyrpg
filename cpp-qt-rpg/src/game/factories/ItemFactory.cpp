#include "ItemFactory.h"
#include <QRandomGenerator>

Item* ItemFactory::generateRandomItem(int enemyLevel)
{
    // Weighted drop rates
    int roll = QRandomGenerator::global()->bounded(100);

    if (roll < 50) {
        // 50% consumable
        QList<Item*> consumables;
        consumables.append(new Item("Health Potion", "consumable", "common", "", 0, 0, "heal", 50, 25));
        consumables.append(new Item("Mana Potion", "consumable", "common", "", 0, 0, "restore_mana", 30, 20));
        consumables.append(new Item("Greater Health Potion", "consumable", "uncommon", "", 0, 0, "heal", 100, 50));
        return consumables.at(QRandomGenerator::global()->bounded(consumables.size()));
    }

    // Determine rarity
    QString rarity;
    double rarityMultiplier = 1.0;
    int rarityRoll = QRandomGenerator::global()->bounded(100);
    if (rarityRoll < 60) {
        rarity = "common";
        rarityMultiplier = 1.0;
    } else if (rarityRoll < 85) {
        rarity = "uncommon";
        rarityMultiplier = 1.5;
    } else if (rarityRoll < 96) {
        rarity = "rare";
        rarityMultiplier = 2.0;
    } else {
        rarity = "epic";
        rarityMultiplier = 3.0;
    }

    int value = static_cast<int>(10 * enemyLevel * rarityMultiplier);

    // Choose equipment type
    QStringList equipmentTypes = {"weapon", "armor", "accessory"};
    QString itemType = equipmentTypes.at(QRandomGenerator::global()->bounded(equipmentTypes.size()));

    if (itemType == "weapon") {
        QStringList weaponNames = {"Iron Sword", "Steel Blade", "Battle Axe", "War Hammer", "Long Spear", "Magic Staff"};
        QString name = weaponNames.at(QRandomGenerator::global()->bounded(weaponNames.size()));
        int attackBonus = static_cast<int>((5 + enemyLevel * 2) * rarityMultiplier);
        return new Item(name, "weapon", rarity, "weapon", attackBonus, 0, "", 0, value, QString("+%1 Attack").arg(attackBonus));
    }
    else if (itemType == "armor") {
        QStringList armorNames = {"Leather Armor", "Chain Mail", "Plate Armor", "Robes", "Battle Vest"};
        QString name = armorNames.at(QRandomGenerator::global()->bounded(armorNames.size()));
        int defenseBonus = static_cast<int>((3 + enemyLevel) * rarityMultiplier);
        return new Item(name, "armor", rarity, "armor", 0, defenseBonus, "", 0, value, QString("+%1 Defense").arg(defenseBonus));
    }
    else {
        QStringList accessoryNames = {"Ring of Power", "Amulet", "Belt", "Gloves", "Boots"};
        QString name = accessoryNames.at(QRandomGenerator::global()->bounded(accessoryNames.size()));
        int attackBonus = static_cast<int>((2 + enemyLevel) * rarityMultiplier);
        int defenseBonus = static_cast<int>((2 + enemyLevel) * rarityMultiplier);
        return new Item(name, "accessory", rarity, "accessory", attackBonus, defenseBonus, "", 0, value,
                       QString("+%1 ATK, +%2 DEF").arg(attackBonus).arg(defenseBonus));
    }
}

QMap<QString, Item*> ItemFactory::getShopItems()
{
    QMap<QString, Item*> items;

    // Consumables
    items.insert("Health Potion", new Item("Health Potion", "consumable", "common", "", 0, 0, "heal", 50, 25, "Restores 50 HP"));
    items.insert("Mana Potion", new Item("Mana Potion", "consumable", "common", "", 0, 0, "restore_mana", 30, 20, "Restores 30 MP"));
    items.insert("Greater Health Potion", new Item("Greater Health Potion", "consumable", "uncommon", "", 0, 0, "heal", 100, 50, "Restores 100 HP"));
    items.insert("Greater Mana Potion", new Item("Greater Mana Potion", "consumable", "uncommon", "", 0, 0, "restore_mana", 60, 40, "Restores 60 MP"));

    // Weapons
    items.insert("Iron Sword", new Item("Iron Sword", "weapon", "common", "weapon", 8, 0, "", 0, 75, "+8 Attack Power"));
    items.insert("Steel Sword", new Item("Steel Sword", "weapon", "uncommon", "weapon", 15, 0, "", 0, 150, "+15 Attack Power"));
    items.insert("Magic Staff", new Item("Magic Staff", "weapon", "rare", "weapon", 20, 0, "", 0, 300, "+20 Attack Power, Enhanced Magic"));
    items.insert("War Hammer", new Item("War Hammer", "weapon", "uncommon", "weapon", 18, 0, "", 0, 175, "+18 Attack Power"));

    // Armor
    items.insert("Leather Armor", new Item("Leather Armor", "armor", "common", "armor", 0, 5, "", 0, 60, "+5 Defense"));
    items.insert("Chain Mail", new Item("Chain Mail", "armor", "uncommon", "armor", 0, 10, "", 0, 120, "+10 Defense"));
    items.insert("Plate Armor", new Item("Plate Armor", "armor", "rare", "armor", 0, 18, "", 0, 280, "+18 Defense"));

    // Accessories
    items.insert("Power Ring", new Item("Power Ring", "accessory", "uncommon", "accessory", 5, 3, "", 0, 100, "+5 ATK, +3 DEF"));
    items.insert("Amulet of Vitality", new Item("Amulet of Vitality", "accessory", "rare", "accessory", 3, 8, "", 0, 200, "+3 ATK, +8 DEF"));

    return items;
}

Item* ItemFactory::createItem(const QString &name)
{
    static QMap<QString, Item> allItems;
    if (allItems.isEmpty()) {
        // Initialize all possible items
        allItems.insert("Health Potion", Item("Health Potion", "consumable", "common", "", 0, 0, "heal", 50, 25, "Restores 50 HP"));
        allItems.insert("Mana Potion", Item("Mana Potion", "consumable", "common", "", 0, 0, "restore_mana", 30, 20, "Restores 30 MP"));
        allItems.insert("Iron Sword", Item("Iron Sword", "weapon", "common", "weapon", 8, 0, "", 0, 75, "+8 Attack Power"));
        allItems.insert("Magic Sword", Item("Magic Sword", "weapon", "rare", "weapon", 15, 0, "", 0, 200, "+15 Attack Power"));
        allItems.insert("Leather Armor", Item("Leather Armor", "armor", "common", "armor", 0, 5, "", 0, 60, "+5 Defense"));
    }

    if (allItems.contains(name)) {
        return new Item(allItems[name]);
    }

    return nullptr; // Or a default item
}
