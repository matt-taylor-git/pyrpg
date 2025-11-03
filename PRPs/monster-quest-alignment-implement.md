# Monster-Quest Alignment Implementation Guide

**Feature**: Fix Monster-Quest System Alignment Issues in PyrpgQt
**Created**: 2025-11-03
**Version**: 1.0

---

## Goal

**Feature Goal**: Fix critical misalignment between quest objectives and actual monster types in MonsterFactory, enabling all 6 main story quests to be completable without errors.

**Deliverable**:
1. New `MonsterTypeRegistry.h/cpp` class with canonical monster type definitions
2. Updated `MonsterFactory.cpp` supporting all quest-referenced monster types (Shadow Wolf, Shadow Lord, Dark Overlord)
3. Validation system in MonsterFactory to ensure quest-monster consistency
4. Updated QuestManager with case-insensitive matching for enemy names
5. Unit tests validating all quest completion paths
6. Updated CMakeLists.txt including new files

**Success Definition**:
- [ ] Quest 1 "A Dark Omen" completable (kill 3 Shadow Wolves)
- [ ] Quest 3 "Shadows Deepen" completable (defeat Shadow Lord)
- [ ] Quest 6 "The Final Darkness" completable (defeat Dark Overlord)
- [ ] All existing tests pass: `ctest -V`
- [ ] Backward compatibility maintained for existing save games
- [ ] No compilation errors or warnings

---

## Why

- **Critical Gameplay Issue**: Players cannot complete 50% of main story quests due to monster name mismatches
- **Narrative Breaking**: Quest text promises specific enemies (Shadow Wolf, Shadow Lord, Dark Overlord) but different monsters spawn
- **Progression Blocker**: Players hit an impassable wall at Quest 1, 3, and 6, preventing completion of main storyline
- **Technical Debt**: MonsterFactory and QuestFactory developed independently without shared registry

---

## What

### Current Problems

1. **Quest 1 (main_quest_01)**:
   - Quest references: `targetId = "Shadow Wolf"` (QuestFactory.cpp:18)
   - MonsterFactory creates: "Wild Wolf" when given "Wolf" (MonsterFactory.cpp:60-68)
   - **Mismatch**: Quest expects "Shadow Wolf" but combat produces "Wild Wolf"

2. **Quest 3 (main_quest_03)**:
   - Quest references: `targetId = "Shadow Lord"` (QuestFactory.cpp:83)
   - MonsterFactory creates: "Orc Chieftain" (MonsterFactory.cpp:122-133)
   - **Mismatch**: Quest expects "Shadow Lord" but boss spawns "Orc Chieftain"

3. **Quest 6 (main_quest_06)**:
   - Quest references: `targetId = "Dark Overlord"` (QuestFactory.cpp:178)
   - MonsterFactory creates: "The Eternal Shadow" (FinalBoss.cpp:4)
   - **Mismatch**: Quest expects "Dark Overlord" but final boss is "The Eternal Shadow"

### Solution Overview

Implement a **MonsterTypeRegistry** pattern (Factory + Registry design pattern) that:
1. Provides canonical source of truth for all monster types
2. Enables MonsterFactory to create quest-specific monsters by name
3. Maintains backward compatibility with existing monster creation patterns
4. Adds validation to catch future mismatches early

---

## All Needed Context

### Context Completeness Check

✅ **Validated**: This PRP contains everything needed for one-pass implementation success, including:
- Exact file paths and line numbers for all relevant code
- Specific implementation patterns from existing codebase
- Integration points with QuestManager and Game systems
- Complete test coverage strategy
- Build system updates for new files

### Current Codebase Structure

