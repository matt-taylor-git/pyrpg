name: "Storyline & Quest System - Phase 4: Final Boss, Victory & Endgame"
description: |
  Implementation PRP for final boss mechanics with multi-phase combat, victory screen,
  game completion tracking, and endgame content for PyRPG Qt. Covers Phase 4 (Final Boss
  & Win Condition) from storyline-quest-system-prd.md.

---

## Goal

**Feature Goal**: Implement a climactic final boss encounter with multi-phase combat mechanics, victory condition tracking, victory screen with end-game statistics, and game completion state persistence.

**Deliverable**:
- FinalBoss class extending Monster with 3-phase combat system
- Phase transition mechanics at 75%, 50%, 25% HP thresholds
- Level gate system requiring level 20+ and all story quests complete
- VictoryScreen UI displaying player statistics and achievements
- Game completion tracking with persistent "gameCompleted" flag
- Point of No Return warning dialog before final boss encounter
- Victory cutscene integration with StoryManager
- Post-game content accessibility (continue playing after victory)

**Success Definition**:
- Final boss only accessible when player level >= 20 AND all main quests completed
- Boss combat transitions through 3 distinct phases with unique attack patterns
- Victory screen displays after boss defeat with: playtime, final level, kills, deaths, gold earned
- Game completion flag persists through save/load cycles
- Player can continue playing post-victory (optional New Game+ foundation)
- All unit tests pass for FinalBoss combat and victory state
- Manual testing confirms dramatic boss encounter experience

## User Persona

**Target User**: RPG player seeking a challenging climax and sense of achievement

**Use Case**:
- Player completes all story quests and reaches level 20
- Player initiates final quest → receives warning about point of no return
- Player confirms → epic boss battle begins with narrative buildup
- Player defeats boss through 3 challenging phases
- Victory cutscene plays → Victory screen shows accomplishments
- Player reviews statistics, feels satisfied, can continue exploring world

**User Journey**:
1. Player completes final pre-boss quest → unlocks final quest
2. Attempts to start final quest at level 18 → blocked with "Level 20 required" message
3. Grinds to level 20, acquires legendary equipment
4. Starts final quest → "Point of No Return" warning appears
5. Confirms → cutscene plays introducing final boss
6. Combat begins → boss at 100% HP (Phase 1: standard attacks)
7. Boss HP drops to 75% → transformation animation → Phase 2 begins (new attacks)
8. Boss HP drops to 50% → second transformation → Phase 3 (ultimate attacks)
9. Boss HP drops to 25% → desperate final phase with maximum difficulty
10. Player defeats boss → victory cutscene triggers
11. VictoryScreen displays: "YOU WIN! Level 22 | Playtime: 3h 45m | Enemies Defeated: 127"
12. Player clicks Continue → returns to world as champion, can keep playing

**Pain Points Addressed**:
- No clear win condition (solved by final boss victory requirement)
- Endless grinding without closure (solved by definitive ending)
- Anticlimactic difficulty spike (solved by multi-phase progressive challenge)
- Lost progress on defeat (solved by retry mechanism without losing quest state)
- No sense of achievement (solved by statistics display and persistent completion flag)

## Why

- **Narrative Closure**: Transforms open-ended grinding into story with beginning, middle, and satisfying end
- **Player Accomplishment**: Victory screen provides tangible proof of achievement
- **Replayability Foundation**: Completion flag enables New Game+ features in future
- **Difficulty Mastery**: Multi-phase boss teaches all combat mechanics through escalating challenge
- **Industry Standard**: All successful RPGs have climactic final boss encounters

This solves the PRD's core goal: "Players need a win condition and sense of accomplishment to feel the game has meaningful progression and closure."

## What

### Core Functionality

**FinalBoss Class**:
- Extends Monster with phase-tracking system
- Three combat phases triggered at 75%, 50%, 25% HP thresholds
- Phase-specific attack patterns and damage multipliers
- Phase transition events with visual/audio feedback
- No escape allowed (run button disabled during boss fight)

**Phase Combat Mechanics**:
- Phase 1 (100-76% HP): Standard attacks, teaches basic boss patterns
- Phase 2 (75-51% HP): +25% attack damage, new attack pattern introduced
- Phase 3 (50-26% HP): +50% attack damage, special abilities every 3 turns
- Phase 4 (25-0% HP): +75% attack damage, desperate final attacks every 2 turns

**Victory Screen**:
- Full-screen QDialog modal display
- Statistics display: Final level, playtime, total enemies defeated, total deaths, gold earned, quests completed
- Victory message with celebratory styling
- Continue button (returns to world as champion)
- Return to Main Menu button
- Keyboard shortcuts: Space/Enter = Continue, Esc = Main Menu

**Game Completion Tracking**:
- Player.hasDefeatedFinalBoss flag
- Player.gameCompletionTime timestamp
- Player.finalGameLevel captured at victory
- SaveManager serialization updated (version 4)
- Completion badge in save slot display

**Level Gate System**:
- Final quest checks: player->level >= 20 AND all main quests completed
- Warning dialog if requirements not met
- "Point of No Return" confirmation before boss encounter begins

**Victory Cutscene Integration**:
- StoryManager triggers "final_boss_defeated" event
- Narrative sequence plays before VictoryScreen
- Seamless transition from combat → cutscene → statistics

### Success Criteria

- [ ] FinalBoss class created extending Monster with currentPhase field
- [ ] Phase transitions trigger automatically at 75%, 50%, 25% HP
- [ ] Phase-specific attack damage applies correctly (+25%, +50%, +75%)
- [ ] Level gate prevents access if player level < 20
- [ ] Quest gate prevents access if any main quest incomplete
- [ ] Point of No Return dialog appears before boss fight
- [ ] Boss combat disables run/escape button
- [ ] Victory condition detected when boss HP <= 0
- [ ] Victory cutscene plays automatically after boss defeat
- [ ] VictoryScreen displays all statistics correctly
- [ ] Game completion flag persists through save/load
- [ ] Save slot shows "COMPLETED" badge for finished games
- [ ] Player can continue playing post-victory
- [ ] Unit tests: FinalBoss phase logic verified
- [ ] Integration tests: Full boss fight flow tested
- [ ] Manual testing: Boss encounter feels epic and challenging

## All Needed Context

### Context Completeness Check

✓ **Monster extension pattern**: Complete analysis of Monster class structure and combat integration
✓ **Dialog patterns**: Comprehensive QDialog vs custom overlay comparison from CombatResultDialog, MenuOverlay, StoryEventDialog
✓ **Combat flow**: Full Game.cpp combat system analysis with integration points identified
✓ **View patterns**: Complete VictoryScreen template from StatsPage and SaveLoadPage patterns
✓ **Phase mechanics**: Research-backed multi-phase boss design patterns from industry best practices
✓ **Save/load integration**: Player serialization patterns with versioning strategy
✓ **Signal/slot architecture**: Game completion signal flow documented

**Validation**: An AI agent unfamiliar with this codebase has everything needed - Monster extension strategy, exact integration points in Game.cpp, complete VictoryScreen template, phase transition algorithms, and save format updates.

### Documentation & References

