# Monster Class Implementation Analysis

## 1. Class Structure & Inheritance

### Monster Class Declaration
```cpp
class Monster : public Character
{
public:
    Monster(const QString &name, int level, const QString &enemyType = "normal");

    QString enemyType;
    int attack;
    int defense;
    int magicAttack;
    int expReward;
    int goldReward;
};
```

### Inheritance Hierarchy
```
Character (base class)
├── name: QString
├── level: int
├── health: int
├── maxHealth: int
├── isAlive(): bool
│
└── Monster (derived)
    ├── enemyType: QString
    ├── attack: int
    ├── defense: int
    ├── magicAttack: int (mostly unused in current implementation)
    ├── expReward: int
    └── goldReward: int
```

## 2. Constructor Implementation

```cpp
Monster::Monster(const QString &name, int level, const QString &enemyType)
    : Character(name, level, 50 + (level * 15), 50 + (level * 15)),
      enemyType(enemyType),
      attack(8 + (level * 2)),
      defense(3 + (level * 1.5)),
      magicAttack(5 + (level * 1.5)),
      expReward(level * 25),
      goldReward(level * 5)
{
}
```

### Key Stats Calculation
- **Health**: 50 + (level * 15) - scales linearly with level
- **Attack**: 8 + (level * 2) - base 8, +2 per level
- **Defense**: 3 + (level * 1.5) - base 3, +1.5 per level
- **Magic Attack**: 5 + (level * 1.5) - defined but mostly unused
- **Experience**: level * 25 - varies by monster type in MonsterFactory
- **Gold**: level * 5 - varies by monster type in MonsterFactory

## 3. Fields and Methods Summary

### Public Fields
| Field | Type | Purpose |
|-------|------|---------|
| `name` (inherited) | QString | Monster name |
| `level` (inherited) | int | Monster level |
| `health` (inherited) | int | Current health |
| `maxHealth` (inherited) | int | Max health capacity |
| `enemyType` | QString | Monster classification (goblin, orc, boss, etc.) |
| `attack` | int | Physical attack power |
| `defense` | int | Physical defense value |
| `magicAttack` | int | Magic attack power (defined but unused) |
| `expReward` | int | Experience given when defeated |
| `goldReward` | int | Gold given when defeated |

### Public Methods
| Method | Purpose |
|--------|---------|
| `Monster(...)` | Constructor - initialize with name, level, and type |
| `isAlive()` (inherited) | Check if health > 0 |

### Important Note: Missing Serialization
**The Monster class DOES NOT implement QDataStream operators** (`operator<<` and `operator>>`). This is significant:
- Monster instances are NOT persisted to disk
- They are created on-demand during combat via `MonsterFactory`
- This simplifies save/load as the current monster is discarded when exiting combat

## 4. Combat System Integration

### How Monster is Used in Game Class

#### Combat Initialization
```cpp
void Game::startCombat()
{
    if (currentMonster) {
        delete currentMonster;
    }
    currentMonster = MonsterFactory::createRandomMonster(player->level);
    combatActive = true;
    combatLog = QString("Combat started! A %1 (Level %2) appears!")
                .arg(currentMonster->name).arg(currentMonster->level);
}
```

#### Player Attack
```cpp
QString Game::playerAttack()
{
    if (!combatActive || !currentMonster || !player) return "";
    
    bool critical = rollCritical(player->dexterity);
    int baseDamage = player->getTotalAttack();
    int damage = calculateDamage(baseDamage, player->level, 
                                 currentMonster->defense, critical);
    
    currentMonster->health -= damage;
    // ... combat log updates
}
```

#### Monster Attack
```cpp
QString Game::monsterAttack()
{
    if (!combatActive || !currentMonster || !player) return "";
    
    int baseDamage = currentMonster->attack;
    int damage = calculateDamage(baseDamage, currentMonster->level, 
                                 player->getTotalDefense());
    
    player->health -= damage;
    // ... combat log updates
}
```