```bash
/home/matt/code/pyrpg/cpp-qt-rpg/
├── src/
│   ├── game/
│   │   ├── Game.cpp                    # Combat flow orchestration (line 439: giveCombatRewards)
│   │   ├── QuestManager.cpp            # Quest progress tracking (line 150: onCombatEnd, line 168: string match)
│   │   └── factories/
│   │       ├── MonsterFactory.h        # Factory header (line 11-14: methods)
│   │       ├── MonsterFactory.cpp      # Current implementation (lines 5-139)
│   │       ├── QuestFactory.h          # Quest definitions header
│   │       └── QuestFactory.cpp        # Quest definitions (lines 5-191: 6 main quests)
│   ├── models/
│   │   ├── Monster.h                   # Monster class (line 1-20)
│   │   ├── FinalBoss.h                 # FinalBoss class
│   │   ├── FinalBoss.cpp               # Returns "The Eternal Shadow" (line 4)
│   │   ├── Quest.h                     # Quest model (line 1-66)
│   │   └── Quest.cpp                   # Quest serialization
│   └── MainWindow.cpp                  # UI orchestration
├── tests/
│   ├── test_quest_system.cpp           # Quest testing (lines 156-163: expects "Shadow Wolf")
│   └── test_quest_models.cpp           # Quest model testing
├── CMakeLists.txt                      # Build configuration (lines 42, 135-143)
└── assets/
```

### Desired Codebase Structure

```bash
/home/matt/code/pyrpg/cpp-qt-rpg/
├── src/
│   ├── game/
│   │   ├── Game.cpp                    # UNCHANGED - Integration already correct (line 501)
│   │   ├── QuestManager.cpp            # MODIFIED - Case-insensitive matching (line 168)
│   │   ├── QuestManager.h              # UNCHANGED
│   │   └── factories/
│   │       ├── MonsterFactory.h        # MODIFIED - Add validation methods
│   │       ├── MonsterFactory.cpp      # MODIFIED - Support quest monsters + validation
│   │       ├── QuestFactory.cpp        # UNCHANGED - Already correct
│   │       ├── QuestFactory.h          # UNCHANGED
│   │       ├── MonsterTypeRegistry.h   # NEW - Canonical monster types
│   │       └── MonsterTypeRegistry.cpp # NEW - Monster type definitions
│   ├── models/
│   │   ├── Monster.h                   # UNCHANGED
│   │   ├── FinalBoss.h                 # MODIFIED - Accept boss name parameter
│   │   ├── FinalBoss.cpp               # MODIFIED - Accept boss name parameter
│   │   ├── Quest.h                     # UNCHANGED
│   │   └── Quest.cpp                   # UNCHANGED
│   └── MainWindow.cpp                  # UNCHANGED
├── tests/
│   ├── test_monster_factory.cpp        # NEW - Factory validation tests
│   ├── test_quest_system.cpp           # MODIFIED - Add quest completion tests
│   └── test_quest_models.cpp           # UNCHANGED
└── CMakeLists.txt                      # MODIFIED - Add new files to build
```

### Critical Files & Patterns

#### File: src/game/factories/MonsterFactory.cpp
**Why**: Core factory pattern implementation
**Pattern**: String-based monster creation with if/else chain (lines 10-94)
**Current Implementation**:
```cpp
if (monsterType == "Goblin" || monsterType == "goblin") {
    // Create Goblin...
}
else if (monsterType == "Orc" || monsterType == "orc") {
    // Create Orc...
}
// ... 8 more monster types
// Default fallback: Unknown Beast (line 93)
```
**Gotcha**: All monsters created with string comparison, case-insensitive matching

#### File: src/game/factories/QuestFactory.cpp
**Why**: Source of truth for quest definitions
**Pattern**: Static factory methods creating Quest objects (lines 3-195)
**Key Lines**:
- Line 18: `targetId = "Shadow Wolf"` (Quest 1)
- Line 83: `targetId = "Shadow Lord"` (Quest 3)
- Line 178: `targetId = "Dark Overlord"` (Quest 6)

#### File: src/game/Game.cpp
**Why**: Integration point - calls QuestManager on combat end
**Pattern**: Combat flow with reward distribution (line 439-508)
**Critical Integration**:
```cpp
// Line 499-507: Quest notification after combat
if (m_questManager) {
    m_questManager->onCombatEnd(currentMonster->name);  // Line 501
}
```
**Gotcha**: Uses `currentMonster->name` string to notify quests

