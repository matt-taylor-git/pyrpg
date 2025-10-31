name: "Storyline & Quest System - Phase 1-2: Foundation and Quest Tracking"
description: |
  Implementation PRP for quest system foundation, data models, quest tracking,
  and UI integration for PyRPG Qt. Covers Phase 1 (Foundation) and Phase 2
  (Quest System) from storyline-quest-system-prd.md.

---

## Goal

**Feature Goal**: Implement a complete quest tracking system with data persistence, automatic progress updates based on game events, and a UI for viewing active/completed quests.

**Deliverable**:
- Quest, QuestObjective, and QuestRewards data models with full QDataStream serialization
- QuestManager class for state management and event-driven updates
- QuestLogPage UI for viewing and tracking quests
- Integration with combat, leveling, and item systems for auto-updates
- 5-10 hardcoded story quests with progression
- Full save/load support for quest state

**Success Definition**:
- Player can view active quests in Quest Log (Q key)
- Quest progress auto-updates on combat win, level up, item collection
- Quest completion triggers notification dialog
- Quest state persists through save/load cycles
- All unit tests pass for Quest models and QuestManager
- Integration tests verify quest flow from acceptance to completion

## User Persona

**Target User**: RPG player seeking narrative structure and clear progression goals

**Use Case**:
- Player defeats enemies and wants to know if it counts toward quest objectives
- Player opens Quest Log to see what to do next
- Player completes quest and receives rewards automatically
- Player saves game and returns later with quest progress intact

**User Journey**:
1. Player creates new character → Intro quest auto-activates
2. Player opens Quest Log (Q key) → Sees "Kill 3 Shadow Wolves" objective
3. Player explores and defeats wolf → Quest progress updates "1/3"
4. Player defeats 2 more wolves → Quest completes, dialog shows rewards
5. Player accepts next quest → Cycle repeats
6. Player saves game → Quest state preserved
7. Player loads game → Quest state restored exactly

**Pain Points Addressed**:
- No clear objectives or guidance (solved by quest descriptions)
- Uncertain if actions count toward goals (solved by auto-tracking)
- Tedious manual quest tracking (solved by automatic updates)
- Lost progress on reload (solved by serialization)

## Why

- **Narrative Structure**: Transforms endless combat into story-driven progression with meaning
- **Player Retention**: Clear goals and milestones keep players engaged longer
- **Integration Foundation**: Quest system enables dialogue, lore, and final boss unlock in future phases
- **Proven Pattern**: Quest systems are standard in RPGs for good reason - they work

This solves the core problem stated in the PRD: "Players engage in endless combat without story context, clear progression goals, or sense of accomplishment."

## What

### Core Functionality

**Quest Data Model**:
- Quest with multiple objectives (kill X enemies, reach level Y, collect item Z)
- Objective types: KillEnemies, ReachLevel, CollectItem, TalkToNPC (future), DefeatBoss
- Quest status: Locked, Available, Active, Completed, Rewarded
- Rewards: experience, gold, items (optional)
- Prerequisites: level requirement, previous quests

**Quest Manager**:
- Load quest definitions from hardcoded factory
- Track active, available, and completed quests
- Auto-update progress on game events (combat end, level up, item pickup)
- Emit signals for quest state changes (available, progressed, completed)
- Check prerequisites to unlock new quests

**Quest Log UI**:
- View all quests (active, available, completed)
- Click quest to see full description and objectives
- Visual progress indicators (3/10 enemies killed)
- Keyboard shortcuts (Q to open, Esc to close, number keys to select)
- Back button returns to combat/adventure view

**Integration Points**:
- Combat system: Update kill quests on combat victory
- Leveling system: Check level quests on player level up
- Item system: Track item collection quests when items added to inventory
- Save system: Serialize quest state with Player data
- MainWindow: Add quest log navigation and keyboard shortcuts

### Success Criteria

- [ ] Quest model serializes/deserializes correctly with all fields
- [ ] QuestManager loads at least 5 predefined quests
- [ ] Kill quest auto-updates when specific enemy defeated
- [ ] Level quest auto-completes when player reaches required level
- [ ] Quest completion shows notification dialog with rewards
- [ ] Rewards correctly added to player (gold, exp, items)
- [ ] QuestLogPage displays all quest categories correctly
- [ ] Clicking quest shows full details in detail pane
- [ ] Quest state saves and loads without corruption
- [ ] Old saves load gracefully (empty quest list if pre-quest version)
- [ ] Keyboard shortcuts work (Q opens log, Esc closes, 1-9 select quests)
- [ ] Unit tests: 100% pass rate for Quest models
- [ ] Integration tests: Quest flow from unlock to completion verified

## All Needed Context

### Context Completeness Check

✓ **Model patterns**: Comprehensive analysis of Character, Player, Item, Skill serialization patterns
✓ **UI patterns**: Complete view structure, dialog patterns, MainWindow integration from existing code
✓ **Save/load patterns**: Full SaveManager architecture with versioning strategy documented
✓ **Qt conventions**: Signal/slot patterns, QStackedWidget navigation, Theme usage
✓ **Factory patterns**: ItemFactory, SkillFactory patterns to follow for QuestFactory
✓ **Testing patterns**: Existing test structure from test_models.cpp, test_persistence.cpp

**Validation**: An AI agent unfamiliar with this codebase has everything needed - file patterns to follow, exact naming conventions, serialization strategies, UI integration steps, and validation commands.

### Documentation & References

