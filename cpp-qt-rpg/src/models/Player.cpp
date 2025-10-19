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
