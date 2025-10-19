#ifndef SKILL_H
#define SKILL_H

#include <QString>

class Skill
{
public:
    Skill(const QString &name, const QString &skillType, int damage, int manaCost, const QString &description = "");

    QString name;
    QString skillType;
    int damage;
    int manaCost;
    QString description;
};

#endif // SKILL_H