```yaml
# PRD Architecture Reference
- file: PRPs/storyline-quest-system-prd.md
  why: Complete Phase 4 requirements, final boss specifications, victory screen specs
  section: "Phase 4: Final Boss & Win Condition (lines 961-1016), Final Boss System (lines 675-695)"
  critical: Boss phase mechanics, level gate requirements, victory screen layout

# Monster Class Pattern (BASE FOR FINALBOSS)
- file: cpp-qt-rpg/src/models/Monster.h
  why: Base class to extend for FinalBoss
  pattern: Simple inheritance from Character, no serialization (ephemeral combat entity)
  gotcha: Monster is NOT serialized - only exists during combat, deleted after

- file: cpp-qt-rpg/src/models/Monster.cpp
  why: Constructor pattern for stat initialization
  pattern: Health = 50 + (level * 15), Attack = 8 + (level * 2)
  critical: Use formula-based stat generation, not hardcoded values

- file: cpp-qt-rpg/src/models/Character.h
  why: Understand base class fields (health, maxHealth, level, name)
  pattern: Protected members inherited by Monster and Player
  usage: FinalBoss will inherit these same fields

# Combat System Integration (CRITICAL)
- file: cpp-qt-rpg/src/game/Game.cpp
  why: Combat flow and boss integration points identified
  pattern: Lines 215-224 startCombat(), 355-365 endCombat(), 403-448 giveCombatRewards()
  critical: Integration points at lines 222 (boss encounter detection), 363 (victory detection), 437 (boss rewards)
  gotcha: currentMonster->enemyType == "boss" is the detection pattern

- file: cpp-qt-rpg/src/game/Game.h
  why: Signal declarations for combat and victory
  pattern: emit combatEnded(bool playerWon) at line 48
  add_signals: void bossEncountered(QString), void finalBossDefeated(), void gameCompleted(int, int)

# Monster Factory Pattern
- file: cpp-qt-rpg/src/game/factories/MonsterFactory.cpp
  why: Boss creation pattern already exists
  pattern: createBoss() at lines 121-133 creates "Orc Chieftain" with enemyType="boss"
  extend: Add createFinalBoss() method for endgame boss with enhanced stats

# Victory Screen Patterns (FROM RESEARCH)
- file: cpp-qt-rpg/src/views/StatsPage.h
  why: Information display pattern for VictoryScreen
  pattern: QWidget base, card-based layout, key-value pairs for statistics

- file: cpp-qt-rpg/src/views/StatsPage.cpp
  why: Implementation of statistics display with Theme constants
  pattern: Lines 21-150 show createStatCard() helper methods, Theme::CARD styling
  critical: Use Theme::PRIMARY for victory highlights, Theme::CARD for containers

- file: cpp-qt-rpg/src/components/CombatResultDialog.h
  why: Modal dialog pattern for VictoryScreen
  pattern: QDialog base, exec() for modal blocking, accept() to close
  usage: VictoryScreen should inherit QDialog for full-screen modal experience

- file: cpp-qt-rpg/src/components/StoryEventDialog.h
  why: Full-screen overlay pattern with dramatic presentation
  pattern: QDialog with custom styling, large text display, continue button
  usage: Victory screen should feel similarly dramatic

# MainWindow Integration
- file: cpp-qt-rpg/src/MainWindow.h
  why: View registration and signal connection pattern
  pattern: Lines 21-84 show view members, signal handlers, keyPressEvent
  add: VictoryScreen* m_victoryScreen member, handleGameCompleted() slot

- file: cpp-qt-rpg/src/MainWindow.cpp
  why: View lifecycle and navigation
  pattern: Lines 35-94 show view creation, signal connection, stacking
  critical: Connect Game::gameCompleted signal to show victory screen

# Player Serialization (VERSION UPDATE REQUIRED)
- file: cpp-qt-rpg/src/models/Player.h
  why: Add game completion fields
  add: bool hasDefeatedFinalBoss, QString gameCompletionTime, int finalGameLevel
  placement: After viewedEventIds (line 32), before quests

- file: cpp-qt-rpg/src/models/Player.cpp
  why: Serialization operator updates for version 4
  pattern: Lines 62-161 show versioned save/load
  critical: Increment to version 4, add completion fields after version 3 data
  gotcha: MUST preserve backward compatibility with version 3 saves

# Save System Integration
- file: cpp-qt-rpg/src/persistence/SaveManager.cpp
  why: Save slot metadata display
  pattern: Lines 85-140 getSaveSlots() returns slot info
  enhance: Add "COMPLETED" badge to SaveSlotInfo for finished games

# Quest System Integration
- file: cpp-qt-rpg/src/game/QuestManager.h
  why: Check if all main quests complete (level gate requirement)
  pattern: getCompletedQuests() method returns completed quest list
  usage: Count completed main quests, require all for final boss access

# Story Event Integration
- file: cpp-qt-rpg/src/game/StoryManager.h
  why: Trigger victory cutscene
  pattern: triggerEvent(eventId) method
  usage: Call triggerEvent("final_boss_defeated") before VictoryScreen

# Theme Constants
- file: cpp-qt-rpg/src/theme/Theme.h
  why: All color, spacing, font constants for VictoryScreen
  pattern: Theme::CARD, Theme::PRIMARY, Theme::SPACING_LG, Theme::FONT_SIZE_XL
  critical: Use Theme::PRIMARY (#dc3545 crimson) for victory highlights

# CMake Build Configuration
- file: cpp-qt-rpg/CMakeLists.txt
  why: How to add new source files
  pattern: Lines 23-64 main executable, lines 75-210 test targets
  critical: Add FinalBoss.cpp, VictoryScreen.cpp to BOTH main and test targets
```

### Current Codebase Tree

```bash
cpp-qt-rpg/
├── src/
│   ├── models/
│   │   ├── Monster.h/.cpp          # Base class for FinalBoss
│   │   ├── Player.h/.cpp           # Add completion tracking fields
│   │   ├── Quest.h/.cpp            # Quest completion checking
│   │   └── [other models]
│   ├── game/
│   │   ├── Game.h/.cpp             # Combat flow with boss integration points
│   │   ├── QuestManager.h/.cpp     # Quest completion verification
│   │   ├── StoryManager.h/.cpp     # Victory cutscene triggering
│   │   └── factories/
│   │       └── MonsterFactory.h/.cpp  # Boss creation patterns
│   ├── views/
│   │   ├── StatsPage.h/.cpp        # Statistics display pattern
│   │   ├── StoryEventDialog.h/.cpp # Full-screen dialog pattern
│   │   └── [other views]
│   ├── components/
│   │   ├── CombatResultDialog.h/.cpp  # Modal dialog pattern
│   │   └── [other components]
│   ├── persistence/
│   │   └── SaveManager.h/.cpp      # Save slot management
│   └── theme/
│       └── Theme.h                  # Styling constants
└── tests/
    ├── test_models.cpp
    ├── test_combat_page_dual_mode.cpp
    └── [other tests]
```

### Desired Codebase Tree (Files to Add)

```bash
cpp-qt-rpg/src/
├── models/
│   └── FinalBoss.h/.cpp           # Multi-phase boss class
├── views/
│   └── VictoryScreen.h/.cpp       # End-game statistics screen
├── components/
│   └── PointOfNoReturnDialog.h/.cpp  # Warning before boss
└── tests/
    ├── test_final_boss.cpp         # Boss phase mechanics tests
    └── test_victory_screen.cpp     # Victory screen display tests
```

### Known Gotchas & Library Quirks