```yaml
# PRD Architecture Reference
- file: PRPs/storyline-quest-system-prd.md
  why: Complete system architecture, quest state machine, data model specifications
  section: "Technical Specifications (lines 457-750), Quest System Architecture"
  critical: Quest status enum, objective types, quest progression flow

# Model Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/models/Player.h
  why: Base pattern for complex model with nested pointers and serialization
  pattern: QList<Skill*> skills, QMap<QString, Item*> equipment - same pattern for quests
  gotcha: Must convert pointer lists to value lists for serialization (lines 87-97 in Player.cpp)

- file: cpp-qt-rpg/src/models/Player.cpp
  why: Versioned serialization pattern for backward compatibility
  pattern: Write quint32 version first, conditional deserialization based on version (lines 62-161)
  critical: Always use qDeleteAll for pointer cleanup in destructor (lines 49-60)

- file: cpp-qt-rpg/src/models/Item.h
  why: Simple model structure pattern (no inheritance)
  pattern: Public members, friend serialization operators, helper methods
  gotcha: Use QString for type/rarity, not C++ enums (easier serialization)

- file: cpp-qt-rpg/src/models/Skill.h
  why: Minimal model with clean constructor pattern
  pattern: Default constructor + parameterized constructor with default values

# UI Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/views/InventoryPage.h
  why: Standard view structure with signals, slots, keyboard handling
  pattern: QWidget base, Q_OBJECT, signals for navigation, updateInventory(Player*) method
  gotcha: All views must have explicit constructor, setupUi(), keyPressEvent override

- file: cpp-qt-rpg/src/views/InventoryPage.cpp
  why: Complete UI implementation pattern
  pattern: setupUi() creates layouts, Theme constants for styling, signal emissions (lines 21-120)
  critical: Use Theme::CARD, Theme::BORDER, Theme::PRIMARY for all styling

- file: cpp-qt-rpg/src/components/CombatResultDialog.h
  why: Modal information dialog pattern
  pattern: QDialog base, constructor takes display data, accept() on button click
  usage: Create dialog, call exec(), no return value needed (just shows info)

# Save/Load Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/persistence/SaveManager.cpp
  why: Complete save/load flow and versioning strategy
  pattern: Magic header validation, version checking, metadata header (lines 16-81)
  critical: ALWAYS set out.setVersion(QDataStream::Qt_6_0) and in.setVersion(QDataStream::Qt_6_0)

- file: cpp-qt-rpg/src/persistence/SaveManager.h
  why: Slot-based save system architecture
  pattern: 10 save slots, SaveSlotInfo for metadata, slot validation (lines 11-36)

# Game Controller Pattern References
- file: cpp-qt-rpg/src/game/Game.h
  why: QObject-based controller with signals, player/monster ownership
  pattern: Private Player* member, public getPlayer() getter, QObject signals
  critical: Game owns Player pointer, must delete old before loading new (Game.cpp lines 41-47)

- file: cpp-qt-rpg/src/game/Game.cpp
  why: Combat event handling and reward distribution
  pattern: playerAttack(), monsterAttack(), checkCombatEndAfterAction() (lines 95-285)
  integration: Quest updates should hook into endCombat(), after rewards given

# MainWindow Integration Pattern
- file: cpp-qt-rpg/src/MainWindow.h
  why: View registration, signal connections, navigation handlers
  pattern: QStackedWidget, view member pointers, handleXxxClicked slots (lines 21-84)

- file: cpp-qt-rpg/src/MainWindow.cpp
  why: Complete view lifecycle management
  pattern: Create view, connect signals, add to stack, navigation handlers (lines 35-94)
  critical: Always call view->updateXxx(player) before setCurrentWidget (line 218)

# Factory Pattern References
- file: cpp-qt-rpg/src/game/factories/ItemFactory.h
  why: Static factory methods for entity creation
  pattern: static Item* createItem(name), static QList<Item*> getShopItems()

- file: cpp-qt-rpg/src/game/factories/ItemFactory.cpp
  why: Hardcoded entity definitions
  pattern: if/else chain for named items, procedural generation methods (lines 8-150)

# Testing Pattern References
- file: cpp-qt-rpg/tests/test_models.cpp
  why: Model unit testing structure
  pattern: QTest framework, QCOMPARE, QVERIFY macros, #include "test_models.moc"

- file: cpp-qt-rpg/tests/test_persistence.cpp
  why: Save/load testing pattern
  pattern: Create player, save, load, compare (lines 15-85)

# Theme Constants
- file: cpp-qt-rpg/src/theme/Theme.h
  why: All color, spacing, font constants
  pattern: Theme::CARD, Theme::PRIMARY, Theme::SPACING_LG, Theme::FONT_SIZE_XL
  critical: ALWAYS use Theme constants, never hardcode colors/sizes

# CMake Build Configuration
- file: cpp-qt-rpg/CMakeLists.txt
  why: How to add new source files to build
  pattern: Add .cpp files to add_executable(pyrpg-qt ...) and test targets (lines 23-64, 75-210)
  critical: Add to BOTH main executable AND relevant test executables
```

### Current Codebase Tree

```bash
cpp-qt-rpg/
├── src/
│   ├── main.cpp
│   ├── MainWindow.h/.cpp
│   ├── models/
│   │   ├── Character.h/.cpp         # Base class pattern
│   │   ├── Player.h/.cpp           # Complex model with serialization
│   │   ├── Monster.h/.cpp          # Inherits Character
│   │   ├── Item.h/.cpp             # Simple model pattern
│   │   └── Skill.h/.cpp            # Minimal model pattern
│   ├── game/
│   │   ├── Game.h/.cpp             # Controller with signals
│   │   └── factories/
│   │       ├── ItemFactory.h/.cpp   # Hardcoded definitions
│   │       ├── SkillFactory.h/.cpp
│   │       └── MonsterFactory.h/.cpp
│   ├── views/
│   │   ├── MainMenu.h/.cpp
│   │   ├── CombatPage.h/.cpp
│   │   ├── InventoryPage.h/.cpp    # View pattern to follow
│   │   ├── StatsPage.h/.cpp
│   │   ├── ShopPage.h/.cpp
│   │   └── SaveLoadPage.h/.cpp
│   ├── components/
│   │   ├── ItemCard.h/.cpp
│   │   ├── LogDisplay.h/.cpp
│   │   ├── CombatResultDialog.h/.cpp  # Dialog pattern
│   │   └── [many other components]
│   ├── persistence/
│   │   └── SaveManager.h/.cpp      # Save/load system
│   └── theme/
│       └── Theme.h                  # Constants only
├── tests/
│   ├── test_models.cpp
│   ├── test_persistence.cpp
│   ├── test_mainwindow.cpp
│   └── [other tests]
└── CMakeLists.txt
```

### Desired Codebase Tree (Files to Add)

```bash
cpp-qt-rpg/src/
├── models/
│   ├── Quest.h              # Quest model with objectives, rewards
│   └── Quest.cpp            # Serialization operators
├── game/
│   ├── QuestManager.h       # Quest state management, event handling
│   ├── QuestManager.cpp     # Auto-update logic, signal emissions
│   └── factories/
│       ├── QuestFactory.h   # Hardcoded quest definitions
│       └── QuestFactory.cpp # 5-10 story quests
├── views/
│   └── QuestLogPage.h/.cpp  # Quest viewing UI
├── components/
│   └── QuestCompletionDialog.h/.cpp  # Quest complete notification
└── tests/
    ├── test_quest_models.cpp      # Quest model unit tests
    └── test_quest_system.cpp      # QuestManager integration tests
```

### Known Gotchas & Library Quirks

```cpp
// CRITICAL: QDataStream Serialization
// Qt6 requires exact version matching between save and load
out.setVersion(QDataStream::Qt_6_0);  // MUST set in SaveManager
in.setVersion(QDataStream::Qt_6_0);   // MUST set in SaveManager

// CRITICAL: Pointer Container Serialization
// Cannot serialize QList<Quest*> directly - must convert to values
QList<Quest> valueList;
for (Quest* quest : player->quests) {
    if (quest != nullptr) {
        valueList.append(*quest);  // Dereference pointer
    }
}
out << valueList;  // Now Qt can serialize

// CRITICAL: Memory Management
// Player destructor MUST clean up quest pointers
qDeleteAll(quests);  // Qt utility for pointer lists
quests.clear();

// GOTCHA: QString "enum" Pattern
// Don't use C++ enum - use QString with specific values
QString status;  // Values: "locked", "active", "completed"
// This pattern allows easy serialization and flexibility

// GOTCHA: Signal Parameter Types
// Pointers can be passed through signals (used throughout codebase)
signals:
    void questCompleted(Quest *quest);  // Valid pattern
emit questCompleted(completedQuest);    // Works fine

// GOTCHA: QMap Serialization
// QMap automatically serializes IF both K and V are serializable
QMap<QString, int> map;  // Works - QString and int both supported
out << map;  // Automatically handles the entire map

// CRITICAL: Base Class Serialization
// Must explicitly cast to base class when serializing
out << static_cast<const Character&>(player);  // Correct
// Player's operator<< then does this for Character data

// GOTCHA: Theme Constants
// ALWAYS use Theme::CONSTANT, never hardcode
"background-color: " + Theme::CARD.name()  // Correct
"background-color: #1e1e1e"                // Wrong - hardcoded

// GOTCHA: MainWindow View Updates
// MUST call updateXxx() before setCurrentWidget()
m_questLogPage->updateQuests(m_game->getPlayer());  // First
stackedWidget->setCurrentWidget(m_questLogPage);    // Then switch
// Otherwise view shows stale data

// CRITICAL: CMakeLists.txt Updates
// Must add .cpp files to BOTH main executable AND test executables
add_executable(pyrpg-qt
    src/models/Quest.cpp      # Add here
    # ... existing files
)
add_executable(test_quest_models tests/test_quest_models.cpp
    src/models/Quest.cpp      # AND here
)

// GOTCHA: Qt Test Framework
// MUST include the .moc file at end of test file
#include "test_quest_models.moc"  // Required at EOF
QTEST_MAIN(TestQuestModels)       // Generates main()
```