#### Combat Rewards
```cpp
void Game::giveCombatRewards()
{
    // EXP: uses currentMonster->expReward
    int expGained = currentMonster->expReward;
    player->gainExperience(expGained);
    
    // GOLD: uses currentMonster->goldReward
    int goldGained = currentMonster->goldReward;
    player->gold += goldGained;
    
    // Quest notifications
    if (m_questManager) {
        m_questManager->onCombatEnd(currentMonster->name);
    }
    if (m_codexManager) {
        m_codexManager->onEnemyKilled(currentMonster->name);
    }
}
```

### Damage Calculation Formula
```cpp
int Game::calculateDamage(int baseDamage, int attackerLevel, 
                          int defenderDefense, bool isCritical)
{
    double levelMultiplier = 1.0 + (attackerLevel * 0.1);
    int damage = static_cast<int>(baseDamage * levelMultiplier) - defenderDefense;
    
    if (isCritical) {
        damage = static_cast<int>(damage * 1.75);
    }
    
    if (damage < 1) damage = 1;
    
    int variance = QRandomGenerator::global()->bounded(damage / 5) - (damage / 10);
    damage += variance;
    
    return damage > 0 ? damage : 1;
}
```

## 5. MonsterFactory: Creation Patterns

### Factory Methods

#### 1. createMonster(type, playerLevel)
Creates a specific monster type with tuned stats.

**Example: Orc**
```cpp
Monster* m = new Monster("Orc", level, "orc");
m->health = 60 + (level * 15);
m->maxHealth = m->health;
m->attack = 10 + (level * 3);
m->defense = 5 + (level * 2);
m->expReward = level * 30;
m->goldReward = level * 12;
return m;
```

#### 2. createRandomMonster(playerLevel)
Weighted random selection:
- 60% Common: Goblin, Wolf, Slime, Spider
- 30% Uncommon: Bandit, Skeleton, Orc
- 10% Rare: Golem

#### 3. createBoss(playerLevel)
Creates hardened boss encounter:
```cpp
Monster* boss = new Monster("Orc Chieftain", bossLevel, "boss");
boss->health = 150 + (bossLevel * 30);
boss->maxHealth = boss->health;
boss->attack = 15 + (bossLevel * 4);
boss->defense = 10 + (bossLevel * 3);
boss->magicAttack = 8 + (bossLevel * 2);
boss->expReward = bossLevel * 100;
boss->goldReward = bossLevel * 50;
```

### Available Monster Types
| Type | Health | Attack | Defense | EXP | Gold | Notes |
|------|--------|--------|---------|-----|------|-------|
| Goblin | 40+(L*10) | 6+(L*2) | 2+L | L*20 | L*8 | Weakest |
| Wolf | 35+(L*9) | 7+(L*2) | 2+L | L*18 | L*5 | Fast |
| Slime | 25+(L*10) | 4+L | 8+(L*2) | L*15 | L*4 | High defense |
| Spider | 30+(L*8) | 6+(L*2) | 1+L | L*20 | L*6 | Has magicAttack |
| Bandit | 45+(L*11) | 9+(L*2) | 4+L | L*22 | L*20 | Gold-rich |
| Skeleton | 50+(L*12) | 8+(L*2) | 3+L | L*25 | L*15 | Balanced |
| Orc | 60+(L*15) | 10+(L*3) | 5+(L*2) | L*30 | L*12 | Strong |
| Golem | 80+(L*20) | 8+(L*2) | 10+(L*3) | L*35 | L*10 | Tank |
| Orc Chieftain (Boss) | 150+(L*30) | 15+(L*4) | 10+(L*3) | L*100 | L*50 | Boss-tier |

## 6. UI Integration (CombatPage)

### Display and State Updates
```cpp
void CombatPage::updateCombatState(Player *player, Monster *monster, 
                                   const QString &log)
{
    if (monster) {
        // Update health bar
        m_enemyHealthBar->setMaximum(monster->maxHealth);
        m_enemyHealthBar->setValue(monster->health);
        
        // Update name label
        m_monsterNameLabel->setText(
            QString("%1 (Level %2)").arg(monster->name).arg(monster->level)
        );
        
        // Load sprite based on enemyType
        QString spritePath = QString(":/assets/%1.png").arg(monster->enemyType);
        QPixmap sprite(spritePath);
        if (!sprite.isNull()) {
            m_enemySpriteLabel->setPixmap(
                sprite.scaled(100, 100, Qt::KeepAspectRatio, 
                            Qt::SmoothTransformation)
            );
        }
    }
}
```