#### File: src/game/QuestManager.cpp
**Why**: Quest progress tracking
**Pattern**: Event-driven quest updates (line 150-176)
**Critical Method** (line 150):
```cpp
void QuestManager::onCombatEnd(const QString &enemyName)
{
    // Line 167-173: Exact string matching - THIS IS THE BUG
    if ((obj.type == "kill_enemies" || obj.type == "defeat_boss") &&
        obj.targetId == enemyName &&  // EXACT MATCH - case sensitive!
        !obj.completed) {
        updateQuestProgress(playerQuest->questId, i, 1);
    }
}
```
**Gotcha**: Uses `operator==` for string comparison (case-sensitive)

#### File: src/models/FinalBoss.cpp
**Why**: Final boss implementation
**Pattern**: Hardcoded boss name in constructor (line 3-16)
```cpp
FinalBoss::FinalBoss(int playerLevel)
    : Monster("The Eternal Shadow", playerLevel + 2, "final_boss"),
      // ...
```
**Gotcha**: Name is hardcoded, cannot be changed per quest

#### File: tests/test_quest_system.cpp
**Why**: Validates quest system behavior
**Pattern**: Qt Test framework (lines 140-164)
**Test Expectation** (line 156):
```cpp
// This test expects "Shadow Wolf" to work
manager.onCombatEnd("Shadow Wolf");
QCOMPARE(playerQuest->objectives[0].current, initialCurrent + 1);
```
**Gotcha**: Test already written for correct behavior - implementation must match test

#### File: cpp-qt-rpg/CMakeLists.txt
**Why**: Build system configuration
**Pattern**: Qt automoc, add_executable, target_link_libraries (lines 42, 135-143)
**Required Updates**:
- Add MonsterTypeRegistry files to main executable
- Add test files to test executables

### Known Gotchas

```cpp
// CRITICAL: Qt Meta-Object Compiler (moc) requirements
// All QObject-derived classes (.h files with Q_OBJECT) must be compiled via CMAKE_AUTOMOC
// MonsterTypeRegistry.h should NOT inherit QObject (simple static class)

// CRITICAL: String comparison is CASE SENSITIVE in C++ QString
// QuestManager.cpp line 168: obj.targetId == enemyName (exact match)
// Must update to case-insensitive: QString::compare(obj.targetId, enemyName, Qt::CaseInsensitive) == 0

// CRITICAL: MonsterFactory returns nullptr for unknown types (line 93)
// createBoss() and createFinalBoss() don't check for nullptr
// Must add validation or return default monster

// CRITICAL: Save game compatibility
// Existing saves may have "Wild Wolf", "Orc Chieftain", "The Eternal Shadow"
// New implementation must support BOTH old names (aliases) and new names
```

---

## Implementation Blueprint

### Data Models and Structure

Create MonsterTypeRegistry as central monster type definition system:

