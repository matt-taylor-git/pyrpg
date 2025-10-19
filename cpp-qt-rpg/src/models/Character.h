#ifndef CHARACTER_H
#define CHARACTER_H

#include <QString>

class Character
{
public:
    explicit Character(const QString &name, int level, int health, int maxHealth);
    virtual ~Character() = default;

    QString name;
    int level;
    int health;
    int maxHealth;

    bool isAlive() const;
};

#endif // CHARACTER_H