The UI expects sprite assets at `:/assets/{enemyType}.png` (e.g., `/assets/orc.png`)

## 7. Serialization Analysis

### Current State: NO SERIALIZATION FOR MONSTER
Monster does NOT implement QDataStream operators.

**Why?**
1. Monsters are ephemeral - they only exist during combat
2. When game is saved, the monster in-combat is discarded
3. When game is loaded, new monsters are created on-demand

**Implication**: Monster data is never persisted in save files.

### How Serialization Works for Player
```cpp
friend QDataStream &operator<<(QDataStream &out, const Character &c);
friend QDataStream &operator>>(QDataStream &in, Character &c);
```

Player implements full serialization including inventory, equipment, stats, etc.

## 8. Extending Monster: FinalBoss with Phase Mechanics

### Design Patterns and Constraints to Consider

#### Current Constraints:
1. **Linear stat scaling** - All stats scale by simple formulas
2. **Single health pool** - No concept of phases
3. **Static behavior** - No attack pattern changes
4. **No serialization** - Won't be saved/loaded
5. **Factory-based creation** - All monsters created via MonsterFactory

#### Strategy for FinalBoss with Phases

### Option 1: Extend Monster Class
```cpp
class FinalBoss : public Monster
{
public:
    FinalBoss(const QString &name, int level);
    
    struct Phase {
        int healthThreshold;  // % of max health to trigger phase
        int attackMultiplier;
        int defenseMultiplier;
        QString attackPattern;
        QList<QString> specialAttacks;
    };
    
    QList<Phase> phases;
    int currentPhase;
    
    void updatePhase();
    bool checkPhaseTransition();
    QString executePhaseAttack();
};
```

### Option 2: Composition Pattern (Cleaner)
```cpp
class BossAI
{
public:
    virtual QString getNextAttack() = 0;
    virtual void onPhaseTransition() = 0;
};

class FinalBossAI : public BossAI
{
    struct Phase {
        int healthThreshold;
        int attackMultiplier;
        QList<QString> attackSequence;
    };
    QList<Phase> phases;
    int currentPhase = 0;
};

// Monster enhanced
class Monster : public Character
{
    BossAI* ai = nullptr;
};
```

### Option 3: Monster Factory Pattern (Recommended - fits current architecture)
Keep Monster simple, enhance MonsterFactory:

```cpp
class MonsterFactory
{
public:
    static Monster* createFinalBoss(int playerLevel);
    static int getFinalBossPhase(Monster* boss);
    static int getFinalBossAttackMultiplier(Monster* boss);
};
```

Then in Game class:
```cpp
// Track phase externally
struct BossState {
    Monster* boss;
    int currentPhase;
    int attackSequence;
};

QString Game::monsterAttack()  // Modified for phase behavior
{
    if (isFinalBoss && currentPhase > 1) {
        // Enhanced attack for phase 2+
        damage = applyPhaseMultiplier(damage, currentPhase);
    }
}
```

## 9. Key Observations and Gotchas

### Design Patterns Used
1. **Factory Pattern**: MonsterFactory for centralized creation
2. **Inheritance**: Monster extends Character
3. **QObject/Signal Architecture**: Game uses Qt signals for combat end
4. **No Persistence**: Monsters are ephemeral

### Important Gotchas
1. **No Serialization** - Don't expect Monster to persist or load from saves
2. **Direct Memory Management** - Game class deletes monsters manually:
   ```cpp
   if (currentMonster) {
       delete currentMonster;  // Explicit cleanup
   }
   ```
3. **Stat Calculation Errors** - defense uses floating point in constructor but stores as int:
   ```cpp
   defense(3 + (level * 1.5))  // 1.5 truncates to 1
   ```
4. **magicAttack Unused** - Defined in Monster but never used in combat calculations
5. **No Enemy AI** - All monsters use same attack: `currentMonster->attack`
   - No special attacks or patterns
   - No evasion or dodge mechanics
   - Deterministic behavior based on single attack value

### Stat Scaling Issues
```cpp
// In Monster constructor:
defense(3 + (level * 1.5))  // WARNING: 1.5 truncated to 1 (int division)

// MonsterFactory corrects this:
m->defense = 5 + (level * 2);  // Properly calculated
```