```cpp
// CRITICAL: Monster Lifecycle
// Monsters are EPHEMERAL - not serialized, only exist during combat
// FinalBoss follows same pattern: created at boss encounter, deleted after combat
Monster* currentMonster;  // Owned by Game, deleted in startCombat() and destructor

// CRITICAL: Boss Detection Pattern
// Game.cpp checks enemyType == "boss" to detect boss encounters
if (currentMonster->enemyType == "boss") {
    // Special boss handling here
}

// CRITICAL: Phase Transition Timing
// Check phase AFTER damage applied but BEFORE checkCombatEndAfterAction()
// Otherwise phase might transition on killing blow, missing final phase

// PATTERN: Phase Detection
int getPhase(int health, int maxHealth) {
    double hpPercent = (double)health / maxHealth * 100.0;
    if (hpPercent > 75.0) return 1;
    if (hpPercent > 50.0) return 2;
    if (hpPercent > 25.0) return 3;
    return 4;  // Desperate final phase
}

// GOTCHA: Phase Transition Event Emission
// Emit ONCE per phase change, not every turn
int m_previousPhase = 1;
int currentPhase = getPhase(health, maxHealth);
if (currentPhase != m_previousPhase) {
    emit phaseChanged(currentPhase);
    m_previousPhase = currentPhase;
}

// CRITICAL: Victory Screen as QDialog
// Use QDialog for modal full-screen blocking behavior
VictoryScreen *victory = new VictoryScreen(stats, this);
victory->exec();  // Blocks until user clicks Continue or Main Menu

// GOTCHA: Player Serialization Versioning
// MUST increment version to 4 and preserve backward compatibility
out << quint32(4);  // Version 4: Added game completion fields

// In operator>> (load):
if (version >= 4) {
    in >> p.hasDefeatedFinalBoss >> p.gameCompletionTime >> p.finalGameLevel;
} else {
    p.hasDefeatedFinalBoss = false;  // Default for old saves
}

// CRITICAL: Quest Completion Check
// Final boss requires ALL main quests complete (orderIndex matters)
QList<Quest*> mainQuests = getMainQuests();  // From QuestManager
for (Quest *quest : mainQuests) {
    if (!quest->isComplete()) {
        return false;  // Block boss access
    }
}

// GOTCHA: Signal Connection Timing
// Connect Game::gameCompleted AFTER Game object created (in newGame/loadGame)
connect(m_game, &Game::gameCompleted, this, &MainWindow::handleGameCompleted, Qt::UniqueConnection);

// CRITICAL: Boss Stats Scaling
// Final boss should be significantly harder than normal boss
FinalBoss stats (level 22):
- Health: 500 + (level * 50) = 1600 HP
- Attack: 30 + (level * 5) = 140 base attack
- Defense: 20 + (level * 4) = 108 defense
- Phase multipliers stack on base attack

// GOTCHA: Theme Constants for Victory
// Use PRIMARY color for victory highlights (crimson #dc3545)
victoryLabel->setStyleSheet(QString(
    "color: %1; font-size: %2px;"
).arg(Theme::PRIMARY.name()).arg(Theme::FONT_SIZE_XXL));

// CRITICAL: Continue Playing Post-Victory
// Don't delete boss or lock game state - just return to world
player->hasDefeatedFinalBoss = true;  // Mark complete
// Player can still explore, fight monsters, complete side content

// GOTCHA: CMakeLists.txt Updates
// FinalBoss.cpp must be added to:
// 1. Main executable (pyrpg-qt)
// 2. test_mainwindow (integration tests)
// 3. test_combat_page_dual_mode (combat tests)
// 4. test_final_boss (new unit test)
```

## Implementation Blueprint

### Data Models and Structure

**FinalBoss Class** (extends Monster):
- Inherits all Character/Monster fields (health, attack, defense, level)
- Adds phase tracking: int currentPhase (1-4)
- Adds phase transition flag: int m_previousPhase
- No serialization needed (ephemeral combat entity)
- Phase-aware attack calculation method

**Player Completion Fields** (add to Player.h):
- bool hasDefeatedFinalBoss = false
- QString gameCompletionTime = "" (ISO 8601 format)
- int finalGameLevel = 0
- Serialized in version 4 format

**VictoryStatistics Structure** (embedded in VictoryScreen):
```cpp
struct VictoryStats {
    int finalLevel;
    QString playtime;  // Formatted: "3h 45m"
    int enemiesDefeated;
    int totalDeaths;
    int goldEarned;
    int questsCompleted;
};
```

### Implementation Tasks (Ordered by Dependencies)