## Implementation Blueprint

### Data Models and Structure

Following the exact patterns from Player, Item, and Skill models:

**Quest Model (src/models/Quest.h)**:
- Public member variables (camelCase naming)
- Default constructor + parameterized constructor with defaults
- Friend QDataStream operators for serialization
- Helper methods (isComplete(), getProgress(), etc.)
- QString for status/types (not C++ enums)
- Nested structures for objectives and rewards

**QuestObjective Structure**:
- Embedded in Quest class (not separate file)
- Simple struct with type, description, target, progress
- ObjectiveType as QString: "kill_enemies", "reach_level", "collect_item", "defeat_boss"

**QuestRewards Structure**:
- Embedded in Quest class
- Fields: int experience, int gold, QList<QString> itemNames
- Items referenced by name (factory creates actual Item* when rewarding)

**Quest Lifecycle**:
1. Created by QuestFactory with all data
2. Added to Player's questList
3. Status changes: "locked" → "available" → "active" → "completed" → "rewarded"
4. Progress tracked in objectives
5. Serialized with Player data
6. Deleted when Player destroyed

### Implementation Tasks (Ordered by Dependencies)

```yaml
Task 1: CREATE src/models/Quest.h
  IMPLEMENT: Quest class with QuestObjective, QuestRewards structs
  FOLLOW pattern: src/models/Item.h (simple model structure)
  NAMING:
    - Class: Quest (PascalCase)
    - Members: questId, title, description, status, objectives, rewards (camelCase)
    - Methods: isComplete(), isActive(), getProgress(), updateObjective() (camelCase)
  FIELDS:
    - QString questId (unique identifier, e.g., "main_quest_01")
    - QString title (display name, e.g., "A Dark Omen")
    - QString description (1-2 sentence summary)
    - QString longDescription (full quest text)
    - QString status ("locked", "available", "active", "completed", "rewarded")
    - int orderIndex (for display ordering)
    - int minimumLevel (prerequisite)
    - QList<QString> prerequisiteQuestIds
    - QList<QuestObjective> objectives
    - QuestRewards rewards
  STRUCTS:
    - QuestObjective: QString type, QString description, QString targetId, int required, int current, bool completed
    - QuestRewards: int experience, int gold, QList<QString> itemNames
  PLACEMENT: cpp-qt-rpg/src/models/Quest.h

Task 2: CREATE src/models/Quest.cpp
  IMPLEMENT: Constructors, helper methods, QDataStream operators
  FOLLOW pattern: src/models/Item.cpp (lines 3-32 for operators)
  SERIALIZATION:
    - Operator<< writes ALL members in order
    - Operator>> reads in EXACT same order
    - QList automatically serialized by Qt
  METHODS:
    - Quest() default constructor: initialize with empty strings, status "locked"
    - Quest(params) constructor: initialize all fields from parameters
    - bool isComplete() const: return status == "completed" || status == "rewarded"
    - bool isActive() const: return status == "active"
    - int getProgress() const: return completed objectives count
    - void updateObjective(int index, int progress): set current += progress, check completion
  PLACEMENT: cpp-qt-rpg/src/models/Quest.cpp
  DEPENDENCIES: Quest.h (Task 1)

Task 3: UPDATE src/models/Player.h
  ADD: Quest data members to Player class
  FOLLOW pattern: Skill list pattern (line 24 in Player.h)
  ADDITIONS:
    - #include "Quest.h" at top
    - QList<Quest*> quests; (in public members section)
    - void addQuest(Quest* quest); (quest management methods)
    - Quest* getQuest(const QString &questId) const;
    - QList<Quest*> getActiveQuests() const;
    - QList<Quest*> getCompletedQuests() const;
  PLACEMENT: After skills member, before equipment (around line 25)
  DEPENDENCIES: Quest.h (Task 1)

Task 4: UPDATE src/models/Player.cpp
  MODIFY: Constructor, destructor, serialization operators
  FOLLOW pattern: Skills serialization (lines 93-99, 146-152 in Player.cpp)
  CHANGES:
    1. Destructor: Add qDeleteAll(quests); quests.clear(); (after skills cleanup, line 57)
    2. Operator<< (line 62): Increment version to 3, add quest serialization at end
       - Convert QList<Quest*> to QList<Quest> (dereference non-null pointers)
       - out << questValueList;
    3. Operator>> (line 104): Add conditional quest deserialization (if version >= 3)
       - QList<Quest> questValueList; in >> questValueList;
       - for (const Quest &q : questValueList) { quests.append(new Quest(q)); }
    4. Quest management methods implementation:
       - void addQuest(Quest* quest) { quests.append(quest); }
       - Quest* getQuest(id): loop quests, return if questId matches, else nullptr
       - getActiveQuests(): filter where isActive() true
       - getCompletedQuests(): filter where isComplete() true
  CRITICAL: Version must be 3, conditional load ensures old saves work
  DEPENDENCIES: Quest.cpp (Task 2), Player.h updated (Task 3)

Task 5: UPDATE src/persistence/SaveManager.cpp
  MODIFY: Save file format version (optional, depends on compatibility strategy)
  FOLLOW pattern: Version checking (lines 29, 61-67)
  IF incrementing file format version:
    - Line 29: out << quint32(3); (was 2)
    - Line 63: if (saveVersion > 3) { warn and reject }
  NOTE: Can skip if Player version 3 is sufficient for compatibility
  DEPENDENCIES: Player.cpp updated (Task 4)

Task 6: CREATE src/game/factories/QuestFactory.h
  IMPLEMENT: Static factory methods for quest creation
  FOLLOW pattern: src/game/factories/ItemFactory.h (lines 8-14)
  NAMING: QuestFactory class, static methods
  METHODS:
    - static Quest* createQuest(const QString &questId);
    - static QList<Quest*> getAllMainQuests();
    - static QList<Quest*> getAvailableQuests(Player* player);
  PLACEMENT: cpp-qt-rpg/src/game/factories/QuestFactory.h
  DEPENDENCIES: Quest.h (Task 1), Player.h updated (Task 3)

Task 7: CREATE src/game/factories/QuestFactory.cpp
  IMPLEMENT: Hardcoded quest definitions (5-10 main story quests)
  FOLLOW pattern: src/game/factories/ItemFactory.cpp (if/else chain, lines 8-75)
  QUESTS to define (from PRD lines 1239-1276):
    1. "main_quest_01": "A Dark Omen" (Level 1, kill 3 Shadow Wolves, talk to Elder)
    2. "main_quest_02": "The Whispering Woods" (Level 3, reach level 5, collect 3 shards)
    3. "main_quest_03": "Shadows Deepen" (Level 5, defeat Shadow Lord mini-boss)
    4. "main_quest_04": "The Scholar's Warning" (Level 7, talk to Scholar, collect Tome)
    5. "main_quest_05": "Gathering Strength" (Level 10, reach level 12, get rare equipment)
  STRUCTURE:
    - if (questId == "main_quest_01") { return new Quest(...); }
    - else if (questId == "main_quest_02") { return new Quest(...); }
    - getAllMainQuests(): return list with all quest IDs created
    - getAvailableQuests(player): filter by prerequisites and level
  OBJECTIVES:
    - QuestObjective obj1; obj1.type = "kill_enemies"; obj1.targetId = "shadow_wolf"; obj1.required = 3;
    - objectives.append(obj1);
  PLACEMENT: cpp-qt-rpg/src/game/factories/QuestFactory.cpp
  DEPENDENCIES: QuestFactory.h (Task 6)

Task 8: CREATE src/game/QuestManager.h
  IMPLEMENT: QuestManager class (QObject) for state management
  FOLLOW pattern: src/game/Game.h (QObject with signals, lines 10-57)
  NAMING: QuestManager class, handleXxx slots, onXxx event methods
  CLASS structure:
    - Inherit from QObject
    - Q_OBJECT macro
    - Constructor: explicit QuestManager(Player* player, QObject* parent = nullptr);
  MEMBERS:
    - Player* m_player (reference to player, not owned)
    - QList<Quest*> m_allQuests (all loaded quests, owned by manager)
    - QMap<QString, Quest*> m_questMap (quick lookup)
  METHODS:
    - void loadQuests(); (call QuestFactory, populate m_allQuests)
    - bool acceptQuest(const QString &questId); (change status, add to player)
    - void updateQuestProgress(const QString &questId, int objIndex, int progress);
    - void completeQuest(const QString &questId); (change status, give rewards)
  EVENT handlers:
    - void onCombatEnd(const QString &enemyName);
    - void onLevelUp(int newLevel);
    - void onItemCollected(const QString &itemName);
  SIGNALS:
    - void questAvailable(const QString &questId);
    - void questAccepted(const QString &questId);
    - void questProgressed(const QString &questId, int objectiveIndex);
    - void questCompleted(const QString &questId, int expReward, int goldReward);
  PLACEMENT: cpp-qt-rpg/src/game/QuestManager.h
  DEPENDENCIES: Quest.h (Task 1), Player.h updated (Task 3)

Task 9: CREATE src/game/QuestManager.cpp
  IMPLEMENT: Quest state machine logic and event handlers
  FOLLOW pattern: src/game/Game.cpp (event-driven logic, lines 95-285)
  KEY implementations:
    1. loadQuests(): Call QuestFactory::getAllMainQuests(), populate m_allQuests and m_questMap
    2. acceptQuest(id): Find quest, change status to "active", add to player->quests
    3. updateQuestProgress(id, objIdx, progress):
       - Find quest, update objective[objIdx].current += progress
       - Check if objective.current >= objective.required, set completed = true
       - Check if ALL objectives complete, emit questCompleted
    4. completeQuest(id):
       - Change status to "completed"
       - Call player->gainExperience(rewards.experience)
       - player->gold += rewards.gold
       - Create items from rewards.itemNames via ItemFactory
       - emit questCompleted signal with rewards
    5. onCombatEnd(enemyName):
       - Loop active quests, check if any have "kill_enemies" objective matching targetId
       - If match, call updateQuestProgress(questId, objIndex, 1)
    6. onLevelUp(newLevel):
       - Loop active quests, check if any have "reach_level" objective
       - If player level >= required level, call updateQuestProgress (set to required)
       - Also check locked quests to unlock if level prerequisite met
    7. onItemCollected(itemName):
       - Loop active quests, check "collect_item" objectives matching targetId
       - Call updateQuestProgress
  PLACEMENT: cpp-qt-rpg/src/game/QuestManager.cpp
  DEPENDENCIES: QuestManager.h (Task 8), QuestFactory.cpp (Task 7)

Task 10: UPDATE src/game/Game.h
  ADD: QuestManager member and getter
  FOLLOW pattern: SaveManager pattern (line 46 in Game.h - owned member)
  ADDITIONS:
    - #include "QuestManager.h" at top
    - QuestManager* m_questManager; (private member, as pointer for lazy init)
    - QuestManager* getQuestManager(); (public getter)
  PLACEMENT: Add m_questManager after saveManager, before friend class
  DEPENDENCIES: QuestManager.h (Task 8)

Task 11: UPDATE src/game/Game.cpp
  MODIFY: Constructor, destructor, combat/level handlers to integrate quest updates
  FOLLOW pattern: Game owns QuestManager, initializes after player created
  CHANGES:
    1. Constructor: Initialize m_questManager(nullptr) in member list
    2. newGame(): After creating player, create QuestManager:
       - m_questManager = new QuestManager(player, this);
       - m_questManager->loadQuests();
       - Auto-activate first quest if appropriate
    3. loadGame(): After loading player, recreate QuestManager:
       - if (m_questManager) delete m_questManager;
       - m_questManager = new QuestManager(player, this);
       - m_questManager->loadQuests();
    4. Destructor: Add: if (m_questManager) delete m_questManager;
    5. endCombat() or playerAttack() after victory:
       - if (m_questManager) m_questManager->onCombatEnd(currentMonster->name);
    6. After player->levelUp() call:
       - if (m_questManager) m_questManager->onLevelUp(player->level);
    7. getQuestManager() implementation: return m_questManager;
  CRITICAL: QuestManager must be recreated on load to reference new Player pointer
  DEPENDENCIES: Game.h updated (Task 10), QuestManager.cpp (Task 9)

Task 12: CREATE src/views/QuestLogPage.h
  IMPLEMENT: Quest viewing UI page
  FOLLOW pattern: src/views/InventoryPage.h (lines 1-52)
  CLASS structure:
    - Inherit from QWidget
    - Q_OBJECT macro
    - explicit QuestLogPage(QWidget *parent = nullptr);
  SIGNALS:
    - void backRequested();
    - void questAccepted(const QString &questId);
  PUBLIC methods:
    - void updateQuests(QuestManager* questManager, Player* player);
  PROTECTED:
    - void keyPressEvent(QKeyEvent *event) override;
  PRIVATE slots:
    - void handleQuestClicked(Quest *quest);
    - void handleAcceptQuest();
  PRIVATE methods:
    - void setupUi();
    - void clearQuests();
    - QWidget* createQuestCard(Quest* quest);
  MEMBERS:
    - QuestManager* m_questManager (reference, not owned)
    - Player* m_currentPlayer (reference, not owned)
    - QLabel* m_titleLabel;
    - QListWidget* m_questList (left pane - list of quests)
    - QTextEdit* m_questDetails (right pane - selected quest details)
    - QPushButton* m_backButton;
    - QPushButton* m_acceptButton (for available quests)
    - Quest* m_selectedQuest (currently selected)
  PLACEMENT: cpp-qt-rpg/src/views/QuestLogPage.h
  DEPENDENCIES: Quest.h (Task 1), QuestManager.h (Task 8)

Task 13: CREATE src/views/QuestLogPage.cpp
  IMPLEMENT: Quest log UI with list and detail views
  FOLLOW pattern: src/views/InventoryPage.cpp (lines 1-323)
  KEY implementations:
    1. setupUi():
       - QHBoxLayout main (2-column: list | details)
       - Left: Title label, QListWidget, back button (VBoxLayout)
       - Right: QTextEdit for details
       - Apply Theme constants for all styling
       - Connect m_questList itemClicked to handleQuestClicked
       - Connect m_backButton to backRequested signal
    2. updateQuests(questManager, player):
       - m_questManager = questManager; m_currentPlayer = player;
       - clearQuests();
       - Get active, available, completed quests from manager
       - Add section headers to list: "=== ACTIVE QUESTS ==="
       - For each quest: Create QListWidgetItem with title, store Quest* in UserRole
       - Repeat for available and completed sections
    3. handleQuestClicked(quest):
       - m_selectedQuest = quest;
       - Build HTML for details pane:
         - Title (h2), Status badge, Description (p)
         - Objectives list with progress (3/10 Enemies Killed)
         - Rewards section (XP, Gold, Items if any)
         - Prerequisites section if locked
       - m_questDetails->setHtml(detailsHtml);
       - Show/hide accept button based on quest status
    4. handleAcceptQuest():
       - if (!m_selectedQuest || !m_questManager) return;
       - emit questAccepted(m_selectedQuest->questId);
       - Call updateQuests to refresh
    5. keyPressEvent():
       - Esc: emit backRequested()
       - 1-9: Select quest at index (if exists)
       - A: Accept selected quest (if available)
  STYLING: Use Theme::CARD for cards, Theme::PRIMARY for highlights, Quest status colors
  PLACEMENT: cpp-qt-rpg/src/views/QuestLogPage.cpp
  DEPENDENCIES: QuestLogPage.h (Task 12), Theme.h

Task 14: CREATE src/components/QuestCompletionDialog.h
  IMPLEMENT: Modal dialog shown on quest completion
  FOLLOW pattern: src/components/CombatResultDialog.h (lines 1-24)
  CLASS structure:
    - Inherit from QDialog
    - Q_OBJECT macro
    - explicit QuestCompletionDialog(const QString &questTitle, int expGained,
        int goldGained, const QList<QString> &itemNames, QWidget *parent = nullptr);
  PRIVATE methods:
    - void setupUi(const QString &title, int exp, int gold, const QList<QString> &items);
  PLACEMENT: cpp-qt-rpg/src/components/QuestCompletionDialog.h
  DEPENDENCIES: None (simple dialog)

Task 15: CREATE src/components/QuestCompletionDialog.cpp
  IMPLEMENT: Quest completion celebration dialog
  FOLLOW pattern: src/components/CombatResultDialog.cpp (lines 1-110)
  STRUCTURE:
    - Constructor: Set window title "Quest Complete!", call setupUi
    - setupUi():
      - VBoxLayout with celebration message
      - Title label with quest name (large, bold, PRIMARY color)
      - "Quest Complete!" message
      - Rewards section: "Gained X XP", "Gained Y Gold", "Received: [items]"
      - Continue button (accept() on click)
      - Apply Theme styling
  PLACEMENT: cpp-qt-rpg/src/components/QuestCompletionDialog.cpp
  DEPENDENCIES: QuestCompletionDialog.h (Task 14), Theme.h

Task 16: UPDATE src/MainWindow.h
  ADD: QuestLogPage member, quest-related handlers, keyboard shortcut
  FOLLOW pattern: Existing view members and handlers (lines 21-84)
  ADDITIONS:
    - #include "views/QuestLogPage.h" at top
    - QuestLogPage *m_questLogPage; (private member with other views, line 78)
    - void handleOpenQuestLog(); (private slot, around line 42)
    - void handleQuestLogBack(); (private slot)
    - void handleQuestAccepted(const QString &questId); (private slot)
    - void handleQuestCompleted(const QString &questId, int exp, int gold); (private slot)
  PLACEMENT: Add members with other view pointers, add slots with other handlers
  DEPENDENCIES: QuestLogPage.h (Task 12)

Task 17: UPDATE src/MainWindow.cpp
  MODIFY: Constructor to create QuestLogPage, connect signals, add to stack
  FOLLOW pattern: InventoryPage integration (lines 66-69, 215-222, 369-378)
  CHANGES:
    1. Constructor (around line 66):
       - m_questLogPage = new QuestLogPage();
       - connect(m_questLogPage, &QuestLogPage::backRequested, this, &MainWindow::handleQuestLogBack);
       - connect(m_questLogPage, &QuestLogPage::questAccepted, this, &MainWindow::handleQuestAccepted);
       - stackedWidget->addWidget(m_questLogPage);
    2. Constructor (connect QuestManager signals, after Game created):
       - connect(m_game->getQuestManager(), &QuestManager::questCompleted,
                 this, &MainWindow::handleQuestCompleted);
    3. handleOpenQuestLog() implementation:
       - if (!m_game || !m_game->getPlayer()) return;
       - m_questLogPage->updateQuests(m_game->getQuestManager(), m_game->getPlayer());
       - stackedWidget->setCurrentWidget(m_questLogPage);
       - m_questLogPage->setFocus();
    4. handleQuestLogBack():
       - stackedWidget->setCurrentWidget(m_combatPage);
    5. handleQuestAccepted(questId):
       - m_game->getQuestManager()->acceptQuest(questId);
       - m_questLogPage->updateQuests(m_game->getQuestManager(), m_game->getPlayer());
    6. handleQuestCompleted(questId, exp, gold):
       - Get quest from manager to get title
       - QuestCompletionDialog dialog(title, exp, gold, items, this);
       - dialog.exec();
       - m_questLogPage->updateQuests(...) if on quest log page
    7. keyPressEvent() (around line 400):
       - case Qt::Key_Q: handleOpenQuestLog(); break;
  CRITICAL: Connect QuestManager signals AFTER Game is created (newGame or loadGame)
  DEPENDENCIES: MainWindow.h updated (Task 16), QuestLogPage.cpp (Task 13), QuestCompletionDialog.cpp (Task 15)

Task 18: UPDATE cpp-qt-rpg/CMakeLists.txt
  ADD: All new source files to build targets
  FOLLOW pattern: Existing file lists (lines 23-64 for main, 75-210 for tests)
  CHANGES:
    1. Main executable (add to add_executable(pyrpg-qt ...) around line 23):
       - src/models/Quest.cpp
       - src/game/QuestManager.cpp
       - src/game/factories/QuestFactory.cpp
       - src/views/QuestLogPage.cpp
       - src/components/QuestCompletionDialog.cpp
    2. Test executables - Add Quest.cpp to:
       - test_mainwindow (line 75): src/models/Quest.cpp, src/game/QuestManager.cpp, src/game/factories/QuestFactory.cpp
       - test_models (line 109): src/models/Quest.cpp
       - test_persistence (line 115): src/models/Quest.cpp
  CRITICAL: Files must be in both main executable AND any test that uses them
  PLACEMENT: Add in alphabetical order within each section for maintainability
  DEPENDENCIES: All previous tasks completed

Task 19: CREATE tests/test_quest_models.cpp
  IMPLEMENT: Unit tests for Quest model
  FOLLOW pattern: tests/test_models.cpp (lines 1-120)
  TEST cases:
    - testQuestCreation(): Verify constructor initializes correctly
    - testQuestSerialization(): Save and load Quest, compare all fields
    - testQuestObjectives(): Add objectives, update progress, check completion
    - testQuestStatusTransitions(): locked → available → active → completed
    - testQuestRewards(): Verify reward structure
  STRUCTURE:
    - #include <QtTest/QtTest>
    - class TestQuestModels : public QObject { Q_OBJECT private slots: ... };
    - QTEST_MAIN(TestQuestModels)
    - #include "test_quest_models.moc"
  PLACEMENT: cpp-qt-rpg/tests/test_quest_models.cpp
  DEPENDENCIES: Quest.cpp (Task 2)

Task 20: CREATE tests/test_quest_system.cpp
  IMPLEMENT: Integration tests for QuestManager
  FOLLOW pattern: tests/test_persistence.cpp (lines 1-95)
  TEST cases:
    - testQuestManagerLoad(): Verify quests load from factory
    - testQuestAcceptance(): Accept quest, verify added to player
    - testKillQuestProgress(): Simulate combat, verify quest updates
    - testLevelQuestCompletion(): Level up, verify quest completes
    - testQuestCompletion(): Complete quest, verify rewards given
    - testQuestSavePersistence(): Save with quests, load, verify state
  STRUCTURE: Same as test_quest_models.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_quest_system.cpp
  DEPENDENCIES: QuestManager.cpp (Task 9), Game.cpp updated (Task 11)

Task 21: UPDATE cpp-qt-rpg/CMakeLists.txt (test targets)
  ADD: New test executables
  FOLLOW pattern: Existing test targets (lines 108-129, 114-128)
  CHANGES:
    1. Add test_quest_models executable (after test_persistence around line 128):
       add_executable(test_quest_models tests/test_quest_models.cpp
           src/models/Quest.cpp
       )
       target_link_libraries(test_quest_models PRIVATE Qt6::Widgets Qt6::Test)
       target_include_directories(test_quest_models PRIVATE src)
       add_test(NAME QuestModelsTest COMMAND test_quest_models)

    2. Add test_quest_system executable:
       add_executable(test_quest_system tests/test_quest_system.cpp
           src/models/Quest.cpp
           src/models/Player.cpp
           src/models/Character.cpp
           src/models/Item.cpp
           src/models/Skill.cpp
           src/game/QuestManager.cpp
           src/game/factories/QuestFactory.cpp
           src/game/factories/ItemFactory.cpp
           src/game/Game.cpp
           src/persistence/SaveManager.cpp
       )
       target_link_libraries(test_quest_system PRIVATE Qt6::Widgets Qt6::Test)
       target_include_directories(test_quest_system PRIVATE src)
       add_test(NAME QuestSystemTest COMMAND test_quest_system)
  DEPENDENCIES: Test files created (Tasks 19, 20)
```