```cpp
// File: src/game/factories/MonsterTypeRegistry.h
#ifndef MONSTERTYPEREGISTRY_H
#define MONSTERTYPEREGISTRY_H

#include <QString>
#include <QStringList>
#include <QMap>

struct MonsterTypeInfo {
    QString displayName;      // "Shadow Wolf" - name shown in combat
    QString factoryKey;       // "shadow_wolf" - input to MonsterFactory
    QString enemyType;        // "wolf", "boss", "final_boss" - category
    bool isBoss;             // true for boss monsters
    bool isFinalBoss;        // true for final boss only
};

class MonsterTypeRegistry
{
public:
    // Access all registered monster types
    static QList<MonsterTypeInfo> getAllMonsterTypes();

    // Get specific monster type info
    static MonsterTypeInfo getMonsterTypeInfo(const QString &typeName);

    // Check if monster type exists (case-insensitive)
    static bool isValidMonsterType(const QString &typeName);

    // Get all valid type names for factory input
    static QStringList getAllValidTypeNames();

    // Backward compatibility: Get aliases for old monster names
    static QStringList getAliases(const QString &typeName);

    // Find type by display name (for quest matching)
    static QString getTypeNameFromDisplayName(const QString &displayName);

private:
    static void initializeRegistry();

    // Registry data - populated once on first access
    static QMap<QString, MonsterTypeInfo> s_registry;
    static QMap<QString, QString> s_displayNameToType;  // "Shadow Wolf" -> "shadow_wolf"
    static QMap<QString, QString> s_aliases;            // "Wild Wolf" -> "shadow_wolf"
};

// File: src/game/factories/MonsterTypeRegistry.cpp
#include "MonsterTypeRegistry.h"

QMap<QString, MonsterTypeInfo> MonsterTypeRegistry::s_registry;
QMap<QString, QString> MonsterTypeRegistry::s_displayNameToType;
QMap<QString, QString> MonsterTypeRegistry::s_aliases;

void MonsterTypeRegistry::initializeRegistry()
{
    if (!s_registry.isEmpty()) return;  // Already initialized

    // Quest-relevant monsters (NEW)
    s_registry["shadow_wolf"] = {"Shadow Wolf", "shadow_wolf", "wolf", false, false};
    s_registry["shadow_lord"] = {"Shadow Lord", "shadow_lord", "boss", true, false};
    s_registry["dark_overlord"] = {"Dark Overlord", "dark_overlord", "final_boss", true, true};

    // Existing monsters (from MonsterFactory.cpp)
    s_registry["goblin"] = {"Goblin", "goblin", "goblin", false, false};
    s_registry["orc"] = {"Orc", "orc", "orc", false, false};
    s_registry["golem"] = {"Stone Golem", "golem", "golem", false, false};
    s_registry["skeleton"] = {"Skeleton Warrior", "skeleton", "skeleton", false, false};
    s_registry["bandit"] = {"Bandit", "bandit", "bandit", false, false};
    s_registry["wolf"] = {"Wild Wolf", "wolf", "wolf", false, false};
    s_registry["spider"] = {"Giant Spider", "spider", "spider", false, false};
    s_registry["slime"] = {"Slime", "slime", "slime", false, false};
    s_registry["orc_chieftain"] = {"Orc Chieftain", "orc_chieftain", "boss", true, false};
    s_registry["eternal_shadow"] = {"The Eternal Shadow", "eternal_shadow", "final_boss", true, true};

    // Build display name lookup
    for (auto it = s_registry.begin(); it != s_registry.end(); ++it) {
        s_displayNameToType[it.value().displayName] = it.key();
    }

    // Backward compatibility aliases
    s_aliases["Wild Wolf"] = "shadow_wolf";
    s_aliases["Shadow Wolf"] = "shadow_wolf";
    s_aliases["Orc Chieftain"] = "shadow_lord";  // Map old to new for backward compatibility
    s_aliases["Shadow Lord"] = "shadow_lord";
    s_aliases["The Eternal Shadow"] = "dark_overlord";
    s_aliases["Dark Overlord"] = "dark_overlord";
}

bool MonsterTypeRegistry::isValidMonsterType(const QString &typeName)
{
    initializeRegistry();

    QString normalized = typeName.toLower();

    // Check direct type match
    if (s_registry.contains(normalized)) {
        return true;
    }

    // Check alias match
    if (s_aliases.contains(typeName)) {
        return true;
    }

    return false;
}

QString MonsterTypeRegistry::getTypeNameFromDisplayName(const QString &displayName)
{
    initializeRegistry();
    return s_displayNameToType.value(displayName, QString());
}
```

### Implementation Tasks (Ordered by Dependencies)