```yaml
Task 1: CREATE src/models/FinalBoss.h
  IMPLEMENT: FinalBoss class extending Monster
  FOLLOW pattern: src/models/Monster.h (lines 1-33)
  NAMING: FinalBoss class (PascalCase), currentPhase/m_previousPhase (camelCase)
  FIELDS:
    - int currentPhase (1-4, tracks current combat phase)
    - int m_previousPhase (for transition detection)
  METHODS:
    - explicit FinalBoss(int playerLevel);
    - int getCurrentPhase() const;
    - void updatePhase();  // Recalculate phase based on HP
    - int getPhaseAttackMultiplier() const;  // Returns 100, 125, 150, 175 (percent)
    - bool shouldEmitPhaseTransition();  // Checks if phase changed
    - QString getPhaseDescription() const;  // For UI display
  PLACEMENT: cpp-qt-rpg/src/models/FinalBoss.h
  DEPENDENCIES: Monster.h (existing)

Task 2: CREATE src/models/FinalBoss.cpp
  IMPLEMENT: Constructor and phase mechanics
  FOLLOW pattern: src/models/Monster.cpp constructor (lines 3-18)
  CONSTRUCTOR:
    - Call Monster constructor with name="The Eternal Shadow", enemyType="final_boss"
    - Calculate enhanced stats:
      - health = 500 + (playerLevel * 50)
      - attack = 30 + (playerLevel * 5)
      - defense = 20 + (playerLevel * 4)
      - expReward = playerLevel * 500
      - goldReward = playerLevel * 200
    - Initialize currentPhase = 1, m_previousPhase = 1
  METHODS:
    - getCurrentPhase(): return (health * 100 / maxHealth) > 75 ? 1 : > 50 ? 2 : > 25 ? 3 : 4
    - updatePhase(): currentPhase = getCurrentPhase()
    - getPhaseAttackMultiplier(): return currentPhase == 1 ? 100 : == 2 ? 125 : == 3 ? 150 : 175
    - shouldEmitPhaseTransition(): bool changed = (currentPhase != m_previousPhase); m_previousPhase = currentPhase; return changed;
    - getPhaseDescription(): switch on phase, return flavor text
  PLACEMENT: cpp-qt-rpg/src/models/FinalBoss.cpp
  DEPENDENCIES: FinalBoss.h (Task 1)

Task 3: UPDATE src/models/Player.h
  ADD: Game completion tracking fields
  FOLLOW pattern: Existing field declarations (lines 16-33)
  ADDITIONS:
    - bool hasDefeatedFinalBoss = false; (after viewedEventIds, line 32)
    - QString gameCompletionTime = ""; (ISO 8601 format)
    - int finalGameLevel = 0;
  PLACEMENT: After narrative tracking fields (line 32), before quests section
  DEPENDENCIES: None

Task 4: UPDATE src/models/Player.cpp
  MODIFY: Serialization operators for version 4
  FOLLOW pattern: Version 3 serialization (lines 62-161)
  CHANGES:
    1. Line 62: Increment version to 4
       out << quint32(4);  // Version 4: Added game completion tracking
    2. After quest serialization (around line 95), add completion fields:
       out << p.hasDefeatedFinalBoss << p.gameCompletionTime << p.finalGameLevel;
    3. In operator>> after quest deserialization (around line 155):
       if (version >= 4) {
           in >> p.hasDefeatedFinalBoss >> p.gameCompletionTime >> p.finalGameLevel;
       } else {
           p.hasDefeatedFinalBoss = false;
           p.gameCompletionTime = "";
           p.finalGameLevel = 0;
       }
  CRITICAL: Preserve backward compatibility - old saves load with default false values
  DEPENDENCIES: Player.h updated (Task 3)

Task 5: UPDATE src/game/factories/MonsterFactory.h
  ADD: Final boss creation method declaration
  FOLLOW pattern: createBoss() declaration (line 14)
  ADDITIONS:
    - #include "../models/FinalBoss.h" at top
    - static FinalBoss* createFinalBoss(int playerLevel);
  PLACEMENT: After createBoss() method (line 14)
  DEPENDENCIES: FinalBoss.h (Task 1)

Task 6: UPDATE src/game/factories/MonsterFactory.cpp
  IMPLEMENT: createFinalBoss() method
  FOLLOW pattern: createBoss() implementation (lines 121-133)
  IMPLEMENTATION:
    FinalBoss* MonsterFactory::createFinalBoss(int playerLevel) {
        return new FinalBoss(playerLevel);
    }
  PLACEMENT: After createBoss() method (around line 133)
  DEPENDENCIES: MonsterFactory.h updated (Task 5), FinalBoss.cpp (Task 2)

Task 7: UPDATE src/game/Game.h
  ADD: Boss encounter and victory signals
  FOLLOW pattern: Existing signal declarations (line 48)
  ADDITIONS:
    - void bossEncountered(const QString &bossName);
    - void bossPhaseChanged(int newPhase);
    - void finalBossDefeated();
    - void gameCompleted(int finalLevel, int playtimeMinutes);
  METHODS:
    - void startFinalBossCombat();  // Special boss initialization
    - bool canAccessFinalBoss() const;  // Level and quest gate check
    - int calculatePlaytimeMinutes() const;  // For statistics
  MEMBERS:
    - QTime m_gameStartTime;  // Track playtime from newGame()
  PLACEMENT: Signals after combatEnded (line 48), methods in public section
  DEPENDENCIES: None

Task 8: UPDATE src/game/Game.cpp
  MODIFY: Combat flow for boss integration
  FOLLOW pattern: Existing combat methods (lines 215-461)
  CHANGES:
    1. Constructor: Initialize m_gameStartTime = QTime::currentTime()
    2. startFinalBossCombat() implementation (new method):
       - Delete currentMonster if exists
       - currentMonster = MonsterFactory::createFinalBoss(player->level)
       - combatActive = true
       - emit bossEncountered(currentMonster->name)
       - combatLog = "The final battle begins! {bossName} emerges!"
    3. playerAttack() modification (after line 245, before checkCombatEndAfterAction):
       if (FinalBoss* boss = dynamic_cast<FinalBoss*>(currentMonster)) {
           int oldPhase = boss->getCurrentPhase();
           boss->updatePhase();
           if (boss->shouldEmitPhaseTransition()) {
               emit bossPhaseChanged(boss->getCurrentPhase());
               combatLog += QString("\n%1 enters Phase %2! %3")
                   .arg(boss->name).arg(boss->getCurrentPhase()).arg(boss->getPhaseDescription());
           }
           // Apply phase attack multiplier
           int multiplier = boss->getPhaseAttackMultiplier();
           // Use multiplier in damage calculation
       }
    4. monsterAttack() modification (similar phase check and multiplier application)
    5. endCombat() modification (after line 363):
       if (currentMonster && currentMonster->enemyType == "final_boss" && playerWon) {
           player->hasDefeatedFinalBoss = true;
           player->gameCompletionTime = QDateTime::currentDateTime().toString(Qt::ISODate);
           player->finalGameLevel = player->level;
           emit finalBossDefeated();
           emit gameCompleted(player->level, calculatePlaytimeMinutes());
       }
    6. giveCombatRewards() modification (after line 437):
       if (currentMonster && currentMonster->enemyType == "final_boss") {
           // 2x XP multiplier
           expGained *= 2;
           // Guaranteed legendary item drop
           Item* legendary = ItemFactory::generateRandomItem(player->level + 5);
           legendary->rarity = "Legendary";
           player->inventory.append(legendary);
           // Trigger victory cutscene
           if (m_storyManager) {
               m_storyManager->triggerEvent("final_boss_defeated");
           }
       }
    7. canAccessFinalBoss() implementation:
       - Check player->level >= 20
       - Check all main quests complete via m_questManager
       - Return true only if both conditions met
    8. calculatePlaytimeMinutes():
       - QTime now = QTime::currentTime();
       - return m_gameStartTime.secsTo(now) / 60;
  CRITICAL: Use dynamic_cast<FinalBoss*> to safely check for boss type
  DEPENDENCIES: Game.h updated (Task 7), FinalBoss.cpp (Task 2)

Task 9: CREATE src/components/PointOfNoReturnDialog.h
  IMPLEMENT: Warning dialog before boss fight
  FOLLOW pattern: src/components/CombatResultDialog.h (lines 1-24)
  CLASS structure:
    - Inherit from QDialog
    - Q_OBJECT macro
    - explicit PointOfNoReturnDialog(QWidget *parent = nullptr);
  PRIVATE methods:
    - void setupUi();
  PLACEMENT: cpp-qt-rpg/src/components/PointOfNoReturnDialog.h
  DEPENDENCIES: None

Task 10: CREATE src/components/PointOfNoReturnDialog.cpp
  IMPLEMENT: Warning UI with accept/cancel
  FOLLOW pattern: src/components/CombatResultDialog.cpp (lines 1-110)
  STRUCTURE:
    - Constructor: Set title "Point of No Return", call setupUi()
    - setupUi():
      - VBoxLayout with warning icon/text
      - Large warning message: "You are about to face the final boss. This is a point of no return."
      - Requirements display: "Required: Level 20+ and all quests complete"
      - Preparation tips: "Ensure you have healing items and your best equipment."
      - Two buttons: "I'm Ready" (accept), "Not Yet" (reject)
      - Apply Theme::DANGER color to warning text
      - Apply Theme::PRIMARY to ready button
  PLACEMENT: cpp-qt-rpg/src/components/PointOfNoReturnDialog.cpp
  DEPENDENCIES: PointOfNoReturnDialog.h (Task 9), Theme.h

Task 11: CREATE src/views/VictoryScreen.h
  IMPLEMENT: End-game statistics display screen
  FOLLOW pattern: src/views/StatsPage.h (lines 1-40)
  CLASS structure:
    - Inherit from QDialog
    - Q_OBJECT macro
    - Constructor: explicit VictoryScreen(int finalLevel, int playtime, int kills, int deaths, int gold, int quests, QWidget *parent);
  SIGNALS:
    - void continuePlaying();
    - void returnToMainMenu();
  PRIVATE methods:
    - void setupUi();
    - QWidget* createVictoryHeader();
    - QWidget* createStatisticsCard(const QString &label, const QString &value);
    - QWidget* createActionButtons();
  MEMBERS:
    - QLabel* m_victoryTitle;
    - QLabel* m_victoryMessage;
    - QWidget* m_statsContainer;
    - QPushButton* m_continueButton;
    - QPushButton* m_menuButton;
    - int m_finalLevel, m_playtime, m_kills, m_deaths, m_gold, m_quests;
  PLACEMENT: cpp-qt-rpg/src/views/VictoryScreen.h
  DEPENDENCIES: None

Task 12: CREATE src/views/VictoryScreen.cpp
  IMPLEMENT: Victory screen UI with statistics
  FOLLOW pattern: src/views/StatsPage.cpp (lines 1-200)
  KEY implementations:
    1. Constructor: Store statistics, setModal(true), call setupUi()
    2. setupUi():
       - QVBoxLayout main layout
       - Add createVictoryHeader() at top
       - Add statistics section (2-column grid layout):
         - Final Level card
         - Playtime card (format minutes to "Xh Ym")
         - Enemies Defeated card
         - Times Died card
         - Gold Earned card
         - Quests Completed card
       - Add createActionButtons() at bottom
       - Apply celebratory styling with Theme::PRIMARY highlights
    3. createVictoryHeader():
       - Large "VICTORY!" title (Theme::FONT_SIZE_XXL)
       - Congratulatory message
       - Gold gradient background
       - Apply QGraphicsDropShadowEffect for glow
    4. createStatisticsCard(label, value):
       - Card container (Theme::CARD background)
       - Label in Theme::TEXT color
       - Value in Theme::PRIMARY color, larger font
       - Return QWidget* with styled content
    5. createActionButtons():
       - HBoxLayout with spacing
       - Continue button (green, connects to continuePlaying signal)
       - Main Menu button (gray, connects to returnToMainMenu signal)
       - Keyboard shortcuts: Space/Enter = continue, Esc = menu
    6. keyPressEvent() override:
       - Space/Enter: emit continuePlaying(), accept()
       - Esc: emit returnToMainMenu(), accept()
  STYLING: Use gold (#FFD700) accents, celebratory colors, large fonts
  PLACEMENT: cpp-qt-rpg/src/views/VictoryScreen.cpp
  DEPENDENCIES: VictoryScreen.h (Task 11), Theme.h

Task 13: UPDATE src/MainWindow.h
  ADD: Victory screen member and handlers
  FOLLOW pattern: Existing view members (lines 71-82)
  ADDITIONS:
    - #include "views/VictoryScreen.h" at top
    - VictoryScreen* m_victoryScreen; (private member, set to nullptr initially)
    - void handleFinalBossRequest(); (private slot)
    - void handleBossEncountered(const QString &bossName); (private slot)
    - void handleBossPhaseChanged(int newPhase); (private slot)
    - void handleFinalBossDefeated(); (private slot)
    - void handleGameCompleted(int finalLevel, int playtime); (private slot)
    - void handleVictoryContinue(); (private slot)
    - void handleVictoryMainMenu(); (private slot)
  PLACEMENT: Add members with other view pointers, add slots with other handlers
  DEPENDENCIES: VictoryScreen.h (Task 11)

Task 14: UPDATE src/MainWindow.cpp
  MODIFY: Integrate victory screen and boss encounter
  FOLLOW pattern: View integration patterns (lines 35-94, 215-378)
  CHANGES:
    1. Constructor: Initialize m_victoryScreen = nullptr (lazy creation)
    2. In newGame() and loadGame() after Game created:
       - connect(m_game, &Game::bossEncountered, this, &MainWindow::handleBossEncountered);
       - connect(m_game, &Game::bossPhaseChanged, this, &MainWindow::handleBossPhaseChanged);
       - connect(m_game, &Game::finalBossDefeated, this, &MainWindow::handleFinalBossDefeated);
       - connect(m_game, &Game::gameCompleted, this, &MainWindow::handleGameCompleted);
    3. handleFinalBossRequest() implementation:
       - Check m_game->canAccessFinalBoss()
       - If false: show error dialog "Level 20+ and all quests required"
       - If true: Show PointOfNoReturnDialog
       - If accepted: m_game->startFinalBossCombat(), switch to combat page
    4. handleBossEncountered(bossName):
       - Disable run button in CombatPage
       - Show dramatic message in combat log
       - Optional: Change combat music/theme
    5. handleBossPhaseChanged(newPhase):
       - Show phase transition message in CombatPage
       - Update UI with phase indicator
       - Optional: Play phase transition animation
    6. handleFinalBossDefeated():
       - Trigger victory cutscene via StoryManager
       - (VictoryScreen shown in handleGameCompleted instead)
    7. handleGameCompleted(finalLevel, playtime):
       - Collect statistics: kills from codex, deaths from player, gold, quests
       - if (!m_victoryScreen) {
           m_victoryScreen = new VictoryScreen(finalLevel, playtime, kills, deaths, gold, quests, this);
           connect(m_victoryScreen, &VictoryScreen::continuePlaying, this, &MainWindow::handleVictoryContinue);
           connect(m_victoryScreen, &VictoryScreen::returnToMainMenu, this, &MainWindow::handleVictoryMainMenu);
       }
       - m_victoryScreen->exec();  // Modal display
    8. handleVictoryContinue():
       - Return to combat page or adventure page
       - Player can continue playing as champion
    9. handleVictoryMainMenu():
       - stackedWidget->setCurrentWidget(m_mainMenu)
       - Show main menu with "Continue" option highlighted
  CRITICAL: Connect signals AFTER Game created, use Qt::UniqueConnection
  DEPENDENCIES: MainWindow.h updated (Task 13), VictoryScreen.cpp (Task 12), PointOfNoReturnDialog.cpp (Task 10)

Task 15: UPDATE src/persistence/SaveManager.h
  ADD: Completion badge to SaveSlotInfo
  FOLLOW pattern: SaveSlotInfo structure (lines 11-18)
  ADDITIONS:
    - bool isCompleted = false; (indicates game beaten)
  PLACEMENT: After timestamp field (line 17)
  DEPENDENCIES: None

Task 16: UPDATE src/persistence/SaveManager.cpp
  MODIFY: Include completion status in save slot metadata
  FOLLOW pattern: getSaveSlots() implementation (lines 85-140)
  CHANGES:
    - In getSaveSlots() loop (around line 110):
      - After loading save file, check if player->hasDefeatedFinalBoss
      - slotInfo.isCompleted = player->hasDefeatedFinalBoss;
  USAGE: SaveLoadPage can display "COMPLETED" badge on finished saves
  DEPENDENCIES: Player.cpp updated (Task 4)

Task 17: UPDATE src/views/SaveLoadPage.cpp
  MODIFY: Display completion badge on save slots
  FOLLOW pattern: Save slot display (lines 50-120)
  CHANGES:
    - In slot rendering loop:
      - if (slotInfo.isCompleted) {
          // Add gold "COMPLETED" badge to slot display
          QLabel *badge = new QLabel("⭐ COMPLETED");
          badge->setStyleSheet(QString("color: %1; font-weight: bold;").arg(Theme::PRIMARY.name()));
          slotLayout->addWidget(badge);
        }
  STYLING: Use gold star and Theme::PRIMARY color
  DEPENDENCIES: SaveManager.cpp updated (Task 16)

Task 18: UPDATE cpp-qt-rpg/CMakeLists.txt
  ADD: All new source files to build targets
  FOLLOW pattern: Existing file lists (lines 23-64 for main, 75-210 for tests)
  CHANGES:
    1. Main executable (add to add_executable(pyrpg-qt ...)):
       - src/models/FinalBoss.cpp
       - src/views/VictoryScreen.cpp
       - src/components/PointOfNoReturnDialog.cpp
    2. Test executables - Add to relevant tests:
       - test_mainwindow: FinalBoss.cpp, VictoryScreen.cpp, PointOfNoReturnDialog.cpp
       - test_models: FinalBoss.cpp
       - test_combat_page_dual_mode: FinalBoss.cpp
  CRITICAL: Alphabetical order within sections for maintainability
  DEPENDENCIES: All previous tasks completed

Task 19: CREATE tests/test_final_boss.cpp
  IMPLEMENT: Unit tests for FinalBoss phase mechanics
  FOLLOW pattern: tests/test_models.cpp (lines 1-120)
  TEST cases:
    - testFinalBossCreation(): Verify stats are enhanced (500+ HP, 30+ base attack)
    - testPhaseTransitions(): Damage boss to 75%, 50%, 25%, verify phase changes
    - testPhaseAttackMultipliers(): Verify 100%, 125%, 150%, 175% scaling
    - testPhaseTransitionDetection(): Verify shouldEmitPhaseTransition() triggers once per phase
    - testPhaseDescriptions(): Verify flavor text changes per phase
    - testBossDefeat(): Full combat simulation, verify victory triggers
  STRUCTURE:
    - #include <QtTest/QtTest>
    - #include "models/FinalBoss.h"
    - class TestFinalBoss : public QObject { Q_OBJECT private slots: ... };
    - QTEST_MAIN(TestFinalBoss)
    - #include "test_final_boss.moc"
  PLACEMENT: cpp-qt-rpg/tests/test_final_boss.cpp
  DEPENDENCIES: FinalBoss.cpp (Task 2)

Task 20: CREATE tests/test_victory_screen.cpp
  IMPLEMENT: Unit tests for VictoryScreen display
  FOLLOW pattern: tests/test_mainwindow.cpp (lines 1-100)
  TEST cases:
    - testVictoryScreenCreation(): Verify construction with statistics
    - testStatisticsDisplay(): Verify all 6 statistics render correctly
    - testContinueButton(): Simulate click, verify continuePlaying signal
    - testMainMenuButton(): Simulate click, verify returnToMainMenu signal
    - testKeyboardShortcuts(): Verify Space/Enter = continue, Esc = menu
  STRUCTURE: Same as test_final_boss.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_victory_screen.cpp
  DEPENDENCIES: VictoryScreen.cpp (Task 12)

Task 21: UPDATE cpp-qt-rpg/CMakeLists.txt (test targets)
  ADD: New test executables
  FOLLOW pattern: Existing test targets (lines 108-210)
  CHANGES:
    1. Add test_final_boss executable:
       add_executable(test_final_boss tests/test_final_boss.cpp
           src/models/FinalBoss.cpp
           src/models/Monster.cpp
           src/models/Character.cpp
       )
       target_link_libraries(test_final_boss PRIVATE Qt6::Widgets Qt6::Test)
       target_include_directories(test_final_boss PRIVATE src)
       add_test(NAME FinalBossTest COMMAND test_final_boss)

    2. Add test_victory_screen executable:
       add_executable(test_victory_screen tests/test_victory_screen.cpp
           src/views/VictoryScreen.cpp
       )
       target_link_libraries(test_victory_screen PRIVATE Qt6::Widgets Qt6::Test)
       target_include_directories(test_victory_screen PRIVATE src)
       add_test(NAME VictoryScreenTest COMMAND test_victory_screen)
  PLACEMENT: After existing test targets (around line 210)
  DEPENDENCIES: Test files created (Tasks 19, 20)
```