### Implementation Patterns & Key Details

```cpp
// ============================================================================
// PATTERN 1: Quest Model Structure
// ============================================================================
// File: src/models/Quest.h
// Follow: Item.h pattern (simple model, public members, friend operators)

class Quest
{
public:
    // Constructors (default + parameterized with defaults)
    Quest();
    Quest(const QString &id, const QString &title, const QString &description = "",
          const QString &status = "locked", int minLevel = 1);

    // Public members (camelCase)
    QString questId;
    QString title;
    QString description;
    QString longDescription;
    QString status;  // "locked", "available", "active", "completed", "rewarded"
    int orderIndex;
    int minimumLevel;
    QList<QString> prerequisiteQuestIds;
    QList<QuestObjective> objectives;  // Nested struct
    QuestRewards rewards;              // Nested struct

    // Helper methods
    bool isComplete() const;
    bool isActive() const;
    int getProgress() const;  // Returns completed objective count
    void updateObjective(int index, int progress);

    // Serialization (REQUIRED)
    friend QDataStream &operator<<(QDataStream &out, const Quest &q);
    friend QDataStream &operator>>(QDataStream &in, Quest &q);
};

// Nested structures (in same file)
struct QuestObjective {
    QString type;         // "kill_enemies", "reach_level", "collect_item", "defeat_boss"
    QString description;  // "Defeat 3 Shadow Wolves"
    QString targetId;     // "shadow_wolf" (monster name/item name)
    int required;         // 3
    int current;          // 0-3
    bool completed;       // false until current >= required
};

struct QuestRewards {
    int experience;           // 100
    int gold;                 // 50
    QList<QString> itemNames; // ["healing_potion", "iron_sword"]
};

// ============================================================================
// PATTERN 2: Quest Serialization
// ============================================================================
// File: src/models/Quest.cpp
// Follow: Item.cpp serialization (lines 18-32)
// CRITICAL: Order must match exactly in << and >>

QDataStream &operator<<(QDataStream &out, const Quest &q)
{
    // Write ALL members in order (primitive types, then containers)
    out << q.questId << q.title << q.description << q.longDescription
        << q.status << q.orderIndex << q.minimumLevel
        << q.prerequisiteQuestIds;  // QList<QString> auto-serializes

    // Serialize objectives (QList of structs)
    out << quint32(q.objectives.size());
    for (const QuestObjective &obj : q.objectives) {
        out << obj.type << obj.description << obj.targetId
            << obj.required << obj.current << obj.completed;
    }

    // Serialize rewards
    out << q.rewards.experience << q.rewards.gold << q.rewards.itemNames;

    return out;
}

QDataStream &operator>>(QDataStream &in, Quest &q)
{
    // Read in EXACT same order
    in >> q.questId >> q.title >> q.description >> q.longDescription
       >> q.status >> q.orderIndex >> q.minimumLevel
       >> q.prerequisiteQuestIds;

    // Deserialize objectives
    quint32 objCount;
    in >> objCount;
    q.objectives.clear();
    for (quint32 i = 0; i < objCount; ++i) {
        QuestObjective obj;
        in >> obj.type >> obj.description >> obj.targetId
           >> obj.required >> obj.current >> obj.completed;
        q.objectives.append(obj);
    }

    // Deserialize rewards
    in >> q.rewards.experience >> q.rewards.gold >> q.rewards.itemNames;

    return in;
}

// ============================================================================
// PATTERN 3: Player Quest Integration
// ============================================================================
// File: src/models/Player.cpp
// Follow: Skills pattern (lines 93-99 for save, 146-152 for load)

// In operator<< (save) - increment version to 3
out << quint32(3);  // Version 3: Added quest data

// After equipment/inventory/skills serialization:
// Convert QList<Quest*> to QList<Quest> for serialization
QList<Quest> questList;
for (Quest* quest : p.quests) {
    if (quest != nullptr) {
        questList.append(*quest);  // Dereference pointer
    }
}
out << questList;  // Qt handles QList<Quest> automatically

// In operator>> (load) - conditional based on version
if (version >= 3) {
    QList<Quest> questList;
    in >> questList;
    for (const Quest &quest : questList) {
        p.quests.append(new Quest(quest));  // Create new heap object
    }
}
// For version < 3, p.quests remains empty (default constructed)

// In destructor:
qDeleteAll(quests);  // Qt utility deletes all pointers in list
quests.clear();

// ============================================================================
// PATTERN 4: QuestManager Event Handling
// ============================================================================
// File: src/game/QuestManager.cpp
// Follow: Game.cpp event patterns

void QuestManager::onCombatEnd(const QString &enemyName)
{
    // Get active quests from player
    QList<Quest*> activeQuests;
    for (Quest* quest : m_player->quests) {
        if (quest && quest->isActive()) {
            activeQuests.append(quest);
        }
    }

    // Check each active quest for matching kill objectives
    for (Quest* quest : activeQuests) {
        for (int i = 0; i < quest->objectives.size(); ++i) {
            QuestObjective &obj = quest->objectives[i];

            // Check if this objective matches the killed enemy
            if (obj.type == "kill_enemies" &&
                obj.targetId == enemyName &&
                !obj.completed) {

                // Update progress
                obj.current++;
                if (obj.current >= obj.required) {
                    obj.completed = true;
                }

                // Emit progress signal
                emit questProgressed(quest->questId, i);

                // Check if ALL objectives complete
                if (quest->isComplete()) {
                    completeQuest(quest->questId);
                }
            }
        }
    }
}

void QuestManager::completeQuest(const QString &questId)
{
    Quest* quest = m_questMap.value(questId, nullptr);
    if (!quest || quest->status != "active") return;

    // Change status
    quest->status = "completed";

    // Give rewards
    m_player->gainExperience(quest->rewards.experience);
    m_player->gold += quest->rewards.gold;

    // Create reward items
    for (const QString &itemName : quest->rewards.itemNames) {
        Item* item = ItemFactory::createItem(itemName);
        if (item) {
            m_player->inventory.append(item);
        }
    }

    // Emit completion signal
    emit questCompleted(questId, quest->rewards.experience, quest->rewards.gold);

    // Check if new quests unlock
    checkQuestUnlocks();
}

// ============================================================================
// PATTERN 5: QuestLogPage UI Structure
// ============================================================================
// File: src/views/QuestLogPage.cpp
// Follow: InventoryPage.cpp layout pattern (lines 21-120)

void QuestLogPage::setupUi()
{
    // Main horizontal layout (list | details)
    QHBoxLayout *mainLayout = new QHBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG,
                                   Theme::SPACING_LG, Theme::SPACING_LG);
    mainLayout->setSpacing(Theme::SPACING_LG);

    // LEFT SIDE: Quest list with title and back button
    QVBoxLayout *listLayout = new QVBoxLayout();

    // Title
    m_titleLabel = new QLabel("Quest Log");
    m_titleLabel->setStyleSheet(QString(
        "font-size: %1px; font-weight: %2; color: %3;"
    ).arg(Theme::FONT_SIZE_XL)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::PRIMARY.name()));
    listLayout->addWidget(m_titleLabel);

    // Quest list widget
    m_questList = new QListWidget();
    m_questList->setStyleSheet(QString(
        "QListWidget {"
        "    background-color: %1;"
        "    border: 2px solid %2;"
        "    border-radius: %3px;"
        "}"
        "QListWidget::item:selected {"
        "    background-color: %4;"
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD)
     .arg(Theme::PRIMARY.name()));

    connect(m_questList, &QListWidget::itemClicked, this, [this](QListWidgetItem *item) {
        Quest *quest = static_cast<Quest*>(item->data(Qt::UserRole).value<void*>());
        handleQuestClicked(quest);
    });
    listLayout->addWidget(m_questList);

    // Back button
    m_backButton = new QPushButton("Back (Esc)");
    m_backButton->setMinimumHeight(40);
    connect(m_backButton, &QPushButton::clicked, this, &QuestLogPage::backRequested);
    listLayout->addWidget(m_backButton);

    mainLayout->addLayout(listLayout, 1);  // Stretch factor 1

    // RIGHT SIDE: Quest details
    m_questDetails = new QTextEdit();
    m_questDetails->setReadOnly(true);
    m_questDetails->setStyleSheet(QString(
        "QTextEdit {"
        "    background-color: %1;"
        "    border: 2px solid %2;"
        "    border-radius: %3px;"
        "    padding: %4px;"
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD)
     .arg(Theme::SPACING_MD));

    mainLayout->addWidget(m_questDetails, 2);  // Stretch factor 2
}

// ============================================================================
// PATTERN 6: MainWindow Quest Integration
// ============================================================================
// File: src/MainWindow.cpp
// Follow: InventoryPage integration (lines 66-69, 215-222)

// In constructor (after Game created):
m_questLogPage = new QuestLogPage();
connect(m_questLogPage, &QuestLogPage::backRequested,
        this, &MainWindow::handleQuestLogBack);
connect(m_questLogPage, &QuestLogPage::questAccepted,
        this, &MainWindow::handleQuestAccepted);
stackedWidget->addWidget(m_questLogPage);

// Connect QuestManager signals (must happen AFTER newGame/loadGame creates QuestManager)
// Put this in newGame() and loadGame() after m_game->getQuestManager() exists:
connect(m_game->getQuestManager(), &QuestManager::questCompleted,
        this, &MainWindow::handleQuestCompleted, Qt::UniqueConnection);

// Navigation handler
void MainWindow::handleOpenQuestLog()
{
    if (!m_game || !m_game->getPlayer() || !m_game->getQuestManager()) return;

    // CRITICAL: Update view BEFORE switching
    m_questLogPage->updateQuests(m_game->getQuestManager(), m_game->getPlayer());

    // Switch view
    stackedWidget->setCurrentWidget(m_questLogPage);
    m_questLogPage->setFocus();
}

// Quest completion handler
void MainWindow::handleQuestCompleted(const QString &questId, int exp, int gold)
{
    // Get quest details for dialog
    Quest* quest = m_game->getQuestManager()->getQuestById(questId);
    if (!quest) return;

    // Show completion dialog
    QuestCompletionDialog dialog(quest->title, exp, gold, quest->rewards.itemNames, this);
    dialog.exec();  // Modal - waits for user to click Continue

    // Refresh quest log if currently visible
    if (stackedWidget->currentWidget() == m_questLogPage) {
        m_questLogPage->updateQuests(m_game->getQuestManager(), m_game->getPlayer());
    }
}
```