```yaml
Task 1: CREATE src/game/factories/MonsterTypeRegistry.h
  - IMPLEMENT: MonsterTypeRegistry class with static methods
  - FOLLOW pattern: Simple static utility class (no QObject inheritance)
  - NAMING: MonsterTypeRegistry, MonsterTypeInfo structs
  - PLACEMENT: src/game/factories/ alongside MonsterFactory
  - CRITICAL: Do NOT use Q_OBJECT - this is a pure C++ utility class

Task 2: CREATE src/game/factories/MonsterTypeRegistry.cpp
  - IMPLEMENT: Static registry initialization with all 13 monster types
  - INCLUDE: Quest monsters (shadow_wolf, shadow_lord, dark_overlord) + existing 10 monsters
  - ADD: Backward compatibility aliases (Wild Wolf, Orc Chieftain, The Eternal Shadow)
  - DEPENDENCIES: Include Qt core types (QString, QMap, QStringList)
  - PLACEMENT: src/game/factories/

Task 3: MODIFY src/game/factories/MonsterFactory.h
  - ADD: static bool isValidMonsterType(const QString &monsterType)
  - ADD: static QStringList getAllValidMonsterTypes()
  - MODIFY: Monster* createMonster(const QString &monsterType, int playerLevel)
  - MODIFY: Monster* createBoss(int playerLevel, const QString &bossType = "")
  - MODIFY: FinalBoss* createFinalBoss(int playerLevel, const QString &bossType = "")
  - FOLLOW pattern: Static factory methods pattern (line 11-14)
  - PLACEMENT: Update existing header (DO NOT replace, ADD only)

Task 4: MODIFY src/game/factories/MonsterFactory.cpp
  - UPDATE: createMonster() to support "Shadow Wolf" case (ADD new if block)
  - UPDATE: createBoss() to accept bossType parameter and create Shadow Lord
  - UPDATE: createFinalBoss() to accept bossType parameter and create Dark Overlord
  - ADD: isValidMonsterType() validation using MonsterTypeRegistry
  - ADD: getAllValidMonsterTypes() helper
  - PRESERVE: All existing monster types (goblin, orc, golem, skeleton, bandit, wolf, spider, slime)
  - CRITICAL: Add "Shadow Wolf" BEFORE line 93 (before fallback)
  - PATTERN: Follow existing if/else structure (line 10-94)

Task 5: MODIFY src/models/FinalBoss.h
  - MODIFY: FinalBoss(int playerLevel, const QString &bossName = "The Eternal Shadow")
  - ADD: QString m_bossName member variable
  - FOLLOW pattern: Constructor parameter with default value
  - PLACEMENT: src/models/FinalBoss.h

Task 6: MODIFY src/models/FinalBoss.cpp
  - UPDATE: Constructor to accept bossName parameter
  - CHANGE: Line 4 from Monster("The Eternal Shadow", ...) to Monster(bossName, ...)
  - UPDATE: Initialization list to include m_bossName(bossName)
  - PRESERVE: All existing stat calculations (lines 9-15)
  - PATTERN: Default parameter value in header, use in constructor

Task 7: MODIFY src/game/QuestManager.cpp
  - UPDATE: Line 168 string comparison to case-insensitive
  - CHANGE: obj.targetId == enemyName
  - TO: QString::compare(obj.targetId, enemyName, Qt::CaseInsensitive) == 0
  - ADD: Include <QString> if needed
  - CRITICAL: This is the key fix - allows "Shadow Wolf" to match "shadow wolf" etc.
  - PATTERN: Qt case-insensitive comparison

Task 8: CREATE tests/test_monster_factory.cpp
  - IMPLEMENT: TestMonsterFactory class with Q_OBJECT
  - ADD: testCreateShadowWolf()
  - ADD: testCreateShadowLord()
  - ADD: testCreateDarkOverlord()
  - ADD: testMonsterTypeValidation()
  - ADD: testBackwardCompatibility()
  - FOLLOW pattern: Qt Test framework (see test_quest_system.cpp)
  - MOCK: No mocking needed - direct factory calls
  - PLACEMENT: tests/ directory

Task 9: MODIFY tests/test_quest_system.cpp
  - VERIFY: Line 156-163 still pass with real MonsterFactory
  - ADD: testQuest1ShadowWolfCompletion() - integrate MonsterFactory
  - ADD: testQuest3ShadowLordCompletion() - test boss creation
  - ADD: testQuest6DarkOverlordCompletion() - test final boss creation
  - CRITICAL: These tests verify end-to-end quest completion
  - PATTERN: Existing test structure (line 140-164)

Task 10: MODIFY cpp-qt-rpg/CMakeLists.txt
  - ADD: MonsterTypeRegistry.h to main executable sources (line 42 area)
  - ADD: MonsterTypeRegistry.cpp to main executable sources
  - ADD: test_monster_factory.cpp to test_models executable
  - FOLLOW pattern: Existing file additions (line 42, 147)
  - ORDER: Keep files alphabetically sorted where possible
```