### Implementation Patterns & Key Details

```cpp
// ============================================================================
// PATTERN 1: FinalBoss Phase Mechanics
// ============================================================================
// File: src/models/FinalBoss.cpp
// Research-backed pattern: 3-4 phase progression at 75%, 50%, 25% HP

class FinalBoss : public Monster
{
public:
    FinalBoss(int playerLevel)
        : Monster("The Eternal Shadow", playerLevel + 2, "final_boss")
        , currentPhase(1)
        , m_previousPhase(1)
    {
        // Enhanced stats (significantly harder than normal boss)
        health = 500 + (playerLevel * 50);  // ~1600 HP at level 22
        maxHealth = health;
        attack = 30 + (playerLevel * 5);     // ~140 base attack
        defense = 20 + (playerLevel * 4);    // ~108 defense
        expReward = playerLevel * 500;       // 11,000 XP
        goldReward = playerLevel * 200;      // 4,400 gold
    }

    int getCurrentPhase() const {
        double hpPercent = ((double)health / maxHealth) * 100.0;
        if (hpPercent > 75.0) return 1;
        if (hpPercent > 50.0) return 2;
        if (hpPercent > 25.0) return 3;
        return 4;  // Desperate final phase
    }

    void updatePhase() {
        currentPhase = getCurrentPhase();
    }

    int getPhaseAttackMultiplier() const {
        switch(currentPhase) {
            case 1: return 100;  // Base damage
            case 2: return 125;  // +25%
            case 3: return 150;  // +50%
            case 4: return 175;  // +75% - desperate final attacks
            default: return 100;
        }
    }

    bool shouldEmitPhaseTransition() {
        if (currentPhase != m_previousPhase) {
            m_previousPhase = currentPhase;
            return true;  // Emit ONCE per phase change
        }
        return false;
    }

    QString getPhaseDescription() const {
        switch(currentPhase) {
            case 1: return "The battle begins...";
            case 2: return "The Shadow grows stronger!";
            case 3: return "Darkness intensifies! Beware powerful attacks!";
            case 4: return "The Shadow's final desperate assault!";
            default: return "";
        }
    }

private:
    int currentPhase;
    int m_previousPhase;
};

// ============================================================================
// PATTERN 2: Boss Combat Integration in Game.cpp
// ============================================================================
// Location: Game.cpp playerAttack() - AFTER damage applied, BEFORE checkCombatEndAfterAction()

QString Game::playerAttack()
{
    // ... existing damage calculation ...

    currentMonster->health -= damage;

    // BOSS PHASE CHECK (before combat end check)
    if (FinalBoss* boss = dynamic_cast<FinalBoss*>(currentMonster)) {
        boss->updatePhase();

        if (boss->shouldEmitPhaseTransition()) {
            emit bossPhaseChanged(boss->getCurrentPhase());

            combatLog += QString("\n\n=== PHASE %1 ===\n%2\n")
                .arg(boss->getCurrentPhase())
                .arg(boss->getPhaseDescription());
        }
    }

    checkCombatEndAfterAction();  // Check victory after phase update
    return combatLog;
}

// BOSS ATTACK MULTIPLIER (in monsterAttack())
QString Game::monsterAttack()
{
    if (!combatActive || !currentMonster || !player) {
        return "No combat active!";
    }

    int baseDamage = currentMonster->attack;

    // Apply boss phase multiplier
    if (FinalBoss* boss = dynamic_cast<FinalBoss*>(currentMonster)) {
        int multiplier = boss->getPhaseAttackMultiplier();
        baseDamage = (baseDamage * multiplier) / 100;  // Scale by percentage
    }

    int damage = calculateDamage(baseDamage, currentMonster->level,
                                  player->getTotalDefense(), false);

    player->health -= damage;
    // ... rest of method
}

// ============================================================================
// PATTERN 3: Victory Detection and Game Completion
// ============================================================================
// Location: Game.cpp endCombat() - After rewards given

void Game::endCombat()
{
    if (!combatActive) return;

    combatActive = false;

    bool playerWon = (currentMonster && currentMonster->health <= 0 &&
                      player && player->health > 0);

    if (playerWon) {
        giveCombatRewards();

        // FINAL BOSS VICTORY DETECTION
        if (currentMonster && currentMonster->enemyType == "final_boss") {
            // Mark player as game completer
            player->hasDefeatedFinalBoss = true;
            player->gameCompletionTime = QDateTime::currentDateTime().toString(Qt::ISODate);
            player->finalGameLevel = player->level;

            // Emit completion signals
            emit finalBossDefeated();
            emit gameCompleted(player->level, calculatePlaytimeMinutes());
        }
    }
}

// ============================================================================
// PATTERN 4: Level and Quest Gate System
// ============================================================================
// Location: Game.cpp canAccessFinalBoss()

bool Game::canAccessFinalBoss() const
{
    if (!player || !m_questManager) return false;

    // Check level requirement
    if (player->level < 20) {
        return false;
    }

    // Check all main quests complete
    QList<Quest*> mainQuests;
    for (Quest* quest : m_questManager->getAllQuests()) {
        if (quest && quest->questId.startsWith("main_quest_")) {
            mainQuests.append(quest);
        }
    }

    for (Quest* quest : mainQuests) {
        if (!quest->isComplete()) {
            return false;  // Block if any main quest incomplete
        }
    }

    return true;  // All requirements met
}

// ============================================================================
// PATTERN 5: VictoryScreen UI Structure
// ============================================================================
// File: src/views/VictoryScreen.cpp
// Pattern: QDialog with celebratory styling and statistics display

void VictoryScreen::setupUi()
{
    setWindowTitle("Victory!");
    setModal(true);
    setMinimumSize(800, 600);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(Theme::SPACING_XL);

    // Victory header with glow effect
    m_victoryTitle = new QLabel("VICTORY!");
    m_victoryTitle->setAlignment(Qt::AlignCenter);
    m_victoryTitle->setStyleSheet(QString(
        "font-size: %1px; "
        "font-weight: %2; "
        "color: %3; "
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
        "    stop:0 #FFD700, stop:1 #FFA500);"
        "-webkit-background-clip: text;"
    ).arg(Theme::FONT_SIZE_XXL * 2)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::PRIMARY.name()));

    // Apply glow effect
    QGraphicsDropShadowEffect *glow = new QGraphicsDropShadowEffect;
    glow->setBlurRadius(20);
    glow->setColor(QColor(255, 215, 0));  // Gold
    glow->setOffset(0, 0);
    m_victoryTitle->setGraphicsEffect(glow);

    mainLayout->addWidget(m_victoryTitle);

    // Statistics grid (2 columns x 3 rows)
    QGridLayout *statsGrid = new QGridLayout();
    statsGrid->setSpacing(Theme::SPACING_MD);

    statsGrid->addWidget(createStatisticsCard("Final Level", QString::number(m_finalLevel)), 0, 0);
    statsGrid->addWidget(createStatisticsCard("Playtime", formatPlaytime(m_playtime)), 0, 1);
    statsGrid->addWidget(createStatisticsCard("Enemies Defeated", QString::number(m_kills)), 1, 0);
    statsGrid->addWidget(createStatisticsCard("Times Died", QString::number(m_deaths)), 1, 1);
    statsGrid->addWidget(createStatisticsCard("Gold Earned", QString::number(m_gold)), 2, 0);
    statsGrid->addWidget(createStatisticsCard("Quests Completed", QString::number(m_quests)), 2, 1);

    mainLayout->addLayout(statsGrid);

    // Action buttons
    mainLayout->addWidget(createActionButtons());
}

QWidget* VictoryScreen::createStatisticsCard(const QString &label, const QString &value)
{
    QWidget *card = new QWidget();
    card->setStyleSheet(QString(
        "background-color: %1; "
        "border: 2px solid %2; "
        "border-radius: %3px; "
        "padding: %4px;"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_LG)
     .arg(Theme::SPACING_LG));

    QVBoxLayout *layout = new QVBoxLayout(card);

    QLabel *labelWidget = new QLabel(label);
    labelWidget->setStyleSheet(QString(
        "font-size: %1px; color: %2;"
    ).arg(Theme::FONT_SIZE_MD).arg(Theme::TEXT.name()));

    QLabel *valueWidget = new QLabel(value);
    valueWidget->setStyleSheet(QString(
        "font-size: %1px; "
        "font-weight: %2; "
        "color: %3;"
    ).arg(Theme::FONT_SIZE_XL)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::PRIMARY.name()));

    layout->addWidget(labelWidget);
    layout->addWidget(valueWidget);

    return card;
}

// ============================================================================
// PATTERN 6: Player Serialization Version 4
// ============================================================================
// File: src/models/Player.cpp operator<<

QDataStream &operator<<(QDataStream &out, const Player &p)
{
    // Version 4: Added game completion tracking
    out << quint32(4);

    // Serialize base Character data
    out << static_cast<const Character&>(p);

    // ... existing fields (mana, stats, inventory, equipment, skills, quests, lore) ...

    // NEW: Game completion fields (at end for version 4)
    out << p.hasDefeatedFinalBoss
        << p.gameCompletionTime
        << p.finalGameLevel;

    return out;
}

QDataStream &operator>>(QDataStream &in, Player &p)
{
    quint32 version;
    in >> version;

    // ... deserialize existing fields based on version ...

    // Version 4: Load game completion fields
    if (version >= 4) {
        in >> p.hasDefeatedFinalBoss
           >> p.gameCompletionTime
           >> p.finalGameLevel;
    } else {
        // Default values for old saves
        p.hasDefeatedFinalBoss = false;
        p.gameCompletionTime = "";
        p.finalGameLevel = 0;
    }

    return in;
}
```