### Integration Points

```yaml
COMBAT_SYSTEM:
  - location: src/game/Game.cpp, endCombat() or after playerAttack() victory
  - add: if (m_questManager) m_questManager->onCombatEnd(currentMonster->name);
  - timing: After rewards given, before combat log updated

LEVELING_SYSTEM:
  - location: src/models/Player.cpp, after levelUp() call or in levelUp() method
  - add: Emit signal or call QuestManager directly if reference available
  - alternative: MainWindow handles Player level change, calls quest manager
  - timing: Immediately after player->level increments

ITEM_COLLECTION:
  - location: Item pickup points (loot drops, shop purchases)
  - add: m_questManager->onItemCollected(item->name);
  - timing: After item added to player->inventory

SAVE_SYSTEM:
  - location: src/models/Player.cpp, operator<< and operator>>
  - changes: Version 3, serialize quests list after skills (convert pointers to values)
  - backward_compat: if (version >= 3) when loading

MAINWINDOW_KEYBOARD:
  - location: src/MainWindow.cpp, keyPressEvent()
  - add: case Qt::Key_Q: handleOpenQuestLog(); break;
  - alternative: Qt::CTRL + Qt::Key_Q if Q conflicts

CMAKE_BUILD:
  - file: cpp-qt-rpg/CMakeLists.txt
  - add_to_main: src/models/Quest.cpp, src/game/QuestManager.cpp,
                 src/game/factories/QuestFactory.cpp, src/views/QuestLogPage.cpp,
                 src/components/QuestCompletionDialog.cpp
  - add_to_tests: Quest.cpp to test_models, test_persistence, test_mainwindow
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# After creating Quest model files
cd cpp-qt-rpg/build
cmake ..
make src/models/Quest.cpp  # Verify syntax compiles

# After creating QuestManager
make src/game/QuestManager.cpp

# After creating UI files
make src/views/QuestLogPage.cpp
make src/components/QuestCompletionDialog.cpp

# Full build
cd cpp-qt-rpg/build
cmake ..
make

# Expected: Zero compile errors. Fix any errors before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test Quest model serialization
cd cpp-qt-rpg/build
./test_quest_models

# Expected output:
# ********* Start testing of TestQuestModels *********
# PASS   : TestQuestModels::testQuestCreation()
# PASS   : TestQuestModels::testQuestSerialization()
# PASS   : TestQuestModels::testQuestObjectives()
# PASS   : TestQuestModels::testQuestStatusTransitions()
# PASS   : TestQuestModels::testQuestRewards()
# ********* Finished testing of TestQuestModels *********

# Test QuestManager integration
./test_quest_system

# Expected output:
# ********* Start testing of TestQuestSystem *********
# PASS   : TestQuestSystem::testQuestManagerLoad()
# PASS   : TestQuestSystem::testQuestAcceptance()
# PASS   : TestQuestSystem::testKillQuestProgress()
# PASS   : TestQuestSystem::testLevelQuestCompletion()
# PASS   : TestQuestSystem::testQuestCompletion()
# PASS   : TestQuestSystem::testQuestSavePersistence()
# ********* Finished testing of TestQuestSystem *********

# Run all tests
ctest

# Expected: All tests pass (0 failures)
```

