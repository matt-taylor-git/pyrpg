#include "Skill.h"

Skill::Skill(const QString &name, const QString &skillType, int damage, int manaCost, const QString &description)
    : name(name), skillType(skillType), damage(damage), manaCost(manaCost), description(description)
{
}