### Implementation Patterns & Key Details

```cpp
// PATTERN: Case-insensitive string matching (QuestManager.cpp:168)
if (QString::compare(obj.targetId, enemyName, Qt::CaseInsensitive) == 0 &&
    !obj.completed) {
    // Quest progress updated
}

// PATTERN: Monster creation with quest-specific names (MonsterFactory.cpp:60-75)
if (monsterType == "Shadow Wolf" || monsterType == "shadow_wolf") {
    Monster* m = new Monster("Shadow Wolf", level, "wolf");
    m->health = 35 + (level * 9);
    m->maxHealth = m->health;
    m->attack = 7 + (level * 2);
    m->defense = 2 + level;
    m->expReward = level * 18;
    m->goldReward = level * 5;
    return m;
}

// PATTERN: Boss creation with type parameter (MonsterFactory.cpp:121-133)
Monster* MonsterFactory::createBoss(int playerLevel, const QString &bossType)
{
    int bossLevel = playerLevel + 2;

    // NEW: Support quest-specific boss
    if (bossType == "Shadow Lord") {
        Monster* boss = new Monster("Shadow Lord", bossLevel, "boss");
        boss->health = 150 + (bossLevel * 30);
        boss->maxHealth = boss->health;
        boss->attack = 15 + (bossLevel * 4);
        boss->defense = 10 + (bossLevel * 3);
        boss->magicAttack = 8 + (bossLevel * 2);
        boss->expReward = bossLevel * 100;
        boss->goldReward = bossLevel * 50;
        return boss;
    }

    // Default to existing behavior
    Monster* boss = new Monster("Orc Chieftain", bossLevel, "boss");
    boss->health = 150 + (bossLevel * 30);
    boss->maxHealth = boss->health;
    boss->attack = 15 + (bossLevel * 4);
    boss->defense = 10 + (bossLevel * 3);
    boss->magicAttack = 8 + (bossLevel * 2);
    boss->expReward = bossLevel * 100;
    boss->goldReward = bossLevel * 50;
    return boss;
}

// PATTERN: Static registry initialization (MonsterTypeRegistry.cpp)
void MonsterTypeRegistry::initializeRegistry()
{
    if (!s_registry.isEmpty()) return;  // Lazy initialization

    // Register all monster types
    s_registry["shadow_wolf"] = {"Shadow Wolf", "shadow_wolf", "wolf", false, false};
    // ... register all types

    // Build reverse lookup map
    for (auto it = s_registry.begin(); it != s_registry.end(); ++it) {
        s_displayNameToType[it.value().displayName] = it.key();
    }

    // Add aliases for backward compatibility
    s_aliases["Wild Wolf"] = "shadow_wolf";
    s_aliases["Orc Chieftain"] = "shadow_lord";
    s_aliases["The Eternal Shadow"] = "dark_overlord";
}

// PATTERN: FinalBoss with customizable name (FinalBoss.cpp:3-16)
FinalBoss::FinalBoss(int playerLevel, const QString &bossName)
    : Monster(bossName, playerLevel + 2, "final_boss"),
      currentPhase(1),
      m_previousPhase(1),
      m_bossName(bossName)
{
    // All existing stat calculations unchanged
    health = 500 + (playerLevel * 50);
    maxHealth = health;
    attack = 30 + (playerLevel * 5);
    defense = 20 + (playerLevel * 4);
    magicAttack = 25 + (playerLevel * 4);
    expReward = playerLevel * 500;
    goldReward = playerLevel * 200;
}
```