### Integration Points

```yaml
COMBAT_SYSTEM:
  - location: src/game/Game.cpp, playerAttack() after line 245
  - add: Phase transition detection with dynamic_cast<FinalBoss*>
  - timing: After damage applied, before checkCombatEndAfterAction()

BOSS_VICTORY:
  - location: src/game/Game.cpp, endCombat() after line 363
  - add: Check enemyType == "final_boss", set completion flags
  - timing: After giveCombatRewards(), before exit

BOSS_REWARDS:
  - location: src/game/Game.cpp, giveCombatRewards() after line 437
  - add: 2x XP multiplier, guaranteed legendary drop, victory cutscene trigger
  - timing: After normal rewards, before quest/codex updates

MAINWINDOW_SIGNALS:
  - location: src/MainWindow.cpp, newGame() and loadGame() after Game created
  - add: Connect bossEncountered, bossPhaseChanged, finalBossDefeated, gameCompleted signals
  - critical: Use Qt::UniqueConnection to prevent duplicate connections

QUEST_INTEGRATION:
  - location: Add final quest to QuestFactory that triggers boss encounter
  - requirements: Level 20+, all previous quests complete
  - action: Call MainWindow::handleFinalBossRequest() on quest acceptance

SAVE_SYSTEM:
  - location: src/models/Player.cpp, operator<< and operator>>
  - changes: Version 4, serialize completion fields after quests
  - backward_compat: if (version >= 4) conditional load

SAVE_SLOT_DISPLAY:
  - location: src/views/SaveLoadPage.cpp, save slot rendering
  - add: Gold star "⭐ COMPLETED" badge for hasDefeatedFinalBoss saves
  - styling: Theme::PRIMARY color

CMAKE_BUILD:
  - file: cpp-qt-rpg/CMakeLists.txt
  - add_to_main: FinalBoss.cpp, VictoryScreen.cpp, PointOfNoReturnDialog.cpp
  - add_to_tests: FinalBoss.cpp to test_models, test_mainwindow, test_combat_page_dual_mode
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Build after creating FinalBoss
cd cpp-qt-rpg/build
cmake ..
make

# Verify FinalBoss compiles
make src/models/FinalBoss.cpp

# Verify VictoryScreen compiles
make src/views/VictoryScreen.cpp

# Full build
cd cpp-qt-rpg/build
cmake .. && make

# Expected: Zero compile errors
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test FinalBoss phase mechanics
cd cpp-qt-rpg/build
./test_final_boss

# Expected output:
# PASS : TestFinalBoss::testFinalBossCreation()
# PASS : TestFinalBoss::testPhaseTransitions()
# PASS : TestFinalBoss::testPhaseAttackMultipliers()
# PASS : TestFinalBoss::testPhaseTransitionDetection()
# PASS : TestFinalBoss::testBossDefeat()

# Test VictoryScreen display
./test_victory_screen

# Expected output:
# PASS : TestVictoryScreen::testVictoryScreenCreation()
# PASS : TestVictoryScreen::testStatisticsDisplay()
# PASS : TestVictoryScreen::testContinueButton()
# PASS : TestVictoryScreen::testKeyboardShortcuts()

# Run all tests
ctest

# Expected: All tests pass (0 failures)
```

