name: "Storyline & Quest System - Phase 3: Narrative Systems (Dialogue, Story Events, Lore)"
description: |
  Implementation PRP for narrative layer: DialogueManager with branching trees,
  StoryManager for cutscenes/events, Lore system with codex UI. Builds on Phase 1-2
  quest foundation to create rich storytelling experience in PyRPG Qt.

---

## Goal

**Feature Goal**: Implement a complete narrative layer with dialogue trees, story events, and lore system that transforms quests from simple objectives into an immersive story-driven experience.

**Deliverable**:
- DialogueData models with branching support and QDataStream serialization
- DialogueManager for state-driven dialogue navigation
- StoryEvent models for narrative cutscenes with timing control
- StoryManager for event triggering and sequencing
- LoreEntry models for world-building content
- CodexManager for lore discovery tracking
- DialogueView UI for NPC conversations with choice selection
- StoryEventDialog overlay for cutscenes/narrative moments
- LoreBookPage UI for browsing discovered codex entries
- 5-10 authored dialogue trees integrated with quest system
- Story events at quest milestones (quest start, completion, critical moments)
- 10-15 lore entries with discovery triggers
- Full save/load support for dialogue/event/lore state

**Success Definition**:
- NPC dialogue displays with player choices affecting quest outcomes
- Story events trigger automatically at quest milestones
- Lore entries unlock through gameplay (killing enemies, finding items, completing quests)
- Dialogue state persists (can't repeat unique conversations)
- Story event viewing tracked (cutscenes don't repeat unless intended)
- Lore codex shows discovered entries organized by category
- All unit tests pass for Dialogue/Story/Lore models and managers
- Integration tests verify dialogue-quest-event flows
- No memory leaks from dialogue trees or event sequences

## User Persona

**Target User**: RPG player seeking narrative depth and world immersion beyond combat mechanics

**Use Case**:
- Player defeats quest objective → Story event cutscene shows consequences
- Player enters town → NPC dialogue provides quest context and lore hints
- Player defeats unique boss → Lore entry unlocks explaining boss backstory
- Player makes dialogue choice → Quest objectives or rewards change based on choice
- Player opens codex → Discovers world history through collected lore entries

**User Journey**:
1. Player accepts first quest → Intro dialogue with Village Elder establishes stakes
2. Elder offers 2 dialogue choices: "What's happening?" or "I'll help immediately"
3. Player selects "What's happening?" → Additional dialogue provides backstory
4. Player completes first objective → Story event cutscene shows shadow creatures advancing
5. Player defeats first boss → Lore entry "Shadow Wolves" unlocks in bestiary
6. Player returns to Elder → Completion dialogue triggers, quest rewards given
7. Player opens Lore Book (L key) → Reviews discovered entries about enemies and world
8. Player saves game → All dialogue history, viewed events, and lore progress preserved
9. Player loads game → Cannot repeat unique dialogues, already-viewed events, lore remains discovered

**Pain Points Addressed**:
- Lack of narrative context for quests (solved by dialogue and story events)
- Repetitive combat without meaning (solved by lore system giving enemies backstory)
- No sense of world depth (solved by codex entries and environmental storytelling)
- Unclear quest motivation (solved by NPC dialogue establishing stakes)
- Lost immersion from lack of cutscenes (solved by story event system)

## Why

- **Narrative Depth**: Transforms the quest system from mechanical objectives into an emotional story arc
- **Player Investment**: Dialogue choices and story events create personal stake in outcomes
- **Replayability**: Branching dialogue creates multiple narrative paths to explore
- **World-Building**: Lore system makes the game world feel lived-in and historically rich
- **Quest Context**: Dialogue at quest milestones provides meaning to combat objectives
- **Industry Standard**: All modern RPGs include dialogue, cutscenes, and lore codexes

This solves PRD pain point: "Players engage in endless combat without story context." By adding narrative layers, combat becomes part of a larger story rather than meaningless grinding.

## What

### Core Functionality

**Dialogue System**:
- DialogueNode model: speaker, text, choices with branching
- DialogueTree structure: interconnected nodes referenced by ID
- DialogueManager: State machine for current dialogue, choice selection, navigation
- DialogueView UI: Modal or overlay showing NPC name, dialogue text, 2-4 player choices
- Choice consequences: Can unlock quests, give items, affect quest rewards
- Conditional choices: Options appear only if player meets requirements (level, items, quest state)
- Linear dialogues: Support for non-branching conversations (NPC monologues)
- Dialogue history tracking: Prevent repeating unique conversations

**Story Event System**:
- StoryEvent model: Title, narrative text, background image paths, timing info
- Event triggers: Quest start/complete, level reached, item acquired, manual
- StoryManager: Checks triggers, queues events, marks events as viewed
- StoryEventDialog UI: Full-screen or overlay with fade-in, narrative text, background art
- Sequential events: Chain multiple story beats (intro → complication → resolution)
- Skippable events: Allow players to skip/fast-forward (with confirmation)
- Event replay: Optional "Story Log" to review past cutscenes

**Lore System**:
- LoreEntry model: Category, title, short/full text, image, discovery triggers
- Categories: Bestiary (enemies), Items, World History, Characters, Locations
- CodexManager: Tracks discovered entries, handles unlock logic
- LoreBookPage UI: Tabbed interface by category, list + detail panes
- Discovery triggers: Kill enemy X times, collect item, complete quest, reach location
- Unlock notifications: Toast/popup when new lore discovered
- Cross-references: Lore entries link to related entries

**Integration Points**:
- **Quest System**: Dialogue advances quests, story events trigger at quest milestones
- **Combat System**: Enemy kills unlock bestiary entries
- **Item System**: Item pickups unlock item lore
- **Save System**: Serialize dialogue history, viewed events, discovered lore
- **MainWindow**: Add keyboard shortcuts (D for dialogue, L for lore book)

### Success Criteria

**Dialogue System**:
- [ ] Dialogue trees load from DialogueFactory with branching structure
- [ ] DialogueView displays NPC name, dialogue text, and 2-4 choices
- [ ] Selecting choice navigates to next dialogue node or ends conversation
- [ ] Dialogue effects apply (unlock quest, give item, give gold/XP)
- [ ] Conditional choices hide/disable if requirements not met
- [ ] Dialogue history tracks viewed dialogues (IDs stored in Player)
- [ ] Cannot repeat unique dialogues (e.g., quest giver's first conversation)
- [ ] Dialogue state saves and loads without corruption

**Story Event System**:
- [ ] Story events load from StoryEventFactory with trigger conditions
- [ ] StoryManager checks triggers after quest events (start, progress, complete)
- [ ] StoryEventDialog displays full-screen narrative with background image
- [ ] Events can be skipped with ESC or skip button (after 1 second delay)
- [ ] Viewed events marked in Player save data
- [ ] Events don't repeat unless explicitly configured as repeatable
- [ ] Sequential events chain (event A completes → event B triggers)
- [ ] Story event state persists through save/load

**Lore System**:
- [ ] Lore entries load from LoreFactory organized by category
- [ ] CodexManager tracks discovered entries per player
- [ ] Lore unlocks trigger on gameplay events (enemy kill, item get, quest complete)
- [ ] LoreBookPage displays categories: Bestiary, Items, World, Characters
- [ ] Clicking category shows discovered entries in that category
- [ ] Clicking entry shows full lore text with image (if available)
- [ ] Undiscovered entries show as "???" or hidden
- [ ] Lore discovery shows notification ("New Codex Entry: Shadow Wolf")
- [ ] Lore state persists through save/load

**Integration**:
- [ ] Quest acceptance triggers introductory dialogue
- [ ] Quest completion triggers reward dialogue and story event
- [ ] Defeating unique boss triggers lore unlock + story event
- [ ] All managers (Dialogue, Story, Codex) owned by Game or MainWindow
- [ ] Keyboard shortcuts work (D opens dialogue, L opens lore book)
- [ ] Unit tests: 100% pass for all models and managers
- [ ] Integration tests: Complete dialogue-quest-event-lore flow verified

## All Needed Context

### Context Completeness Check

✓ **Dialogue UI patterns**: Comprehensive analysis of QDialog patterns, modal behavior, choice button layouts
✓ **Event system patterns**: Complete understanding of signal/slot architecture, state machines, timing control
✓ **Factory patterns**: All factory classes analyzed (Item, Monster, Skill, Quest) with exact patterns to follow
✓ **Save/load architecture**: Full SaveManager versioning strategy, QDataStream serialization patterns
✓ **UI component patterns**: LogDisplay, QTextEdit, scrollable layouts, Theme integration
✓ **Testing patterns**: Complete test structure for models, managers, UI, signals, and integration flows
✓ **External best practices**: Qt6 modern patterns, dialogue tree architectures, narrative sequencing strategies

**Validation**: An AI agent unfamiliar with this codebase has everything needed - exact file patterns, naming conventions, serialization strategies, UI integration examples, factory structures, test patterns, and external research references.

### Documentation & References

```yaml
# PRD Architecture Reference
- file: PRPs/storyline-quest-system-prd.md
  why: Complete Phase 3 requirements, dialogue/story/lore specifications
  section: "Phase 3: Narrative Systems (lines 932-958), Dialogue System Architecture (lines 563-638), Story Event System (lines 640-673)"
  critical: DialogueNode/DialogueTree structures, StoryEvent model, LoreEntry model

# Existing Phase 1-2 Implementation (Quest System)
- file: PRPs/storyline-quest-system-phase1.md
  why: Quest system integration points, QuestManager signal patterns
  section: "QuestManager signals (lines 535-550), Quest completion handling (lines 1012-1038)"
  critical: How to connect story events to quest milestones

# Model Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/models/Player.h
  why: Player extensions for dialogue/story/lore tracking
  pattern: QList<QString> for tracking viewed IDs (lines 24-27)
  gotcha: Must serialize new lists in operator<< with version increment

- file: cpp-qt-rpg/src/models/Player.cpp
  why: Versioned serialization pattern for backward compatibility
  pattern: Version 3 for quest data (lines 62-161), use Version 4 for narrative data
  critical: Conditional deserialization based on version (if version >= 4)

- file: cpp-qt-rpg/src/models/Quest.h
  why: Complex nested struct pattern (QuestObjective, QuestRewards)
  pattern: Embedded structs within main class (lines 15-27)
  usage: Follow same pattern for DialogueChoice and DialogueEffect structs

- file: cpp-qt-rpg/src/models/Item.h
  why: Simple model with description field
  pattern: QString description member (line 27)
  usage: LoreEntry follows similar pattern with extended text fields

# UI Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/components/CombatResultDialog.h
  why: Modal information dialog pattern with rich formatting
  pattern: QDialog with data in constructor, setupUi() private method (lines 7-14)
  usage: StoryEventDialog follows this exact pattern

- file: cpp-qt-rpg/src/components/CombatResultDialog.cpp
  why: Multi-line formatted text display with Theme styling
  pattern: setModal(true), HTML formatting in labels, emoji usage (lines 8-112)
  critical: Use QString::arg() for Theme colors, setMinimumWidth(400)

- file: cpp-qt-rpg/src/components/MenuOverlay.h
  why: Full-screen overlay pattern with animation
  pattern: QWidget with Q_PROPERTY(qreal opacity), QPropertyAnimation (lines 10-25)
  usage: StoryEventDialog can use fade-in animation for cinematic effect

- file: cpp-qt-rpg/src/components/MenuOverlay.cpp
  why: Fade animation implementation
  pattern: QPropertyAnimation with 200ms duration, easing curves (lines 92-102)
  critical: Connect animation->finished() to handle completion

- file: cpp-qt-rpg/src/components/LogDisplay.h
  why: Scrollable message list with typed entries
  pattern: Custom widget with entry management, auto-scroll (lines 8-30)
  usage: Can adapt for story log / dialogue history display

- file: cpp-qt-rpg/src/views/QuestLogPage.h
  why: Multi-pane UI with list + details
  pattern: QHBoxLayout with QListWidget (1/3 width) + QTextEdit (2/3 width) (lines 14-34)
  usage: LoreBookPage follows identical layout pattern

- file: cpp-qt-rpg/src/views/QuestLogPage.cpp
  why: Category headers in list widget, HTML details pane
  pattern: Add section headers to QListWidget, build HTML in detail pane (lines 60-250)
  critical: Use Theme constants for all styling, QVariant::fromValue for data storage

- file: cpp-qt-rpg/src/components/SkillSelectionDialog.h
  why: Choice selection dialog pattern
  pattern: QListWidget with selectable items, accept/cancel buttons (lines 8-24)
  usage: DialogueView uses similar choice selection pattern

- file: cpp-qt-rpg/src/components/SkillSelectionDialog.cpp
  why: Disabled item handling for conditional options
  pattern: item->setFlags(item->flags() & ~Qt::ItemIsEnabled) (line 47)
  usage: Dialogue choices disabled if requirements not met

# Manager Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/game/QuestManager.h
  why: Manager class structure with signals and event handlers
  pattern: QObject base, explicit constructor with Player*, signals for state changes (lines 10-59)
  critical: Manager owns content objects (m_allQuests), Player owns active/completed references

- file: cpp-qt-rpg/src/game/QuestManager.cpp
  why: Event-driven update pattern
  pattern: onCombatEnd(), onLevelUp(), onItemCollected() event handlers (lines 134-240)
  usage: DialogueManager and StoryManager follow same event handler pattern

- file: cpp-qt-rpg/src/game/Game.h
  why: Game controller integration pattern
  pattern: QuestManager* member, getter method, ownership (lines 46-48)
  usage: Add DialogueManager, StoryManager, CodexManager similarly

- file: cpp-qt-rpg/src/game/Game.cpp
  why: Manager lifecycle management
  pattern: Create in newGame/loadGame, delete in destructor (lines 41-47, 95-108)
  critical: Recreate managers on load to reference new Player pointer

# Factory Pattern References (MUST FOLLOW)
- file: cpp-qt-rpg/src/game/factories/QuestFactory.h
  why: Static factory methods for content creation
  pattern: static Quest* createQuest(id), static QList<Quest*> getAll() (lines 8-15)

- file: cpp-qt-rpg/src/game/factories/QuestFactory.cpp
  why: Hardcoded content definitions with rich data structures
  pattern: if/else chain for IDs, inline object construction (lines 8-258)
  critical: Use raw string literals R"(...)" for multi-line text

- file: cpp-qt-rpg/src/game/factories/ItemFactory.cpp
  why: Static map caching to prevent memory leaks
  pattern: static QMap<QString, Item*> items; if (items.isEmpty()) { initialize } (lines 73-118)
  usage: DialogueFactory and StoryEventFactory should use same caching pattern

# Save/Load Pattern References
- file: cpp-qt-rpg/src/persistence/SaveManager.cpp
  why: Complete save/load flow and versioning strategy
  pattern: Magic header, version checking, metadata, full serialization (lines 16-81)
  critical: ALWAYS set out.setVersion(QDataStream::Qt_6_0)

# MainWindow Integration Pattern
- file: cpp-qt-rpg/src/MainWindow.h
  why: View registration and keyboard shortcut handling
  pattern: View member pointers, handleXxxClicked slots, keyPressEvent override (lines 21-84)

- file: cpp-qt-rpg/src/MainWindow.cpp
  why: View lifecycle and signal connections
  pattern: Create view, connect signals, add to stack, update before switching (lines 35-226)
  critical: Always call view->updateXxx() before setCurrentWidget()

# Testing Pattern References
- file: cpp-qt-rpg/tests/test_quest_system.cpp
  why: Manager integration testing pattern
  pattern: QSignalSpy for signals, state transition verification (lines 1-152)
  usage: test_dialogue_system.cpp and test_story_system.cpp follow same pattern

- file: cpp-qt-rpg/tests/test_persistence.cpp
  why: Save/load testing pattern
  pattern: Create object, save, load, compare all fields (lines 15-95)
  usage: Test dialogue history, viewed events, discovered lore persistence

- file: cpp-qt-rpg/tests/test_mainwindow.cpp
  why: UI component testing with Qt Test
  pattern: QTest::qWait() for animations, QKeyEvent simulation (lines 1-120)
  usage: Test dialogue view, story event overlay, lore book page

# Theme Constants
- file: cpp-qt-rpg/src/theme/Theme.h
  why: All color, spacing, font constants
  pattern: Theme::CARD, Theme::PRIMARY, Theme::SPACING_LG
  critical: ALWAYS use Theme constants, never hardcode

# CMake Build Configuration
- file: cpp-qt-rpg/CMakeLists.txt
  why: Adding new source files and test targets
  pattern: Add .cpp to add_executable(pyrpg-qt ...) and test targets (lines 23-267)
  critical: Add to BOTH main executable AND relevant test executables

# External Research References
- url: https://doc.qt.io/qt-6/qdialog.html
  why: Qt6 QDialog best practices
  critical: Modern pattern uses show() with signals, not exec() for non-blocking

- url: https://en.wikipedia.org/wiki/Dialogue_tree
  why: Dialogue tree architectures and branching patterns
  critical: Branch-and-bottleneck pattern prevents exponential growth

- url: https://www.helika.io/how-to-write-branching-dialogue-systems-in-games/
  why: Professional dialogue system design patterns
  critical: Conditional branching, network structures, managing complexity

- url: https://link.springer.com/chapter/10.1007/978-3-319-07626-3_62
  why: Cutscene system architecture in games
  critical: Separate cinematic space, player agency preservation, information system role

# AI Research Documentation
- docfile: PRPs/ai_docs/dialogue-trees-design.md (CREATE THIS)
  why: Consolidated dialogue tree implementation strategies
  section: Branch-and-bottleneck pattern, conditional options, data structures

- docfile: PRPs/ai_docs/qt6-modern-dialogs.md (CREATE THIS)
  why: Qt6 modal dialog modern patterns avoiding exec()
  section: Signal-based completion handling, non-blocking patterns
```

### Current Codebase Tree

```bash
cpp-qt-rpg/
├── src/
│   ├── main.cpp
│   ├── MainWindow.h/.cpp
│   ├── models/
│   │   ├── Character.h/.cpp
│   │   ├── Player.h/.cpp            # ← MODIFY: Add dialogue/story/lore tracking
│   │   ├── Monster.h/.cpp
│   │   ├── Item.h/.cpp
│   │   ├── Skill.h/.cpp
│   │   └── Quest.h/.cpp             # ← Already exists from Phase 1-2
│   ├── game/
│   │   ├── Game.h/.cpp              # ← MODIFY: Add narrative managers
│   │   ├── QuestManager.h/.cpp      # ← Already exists, integrate with DialogueManager
│   │   └── factories/
│   │       ├── ItemFactory.h/.cpp
│   │       ├── SkillFactory.h/.cpp
│   │       ├── MonsterFactory.h/.cpp
│   │       └── QuestFactory.h/.cpp  # ← Already exists
│   ├── views/
│   │   ├── MainMenu.h/.cpp
│   │   ├── CombatPage.h/.cpp
│   │   ├── InventoryPage.h/.cpp
│   │   ├── StatsPage.h/.cpp
│   │   ├── ShopPage.h/.cpp
│   │   ├── SaveLoadPage.h/.cpp
│   │   └── QuestLogPage.h/.cpp      # ← Already exists
│   ├── components/
│   │   ├── ItemCard.h/.cpp
│   │   ├── LogDisplay.h/.cpp
│   │   ├── CombatResultDialog.h/.cpp
│   │   ├── QuestCompletionDialog.h/.cpp  # ← Already exists
│   │   ├── MenuOverlay.h/.cpp
│   │   ├── AnimationManager.h/.cpp
│   │   └── [many other components]
│   ├── persistence/
│   │   └── SaveManager.h/.cpp       # ← MODIFY: Update version for narrative data
│   └── theme/
│       └── Theme.h
├── tests/
│   ├── test_models.cpp
│   ├── test_persistence.cpp
│   ├── test_mainwindow.cpp
│   ├── test_quest_models.cpp         # ← Already exists
│   └── test_quest_system.cpp         # ← Already exists
└── CMakeLists.txt                    # ← MODIFY: Add new files to build
```

### Desired Codebase Tree (Files to Add)

```bash
cpp-qt-rpg/src/
├── models/
│   ├── DialogueData.h         # DialogueNode, DialogueChoice, DialogueTree structures
│   ├── DialogueData.cpp       # Serialization operators
│   ├── StoryEvent.h           # StoryEvent model (header-only, simple struct)
│   └── LoreEntry.h            # LoreEntry model (header-only, simple struct)
├── game/
│   ├── DialogueManager.h      # Dialogue state machine and navigation
│   ├── DialogueManager.cpp    # Choice handling, effect application
│   ├── StoryManager.h         # Event triggering and tracking
│   ├── StoryManager.cpp       # Trigger checking, event queueing
│   ├── CodexManager.h         # Lore discovery and tracking
│   ├── CodexManager.cpp       # Unlock logic, category management
│   └── factories/
│       ├── DialogueFactory.h   # Hardcoded dialogue tree definitions
│       ├── DialogueFactory.cpp # 5-10 branching dialogues
│       ├── StoryEventFactory.h # Hardcoded story event definitions
│       ├── StoryEventFactory.cpp # Quest milestone events
│       ├── LoreFactory.h       # Hardcoded lore entry definitions
│       └── LoreFactory.cpp     # Bestiary, items, world lore
├── views/
│   ├── DialogueView.h/.cpp      # NPC dialogue with choice UI
│   ├── StoryEventDialog.h/.cpp  # Full-screen narrative cutscene
│   └── LoreBookPage.h/.cpp      # Codex browser UI
└── tests/
    ├── test_dialogue_models.cpp      # DialogueData serialization tests
    ├── test_dialogue_system.cpp      # DialogueManager integration tests
    ├── test_story_system.cpp         # StoryManager event tests
    └── test_lore_system.cpp          # CodexManager lore discovery tests
```

### Known Gotchas & Library Quirks

```cpp
// CRITICAL: QDataStream Serialization (Same as Phase 1-2)
out.setVersion(QDataStream::Qt_6_0);
in.setVersion(QDataStream::Qt_6_0);

// CRITICAL: Player Version Increment
// Phase 1-2 used Version 3 for quests
// Phase 3 must use Version 4 for dialogue/story/lore
out << quint32(4);  // NEW VERSION

// CRITICAL: QList<QString> Serialization
// QList<QString> auto-serializes, no conversion needed
QList<QString> viewedDialogueIds;
out << viewedDialogueIds;  // Works directly

// GOTCHA: Dialogue Tree Circular References
// Avoid: DialogueNode A → B → A (infinite loop)
// Solution: Track visited nodes, implement max depth limit
QSet<QString> visitedNodes;
if (visitedNodes.contains(nodeId)) {
    // End dialogue to prevent infinite loop
}

// GOTCHA: Story Event Timing
// DO NOT use QTimer for cutscene delays in modal dialogs
// Modal dialogs block event loop, timers won't fire
// Solution: Use QEventLoop with QTimer or non-modal approach

// CRITICAL: Modal Dialog Modern Pattern
// OLD (discouraged): int result = dialog.exec();
// NEW (Qt6 best practice):
DialogueView *dialog = new DialogueView(this);
dialog->setAttribute(Qt::WA_DeleteOnClose);
dialog->setModal(true);
connect(dialog, &DialogueView::choiceSelected, this, &handleDialogueChoice);
dialog->show();  // Non-blocking

// GOTCHA: Choice Button Memory Management
// If creating buttons dynamically, track in list for cleanup
QList<QPushButton*> m_choiceButtons;
void clearChoices() {
    for (QPushButton *btn : m_choiceButtons) {
        delete btn;  // Manual cleanup
    }
    m_choiceButtons.clear();
}

// GOTCHA: HTML in QLabel vs QTextEdit
// QLabel: Must call setTextFormat(Qt::RichText) to enable HTML
label->setTextFormat(Qt::RichText);
label->setText("<b>Bold text</b>");

// QTextEdit: HTML enabled by default
textEdit->setHtml("<b>Bold text</b>");  // Works immediately

// CRITICAL: Theme Color Usage in HTML
// CORRECT: Use .name() and QString::arg()
QString html = QString("<span style='color: %1;'>Text</span>")
               .arg(Theme::PRIMARY.name());

// WRONG: Hardcoded color
QString html = "<span style='color: #dc3545;'>Text</span>";  // DON'T

// GOTCHA: SaveManager File Format Version
// If incrementing save file format version (optional):
// Line 29: out << quint32(3); // was 2, now 3
// Line 63: if (saveVersion > 3) { reject }
// NOTE: Can skip if Player version 4 is sufficient

// CRITICAL: Manager Ownership and Lifecycle
// Game or MainWindow owns managers, Player references them
// Pattern:
class Game {
    DialogueManager* m_dialogueManager;  // Owned pointer
    StoryManager* m_storyManager;        // Owned pointer
    CodexManager* m_codexManager;        // Owned pointer
};

// In newGame() and loadGame():
if (m_dialogueManager) delete m_dialogueManager;
m_dialogueManager = new DialogueManager(m_player, this);

// GOTCHA: Signal Connection Timing
// Connect manager signals AFTER manager created in newGame/loadGame
// Use Qt::UniqueConnection to prevent duplicates
connect(m_dialogueManager, &DialogueManager::dialogueCompleted,
        this, &MainWindow::handleDialogueCompleted, Qt::UniqueConnection);

// CRITICAL: Lore Unlock Deduplication
// Check if already unlocked before showing notification
if (!player->unlockedLoreEntries.contains(entryId)) {
    player->unlockedLoreEntries.append(entryId);
    emit loreUnlocked(entryId);  // Show notification
}

// GOTCHA: Story Event Skip Delay
// Prevent accidental skip by adding 1-second delay
m_eventStartTime = QDateTime::currentMSecsSinceEpoch();
// In keyPressEvent:
if (QDateTime::currentMSecsSinceEpoch() - m_eventStartTime < 1000) {
    return;  // Ignore ESC within first second
}

// CRITICAL: Factory Static Map Pattern (Prevent Memory Leaks)
static QMap<QString, DialogueTree*> dialogueTrees;
if (dialogueTrees.isEmpty()) {
    // Initialize once
    dialogueTrees["elder_intro"] = createElderIntroDialogue();
}
return dialogueTrees.value(dialogueId, nullptr);

// GOTCHA: QStackedWidget Index Management
// Don't rely on index numbers, use widget pointers
stackedWidget->setCurrentWidget(m_dialogueView);  // CORRECT
stackedWidget->setCurrentIndex(5);                // WRONG (brittle)

// CRITICAL: Qt Test Include Order
// MUST be at end of test file:
#include "test_dialogue_system.moc"  // After all code
QTEST_MAIN(TestDialogueSystem)       // Generates main()
```

## Implementation Blueprint

### Data Models and Structure

Following exact patterns from Player, Quest, and Item models:

**DialogueData Models (src/models/DialogueData.h)**:
- `DialogueChoice` struct: text, targetNodeId, effects, requirements
- `DialogueEffect` struct: type (AdvanceQuest, GiveItem, GiveGold, GiveXP, UnlockQuest), target, value
- `DialogueNode` struct: id, speaker, text, choices list, autoNextNodeId, endsDialogue flag
- `DialogueTree` class: id, npcName, startNodeId, QMap<QString, DialogueNode> nodes
- Public member variables (camelCase naming)
- Friend QDataStream operators for DialogueTree serialization

**StoryEvent Model (src/models/StoryEvent.h)**:
- Header-only struct (simple data container)
- Fields: eventId, title, eventText, imagePaths, prerequisites, triggerType, triggerId, viewed
- No serialization needed (viewed status tracked in Player)

**LoreEntry Model (src/models/LoreEntry.h)**:
- Header-only struct (simple data container)
- Fields: entryId, category, title, shortDescription, fullText, imagePath, discoveryTrigger
- Discovery triggers: "kill_X_10" (kill X enemy 10 times), "quest_complete_X", "item_get_X"

**Player Extensions (src/models/Player.h)**:
- Add: `QList<QString> viewedDialogueIds;` (track completed unique dialogues)
- Add: `QList<QString> viewedEventIds;` (track viewed story events)
- Add: `QList<QString> unlockedLoreEntries;` (track discovered lore)
- Methods: `hasViewedDialogue(id)`, `hasViewedEvent(id)`, `hasUnlockedLore(id)`

### Implementation Tasks (Ordered by Dependencies)

```yaml
Task 1: CREATE src/models/DialogueData.h
  IMPLEMENT: DialogueChoice, DialogueEffect, DialogueNode structs, DialogueTree class
  FOLLOW pattern: src/models/Quest.h (nested structs, lines 15-40)
  NAMING:
    - Structs: DialogueChoice, DialogueEffect, DialogueNode (PascalCase)
    - Class: DialogueTree (PascalCase)
    - Members: dialogueId, speakerName, text, choices, targetNodeId (camelCase)
  STRUCTURES:
    - DialogueEffect: QString type ("AdvanceQuest", "GiveItem", "GiveGold", "GiveXP", "UnlockQuest"), QString target, int value
    - DialogueChoice: QString text, QString targetNodeId, QList<DialogueEffect> effects, bool requiresLevel, int requiredLevel
    - DialogueNode: QString id, QString speaker, QString text, QList<DialogueChoice> choices, QString autoNextNodeId, bool endsDialogue
    - DialogueTree: QString id, QString npcName, QString startNodeId, QMap<QString, DialogueNode> nodes, getNode(id), getStartNode()
  PLACEMENT: cpp-qt-rpg/src/models/DialogueData.h
  DEPENDENCIES: None (header-only for structs, minimal class for tree)

Task 2: CREATE src/models/DialogueData.cpp
  IMPLEMENT: DialogueTree methods, QDataStream operators for serialization
  FOLLOW pattern: src/models/Quest.cpp (struct serialization, lines 45-78)
  SERIALIZATION:
    - DialogueTree operator<< writes: id, npcName, startNodeId, then QMap<QString, DialogueNode>
    - DialogueNode serialization: id, speaker, text, choicesCount, then each choice, autoNextNodeId, endsDialogue
    - DialogueChoice serialization: text, targetNodeId, effectsCount, then each effect, requiresLevel, requiredLevel
    - DialogueEffect serialization: type, target, value
  METHODS:
    - DialogueNode* getNode(const QString &nodeId): return &nodes[nodeId] if exists, else nullptr
    - DialogueNode* getStartNode(): return getNode(startNodeId)
  PLACEMENT: cpp-qt-rpg/src/models/DialogueData.cpp
  DEPENDENCIES: DialogueData.h (Task 1)

Task 3: CREATE src/models/StoryEvent.h
  IMPLEMENT: StoryEvent struct (header-only)
  FOLLOW pattern: Simple struct like QuestObjective (Quest.h lines 15-22)
  NAMING:
    - Struct: StoryEvent (PascalCase)
    - Members: eventId, title, eventText, imagePaths, prerequisites, triggerType, triggerId, viewed (camelCase)
  FIELDS:
    - QString eventId (unique ID, e.g., "intro_cutscene")
    - QString title ("A Dark Omen")
    - QString eventText (multi-line narrative using R"(...)")
    - QList<QString> imagePaths (background images from resources)
    - QList<QString> prerequisites (quest IDs or level requirements)
    - QString triggerType ("quest_start", "quest_complete", "level_reached", "manual")
    - QString triggerId (associated quest ID or level number)
    - bool viewed (false by default, player-specific state tracked separately)
  PLACEMENT: cpp-qt-rpg/src/models/StoryEvent.h
  DEPENDENCIES: None (simple struct)

Task 4: CREATE src/models/LoreEntry.h
  IMPLEMENT: LoreEntry struct (header-only)
  FOLLOW pattern: Simple struct like QuestRewards (Quest.h lines 24-29)
  NAMING:
    - Struct: LoreEntry (PascalCase)
    - Members: entryId, category, title, shortDescription, fullText, imagePath, discoveryTrigger (camelCase)
  FIELDS:
    - QString entryId ("bestiary_goblin", "world_ancient_war")
    - QString category ("Bestiary", "Items", "World", "Characters", "Locations")
    - QString title ("Goblin")
    - QString shortDescription ("Small, cunning creatures that hunt in packs.")
    - QString fullText (multi-line lore text using R"(...)")
    - QString imagePath (":/assets/goblin.png" or empty)
    - QString discoveryTrigger ("kill_Goblin_5", "quest_complete_main_quest_01", "item_get_Ancient_Tome")
  PLACEMENT: cpp-qt-rpg/src/models/LoreEntry.h
  DEPENDENCIES: None (simple struct)

Task 5: UPDATE src/models/Player.h
  ADD: Narrative tracking fields
  FOLLOW pattern: Existing quest list (line 24-26)
  ADDITIONS:
    - #include <QList> at top (if not present)
    - QList<QString> viewedDialogueIds; (after quests)
    - QList<QString> viewedEventIds;
    - QList<QString> unlockedLoreEntries;
    - bool hasViewedDialogue(const QString &dialogueId) const;
    - bool hasViewedEvent(const QString &eventId) const;
    - bool hasUnlockedLore(const QString &entryId) const;
    - void markDialogueViewed(const QString &dialogueId);
    - void markEventViewed(const QString &eventId);
    - void unlockLore(const QString &entryId);
  PLACEMENT: After quest members (around line 26)
  DEPENDENCIES: None (using Qt containers)

Task 6: UPDATE src/models/Player.cpp
  MODIFY: Constructor, destructor, serialization operators, add helper methods
  FOLLOW pattern: Quest serialization (lines 93-161 for version 3)
  CHANGES:
    1. Operator<< (save): Increment version to 4 (line 62)
       - After quest serialization, add:
       - out << viewedDialogueIds;
       - out << viewedEventIds;
       - out << unlockedLoreEntries;
    2. Operator>> (load): Add conditional narrative deserialization
       - After quest deserialization (after if version >= 3 block):
       - if (version >= 4) {
       -     in >> viewedDialogueIds;
       -     in >> viewedEventIds;
       -     in >> unlockedLoreEntries;
       - }
    3. Helper method implementations:
       - bool hasViewedDialogue(id) const { return viewedDialogueIds.contains(id); }
       - bool hasViewedEvent(id) const { return viewedEventIds.contains(id); }
       - bool hasUnlockedLore(id) const { return unlockedLoreEntries.contains(id); }
       - void markDialogueViewed(id) { if (!viewedDialogueIds.contains(id)) viewedDialogueIds.append(id); }
       - void markEventViewed(id) { if (!viewedEventIds.contains(id)) viewedEventIds.append(id); }
       - void unlockLore(id) { if (!unlockedLoreEntries.contains(id)) unlockedLoreEntries.append(id); }
  CRITICAL: Version 4 ensures old saves load (empty narrative lists for version < 4)
  DEPENDENCIES: Player.h updated (Task 5), DialogueData.cpp (Task 2)

Task 7: CREATE src/game/factories/DialogueFactory.h
  IMPLEMENT: Static factory methods for dialogue tree creation
  FOLLOW pattern: src/game/factories/QuestFactory.h (lines 8-15)
  NAMING: DialogueFactory class, static methods
  METHODS:
    - static DialogueTree* createDialogue(const QString &dialogueId);
    - static QList<DialogueTree*> getAllDialogues();
    - static DialogueTree* getDialogueForQuest(const QString &questId);
  PLACEMENT: cpp-qt-rpg/src/game/factories/DialogueFactory.h
  DEPENDENCIES: DialogueData.h (Task 1)

Task 8: CREATE src/game/factories/DialogueFactory.cpp
  IMPLEMENT: Hardcoded dialogue tree definitions (5-10 dialogues)
  FOLLOW pattern: src/game/factories/QuestFactory.cpp (if/else chain, lines 8-258)
  DIALOGUES to define:
    1. "elder_intro" - Village Elder introduction (branching: What's happening? / I'll help!)
    2. "elder_quest_complete" - Elder quest completion dialogue
    3. "merchant_greeting" - Merchant shop dialogue with flavor text
    4. "scholar_warning" - Scholar provides lore exposition
    5. "boss_pre_battle" - Final boss confrontation dialogue
  STRUCTURE:
    - static QMap<QString, DialogueTree*> cache;
    - if (cache.isEmpty()) { initialize all dialogues }
    - return cache.value(dialogueId, nullptr);
  DIALOGUE example structure:
    - DialogueTree* tree = new DialogueTree();
    - tree->id = "elder_intro";
    - tree->npcName = "Village Elder";
    - tree->startNodeId = "greeting";
    - DialogueNode greeting; greeting.id = "greeting"; greeting.speaker = "Village Elder";
    - greeting.text = "Greetings, brave adventurer...";
    - DialogueChoice choice1; choice1.text = "What's happening?"; choice1.targetNodeId = "explain";
    - DialogueChoice choice2; choice2.text = "I'll help!"; choice2.targetNodeId = "accept_quest";
    - DialogueEffect effect; effect.type = "UnlockQuest"; effect.target = "main_quest_01";
    - choice2.effects.append(effect);
    - greeting.choices.append(choice1); greeting.choices.append(choice2);
    - tree->nodes["greeting"] = greeting;
    - (Continue for "explain" and "accept_quest" nodes)
  PLACEMENT: cpp-qt-rpg/src/game/factories/DialogueFactory.cpp
  DEPENDENCIES: DialogueFactory.h (Task 7), DialogueData.cpp (Task 2)

Task 9: CREATE src/game/factories/StoryEventFactory.h
  IMPLEMENT: Static factory methods for story event creation
  FOLLOW pattern: src/game/factories/QuestFactory.h
  METHODS:
    - static StoryEvent* createEvent(const QString &eventId);
    - static QList<StoryEvent*> getAllEvents();
    - static QList<StoryEvent*> getEventsForQuest(const QString &questId);
  PLACEMENT: cpp-qt-rpg/src/game/factories/StoryEventFactory.h
  DEPENDENCIES: StoryEvent.h (Task 3)

Task 10: CREATE src/game/factories/StoryEventFactory.cpp
  IMPLEMENT: Hardcoded story event definitions
  FOLLOW pattern: QuestFactory.cpp if/else chain
  EVENTS to define:
    1. "intro_cutscene" - Game opening narrative
    2. "quest_01_start" - First quest intro cutscene
    3. "quest_01_complete" - First quest completion event
    4. "boss_intro" - Final boss introduction
    5. "victory_event" - Game completion celebration
  STRUCTURE:
    - static QMap<QString, StoryEvent*> cache;
    - if (cache.isEmpty()) { initialize }
    - return cache.value(eventId, nullptr);
  EVENT example:
    - StoryEvent* event = new StoryEvent();
    - event->eventId = "intro_cutscene";
    - event->title = "A Dark Omen";
    - event->eventText = R"(The sun sets over the village of Thornhaven.
For generations, your people have lived in peace...
Until now.)";
    - event->imagePaths.append(":/assets/intro_background.png");
    - event->triggerType = "manual";
    - event->viewed = false;
  PLACEMENT: cpp-qt-rpg/src/game/factories/StoryEventFactory.cpp
  DEPENDENCIES: StoryEventFactory.h (Task 9), StoryEvent.h (Task 3)

Task 11: CREATE src/game/factories/LoreFactory.h
  IMPLEMENT: Static factory methods for lore entry creation
  FOLLOW pattern: QuestFactory.h
  METHODS:
    - static LoreEntry* createLoreEntry(const QString &entryId);
    - static QList<LoreEntry*> getAllLoreEntries();
    - static QList<LoreEntry*> getLoreByCategory(const QString &category);
  PLACEMENT: cpp-qt-rpg/src/game/factories/LoreFactory.h
  DEPENDENCIES: LoreEntry.h (Task 4)

Task 12: CREATE src/game/factories/LoreFactory.cpp
  IMPLEMENT: Hardcoded lore entry definitions (10-15 entries)
  FOLLOW pattern: QuestFactory.cpp
  ENTRIES to define:
    - Bestiary: "bestiary_goblin", "bestiary_shadow_wolf", "bestiary_orc"
    - Items: "item_ancient_sword", "item_healing_potion_lore"
    - World: "world_ancient_war", "world_shadow_threat"
    - Characters: "character_village_elder", "character_dark_lord"
  STRUCTURE:
    - static QMap<QString, LoreEntry*> cache;
    - if (cache.isEmpty()) { initialize }
    - return cache.value(entryId, nullptr);
  LORE example:
    - LoreEntry* entry = new LoreEntry();
    - entry->entryId = "bestiary_goblin";
    - entry->category = "Bestiary";
    - entry->title = "Goblin";
    - entry->shortDescription = "Small, cunning creatures.";
    - entry->fullText = R"(Goblins are the most common threat...
Habitat: Forests, caves
Weakness: Fire-based attacks)";
    - entry->imagePath = ":/assets/goblin.png";
    - entry->discoveryTrigger = "kill_Goblin_3";
  PLACEMENT: cpp-qt-rpg/src/game/factories/LoreFactory.cpp
  DEPENDENCIES: LoreFactory.h (Task 11), LoreEntry.h (Task 4)

Task 13: CREATE src/game/DialogueManager.h
  IMPLEMENT: DialogueManager class (QObject) for dialogue state management
  FOLLOW pattern: src/game/QuestManager.h (lines 10-59)
  CLASS structure:
    - Inherit from QObject with Q_OBJECT macro
    - explicit DialogueManager(Player* player, QObject* parent = nullptr);
  MEMBERS:
    - Player* m_player (reference, not owned)
    - QMap<QString, DialogueTree*> m_dialogueTrees (all dialogues, owned)
    - DialogueTree* m_currentTree (current dialogue in progress)
    - DialogueNode* m_currentNode (current node in tree)
    - QString m_currentDialogueId (for tracking and saving)
  METHODS:
    - void loadDialogues(); (call DialogueFactory, populate m_dialogueTrees)
    - void startDialogue(const QString &dialogueId);
    - DialogueNode* getCurrentNode() const;
    - void selectChoice(int choiceIndex);
    - void advance(); (for linear dialogues with autoNextNodeId)
    - bool isDialogueActive() const;
    - void endDialogue();
  SIGNALS:
    - void dialogueStarted(const QString &dialogueId, const QString &npcName);
    - void dialogueNodeChanged(const QString &nodeId, const QString &speaker, const QString &text);
    - void dialogueEnded();
    - void effectTriggered(const QString &effectType, const QString &target, int value);
  PLACEMENT: cpp-qt-rpg/src/game/DialogueManager.h
  DEPENDENCIES: DialogueData.h (Task 1), Player.h updated (Task 5)

Task 14: CREATE src/game/DialogueManager.cpp
  IMPLEMENT: Dialogue state machine logic and effect application
  FOLLOW pattern: src/game/QuestManager.cpp (event-driven logic, lines 95-240)
  KEY implementations:
    1. loadDialogues():
       - QList<DialogueTree*> dialogues = DialogueFactory::getAllDialogues();
       - for (DialogueTree* tree : dialogues) { m_dialogueTrees[tree->id] = tree; }
    2. startDialogue(dialogueId):
       - Check if player has viewed (if unique): if (m_player->hasViewedDialogue(dialogueId)) return;
       - m_currentTree = m_dialogueTrees.value(dialogueId, nullptr);
       - if (!m_currentTree) return;
       - m_currentNode = m_currentTree->getStartNode();
       - m_currentDialogueId = dialogueId;
       - emit dialogueStarted(dialogueId, m_currentTree->npcName);
       - emit dialogueNodeChanged(m_currentNode->id, m_currentNode->speaker, m_currentNode->text);
    3. selectChoice(choiceIndex):
       - if (!m_currentNode || choiceIndex >= m_currentNode->choices.size()) return;
       - DialogueChoice &choice = m_currentNode->choices[choiceIndex];
       - Check requirements: if (choice.requiresLevel && m_player->level < choice.requiredLevel) return;
       - Apply effects: for (effect : choice.effects) { applyEffect(effect); }
       - Navigate to next node: m_currentNode = m_currentTree->getNode(choice.targetNodeId);
       - if (m_currentNode) { emit dialogueNodeChanged(...); }
       - else { endDialogue(); }
    4. advance():
       - if (!m_currentNode || m_currentNode->autoNextNodeId.isEmpty()) return;
       - m_currentNode = m_currentTree->getNode(m_currentNode->autoNextNodeId);
       - if (m_currentNode) { emit dialogueNodeChanged(...); }
       - else { endDialogue(); }
    5. endDialogue():
       - Mark as viewed: m_player->markDialogueViewed(m_currentDialogueId);
       - m_currentTree = nullptr; m_currentNode = nullptr; m_currentDialogueId = "";
       - emit dialogueEnded();
    6. applyEffect(const DialogueEffect &effect):
       - if (effect.type == "UnlockQuest") { emit effectTriggered("UnlockQuest", effect.target, 0); }
       - if (effect.type == "GiveGold") { m_player->gold += effect.value; }
       - if (effect.type == "GiveXP") { m_player->gainExperience(effect.value); }
       - if (effect.type == "GiveItem") { /* Create item via ItemFactory, add to inventory */ }
       - emit effectTriggered for all effects for UI notification
  PLACEMENT: cpp-qt-rpg/src/game/DialogueManager.cpp
  DEPENDENCIES: DialogueManager.h (Task 13), DialogueFactory.cpp (Task 8)

Task 15: CREATE src/game/StoryManager.h
  IMPLEMENT: StoryManager class (QObject) for event triggering
  FOLLOW pattern: QuestManager.h (QObject with signals)
  CLASS structure:
    - Inherit from QObject with Q_OBJECT
    - explicit StoryManager(Player* player, QObject* parent = nullptr);
  MEMBERS:
    - Player* m_player (reference)
    - QList<StoryEvent*> m_allEvents (all events, owned)
    - QMap<QString, StoryEvent*> m_eventMap (quick lookup)
  METHODS:
    - void loadEvents(); (call StoryEventFactory)
    - void checkEventTriggers(); (check all events for trigger conditions)
    - void triggerEvent(const QString &eventId);
    - void onQuestStarted(const QString &questId);
    - void onQuestCompleted(const QString &questId);
    - void onLevelReached(int level);
  SIGNALS:
    - void eventTriggered(const StoryEvent &event);
  PLACEMENT: cpp-qt-rpg/src/game/StoryManager.h
  DEPENDENCIES: StoryEvent.h (Task 3), Player.h updated (Task 5)

Task 16: CREATE src/game/StoryManager.cpp
  IMPLEMENT: Event trigger checking and sequencing
  FOLLOW pattern: QuestManager.cpp event handlers
  KEY implementations:
    1. loadEvents():
       - QList<StoryEvent*> events = StoryEventFactory::getAllEvents();
       - for (StoryEvent* event : events) { m_eventMap[event->eventId] = event; m_allEvents.append(event); }
    2. checkEventTriggers():
       - Loop all events, check trigger conditions:
       - if (event->triggerType == "level_reached" && m_player->level >= event->triggerId.toInt()) { triggerEvent(event->eventId); }
       - if (event->triggerType == "quest_complete" && player has completed quest) { triggerEvent(event->eventId); }
    3. triggerEvent(eventId):
       - StoryEvent* event = m_eventMap.value(eventId, nullptr);
       - if (!event) return;
       - Check if already viewed: if (m_player->hasViewedEvent(eventId)) return;
       - emit eventTriggered(*event);  // Copy event data for UI
       - m_player->markEventViewed(eventId);
    4. onQuestStarted(questId):
       - Find events with triggerType "quest_start" and triggerId matching questId
       - triggerEvent(eventId);
    5. onQuestCompleted(questId):
       - Find events with triggerType "quest_complete" and triggerId matching questId
       - triggerEvent(eventId);
    6. onLevelReached(level):
       - checkEventTriggers(); (checks all level-based triggers)
  PLACEMENT: cpp-qt-rpg/src/game/StoryManager.cpp
  DEPENDENCIES: StoryManager.h (Task 15), StoryEventFactory.cpp (Task 10)

Task 17: CREATE src/game/CodexManager.h
  IMPLEMENT: CodexManager class (QObject) for lore tracking
  FOLLOW pattern: QuestManager.h
  CLASS structure:
    - Inherit from QObject with Q_OBJECT
    - explicit CodexManager(Player* player, QObject* parent = nullptr);
  MEMBERS:
    - Player* m_player (reference)
    - QMap<QString, LoreEntry*> m_loreMap (all lore, owned)
    - QMap<QString, QList<LoreEntry*>> m_categoryMap (entries by category)
  METHODS:
    - void loadLoreEntries(); (call LoreFactory)
    - void checkDiscoveryTriggers(const QString &triggerString);
    - void unlockEntry(const QString &entryId);
    - LoreEntry* getEntry(const QString &entryId) const;
    - QList<LoreEntry*> getUnlockedEntries(const QString &category) const;
    - QList<LoreEntry*> getAllEntriesInCategory(const QString &category) const;
    - void onEnemyKilled(const QString &enemyName);
    - void onQuestCompleted(const QString &questId);
    - void onItemCollected(const QString &itemName);
  SIGNALS:
    - void loreUnlocked(const QString &entryId, const QString &title);
  PLACEMENT: cpp-qt-rpg/src/game/CodexManager.h
  DEPENDENCIES: LoreEntry.h (Task 4), Player.h updated (Task 5)

Task 18: CREATE src/game/CodexManager.cpp
  IMPLEMENT: Lore discovery logic and category management
  FOLLOW pattern: QuestManager.cpp
  KEY implementations:
    1. loadLoreEntries():
       - QList<LoreEntry*> entries = LoreFactory::getAllLoreEntries();
       - for (LoreEntry* entry : entries) {
       -     m_loreMap[entry->entryId] = entry;
       -     m_categoryMap[entry->category].append(entry);
       - }
    2. checkDiscoveryTriggers(triggerString):
       - Loop all lore entries: if (entry->discoveryTrigger == triggerString) { unlockEntry(entry->entryId); }
    3. unlockEntry(entryId):
       - if (m_player->hasUnlockedLore(entryId)) return;  // Already unlocked
       - m_player->unlockLore(entryId);
       - LoreEntry* entry = m_loreMap.value(entryId, nullptr);
       - if (entry) { emit loreUnlocked(entryId, entry->title); }
    4. getUnlockedEntries(category):
       - QList<LoreEntry*> result;
       - for (LoreEntry* entry : m_categoryMap[category]) {
       -     if (m_player->hasUnlockedLore(entry->entryId)) { result.append(entry); }
       - }
       - return result;
    5. onEnemyKilled(enemyName):
       - static QMap<QString, int> killCounts;  // Track kills
       - killCounts[enemyName]++;
       - checkDiscoveryTriggers(QString("kill_%1_%2").arg(enemyName).arg(killCounts[enemyName]));
    6. onQuestCompleted(questId):
       - checkDiscoveryTriggers(QString("quest_complete_%1").arg(questId));
    7. onItemCollected(itemName):
       - checkDiscoveryTriggers(QString("item_get_%1").arg(itemName));
  PLACEMENT: cpp-qt-rpg/src/game/CodexManager.cpp
  DEPENDENCIES: CodexManager.h (Task 17), LoreFactory.cpp (Task 12)

Task 19: UPDATE src/game/Game.h
  ADD: Narrative manager members and getters
  FOLLOW pattern: QuestManager member (line 46-48)
  ADDITIONS:
    - #include "DialogueManager.h" at top
    - #include "StoryManager.h"
    - #include "CodexManager.h"
    - DialogueManager* m_dialogueManager; (private member)
    - StoryManager* m_storyManager;
    - CodexManager* m_codexManager;
    - DialogueManager* getDialogueManager();  (public getter)
    - StoryManager* getStoryManager();
    - CodexManager* getCodexManager();
  PLACEMENT: Add members after m_questManager (around line 47)
  DEPENDENCIES: DialogueManager.h (Task 13), StoryManager.h (Task 15), CodexManager.h (Task 17)

Task 20: UPDATE src/game/Game.cpp
  MODIFY: Constructor, destructor, newGame/loadGame to integrate narrative managers
  FOLLOW pattern: QuestManager integration (lines 41-108)
  CHANGES:
    1. Constructor: Initialize all to nullptr in initializer list
       - m_dialogueManager(nullptr), m_storyManager(nullptr), m_codexManager(nullptr)
    2. newGame(): After creating QuestManager (around line 95):
       - m_dialogueManager = new DialogueManager(m_player, this);
       - m_dialogueManager->loadDialogues();
       - m_storyManager = new StoryManager(m_player, this);
       - m_storyManager->loadEvents();
       - m_codexManager = new CodexManager(m_player, this);
       - m_codexManager->loadLoreEntries();
    3. loadGame(): After creating QuestManager (around line 105):
       - Delete old managers: if (m_dialogueManager) delete m_dialogueManager;
       - Recreate: m_dialogueManager = new DialogueManager(m_player, this);
       - m_dialogueManager->loadDialogues();
       - (Repeat for StoryManager and CodexManager)
    4. Destructor: Add cleanup (before Game destructor ends):
       - if (m_dialogueManager) delete m_dialogueManager;
       - if (m_storyManager) delete m_storyManager;
       - if (m_codexManager) delete m_codexManager;
    5. Getter implementations:
       - DialogueManager* getDialogueManager() { return m_dialogueManager; }
       - StoryManager* getStoryManager() { return m_storyManager; }
       - CodexManager* getCodexManager() { return m_codexManager; }
    6. Connect managers to events (in newGame and loadGame):
       - connect(m_questManager, &QuestManager::questAccepted, m_storyManager, &StoryManager::onQuestStarted);
       - connect(m_questManager, &QuestManager::questCompleted, m_storyManager, &StoryManager::onQuestCompleted);
       - connect(m_questManager, &QuestManager::questCompleted, m_codexManager, &CodexManager::onQuestCompleted);
       - // After combat: connect to CodexManager::onEnemyKilled (see Task 21)
  CRITICAL: Managers must be recreated on load to reference new Player pointer
  DEPENDENCIES: Game.h updated (Task 19), all manager .cpp files (Tasks 14, 16, 18)

Task 21: MODIFY src/game/Game.cpp (Combat Integration)
  ADD: Lore unlock trigger on enemy kill
  FOLLOW pattern: Quest onCombatEnd integration
  CHANGES:
    - Find the location where combat ends with victory (after expReward/goldReward given)
    - Add: if (m_codexManager) { m_codexManager->onEnemyKilled(currentMonster->name); }
  PLACEMENT: In combat victory handling code (likely in Game::playerAttack() or Game::endCombat())
  DEPENDENCIES: Game.cpp updated (Task 20), CodexManager.cpp (Task 18)

Task 22: CREATE src/views/DialogueView.h
  IMPLEMENT: Dialogue UI with choice selection
  FOLLOW pattern: src/components/SkillSelectionDialog.h (choice UI, lines 8-24)
  CLASS structure:
    - Inherit from QDialog with Q_OBJECT
    - explicit DialogueView(QWidget *parent = nullptr);
  SIGNALS:
    - void choiceSelected(int choiceIndex);
    - void dialogueClosed();
  PUBLIC methods:
    - void displayNode(const QString &speaker, const QString &text, const QStringList &choiceTexts);
    - void setChoiceEnabled(int index, bool enabled);
  PROTECTED:
    - void keyPressEvent(QKeyEvent *event) override; (1-9 for choices, ESC for close)
  PRIVATE methods:
    - void setupUi();
    - void clearChoices();
  MEMBERS:
    - QLabel* m_speakerLabel;
    - QTextEdit* m_dialogueText;
    - QVBoxLayout* m_choicesLayout;
    - QList<QPushButton*> m_choiceButtons;
  PLACEMENT: cpp-qt-rpg/src/views/DialogueView.h
  DEPENDENCIES: None (Qt widgets only)

Task 23: CREATE src/views/DialogueView.cpp
  IMPLEMENT: Dialogue display with styled choice buttons
  FOLLOW pattern: src/components/SkillSelectionDialog.cpp (lines 1-85)
  KEY implementations:
    1. setupUi():
       - VBoxLayout main layout
       - Speaker label: XL font, bold, ACCENT color
       - Dialogue text: QTextEdit read-only, scrollable, CARD background
       - Choices layout: VBoxLayout for buttons
       - Apply Theme constants for all styling
    2. displayNode(speaker, text, choiceTexts):
       - clearChoices();
       - m_speakerLabel->setText(speaker);
       - m_dialogueText->setText(text);  // Plain text or HTML
       - for (int i = 0; i < choiceTexts.size(); ++i) {
       -     QPushButton *btn = new QPushButton(QString("[%1] %2").arg(i+1).arg(choiceTexts[i]));
       -     btn->setMinimumHeight(50);
       -     // Style with Theme constants
       -     connect(btn, &QPushButton::clicked, this, [this, i]() { emit choiceSelected(i); });
       -     m_choiceButtons.append(btn);
       -     m_choicesLayout->addWidget(btn);
       - }
    3. setChoiceEnabled(index, enabled):
       - if (index < m_choiceButtons.size()) {
       -     m_choiceButtons[index]->setEnabled(enabled);
       -     // Apply disabled styling
       - }
    4. clearChoices():
       - for (QPushButton *btn : m_choiceButtons) { delete btn; }
       - m_choiceButtons.clear();
    5. keyPressEvent(event):
       - if (event->key() == Qt::Key_Escape) { emit dialogueClosed(); reject(); }
       - if (event->key() >= Qt::Key_1 && event->key() <= Qt::Key_9) {
       -     int index = event->key() - Qt::Key_1;
       -     if (index < m_choiceButtons.size() && m_choiceButtons[index]->isEnabled()) {
       -         emit choiceSelected(index);
       -     }
       - }
  STYLING: Use Theme::CARD, PRIMARY, ACCENT, FOREGROUND for all elements
  PLACEMENT: cpp-qt-rpg/src/views/DialogueView.cpp
  DEPENDENCIES: DialogueView.h (Task 22), Theme.h

Task 24: CREATE src/views/StoryEventDialog.h
  IMPLEMENT: Full-screen story event/cutscene overlay
  FOLLOW pattern: src/components/CombatResultDialog.h (lines 7-14)
  CLASS structure:
    - Inherit from QDialog with Q_OBJECT
    - explicit StoryEventDialog(const StoryEvent &event, QWidget *parent = nullptr);
  PRIVATE methods:
    - void setupUi(const StoryEvent &event);
  MEMBERS:
    - qint64 m_eventStartTime; (for skip delay)
  PROTECTED:
    - void keyPressEvent(QKeyEvent *event) override; (ESC to skip after 1 second)
  PLACEMENT: cpp-qt-rpg/src/views/StoryEventDialog.h
  DEPENDENCIES: StoryEvent.h (Task 3)

Task 25: CREATE src/views/StoryEventDialog.cpp
  IMPLEMENT: Cinematic story event display
  FOLLOW pattern: src/components/CombatResultDialog.cpp (lines 1-112)
  KEY implementations:
    1. Constructor:
       - setModal(true);
       - setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);  // Full-screen feel
       - setMinimumSize(600, 400);
       - m_eventStartTime = QDateTime::currentMSecsSinceEpoch();
       - setupUi(event);
    2. setupUi(event):
       - VBoxLayout main
       - Background image (if available): QLabel with pixmap from event.imagePaths[0]
       - Title label: XXXL font, bold, centered, PRIMARY color
       - Event text: QTextEdit read-only, centered, large font, formatted with line breaks
       - Continue button: Large, themed, at bottom
       - Apply dark overlay effect if background image present
    3. keyPressEvent(event):
       - qint64 elapsed = QDateTime::currentMSecsSinceEpoch() - m_eventStartTime;
       - if (elapsed < 1000) return;  // Prevent accidental skip
       - if (event->key() == Qt::Key_Escape) { accept(); }
    4. Styling:
       - Use semi-transparent overlay for text readability
       - ACCENT border around content
       - Fade-in animation optional (QPropertyAnimation like MenuOverlay)
  PLACEMENT: cpp-qt-rpg/src/views/StoryEventDialog.cpp
  DEPENDENCIES: StoryEventDialog.h (Task 24), Theme.h

Task 26: CREATE src/views/LoreBookPage.h
  IMPLEMENT: Codex browser UI
  FOLLOW pattern: src/views/QuestLogPage.h (multi-pane UI, lines 14-34)
  CLASS structure:
    - Inherit from QWidget with Q_OBJECT
    - explicit LoreBookPage(QWidget *parent = nullptr);
  SIGNALS:
    - void backRequested();
  PUBLIC methods:
    - void updateLore(CodexManager* codexManager);
  PROTECTED:
    - void keyPressEvent(QKeyEvent *event) override;
  PRIVATE slots:
    - void handleCategoryChanged(int index);
    - void handleEntryClicked(LoreEntry *entry);
  PRIVATE methods:
    - void setupUi();
    - void refreshEntryList(const QString &category);
  MEMBERS:
    - CodexManager* m_codexManager (reference)
    - QLabel* m_titleLabel;
    - QTabWidget* m_categoryTabs; (or QListWidget for categories)
    - QListWidget* m_entryList; (left pane)
    - QTextEdit* m_entryDetails; (right pane)
    - QPushButton* m_backButton;
    - QString m_currentCategory;
  PLACEMENT: cpp-qt-rpg/src/views/LoreBookPage.h
  DEPENDENCIES: CodexManager.h (Task 17), LoreEntry.h (Task 4)

Task 27: CREATE src/views/LoreBookPage.cpp
  IMPLEMENT: Lore browsing with categories and details
  FOLLOW pattern: src/views/QuestLogPage.cpp (lines 1-250)
  KEY implementations:
    1. setupUi():
       - QHBoxLayout main (3-column: categories | entries | details)
       - Left: Category tabs (Bestiary, Items, World, Characters, Locations)
       - Middle: Entry list (titles only)
       - Right: Entry details (full text with image)
       - Back button at bottom
    2. updateLore(codexManager):
       - m_codexManager = codexManager;
       - refreshEntryList(m_currentCategory);
    3. handleCategoryChanged(index):
       - Map index to category string
       - m_currentCategory = category;
       - refreshEntryList(category);
    4. refreshEntryList(category):
       - m_entryList->clear();
       - QList<LoreEntry*> unlocked = m_codexManager->getUnlockedEntries(category);
       - for (LoreEntry* entry : unlocked) {
       -     QListWidgetItem *item = new QListWidgetItem(entry->title);
       -     item->setData(Qt::UserRole, QVariant::fromValue(static_cast<void*>(entry)));
       -     m_entryList->addItem(item);
       - }
    5. handleEntryClicked(entry):
       - Build HTML details:
       - QString html = QString("<h2 style='color: %1;'>%2</h2>").arg(Theme::PRIMARY.name(), entry->title);
       - html += QString("<p style='font-style: italic;'>%1</p>").arg(entry->shortDescription);
       - html += QString("<p>%1</p>").arg(entry->fullText);
       - if (!entry->imagePath.isEmpty()) { /* Add image */ }
       - m_entryDetails->setHtml(html);
    6. keyPressEvent(event):
       - ESC: emit backRequested();
       - Tab: Switch category
  STYLING: Use Theme constants, match QuestLogPage aesthetic
  PLACEMENT: cpp-qt-rpg/src/views/LoreBookPage.cpp
  DEPENDENCIES: LoreBookPage.h (Task 26), Theme.h

Task 28: UPDATE src/MainWindow.h
  ADD: Narrative view members, handlers, keyboard shortcuts
  FOLLOW pattern: QuestLogPage integration (lines 21-84)
  ADDITIONS:
    - #include "views/DialogueView.h" at top
    - #include "views/StoryEventDialog.h"
    - #include "views/LoreBookPage.h"
    - DialogueView* m_dialogueView; (private member)
    - LoreBookPage* m_loreBookPage;
    - void handleDialogueNodeChanged(const QString &nodeId, const QString &speaker, const QString &text); (private slot)
    - void handleDialogueChoiceSelected(int choiceIndex);
    - void handleDialogueEnded();
    - void handleStoryEventTriggered(const StoryEvent &event);
    - void handleLoreUnlocked(const QString &entryId, const QString &title);
    - void handleOpenLoreBook();
    - void handleLoreBookBack();
  PLACEMENT: Add members with other view pointers, add slots with other handlers
  DEPENDENCIES: DialogueView.h (Task 22), StoryEventDialog.h (Task 24), LoreBookPage.h (Task 26)

Task 29: UPDATE src/MainWindow.cpp
  MODIFY: Constructor to create narrative views, connect signals, add keyboard shortcuts
  FOLLOW pattern: QuestLogPage integration (lines 66-226)
  CHANGES:
    1. Constructor (around line 66):
       - m_dialogueView = new DialogueView();
       - connect(m_dialogueView, &DialogueView::choiceSelected, this, &MainWindow::handleDialogueChoiceSelected);
       - connect(m_dialogueView, &DialogueView::dialogueClosed, this, &MainWindow::handleDialogueEnded);
       - stackedWidget->addWidget(m_dialogueView);
       - m_loreBookPage = new LoreBookPage();
       - connect(m_loreBookPage, &LoreBookPage::backRequested, this, &MainWindow::handleLoreBookBack);
       - stackedWidget->addWidget(m_loreBookPage);
    2. Connect narrative manager signals (in newGame and loadGame, after managers created):
       - connect(m_game->getDialogueManager(), &DialogueManager::dialogueNodeChanged,
       -         this, &MainWindow::handleDialogueNodeChanged, Qt::UniqueConnection);
       - connect(m_game->getDialogueManager(), &DialogueManager::dialogueEnded,
       -         this, &MainWindow::handleDialogueEnded, Qt::UniqueConnection);
       - connect(m_game->getStoryManager(), &StoryManager::eventTriggered,
       -         this, &MainWindow::handleStoryEventTriggered, Qt::UniqueConnection);
       - connect(m_game->getCodexManager(), &CodexManager::loreUnlocked,
       -         this, &MainWindow::handleLoreUnlocked, Qt::UniqueConnection);
       - connect(m_game->getDialogueManager(), &DialogueManager::effectTriggered,
       -         this, &MainWindow::handleDialogueEffect, Qt::UniqueConnection);
    3. handleDialogueNodeChanged(nodeId, speaker, text):
       - QStringList choiceTexts;
       - DialogueNode* node = m_game->getDialogueManager()->getCurrentNode();
       - for (const DialogueChoice &choice : node->choices) { choiceTexts.append(choice.text); }
       - m_dialogueView->displayNode(speaker, text, choiceTexts);
       - Check choice requirements, disable if not met:
       - for (int i = 0; i < node->choices.size(); ++i) {
       -     if (node->choices[i].requiresLevel && m_game->getPlayer()->level < node->choices[i].requiredLevel) {
       -         m_dialogueView->setChoiceEnabled(i, false);
       -     }
       - }
       - stackedWidget->setCurrentWidget(m_dialogueView);
    4. handleDialogueChoiceSelected(choiceIndex):
       - m_game->getDialogueManager()->selectChoice(choiceIndex);
    5. handleDialogueEnded():
       - stackedWidget->setCurrentWidget(m_combatPage);  // Return to main view
    6. handleStoryEventTriggered(event):
       - StoryEventDialog dialog(event, this);
       - dialog.exec();  // Modal, blocks until player dismisses
    7. handleLoreUnlocked(entryId, title):
       - Show toast notification: "New Codex Entry: " + title
       - (Can use LogDisplay or create toast component)
    8. handleOpenLoreBook():
       - if (!m_game || !m_game->getCodexManager()) return;
       - m_loreBookPage->updateLore(m_game->getCodexManager());
       - stackedWidget->setCurrentWidget(m_loreBookPage);
    9. handleLoreBookBack():
       - stackedWidget->setCurrentWidget(m_combatPage);
    10. keyPressEvent() (add new shortcuts, around line 400):
       - case Qt::Key_D: startDialogue("elder_intro"); break;  // Example dialogue trigger
       - case Qt::Key_L: handleOpenLoreBook(); break;
  CRITICAL: Connect manager signals AFTER managers exist in newGame/loadGame
  DEPENDENCIES: MainWindow.h updated (Task 28), all view .cpp files (Tasks 23, 25, 27)

Task 30: UPDATE cpp-qt-rpg/CMakeLists.txt (Main Executable)
  ADD: All new source files to build targets
  FOLLOW pattern: Existing file lists (lines 23-64 for main)
  CHANGES:
    - Add to add_executable(pyrpg-qt ...) around line 23:
      - src/models/DialogueData.cpp
      - src/game/DialogueManager.cpp
      - src/game/StoryManager.cpp
      - src/game/CodexManager.cpp
      - src/game/factories/DialogueFactory.cpp
      - src/game/factories/StoryEventFactory.cpp
      - src/game/factories/LoreFactory.cpp
      - src/views/DialogueView.cpp
      - src/views/StoryEventDialog.cpp
      - src/views/LoreBookPage.cpp
  PLACEMENT: Add in alphabetical order within existing source list
  DEPENDENCIES: All previous implementation tasks completed

Task 31: CREATE tests/test_dialogue_models.cpp
  IMPLEMENT: Unit tests for DialogueData serialization
  FOLLOW pattern: tests/test_quest_models.cpp (lines 1-120)
  TEST cases:
    - testDialogueTreeCreation(): Verify tree structure
    - testDialogueNodeCreation(): Verify node with choices
    - testDialogueSerialization(): Save and load DialogueTree, compare fields
    - testDialogueChoiceEffects(): Verify effect structure
    - testDialogueTreeNavigation(): Test getNode() and getStartNode()
  STRUCTURE:
    - class TestDialogueModels : public QObject { Q_OBJECT private slots: ... };
    - QTEST_MAIN(TestDialogueModels)
    - #include "test_dialogue_models.moc"
  PLACEMENT: cpp-qt-rpg/tests/test_dialogue_models.cpp
  DEPENDENCIES: DialogueData.cpp (Task 2)

Task 32: CREATE tests/test_dialogue_system.cpp
  IMPLEMENT: Integration tests for DialogueManager
  FOLLOW pattern: tests/test_quest_system.cpp (lines 1-152)
  TEST cases:
    - testDialogueManagerLoad(): Verify dialogues load from factory
    - testStartDialogue(): Start dialogue, verify signals emitted
    - testChoiceSelection(): Select choice, verify navigation
    - testEffectApplication(): Choice effects applied to player
    - testConditionalChoices(): Disabled choices for requirements
    - testDialogueCompletion(): Dialogue ends, marked as viewed
    - testDialoguePersistence(): Save with viewed dialogues, load, verify state
  STRUCTURE: Same as test_dialogue_models.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_dialogue_system.cpp
  DEPENDENCIES: DialogueManager.cpp (Task 14), DialogueFactory.cpp (Task 8)

Task 33: CREATE tests/test_story_system.cpp
  IMPLEMENT: Integration tests for StoryManager
  FOLLOW pattern: test_quest_system.cpp
  TEST cases:
    - testStoryManagerLoad(): Verify events load
    - testEventTriggerOnQuestStart(): Quest accepted → event triggered
    - testEventTriggerOnQuestComplete(): Quest completed → event triggered
    - testEventTriggerOnLevel(): Player levels → event triggered
    - testEventViewedTracking(): Event viewed once, doesn't repeat
    - testEventPersistence(): Save with viewed events, load, verify
  PLACEMENT: cpp-qt-rpg/tests/test_story_system.cpp
  DEPENDENCIES: StoryManager.cpp (Task 16), StoryEventFactory.cpp (Task 10)

Task 34: CREATE tests/test_lore_system.cpp
  IMPLEMENT: Integration tests for CodexManager
  FOLLOW pattern: test_quest_system.cpp
  TEST cases:
    - testCodexManagerLoad(): Verify lore entries load
    - testLoreUnlockOnEnemyKill(): Kill enemy → lore unlocks
    - testLoreUnlockOnQuestComplete(): Complete quest → lore unlocks
    - testLoreUnlockDeduplication(): Same lore doesn't unlock twice
    - testLoreCategoryFiltering(): Get entries by category
    - testLorePersistence(): Save with unlocked lore, load, verify
  PLACEMENT: cpp-qt-rpg/tests/test_lore_system.cpp
  DEPENDENCIES: CodexManager.cpp (Task 18), LoreFactory.cpp (Task 12)

Task 35: UPDATE cpp-qt-rpg/CMakeLists.txt (Test Targets)
  ADD: New test executables and dependencies
  FOLLOW pattern: Existing test targets (lines 108-267)
  CHANGES:
    1. Add test_dialogue_models:
       - add_executable(test_dialogue_models tests/test_dialogue_models.cpp
       -     src/models/DialogueData.cpp
       - )
       - target_link_libraries(test_dialogue_models PRIVATE Qt6::Widgets Qt6::Test)
       - target_include_directories(test_dialogue_models PRIVATE src)
       - add_test(NAME DialogueModelsTest COMMAND test_dialogue_models)
    2. Add test_dialogue_system:
       - add_executable(test_dialogue_system tests/test_dialogue_system.cpp
       -     src/models/DialogueData.cpp
       -     src/models/Player.cpp
       -     src/models/Character.cpp
       -     src/game/DialogueManager.cpp
       -     src/game/factories/DialogueFactory.cpp
       -     src/game/factories/ItemFactory.cpp
       -     src/models/Item.cpp
       - )
       - target_link_libraries(test_dialogue_system PRIVATE Qt6::Widgets Qt6::Test)
       - target_include_directories(test_dialogue_system PRIVATE src)
       - add_test(NAME DialogueSystemTest COMMAND test_dialogue_system)
    3. Add test_story_system:
       - (Similar structure, include StoryManager, StoryEventFactory, Player, Character)
    4. Add test_lore_system:
       - (Similar structure, include CodexManager, LoreFactory, Player, Character)
    5. Update test_mainwindow: Add new model/manager files:
       - src/models/DialogueData.cpp
       - src/game/DialogueManager.cpp
       - src/game/StoryManager.cpp
       - src/game/CodexManager.cpp
       - (All factory files)
    6. Update test_persistence: Add DialogueData.cpp for serialization tests
  DEPENDENCIES: Test files created (Tasks 31-34)
```

### Implementation Patterns & Key Details

```cpp
// ============================================================================
// PATTERN 1: Dialogue Tree Structure
// ============================================================================
// File: src/models/DialogueData.h
// Follow: Quest.h nested struct pattern

struct DialogueEffect {
    QString type;     // "AdvanceQuest", "GiveItem", "GiveGold", "GiveXP", "UnlockQuest"
    QString target;   // Quest ID, item name, etc.
    int value;        // Amount for gold/XP
};

struct DialogueChoice {
    QString text;                     // "What's happening?"
    QString targetNodeId;             // "explain_situation"
    QList<DialogueEffect> effects;   // Effects applied when chosen
    bool requiresLevel;               // false by default
    int requiredLevel;                // 0 by default
};

struct DialogueNode {
    QString id;                       // "greeting"
    QString speaker;                  // "Village Elder"
    QString text;                     // "Greetings, brave adventurer..."
    QList<DialogueChoice> choices;   // Player response options
    QString autoNextNodeId;           // For linear dialogues (empty if branching)
    bool endsDialogue;                // true to end conversation
};

class DialogueTree {
public:
    QString id;                       // "elder_intro"
    QString npcName;                  // "Village Elder"
    QString startNodeId;              // "greeting"
    QMap<QString, DialogueNode> nodes; // All nodes in tree

    DialogueNode* getNode(const QString &nodeId);
    DialogueNode* getStartNode();

    friend QDataStream &operator<<(QDataStream &out, const DialogueTree &tree);
    friend QDataStream &operator>>(QDataStream &in, DialogueTree &tree);
};

// ============================================================================
// PATTERN 2: Dialogue Tree Serialization
// ============================================================================
// File: src/models/DialogueData.cpp
// CRITICAL: Nested structure serialization

QDataStream &operator<<(QDataStream &out, const DialogueTree &tree)
{
    out << tree.id << tree.npcName << tree.startNodeId;

    // Serialize nodes map
    out << quint32(tree.nodes.size());
    for (const DialogueNode &node : tree.nodes) {
        out << node.id << node.speaker << node.text << node.autoNextNodeId << node.endsDialogue;

        // Serialize choices
        out << quint32(node.choices.size());
        for (const DialogueChoice &choice : node.choices) {
            out << choice.text << choice.targetNodeId << choice.requiresLevel << choice.requiredLevel;

            // Serialize effects
            out << quint32(choice.effects.size());
            for (const DialogueEffect &effect : choice.effects) {
                out << effect.type << effect.target << effect.value;
            }
        }
    }

    return out;
}

QDataStream &operator>>(QDataStream &in, DialogueTree &tree)
{
    in >> tree.id >> tree.npcName >> tree.startNodeId;

    quint32 nodeCount;
    in >> nodeCount;
    tree.nodes.clear();

    for (quint32 i = 0; i < nodeCount; ++i) {
        DialogueNode node;
        in >> node.id >> node.speaker >> node.text >> node.autoNextNodeId >> node.endsDialogue;

        quint32 choiceCount;
        in >> choiceCount;
        for (quint32 j = 0; j < choiceCount; ++j) {
            DialogueChoice choice;
            in >> choice.text >> choice.targetNodeId >> choice.requiresLevel >> choice.requiredLevel;

            quint32 effectCount;
            in >> effectCount;
            for (quint32 k = 0; k < effectCount; ++k) {
                DialogueEffect effect;
                in >> effect.type >> effect.target >> effect.value;
                choice.effects.append(effect);
            }
            node.choices.append(choice);
        }

        tree.nodes[node.id] = node;
    }

    return in;
}

// ============================================================================
// PATTERN 3: DialogueFactory Hardcoded Trees
// ============================================================================
// File: src/game/factories/DialogueFactory.cpp
// Follow: QuestFactory.cpp pattern with static cache

DialogueTree* DialogueFactory::createDialogue(const QString &dialogueId)
{
    // Static cache to prevent memory leaks
    static QMap<QString, DialogueTree*> cache;

    if (cache.isEmpty()) {
        // Initialize all dialogues once

        // Dialogue 1: Village Elder Introduction
        DialogueTree* elderIntro = new DialogueTree();
        elderIntro->id = "elder_intro";
        elderIntro->npcName = "Village Elder";
        elderIntro->startNodeId = "greeting";

        // Node 1: Greeting
        DialogueNode greeting;
        greeting.id = "greeting";
        greeting.speaker = "Village Elder";
        greeting.text = R"(Greetings, brave adventurer. Dark times have fallen upon our village.
Shadow creatures emerge from the forest at night, and our people live in fear.)";
        greeting.endsDialogue = false;

        DialogueChoice choice1;
        choice1.text = "What's happening here?";
        choice1.targetNodeId = "explain";

        DialogueChoice choice2;
        choice2.text = "I'll help immediately!";
        choice2.targetNodeId = "accept_quest";

        greeting.choices.append(choice1);
        greeting.choices.append(choice2);
        elderIntro->nodes["greeting"] = greeting;

        // Node 2: Explanation
        DialogueNode explain;
        explain.id = "explain";
        explain.speaker = "Village Elder";
        explain.text = R"(For generations, the Shadow Wolves stayed deep in the Whispering Woods.
But something has changed. They grow bolder, venturing closer each night.
We need someone brave enough to drive them back.)";
        explain.endsDialogue = false;

        DialogueChoice choice3;
        choice3.text = "I'll take care of it.";
        choice3.targetNodeId = "accept_quest";

        DialogueChoice choice4;
        choice4.text = "This sounds dangerous. I need time to think.";
        choice4.targetNodeId = "goodbye";

        explain.choices.append(choice3);
        explain.choices.append(choice4);
        elderIntro->nodes["explain"] = explain;

        // Node 3: Accept Quest
        DialogueNode acceptQuest;
        acceptQuest.id = "accept_quest";
        acceptQuest.speaker = "Village Elder";
        acceptQuest.text = R"(Thank you, brave one. May fortune favor you in the Whispering Woods.
Defeat at least three Shadow Wolves and return to me with news of your victory.)";
        acceptQuest.endsDialogue = true;

        // Add effect: Unlock quest
        DialogueChoice choice5;
        choice5.text = "I won't let you down.";
        choice5.targetNodeId = "";  // Empty = end dialogue

        DialogueEffect unlockEffect;
        unlockEffect.type = "UnlockQuest";
        unlockEffect.target = "main_quest_01";
        unlockEffect.value = 0;
        choice5.effects.append(unlockEffect);

        acceptQuest.choices.append(choice5);
        elderIntro->nodes["accept_quest"] = acceptQuest;

        // Node 4: Goodbye
        DialogueNode goodbye;
        goodbye.id = "goodbye";
        goodbye.speaker = "Village Elder";
        goodbye.text = "Very well. Return when you're ready to face the shadows.";
        goodbye.endsDialogue = true;

        DialogueChoice choice6;
        choice6.text = "I'll be back.";
        choice6.targetNodeId = "";
        goodbye.choices.append(choice6);

        elderIntro->nodes["goodbye"] = goodbye;

        cache["elder_intro"] = elderIntro;

        // Add more dialogues...
        // (Dialogue 2: Merchant, Dialogue 3: Scholar, etc.)
    }

    return cache.value(dialogueId, nullptr);
}

// ============================================================================
// PATTERN 4: DialogueManager State Machine
// ============================================================================
// File: src/game/DialogueManager.cpp

void DialogueManager::startDialogue(const QString &dialogueId)
{
    // Check if already viewed (for unique dialogues)
    if (m_player->hasViewedDialogue(dialogueId)) {
        qDebug() << "Dialogue already viewed:" << dialogueId;
        return;
    }

    m_currentTree = m_dialogueTrees.value(dialogueId, nullptr);
    if (!m_currentTree) {
        qWarning() << "Dialogue tree not found:" << dialogueId;
        return;
    }

    m_currentNode = m_currentTree->getStartNode();
    if (!m_currentNode) {
        qWarning() << "Start node not found in dialogue:" << dialogueId;
        return;
    }

    m_currentDialogueId = dialogueId;

    emit dialogueStarted(dialogueId, m_currentTree->npcName);
    emit dialogueNodeChanged(m_currentNode->id, m_currentNode->speaker, m_currentNode->text);
}

void DialogueManager::selectChoice(int choiceIndex)
{
    if (!m_currentNode) return;
    if (choiceIndex < 0 || choiceIndex >= m_currentNode->choices.size()) {
        qWarning() << "Invalid choice index:" << choiceIndex;
        return;
    }

    const DialogueChoice &choice = m_currentNode->choices[choiceIndex];

    // Check requirements
    if (choice.requiresLevel && m_player->level < choice.requiredLevel) {
        qDebug() << "Choice requires level" << choice.requiredLevel << "but player is" << m_player->level;
        return;  // Don't allow selection
    }

    // Apply effects
    for (const DialogueEffect &effect : choice.effects) {
        applyEffect(effect);
    }

    // Navigate to next node
    if (choice.targetNodeId.isEmpty() || m_currentNode->endsDialogue) {
        endDialogue();
        return;
    }

    m_currentNode = m_currentTree->getNode(choice.targetNodeId);
    if (m_currentNode) {
        emit dialogueNodeChanged(m_currentNode->id, m_currentNode->speaker, m_currentNode->text);

        // Check if new node ends dialogue
        if (m_currentNode->endsDialogue && m_currentNode->choices.isEmpty()) {
            endDialogue();
        }
    } else {
        endDialogue();
    }
}

void DialogueManager::applyEffect(const DialogueEffect &effect)
{
    if (effect.type == "UnlockQuest") {
        emit effectTriggered("UnlockQuest", effect.target, 0);
    } else if (effect.type == "GiveGold") {
        m_player->gold += effect.value;
        emit effectTriggered("GiveGold", "", effect.value);
    } else if (effect.type == "GiveXP") {
        m_player->gainExperience(effect.value);
        emit effectTriggered("GiveXP", "", effect.value);
    } else if (effect.type == "GiveItem") {
        // Create item via ItemFactory
        Item* item = ItemFactory::createItem(effect.target);
        if (item) {
            m_player->inventory.append(item);
            emit effectTriggered("GiveItem", effect.target, 1);
        }
    } else if (effect.type == "AdvanceQuest") {
        emit effectTriggered("AdvanceQuest", effect.target, effect.value);
    }
}

void DialogueManager::endDialogue()
{
    if (!m_currentDialogueId.isEmpty()) {
        m_player->markDialogueViewed(m_currentDialogueId);
    }

    m_currentTree = nullptr;
    m_currentNode = nullptr;
    m_currentDialogueId = "";

    emit dialogueEnded();
}

// ============================================================================
// PATTERN 5: StoryManager Event Triggers
// ============================================================================
// File: src/game/StoryManager.cpp

void StoryManager::onQuestCompleted(const QString &questId)
{
    for (StoryEvent* event : m_allEvents) {
        if (event->triggerType == "quest_complete" && event->triggerId == questId) {
            triggerEvent(event->eventId);
        }
    }
}

void StoryManager::triggerEvent(const QString &eventId)
{
    StoryEvent* event = m_eventMap.value(eventId, nullptr);
    if (!event) return;

    // Check if already viewed (prevent repeats)
    if (m_player->hasViewedEvent(eventId)) {
        qDebug() << "Story event already viewed:" << eventId;
        return;
    }

    // Check prerequisites
    for (const QString &prereq : event->prerequisites) {
        if (prereq.startsWith("quest_")) {
            QString questId = prereq.mid(6);  // Remove "quest_" prefix
            Quest* quest = /* Get from QuestManager */;
            if (!quest || !quest->isComplete()) {
                qDebug() << "Event prerequisite not met:" << prereq;
                return;
            }
        } else if (prereq.startsWith("level_")) {
            int requiredLevel = prereq.mid(6).toInt();
            if (m_player->level < requiredLevel) {
                qDebug() << "Event requires level" << requiredLevel;
                return;
            }
        }
    }

    // Emit event (copy event data for UI)
    emit eventTriggered(*event);

    // Mark as viewed
    m_player->markEventViewed(eventId);
}

// ============================================================================
// PATTERN 6: CodexManager Lore Discovery
// ============================================================================
// File: src/game/CodexManager.cpp

void CodexManager::onEnemyKilled(const QString &enemyName)
{
    // Track kill counts per enemy
    static QMap<QString, int> killCounts;
    killCounts[enemyName]++;

    int kills = killCounts[enemyName];
    QString trigger = QString("kill_%1_%2").arg(enemyName).arg(kills);

    checkDiscoveryTriggers(trigger);
}

void CodexManager::checkDiscoveryTriggers(const QString &triggerString)
{
    for (LoreEntry* entry : m_loreMap.values()) {
        if (entry->discoveryTrigger == triggerString) {
            unlockEntry(entry->entryId);
        }
    }
}

void CodexManager::unlockEntry(const QString &entryId)
{
    // Check if already unlocked
    if (m_player->hasUnlockedLore(entryId)) {
        return;
    }

    m_player->unlockLore(entryId);

    LoreEntry* entry = m_loreMap.value(entryId, nullptr);
    if (entry) {
        emit loreUnlocked(entryId, entry->title);
    }
}

QList<LoreEntry*> CodexManager::getUnlockedEntries(const QString &category) const
{
    QList<LoreEntry*> result;

    for (LoreEntry* entry : m_categoryMap.value(category)) {
        if (m_player->hasUnlockedLore(entry->entryId)) {
            result.append(entry);
        }
    }

    return result;
}

// ============================================================================
// PATTERN 7: DialogueView Choice UI
// ============================================================================
// File: src/views/DialogueView.cpp

void DialogueView::displayNode(const QString &speaker, const QString &text, const QStringList &choiceTexts)
{
    m_speakerLabel->setText(speaker);
    m_dialogueText->setText(text);

    // Clear previous choices
    clearChoices();

    // Create choice buttons
    for (int i = 0; i < choiceTexts.size(); ++i) {
        QPushButton *btn = new QPushButton(QString("[%1] %2").arg(i + 1).arg(choiceTexts[i]));
        btn->setMinimumHeight(50);
        btn->setCursor(Qt::PointingHandCursor);

        btn->setStyleSheet(QString(
            "QPushButton {"
            "    background-color: %1;"
            "    color: %2;"
            "    border: 2px solid %3;"
            "    border-radius: %4px;"
            "    padding: %5px;"
            "    font-size: %6px;"
            "    text-align: left;"
            "}"
            "QPushButton:hover {"
            "    background-color: %7;"
            "    border-color: %8;"
            "}"
            "QPushButton:disabled {"
            "    background-color: %9;"
            "    color: %10;"
            "    border-color: %11;"
            "}"
        ).arg(Theme::CARD.name())
         .arg(Theme::FOREGROUND.name())
         .arg(Theme::BORDER.name())
         .arg(Theme::BORDER_RADIUS_MD)
         .arg(Theme::SPACING_MD)
         .arg(Theme::FONT_SIZE_MD)
         .arg(Theme::MUTED.name())
         .arg(Theme::ACCENT.name())
         .arg(Theme::MUTED.name())
         .arg(Theme::MUTED_FOREGROUND.name())
         .arg(Theme::MUTED.name()));

        connect(btn, &QPushButton::clicked, this, [this, i]() {
            emit choiceSelected(i);
        });

        m_choiceButtons.append(btn);
        m_choicesLayout->addWidget(btn);
    }
}

void DialogueView::setChoiceEnabled(int index, bool enabled)
{
    if (index >= 0 && index < m_choiceButtons.size()) {
        m_choiceButtons[index]->setEnabled(enabled);
        if (!enabled) {
            m_choiceButtons[index]->setToolTip("Requirements not met");
        }
    }
}

void DialogueView::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        emit dialogueClosed();
        reject();
        return;
    }

    // Number keys 1-9 select choices
    if (event->key() >= Qt::Key_1 && event->key() <= Qt::Key_9) {
        int index = event->key() - Qt::Key_1;
        if (index < m_choiceButtons.size() && m_choiceButtons[index]->isEnabled()) {
            emit choiceSelected(index);
        }
        return;
    }

    QDialog::keyPressEvent(event);
}

// ============================================================================
// PATTERN 8: MainWindow Narrative Integration
// ============================================================================
// File: src/MainWindow.cpp

void MainWindow::handleDialogueNodeChanged(const QString &nodeId, const QString &speaker, const QString &text)
{
    DialogueNode* node = m_game->getDialogueManager()->getCurrentNode();
    if (!node) return;

    // Build choice texts
    QStringList choiceTexts;
    for (const DialogueChoice &choice : node->choices) {
        choiceTexts.append(choice.text);
    }

    // Display dialogue
    m_dialogueView->displayNode(speaker, text, choiceTexts);

    // Check requirements and disable invalid choices
    for (int i = 0; i < node->choices.size(); ++i) {
        const DialogueChoice &choice = node->choices[i];
        bool enabled = true;

        if (choice.requiresLevel && m_game->getPlayer()->level < choice.requiredLevel) {
            enabled = false;
        }

        m_dialogueView->setChoiceEnabled(i, enabled);
    }

    // Switch to dialogue view
    stackedWidget->setCurrentWidget(m_dialogueView);
    m_dialogueView->setFocus();
}

void MainWindow::handleDialogueChoiceSelected(int choiceIndex)
{
    m_game->getDialogueManager()->selectChoice(choiceIndex);
}

void MainWindow::handleDialogueEnded()
{
    // Return to previous view (typically combat page)
    stackedWidget->setCurrentWidget(m_combatPage);
}

void MainWindow::handleStoryEventTriggered(const StoryEvent &event)
{
    // Show modal story event dialog
    StoryEventDialog dialog(event, this);
    dialog.exec();  // Blocks until player dismisses
}

void MainWindow::handleLoreUnlocked(const QString &entryId, const QString &title)
{
    // Show notification (can use LogDisplay or toast)
    QString message = QString("New Codex Entry: %1").arg(title);
    m_combatPage->addLogEntry(message, "success");  // If combat log accessible

    // Or create toast notification component for non-intrusive notification
}

// ============================================================================
// PATTERN 9: Player Serialization Version 4
// ============================================================================
// File: src/models/Player.cpp

QDataStream &operator<<(QDataStream &out, const Player &p)
{
    // Write version 4 (was 3 for quests)
    out << quint32(4);

    // Base class
    out << static_cast<const Character&>(p);

    // Player-specific data
    out << p.characterClass << p.experience << p.nextLevelExperience
        << p.strength << p.dexterity << p.intelligence << p.vitality
        << p.maxMana << p.mana << p.gold << p.statPoints << p.skillPoints;

    // Skills (existing version 1 data)
    QList<Skill> skillList;
    for (Skill* skill : p.skills) {
        if (skill) skillList.append(*skill);
    }
    out << skillList;

    // Equipment (existing version 1 data)
    out << p.equipment;

    // Inventory (existing version 2 data)
    QList<Item> itemList;
    for (Item* item : p.inventory) {
        if (item) itemList.append(*item);
    }
    out << itemList;

    // Quests (existing version 3 data)
    QList<Quest> questList;
    for (Quest* quest : p.quests) {
        if (quest) questList.append(*quest);
    }
    out << questList;

    // NEW VERSION 4: Narrative tracking
    out << p.viewedDialogueIds;
    out << p.viewedEventIds;
    out << p.unlockedLoreEntries;

    return out;
}

QDataStream &operator>>(QDataStream &in, Player &p)
{
    quint32 version;
    in >> version;

    // Base class
    Character c;
    in >> c;
    static_cast<Character&>(p) = c;

    // Player-specific data
    in >> p.characterClass >> p.experience >> p.nextLevelExperience
       >> p.strength >> p.dexterity >> p.intelligence >> p.vitality
       >> p.maxMana >> p.mana >> p.gold >> p.statPoints >> p.skillPoints;

    // Skills (version 1+)
    QList<Skill> skillList;
    in >> skillList;
    qDeleteAll(p.skills);
    p.skills.clear();
    for (const Skill &skill : skillList) {
        p.skills.append(new Skill(skill));
    }

    // Equipment (version 1+)
    in >> p.equipment;

    // Inventory (version 2+)
    if (version >= 2) {
        QList<Item> itemList;
        in >> itemList;
        qDeleteAll(p.inventory);
        p.inventory.clear();
        for (const Item &item : itemList) {
            p.inventory.append(new Item(item));
        }
    }

    // Quests (version 3+)
    if (version >= 3) {
        QList<Quest> questList;
        in >> questList;
        qDeleteAll(p.quests);
        p.quests.clear();
        for (const Quest &quest : questList) {
            p.quests.append(new Quest(quest));
        }
    }

    // Narrative tracking (version 4+)
    if (version >= 4) {
        in >> p.viewedDialogueIds;
        in >> p.viewedEventIds;
        in >> p.unlockedLoreEntries;
    }

    return in;
}
```

### Integration Points

```yaml
DIALOGUE_SYSTEM:
  - location: Quest acceptance → Start dialogue with quest giver
  - trigger: QuestManager::acceptQuest() → DialogueManager::startDialogue("elder_intro")
  - effects: Dialogue choices can unlock quests via DialogueEffect

STORY_EVENTS:
  - location: Quest milestones → Story events
  - trigger: QuestManager::questAccepted signal → StoryManager::onQuestStarted()
  - trigger: QuestManager::questCompleted signal → StoryManager::onQuestCompleted()
  - display: StoryEventDialog shown modally when event triggered

LORE_SYSTEM:
  - location: Combat victory → Lore unlock
  - trigger: Game::endCombat() → CodexManager::onEnemyKilled()
  - location: Quest completion → Lore unlock
  - trigger: QuestManager::questCompleted → CodexManager::onQuestCompleted()
  - notification: CodexManager::loreUnlocked signal → MainWindow shows toast

SAVE_SYSTEM:
  - location: Player serialization (Version 4)
  - additions: viewedDialogueIds, viewedEventIds, unlockedLoreEntries
  - backward_compat: if (version >= 4) conditional load

MAINWINDOW_KEYBOARD:
  - location: MainWindow::keyPressEvent()
  - add: Qt::Key_D → Start dialogue (context-dependent, e.g., near NPC)
  - add: Qt::Key_L → Open lore book
  - existing: Qt::Key_Q → Quest log (already exists from Phase 1-2)

CMAKE_BUILD:
  - file: cpp-qt-rpg/CMakeLists.txt
  - add_to_main: All new .cpp files (DialogueData, managers, factories, views)
  - add_to_tests: New model/manager files to test executables
  - new_tests: test_dialogue_models, test_dialogue_system, test_story_system, test_lore_system
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# After creating model files
cd cpp-qt-rpg/build
cmake ..
make src/models/DialogueData.cpp  # Verify syntax

# After creating manager files
make src/game/DialogueManager.cpp
make src/game/StoryManager.cpp
make src/game/CodexManager.cpp

# After creating view files
make src/views/DialogueView.cpp
make src/views/StoryEventDialog.cpp
make src/views/LoreBookPage.cpp

# Full build
cd cpp-qt-rpg/build
cmake ..
make

# Expected: Zero compile errors. Fix any errors before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test dialogue model serialization
cd cpp-qt-rpg/build
./test_dialogue_models

# Expected output:
# ********* Start testing of TestDialogueModels *********
# PASS   : TestDialogueModels::testDialogueTreeCreation()
# PASS   : TestDialogueModels::testDialogueSerialization()
# ********* Finished testing of TestDialogueModels *********

# Test DialogueManager integration
./test_dialogue_system

# Test StoryManager integration
./test_story_system

# Test CodexManager integration
./test_lore_system

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
# 2. Press D or interact with NPC → Dialogue appears
#    - Verify dialogue text displays
#    - Verify choices show (1-4)
# 3. Select choice 1 → Dialogue advances
#    - Verify next dialogue node shows
# 4. Select final choice → Dialogue ends, quest unlocked
#    - Verify quest appears in Quest Log (Q)
# 5. Complete quest objective (kill enemies)
# 6. Story event cutscene appears
#    - Verify full-screen narrative displays
#    - ESC to skip after 1 second
# 7. Defeat first enemy type 3 times
# 8. Check lore book (L key)
#    - Verify bestiary entry unlocked
#    - Verify entry shows full text
# 9. Open lore book → Select category
#    - Verify only unlocked entries show
# 10. Save game (slot 1)
# 11. Exit and reload save
#     - Verify viewed dialogues don't repeat
#     - Verify story events don't repeat
#     - Verify lore remains unlocked

# Expected: All manual tests pass, no crashes, state persists correctly
```

### Level 4: Save/Load Compatibility Testing

```bash
# Test backward compatibility
# 1. If you have a Phase 1-2 save (Version 3), load it
# 2. Verify loads successfully with empty narrative lists
# 3. Play and unlock dialogue/lore
# 4. Save as Version 4
# 5. Load Version 4 save
# 6. Verify all narrative data preserved

# Test dialogue tree navigation
# 1. Start dialogue with multiple branches
# 2. Save mid-dialogue (should end dialogue on save)
# 3. Load save
# 4. Verify dialogue state (should not be mid-conversation)

# Test lore persistence
# 1. Unlock 5 lore entries
# 2. Save and load
# 3. Verify all 5 entries remain unlocked
# 4. Verify notification doesn't show again for already-unlocked entries
```

## Final Validation Checklist

### Technical Validation

- [ ] All files compile without warnings: `make` succeeds with 0 warnings
- [ ] Unit tests pass: All 4 new test executables pass 100%
- [ ] Integration tests pass: `ctest` shows 0 failures
- [ ] No memory leaks: Dialogue trees properly cleaned up
- [ ] No segfaults: All null pointer checks in place
- [ ] Save file version 4 correctly incremented

### Feature Validation

**Dialogue System**:
- [ ] Dialogue view opens and displays NPC name, text, choices
- [ ] Selecting choice navigates to next node or ends dialogue
- [ ] Dialogue effects apply (quest unlock, gold/XP given)
- [ ] Conditional choices disabled if requirements not met
- [ ] Unique dialogues tracked, can't repeat
- [ ] Dialogue state persists through save/load

**Story Event System**:
- [ ] Story events trigger at quest milestones (start, complete)
- [ ] StoryEventDialog displays full-screen with narrative text
- [ ] ESC skips event after 1-second delay
- [ ] Viewed events marked, don't repeat
- [ ] Event state persists through save/load

**Lore System**:
- [ ] Lore unlocks on enemy kills (after X kills)
- [ ] Lore unlocks on quest completion
- [ ] Lore Book (L key) opens and displays categories
- [ ] Selecting category shows unlocked entries
- [ ] Selecting entry shows full text with image
- [ ] Lore notification shows on unlock
- [ ] Lore state persists through save/load

**Integration**:
- [ ] Dialogue integrates with quest system (unlock quests via choices)
- [ ] Story events integrate with quest system (trigger on milestones)
- [ ] Lore integrates with combat (unlock on enemy kills)
- [ ] All managers owned by Game, lifecycle managed correctly
- [ ] Keyboard shortcuts work (D for dialogue context, L for lore book)

### Code Quality Validation

- [ ] Follows existing codebase patterns (verified against pattern files)
- [ ] All Theme constants used (no hardcoded colors/sizes)
- [ ] Signal/slot connections follow naming conventions
- [ ] QDataStream serialization follows versioning pattern
- [ ] Memory management follows Qt ownership patterns
- [ ] CMakeLists.txt updated correctly (files in main + tests)
- [ ] Factory classes use static caching pattern to prevent leaks
- [ ] No circular dependencies in dialogue trees

### Documentation Validation

- [ ] Dialogue tree structures documented with comments
- [ ] Story event trigger logic documented
- [ ] Lore discovery triggers documented
- [ ] Manager public APIs documented
- [ ] Factory definitions have clear comments explaining narratives
- [ ] Complex algorithms (dialogue navigation, trigger checking) have explanatory comments

## Anti-Patterns to Avoid

**Dialogue System**:
- ❌ Don't create circular dialogue references (A → B → A infinite loop)
- ❌ Don't use exec() for DialogueView - use show() with signal connections (Qt6 best practice)
- ❌ Don't forget to clear choice buttons before displaying new node
- ❌ Don't apply dialogue effects before checking choice requirements
- ❌ Don't hardcode dialogue text in manager - keep all text in factory
- ❌ Don't forget to mark dialogue as viewed in endDialogue()

**Story Event System**:
- ❌ Don't use QTimer delays in modal dialogs (event loop blocked)
- ❌ Don't trigger events without checking viewed status (causes repeats)
- ❌ Don't forget the 1-second skip delay (prevents accidental skips)
- ❌ Don't emit eventTriggered signal without copying event data (pointer may be deleted)

**Lore System**:
- ❌ Don't show lore unlock notification if already unlocked
- ❌ Don't forget to track kill counts per enemy (not global kill count)
- ❌ Don't hardcode discovery triggers - use factory pattern for maintainability
- ❌ Don't display undiscovered lore entries (spoils discovery)

**Save/Load**:
- ❌ Don't forget to increment Player version to 4
- ❌ Don't serialize without conditional version checks (breaks old saves)
- ❌ Don't skip backward compatibility testing
- ❌ Don't forget to recreate managers on load (they reference Player pointer)

**UI**:
- ❌ Don't use hardcoded colors/sizes - always use Theme constants
- ❌ Don't forget keyboard shortcuts (1-9 for choices, ESC for close, L for lore book)
- ❌ Don't create choice buttons without tracking them for cleanup
- ❌ Don't call setCurrentWidget() without updateXxx() first (stale data)

**General**:
- ❌ Don't add files to main executable without adding to test executables
- ❌ Don't connect manager signals before managers exist (crashes)
- ❌ Don't forget #include "test_xxx.moc" at end of test files
- ❌ Don't use nested event loops unnecessarily (prefer async patterns)
- ❌ Don't emit signals in tight loops without batching

---

## Confidence Score: 9/10

**Rationale**: This PRP has comprehensive context from extensive codebase and external research:

**Strengths**:
- ✅ Complete dialogue UI patterns from CombatResultDialog, SkillSelectionDialog, MenuOverlay
- ✅ Full event system architecture from QuestManager, Game signal patterns
- ✅ Factory patterns from all 4 existing factories (Item, Monster, Skill, Quest)
- ✅ Save/load versioning strategy with backward compatibility
- ✅ Testing patterns from 8 existing test files
- ✅ External research: Qt6 modern dialog patterns, RPG dialogue tree architectures, narrative sequencing
- ✅ Theme integration patterns documented with specific constants
- ✅ Memory management patterns (qDeleteAll, Qt ownership)
- ✅ CMake build configuration with exact patterns to follow
- ✅ Specific line references for all critical patterns

**Deduction (-1)**:
- Minor uncertainty around exact dialogue trigger points (when to start NPC dialogues - manual via key press vs. automatic proximity detection)
- Dialogue UI could use non-modal approach for better UX, but modal is simpler for Phase 3 MVP

**Validation**: An AI agent can implement Phase 3 successfully with only:
1. This PRP
2. Access to codebase files (for verification and pattern reference)
3. Training data for Qt6/C++ knowledge

All patterns, factory structures, UI layouts, serialization strategies, testing approaches, and integration points are explicitly documented with file:line references and executable patterns. The external research provides best practices for dialogue trees (branch-and-bottleneck pattern) and modern Qt6 non-blocking dialogs.

---

**Document Status**: ✅ Complete and Ready for Implementation
**Next Steps**: Execute Phase 3 implementation following task order
**Estimated Implementation Time**: 2-3 weeks (depending on content authoring for dialogues/events/lore)
**Dependencies**: Phase 1-2 (Quest System) must be complete - ✅ Already implemented