### Integration Points

```yaml
CMAKE:
  - file: cpp-qt-rpg/CMakeLists.txt
  - location: Line 42 (main executable)
  - add: src/game/factories/MonsterTypeRegistry.cpp
  - pattern: Follow existing source file additions

  - location: Line 147 (test_models executable)
  - add: tests/test_monster_factory.cpp
  - pattern: Add test file to test_models target

GAME:
  - file: src/game/Game.cpp
  - location: Line 532 (startFinalBossCombat)
  - update: currentMonster = MonsterFactory::createFinalBoss(player->level, "Dark Overlord")
  - pattern: Pass boss type to factory

FACTORY:
  - file: src/game/factories/MonsterFactory.cpp
  - location: Line 5-139 (all creation methods)
  - integrate: Use MonsterTypeRegistry::isValidMonsterType() for validation
  - pattern: Check validity before creation

QUEST:
  - file: src/game/QuestManager.cpp
  - location: Line 168 (onCombatEnd string comparison)
  - update: Case-insensitive matching
  - pattern: Qt::CaseInsensitive flag

TESTS:
  - file: tests/test_quest_system.cpp
  - location: Line 156 (combat event test)
  - verify: "Shadow Wolf" matching works
  - pattern: Direct MonsterFactory integration
```

---

## Validation Loop

### Level 1: Syntax & Build Validation

```bash
# Navigate to build directory
cd /home/matt/code/pyrpg/cpp-qt-rpg/build

# Clean build to catch all dependencies
rm -rf *

# Configure with CMake
cmake ..

# Build the project
make -j$(nproc)

# Expected: Zero compilation errors
# If errors: Read output, fix include paths, verify CMakeLists.txt additions
```

### Level 2: Unit Tests

```bash
# Run MonsterFactory unit tests
./test_models

# Run Quest system integration tests
./test_quest_system

# Run all tests
ctest -V

# Expected: All tests pass
# test_quest_system::TestQuestSystem::testCombatEventHandling should now pass
```

### Level 3: Integration Testing (Quest Completion)

```bash
# Start the game
./pyrpg-qt &

# Test Quest 1 progression (via test_quest_system.cpp logic):
# 1. Create player at level 1
# 2. Accept main_quest_01
# 3. Simulate combat and defeat "Shadow Wolf" (3 times)
# 4. Verify quest completes

# Quest 3 progression:
# 1. Create player at level 5+
# 2. Complete prerequisites
# 3. Accept main_quest_03
# 4. Spawn and defeat "Shadow Lord"
# 5. Verify quest completes

# Quest 6 progression:
# 1. Create player at level 15+
# 2. Complete all prerequisites
# 3. Accept main_quest_06
# 4. Spawn and defeat "Dark Overlord"
# 5. Verify quest completes

# Expected: All quests complete successfully without errors
```

### Level 4: Backward Compatibility Testing

```bash
# Verify existing monsters still work
# Create test that spawns: Goblin, Orc, Wild Wolf, Orc Chieftain, The Eternal Shadow
# Expected: All spawn correctly

# Test save/load compatibility (if save system works in tests)
# Expected: Old saves with "Wild Wolf" progress still valid
```

---

## Final Validation Checklist

### Technical Validation

- [ ] Build completes without errors: `make -j$(nproc)`
- [ ] All unit tests pass: `ctest -V`
- [ ] No memory leaks: Run with valgrind if available
- [ ] CMakeLists.txt updated correctly (verify with `cmake --build . --target help`)

### Feature Validation