### Level 3: Integration Testing (System Validation)

```bash
# Run the game
cd cpp-qt-rpg/build
./pyrpg-qt

# Manual test flow:
# 1. Start New Game
# 2. Press Q to open Quest Log
#    - Verify first quest is active ("A Dark Omen")
#    - Verify quest shows objectives (Kill 3 Shadow Wolves)
# 3. Close quest log (Esc), Explore
# 4. Defeat Shadow Wolf enemy
#    - Combat should complete normally
# 5. Open Quest Log again (Q)
#    - Verify quest progress updated (1/3 Shadow Wolves)
# 6. Defeat 2 more Shadow Wolves
# 7. After third wolf defeated:
#    - Quest Completion Dialog should appear
#    - Shows rewards (100 XP, 50 Gold)
#    - Click Continue
# 8. Check player stats:
#    - Gold increased by 50
#    - Experience increased by 100
# 9. Open Quest Log:
#    - Quest moved to "Completed" section
#    - New quest available
# 10. Save game (slot 1)
# 11. Exit and reload save
#     - Open Quest Log
#     - Verify quest state preserved (completed quest still shows)

# Expected: All manual tests pass, no crashes, quest state persists
```

### Level 4: Save/Load Compatibility Testing

```bash
# Test backward compatibility
# 1. Create a save file with current version (before quest implementation)
# 2. Add quest system code
# 3. Load old save
# Expected: Loads successfully, quest list is empty but game works

# Test forward compatibility
# 1. Create save with quest data
# 2. Verify file format version check rejects future versions
# Expected: Appropriate error message if loading newer format

# Test corrupted save handling
# 1. Manually corrupt a save file
# 2. Attempt to load
# Expected: Graceful error, no crash, returns to main menu
```

