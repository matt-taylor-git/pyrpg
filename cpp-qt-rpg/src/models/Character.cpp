#include "Character.h"

Character::Character(const QString &name, int level, int health, int maxHealth)
    : name(name), level(level), health(health), maxHealth(maxHealth)
{
}

bool Character::isAlive() const
{
    return health > 0;
}