- [ ] Quest 1 "A Dark Omen" completable (defeat 3 Shadow Wolves)
- [ ] Quest 3 "Shadows Deepen" completable (defeat Shadow Lord)
- [ ] Quest 6 "The Final Darkness" completable (defeat Dark Overlord)
- [ ] Existing quests (2, 4, 5) still work correctly
- [ ] MonsterFactory can create all 13 monster types
- [ ] Backward compatibility: Old monster names still work (Wild Wolf, Orc Chieftain, The Eternal Shadow)

### Quest Completion Verification

- [ ] test_quest_system::testCombatEventHandling passes
- [ ] MonsterFactory creates correct monster names matching quest objectives
- [ ] Case-insensitive matching works (no case sensitivity issues)
- [ ] No "Unknown Beast" spawns for quest-relevant encounters

### Code Quality

- [ ] Follows existing naming conventions (camelCase for variables, PascalCase for classes)
- [ ] File placement matches desired structure
- [ ] No code duplication (use MonsterTypeRegistry for shared logic)
- [ ] Proper memory management (no leaks, proper delete calls)
- [ ] Code formatting matches project style (run clang-format if available)

### Integration Validation

- [ ] Game.cpp line 501: QuestManager receives correct monster names
- [ ] QuestManager.cpp line 168: Case-insensitive comparison works
- [ ] MonsterFactory validation prevents invalid monster types
- [ ] FinalBoss accepts boss name parameter correctly

---

## Anti-Patterns to Avoid

- ❌ **DON'T** break existing monster types (Goblin, Orc, etc.) - they must continue working
- ❌ **DON'T** remove backward compatibility aliases - existing saves must load correctly
- ❌ **DON'T** make MonsterTypeRegistry inherit QObject - it's a pure C++ utility class
- ❌ **DON'T** change quest IDs or objective targetIds - update MonsterFactory to match quests
- ❌ **DON'T** use dynamic_cast unnecessarily - just check enemyType string
- ❌ **DON'T** add Q_OBJECT to MonsterTypeRegistry - it doesn't need signals/slots
- ❌ **DON'T** forget to add new files to CMakeLists.txt - will cause build errors
- ❌ **DON'T** use hardcoded strings - use MonsterTypeRegistry constants
- ❌ **DON'T** skip validation testing - ensure isValidMonsterType() works correctly
- ❌ **DON'T** change the combat flow in Game.cpp - it's already correct, just needs proper monster names

---

## Implementation Timeline

**Phase 1** (Foundation - Low Risk):
- Task 1-2: Create MonsterTypeRegistry
- Task 3-4: Update MonsterFactory
- Build & unit test validation

**Phase 2** (Core Alignment - High Impact):
- Task 5-7: Update FinalBoss and QuestManager
- End-to-end quest completion testing

**Phase 3** (Quality & Testing):
- Task 8-10: Tests and build system updates
- Full integration testing and validation

**Estimated Total Time**: 4-6 hours
**Risk Level**: Low (mostly additions, minimal breaking changes)

---

## References

- **PRD Document**: PRPs/monster-quest-alignment-prd.md (complete problem analysis)
- **Codebase Analysis**: Extensive codebase review with exact file paths and line numbers
- **Test Suite**: tests/test_quest_system.cpp (existing test structure and expectations)
- **Build System**: cpp-qt-rpg/CMakeLists.txt (exact patterns for file additions)

---

## Confidence Score: 10/10

**Rationale**: This PRP provides complete context for one-pass implementation success:
- ✅ Exact file paths and line numbers for all relevant code
- ✅ Specific implementation patterns from existing codebase
- ✅ Complete integration points with QuestManager and Game systems
- ✅ Comprehensive test coverage strategy
- ✅ Build system updates with exact file additions
- ✅ Backward compatibility plan
- ✅ No guesswork required - everything specified with precision

**Expected Outcome**: An AI agent unfamiliar with the codebase can successfully implement this feature using only this PRP and code access.