### Level 3: Integration Testing (System Validation)

```bash
# Run the game
cd cpp-qt-rpg/build
./pyrpg-qt

# Manual test flow - FINAL BOSS ENCOUNTER:
# 1. Start New Game, level up to 20
# 2. Complete all main quests (main_quest_01 through main_quest_08)
# 3. Accept final quest (main_quest_09)
#    - Verify: "Point of No Return" dialog appears
#    - Cancel → quest not started
# 4. Re-accept final quest, click "I'm Ready"
#    - Verify: Boss combat begins
#    - Verify: Boss name "The Eternal Shadow" displayed
#    - Verify: Run button disabled
# 5. Attack boss repeatedly:
#    - At ~75% HP: Verify phase 2 message appears
#    - At ~50% HP: Verify phase 3 message appears
#    - At ~25% HP: Verify phase 4 message appears
#    - Verify: Boss attacks get stronger each phase
# 6. Defeat boss (bring HP to 0):
#    - Verify: Victory cutscene plays
#    - Verify: VictoryScreen appears with statistics
#    - Verify: Statistics are correct (level, playtime, kills, etc.)
# 7. Click Continue button:
#    - Verify: Returns to game world
#    - Verify: Can still explore and fight monsters
# 8. Save game (slot 1)
# 9. Load save:
#    - Verify: "⭐ COMPLETED" badge shows on slot 1
# 10. Load save and verify:
#     - Verify: Player.hasDefeatedFinalBoss == true
#     - Verify: Completion timestamp exists
#     - Verify: Can still play normally

# Test level gate:
# 1. New game, reach level 19
# 2. Try to accept final quest
#    - Verify: Error message "Level 20+ required"
#    - Verify: Quest not started
# 3. Level up to 20, try again
#    - Verify: "Point of No Return" dialog appears

# Test quest gate:
# 1. New game, reach level 20
# 2. Skip main_quest_05
# 3. Try to accept final quest
#    - Verify: Error message "All main quests must be complete"
#    - Verify: Quest not started

# Expected: All manual tests pass, no crashes, epic boss feel
```