## Final Validation Checklist

### Technical Validation

- [ ] All files compile without warnings: `make` succeeds with 0 warnings
- [ ] Unit tests pass: `./test_quest_models` and `./test_quest_system` pass all tests
- [ ] Integration tests pass: `ctest` shows 0 failures
- [ ] No memory leaks: Quest pointers properly cleaned up in Player destructor
- [ ] No segfaults: All null pointer checks in place

### Feature Validation

- [ ] Quest Log opens with Q key
- [ ] Quest list displays active, available, and completed quests in sections
- [ ] Clicking quest shows full details (description, objectives, rewards)
- [ ] Kill quest auto-updates when matching enemy defeated
- [ ] Quest completion dialog appears when all objectives complete
- [ ] Rewards correctly added to player (gold, experience, items)
- [ ] Quest state persists through save/load cycles
- [ ] Old saves (pre-quest) load without errors (empty quest list)
- [ ] Keyboard shortcuts work (Q, Esc, 1-9, A for accept)

### Code Quality Validation

- [ ] Follows existing codebase patterns (verified against pattern files)
- [ ] All Theme constants used (no hardcoded colors/sizes)
- [ ] Signal/slot connections follow naming conventions
- [ ] QDataStream serialization follows versioning pattern
- [ ] Memory management follows Qt ownership patterns
- [ ] CMakeLists.txt updated correctly (files in main + tests)