The factory creates all monsters, so raw Monster() constructor is rarely used directly.

### Memory Management Pattern
```cpp
// Monsters are heap-allocated
currentMonster = MonsterFactory::createRandomMonster(playerLevel);

// Cleaned up explicitly
if (currentMonster) {
    delete currentMonster;
}

// No shared_ptr or unique_ptr - manual management
```

## 10. Integration Points with Game Systems

### Quest System
```cpp
void Game::giveCombatRewards()
{
    if (m_questManager) {
        m_questManager->onCombatEnd(currentMonster->name);  // Uses monster name
    }
}
```
Quests track enemy kills by name, e.g., "Kill Goblins (3/5)"

### Codex/Lore System (Phase 3)
```cpp
if (m_codexManager) {
    m_codexManager->onEnemyKilled(currentMonster->name);  // Unlocks lore
}
```
Killing enemies can unlock lore entries

### Difficulty Scaling
```cpp
// Player level determines monster level
currentMonster = MonsterFactory::createRandomMonster(player->level);

// Monster level affects all stats through formulas
int level = playerLevel + QRandomGenerator::global()->bounded(-1, 2);
```

## 11. Recommendations for FinalBoss Implementation

### Architecture Decision
Use **Option 3 (Enhanced Factory Pattern)** because:
1. Maintains simple Monster class design
2. Fits existing MonsterFactory pattern
3. Allows incremental complexity without inheritance tree
4. Compatible with current Combat system
5. Easier to balance and adjust

### Implementation Outline
```cpp
// In MonsterFactory.h
enum BossPhase { PHASE_1, PHASE_2, PHASE_3 };

class MonsterFactory
{
    static Monster* createFinalBoss(int playerLevel);
    static BossPhase getBossPhase(int currentHealth, int maxHealth);
    static int getPhaseAttackBonus(BossPhase phase);
    static QString getPhaseSpecialAttack(BossPhase phase);
};

// In Game.h - add boss state tracking
struct BossState {
    BossPhase currentPhase;
    int lastPhaseChangeHealth;
    int specialAttackCounter;
};

// In Game.cpp - modify monsterAttack() and skill handling
QString Game::monsterAttack()
{
    // ... existing code ...
    
    if (isFinalBoss(currentMonster)) {
        BossPhase phase = MonsterFactory::getBossPhase(
            currentMonster->health, 
            currentMonster->maxHealth
        );
        
        int attackBonus = MonsterFactory::getPhaseAttackBonus(phase);
        damage = static_cast<int>(damage * (1.0 + attackBonus * 0.1));
        
        if (phase > currentBossState.currentPhase) {
            currentBossState.currentPhase = phase;
            combatLog += QString("\n%1 enters PHASE %2!").arg(
                currentMonster->name).arg(static_cast<int>(phase) + 1);
        }
    }
    
    // ... rest of method ...
}
```

### Phase Mechanics Example
```
Phase 1 (100-66% health):
  - Base attack
  - Uses regular attack pattern

Phase 2 (65-33% health):
  - +25% attack bonus
  - Every 3rd turn: Special AOE attack
  - Dialogue: "You dare challenge me?"

Phase 3 (33-0% health):
  - +50% attack bonus
  - Every 2nd turn: Special attack
  - Defense reduced by 20%
  - Dialogue: "Impossible! I am eternal!"
```

---

## Summary Table

| Aspect | Detail |
|--------|--------|
| **Inheritance** | Extends Character |
| **Fields** | 9 public fields (name, level, health via inheritance + 5 unique) |
| **Methods** | Constructor only; inherits isAlive() |
| **Serialization** | NONE - monsters are ephemeral |
| **Creation** | Via MonsterFactory only |
| **Memory Model** | Heap-allocated, manually deleted by Game |
| **Combat Role** | Takes damage, deals damage, provides rewards |
| **AI Complexity** | None - uses static attack value |
| **UI Integration** | Displayed in CombatPage with sprite based on enemyType |
| **Scaling** | Level-based stat scaling via formulas |
| **Boss Implementation** | Recommend factory enhancement, not inheritance |