### Level 4: Boss Encounter Experience Validation

```bash
# Subjective quality checks:

# 1. Boss Difficulty:
#    - Is boss significantly harder than normal enemies?
#    - Do phases progressively increase challenge?
#    - Is final phase dramatic and tense?
#    - Expected: Boss requires strategy, not just grinding

# 2. Phase Transitions:
#    - Are phase messages visible and impactful?
#    - Do phase changes feel dramatic?
#    - Is attack pattern change noticeable?
#    - Expected: Clear feedback, player feels phase shift

# 3. Victory Experience:
#    - Does victory feel rewarding?
#    - Are statistics meaningful?
#    - Is VictoryScreen visually appealing?
#    - Expected: Sense of accomplishment

# 4. Narrative Integration:
#    - Does final boss fit story context?
#    - Do cutscenes enhance experience?
#    - Is "point of no return" clear?
#    - Expected: Cohesive narrative climax

# 5. Post-Victory:
#    - Can player continue playing?
#    - Does completion badge appear?
#    - Is save file marked correctly?
#    - Expected: Seamless continuation, clear completion status
```

## Final Validation Checklist

### Technical Validation

- [ ] All files compile without warnings
- [ ] Unit tests pass: `./test_final_boss` and `./test_victory_screen`
- [ ] Integration tests pass: `ctest` shows 0 failures
- [ ] No memory leaks: FinalBoss deleted after combat
- [ ] No segfaults: All dynamic_cast checks in place
- [ ] Save/load works: Completion flag persists correctly

### Feature Validation

- [ ] Final boss only accessible at level 20+ with all quests complete
- [ ] "Point of No Return" dialog appears before boss fight
- [ ] Boss combat has 3 visible phase transitions
- [ ] Phase transitions occur at 75%, 50%, 25% HP
- [ ] Boss attacks increase in power each phase
- [ ] Run button disabled during boss fight
- [ ] Victory cutscene plays after boss defeat
- [ ] VictoryScreen displays all 6 statistics correctly
- [ ] Completion flag persists through save/load
- [ ] Save slots show "COMPLETED" badge
- [ ] Player can continue playing post-victory
- [ ] Keyboard shortcuts work (Space = continue, Esc = menu)

### Code Quality Validation

- [ ] Follows existing codebase patterns
- [ ] Theme constants used (no hardcoded colors)
- [ ] dynamic_cast used safely for boss type checking
- [ ] Signal/slot connections follow naming conventions
- [ ] Player serialization maintains backward compatibility
- [ ] CMakeLists.txt updated correctly
- [ ] No duplicate signal connections (Qt::UniqueConnection used)

### Experience Validation

- [ ] Boss encounter feels epic and challenging
- [ ] Phase transitions are dramatic and clear
- [ ] Victory screen is celebratory and satisfying
- [ ] Statistics feel meaningful and accurate
- [ ] Level/quest gates prevent premature access
- [ ] "Point of no return" creates appropriate tension
- [ ] Post-victory gameplay is seamless
- [ ] Completion badge provides sense of achievement

## Anti-Patterns to Avoid

- ❌ Don't serialize FinalBoss - it's ephemeral like Monster (created at combat start, deleted after)
- ❌ Don't check phase after combat ends - phase check must happen BEFORE checkCombatEndAfterAction()
- ❌ Don't emit phaseChanged signal every turn - only once per actual phase transition
- ❌ Don't use static_cast for boss detection - use dynamic_cast<FinalBoss*> for type safety
- ❌ Don't hardcode colors in VictoryScreen - always use Theme::PRIMARY and Theme::CARD
- ❌ Don't forget backward compatibility - version 3 saves must load with default false values
- ❌ Don't connect signals multiple times - use Qt::UniqueConnection to prevent duplicates
- ❌ Don't block post-victory gameplay - allow player to continue exploring world
- ❌ Don't skip "point of no return" dialog - it's critical for player preparation
- ❌ Don't make boss too easy - should require level 20+ and good equipment
- ❌ Don't make boss impossibly hard - 3-5 attempts should lead to victory with strategy
- ❌ Don't forget to disable run button - final boss is mandatory challenge
- ❌ Don't skip victory cutscene - narrative closure is essential
- ❌ Don't display VictoryScreen before cutscene - story then statistics

---

## Confidence Score: 9/10

**Rationale**: This PRP has comprehensive context from deep research:
- ✅ Complete Monster class analysis with inheritance patterns
- ✅ Full Game.cpp combat flow with exact integration points (lines 222, 245, 363, 437)
- ✅ Research-backed multi-phase boss design (75%, 50%, 25% thresholds)
- ✅ Complete VictoryScreen template from StatsPage and CombatResultDialog patterns
- ✅ Dialog patterns analyzed (QDialog vs custom overlay decision made)
- ✅ Player serialization versioning strategy (version 4 with backward compatibility)
- ✅ Signal/slot architecture documented with MainWindow integration
- ✅ Save system integration (completion badge in save slots)
- ✅ Theme constants and styling patterns extracted
- ✅ CMake build patterns for adding new files
- ✅ Testing patterns from existing test suite
- ✅ Memory management (FinalBoss ephemeral, no serialization)

**Deduction (-1)**: Minor uncertainty around exact "epic feel" tuning - boss difficulty balance requires playtesting iteration, though framework provides all tools for adjustment.

**Validation**: An AI agent can implement this successfully with:
1. This PRP
2. Access to codebase files (for pattern verification)
3. Training data for Qt6/C++ and RPG game design

All patterns, integration points, phase algorithms, UI templates, and save format updates are explicitly documented with file:line references and research-backed recommendations.