### Documentation Validation

- [ ] Quest data structures documented with comments
- [ ] QuestManager public API documented
- [ ] Quest factory quest definitions have clear comments
- [ ] Complex algorithms (quest matching) have explanatory comments

## Anti-Patterns to Avoid

- ❌ Don't use C++ enums for quest types/status - use QString (easier serialization)
- ❌ Don't serialize QList<Quest*> directly - convert to QList<Quest> first
- ❌ Don't forget qDeleteAll(quests) in Player destructor - causes memory leaks
- ❌ Don't hardcode colors/fonts - always use Theme::CONSTANT
- ❌ Don't call setCurrentWidget() before updateQuests() - shows stale data
- ❌ Don't add files to main executable without adding to test executables
- ❌ Don't connect QuestManager signals before QuestManager exists - will crash
- ❌ Don't forget to set QDataStream version - causes serialization bugs
- ❌ Don't skip version increment when adding new serialized fields
- ❌ Don't emit signals in tight loops - batch updates if possible
- ❌ Don't assume quests will be in Player from old saves - check version
- ❌ Don't update quest progress without checking if objective already completed
- ❌ Don't give rewards multiple times - check quest status before completing

---

## Confidence Score: 9/10

**Rationale**: This PRP has comprehensive context from actual codebase analysis:
- ✅ Exact file patterns extracted from existing models (Player, Item, Skill)
- ✅ Complete UI patterns from InventoryPage, CombatResultDialog
- ✅ Full save/load strategy from SaveManager with versioning
- ✅ Signal/slot patterns from MainWindow integration
- ✅ Theme constants and styling patterns documented
- ✅ CMake build pattern for adding files
- ✅ Testing patterns from existing test suite
- ✅ Memory management patterns (qDeleteAll usage)
- ✅ Specific line references for all critical patterns

**Deduction (-1)**: Minor uncertainty around exact combat event integration point (endCombat vs after playerAttack) - requires reading full combat flow, but both approaches work.

**Validation**: An AI agent can implement this successfully with only:
1. This PRP
2. Access to codebase files (for verification)
3. Training data for Qt6/C++ knowledge

All patterns, gotchas, naming conventions, and integration points are explicitly documented with file:line references.
