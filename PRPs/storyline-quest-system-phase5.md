name: "Storyline & Quest System - Phase 5: Lore System Completion, Comprehensive Testing, and Polish"
description: |
  Implementation PRP for completing the lore/codex system with rich content, comprehensive testing
  of all quest/narrative systems, final boss balancing, UI/UX polish, and documentation updates.
  This is the final polish phase that ensures all storyline systems work together seamlessly.

---

## Goal

**Feature Goal**: Complete the lore/codex system with 20-30 rich entries, add lore to all relevant items, implement comprehensive testing for all storyline systems (quests, dialogue, lore, final boss), balance final boss difficulty, polish UI/UX across all narrative pages, and update documentation for maintainability.

**Deliverable**:
- 20-30 new LoreEntry definitions across all 5 categories (Bestiary, Items, World, Characters, Locations)
- Item model extended with loreId field linking items to lore entries
- Lore discovery notifications integrated with LogDisplay combat log
- Comprehensive test suite (4 new test files: lore_discovery, item_lore, lore_notification, lore_integration)
- Quest progression edge case testing (dialogue branching, save/load integrity, final boss phases)
- Final boss difficulty tuning (playtesting metrics, phase balance adjustments)
- UI/UX polish for LoreBookPage (search, sorting, progress indicators, locked entry previews)
- Updated CLAUDE.md documentation with lore system architecture
- Player-facing README updates with lore discovery instructions

**Success Definition**:
- All 20-30 lore entries authored with consistent voice/tone and actionable content
- Every legendary/rare item has associated lore entry (loreId field populated)
- Lore discoveries trigger combat log notifications with lore title
- All unit tests pass: test_lore_discovery, test_item_lore, test_lore_notification, test_lore_integration
- Integration tests verify complete quest → lore → notification → save/load flows
- Final boss balanced: requires 3-5 attempts for skilled player at level 20+
- LoreBookPage UI has search bar, category progress indicators, locked entry hints
- Save/load tested with quest state corruption, dialogue history, lore persistence
- CLAUDE.md updated with lore system diagram and API reference
- Player documentation explains lore discovery mechanics

## User Persona

**Target User**: RPG player who values narrative depth, world immersion, and collecting/discovering hidden content

**Use Case**:
- Player defeats rare enemy → Lore entry "Ancient Shadow Wolves" unlocks → Combat log shows "New Codex Entry: Ancient Shadow Wolves"
- Player opens Lore Book (L key) → Sees "Bestiary (3/12 unlocked)" → Clicks Bestiary tab → Reads about defeated enemies
- Player finds legendary weapon → Item tooltip shows lore snippet → Full lore entry unlocks in codex
- Player completes major quest → Multiple lore entries unlock (characters, locations, world history)
- Player searches codex for "shadow" → Finds all shadow-related entries across categories
- Player saves game with 15/30 lore unlocked → Loads game weeks later → All discoveries persist

**User Journey**:
1. Player defeats Shadow Wolf (3rd kill) → "New Codex Entry: Shadow Wolves" appears in combat log
2. Player presses L key → LoreBookPage opens showing Bestiary tab
3. Bestiary shows "3/12 unlocked" progress bar
4. Player clicks "Shadow Wolves" entry → Full lore text with wolf backstory displayed
5. Player equips legendary "Ancient Blade" from shop → Item tooltip shows "An blade forged in the first war..."
6. Lore entry "The First War" automatically unlocks
7. Player completes quest "The Whispering Woods" → 3 new lore entries unlock (location, character, world event)
8. Combat log shows 3 sequential notifications
9. Player opens codex → Uses search bar to find "whispering" → Sees all related entries highlighted
10. Player saves game → All lore discoveries persist through save/load cycle

**Pain Points Addressed**:
- Shallow world-building (solved by rich interconnected lore across 30+ entries)
- No item backstory (solved by linking items to lore entries)
- Missed lore discoveries (solved by combat log notifications)
- Forgotten lore between sessions (solved by robust save/load persistence)
- Hard-to-find lore (solved by search and category organization)

## Why

- **World Depth**: 30+ lore entries transform the game from combat simulator into immersive story world
- **Player Investment**: Collecting lore creates completionist gameplay loop beyond combat
- **Narrative Integration**: Items, quests, enemies all tell interconnected story through lore
- **Replayability**: Hidden lore encourages exploration and experimentation across playthroughs
- **Quality Assurance**: Comprehensive testing prevents quest bugs, save corruption, balance issues
- **Maintainability**: Updated documentation enables future feature additions
- **Polish**: UI/UX improvements make narrative systems delightful to use

This solves PRD pain point: "Players engage in combat without meaningful context." Phase 5 ensures every combat, quest, and item contributes to understanding the world's story.

## What

### Core Functionality

**Lore Content Expansion**:
- 20-30 new LoreEntry definitions authored in LoreFactory
- Categories breakdown: 8 Bestiary, 6 Items, 6 World History, 5 Characters, 5 Locations
- Entry structure: entryId, category, title, shortDescription (1-2 sentences), fullText (100-300 words)
- Discovery triggers aligned with gameplay: kill_EnemyName_Count, quest_complete_QuestId, item_get_ItemName
- Interconnected references: Entries reference each other (e.g., "Shadow Wolf" entry mentions "Ancient War" lore)
- Voice/tone consistency: All entries written in dark fantasy style matching game atmosphere

**Item-Lore Integration**:
- Item model extended: Add QString loreId field to Item.h
- Item.cpp serialization updated (version 2) with backward compatibility for old saves
- ItemFactory updated: Assign lore IDs to all legendary/rare items (15-20 items)
- Shop items: 5 shop items get lore entries (Ancient Sword, Magic Staff, etc.)
- Lore unlock triggers: On item acquisition (combat loot, shop purchase, quest reward), unlock associated lore

**Lore Discovery Notifications**:
- LogDisplay integration: CodexManager::loreUnlocked signal → MainWindow → LogDisplay message
- Message format: "New Codex Entry: {lore title}" in Theme::PRIMARY color
- Non-intrusive: Appears in combat log, doesn't block gameplay
- Multiple unlocks: Queue sequential notifications in combat log
- Already integrated: MainWindow.cpp lines 753-757 connect signal (verify functionality)

**Comprehensive Testing**:
- test_lore_discovery.cpp: Lore unlocks from quests, combat, items (6 test methods)
- test_item_lore.cpp: Item-lore associations, serialization (5 test methods)
- test_lore_notification.cpp: Notification display, queueing (4 test methods)
- test_lore_integration.cpp: End-to-end quest → lore → save/load (6 test methods)
- Edge case coverage: Quest state corruption, dialogue replay, save file version migration
- Final boss testing: Phase transitions, difficulty tuning, victory condition

**Final Boss Balancing**:
- Metrics collection: Win/loss ratio, average attempts, player feedback
- Phase difficulty curve: Phase 1 (intro), Phase 2 (+25% attack), Phase 3 (+50% attack), Phase 4 (+75% attack)
- Health tuning: Adjust maxHealth from 1600 to achieve 5-7 minute fight duration
- Attack balancing: Ensure player can survive with healing items but requires strategy
- Playtesting: 3-5 playthroughs at level 20 to validate difficulty

**UI/UX Polish** (LoreBookPage enhancements):
- Search bar: QLineEdit at top filters entries across all categories by title/text
- Category progress indicators: "Bestiary (3/12)" shows discovered/total entries
- Locked entry previews: Show "???" with unlock hint ("Defeat more Shadow Wolves")
- Sorting options: Alphabetical, Discovery Order (newest first)
- Visual feedback: Newly unlocked entries highlighted for 5 seconds
- Image display: Show entry images if imagePath not empty

**Documentation Updates**:
- CLAUDE.md: Add "Lore System Architecture" section with component diagram, data flow
- CLAUDE.md: Document LoreEntry structure, CodexManager API, discovery triggers
- README.md: Add "Lore Discovery Guide" for players explaining codex mechanics
- Code comments: Add docstrings to LoreFactory, CodexManager public methods

### Success Criteria

**Lore Content**:
- [ ] 20-30 lore entries authored in LoreFactory.cpp
- [ ] All entries have category, title, shortDescription, fullText
- [ ] Discovery triggers assigned to all entries
- [ ] Entries reference each other for interconnected narrative
- [ ] Voice/tone consistent across all entries (dark fantasy theme)

**Item-Lore Integration**:
- [ ] Item.h has QString loreId field added
- [ ] Item.cpp serialization updated to version 2
- [ ] Backward compatibility: Version 1 saves load without loreId
- [ ] ItemFactory assigns loreId to 15-20 legendary/rare items
- [ ] Lore unlocks on item acquisition in Game.cpp, ShopPage.cpp, DialogueManager.cpp

**Lore Notifications**:
- [ ] CodexManager::loreUnlocked signal connected to LogDisplay
- [ ] Combat log shows "New Codex Entry: {title}" on unlock
- [ ] Multiple unlocks queue sequentially without overlap
- [ ] Notification color matches Theme::PRIMARY

**Comprehensive Testing**:
- [ ] test_lore_discovery.cpp created with 6 tests (all pass)
- [ ] test_item_lore.cpp created with 5 tests (all pass)
- [ ] test_lore_notification.cpp created with 4 tests (all pass)
- [ ] test_lore_integration.cpp created with 6 tests (all pass)
- [ ] Edge cases covered: quest corruption, dialogue replay, save migration
- [ ] Final boss tests: phase transitions, victory condition, balance

**Final Boss Balancing**:
- [ ] 3-5 playtests completed at level 20
- [ ] Win requires 3-5 attempts for skilled player
- [ ] Phase transitions feel dramatic and meaningful
- [ ] Attack damage tuned: challenging but survivable with healing items
- [ ] Fight duration: 5-7 minutes average

**UI/UX Polish**:
- [ ] LoreBookPage search bar functional (filters by title/text)
- [ ] Category progress indicators show "X/Y unlocked"
- [ ] Locked entries show "???" with unlock hint
- [ ] Sorting options: Alphabetical, Discovery Order
- [ ] New entry highlight (5 second fade)
- [ ] Images display if imagePath populated

**Documentation**:
- [ ] CLAUDE.md "Lore System Architecture" section added
- [ ] CLAUDE.md documents LoreEntry, CodexManager, discovery triggers
- [ ] README.md "Lore Discovery Guide" added for players
- [ ] LoreFactory.h, CodexManager.h methods have docstrings

## All Needed Context

### Context Completeness Check

✓ **Lore system infrastructure**: Complete analysis of existing LoreEntry, CodexManager, LoreBookPage, LoreFactory implementations
✓ **Item system analysis**: Full Item model structure, factory patterns, acquisition hooks identified
✓ **Notification patterns**: Comprehensive documentation of LogDisplay integration and Qt notification best practices
✓ **Testing infrastructure**: Complete test patterns for models, UI, integration, and save/load
✓ **External best practices**: Industry research on RPG lore design, content writing guidelines, unlock mechanics, balancing methodologies
✓ **Serialization patterns**: Player versioning strategy, backward compatibility approach
✓ **UI component patterns**: Search bars, progress indicators, list filtering from existing codebase

**Validation**: An AI agent unfamiliar with this codebase has everything needed - all existing lore infrastructure documented with line numbers, item integration hooks identified, notification system fully specified, test patterns with code examples, external research citations, and exact file patterns for all modifications.

### Documentation & References

```yaml
# PRD Architecture Reference
- file: PRPs/storyline-quest-system-prd.md
  why: Phase 5 requirements (lines 989-1016), lore system specs (lines 402-426), testing strategies
  section: "Phase 5: Polish & Integration, Story 2.3: Lore & World-Building"
  critical: Task list, deliverables, edge cases to test, balancing guidelines

# Existing Lore Infrastructure (COMPLETE - Phase 3 implemented)
- file: cpp-qt-rpg/src/models/LoreEntry.h
  why: Data structure pattern for all lore entries (8 fields defined)
  pattern: Lines 7-17 struct with entryId, category, title, shortDescription, fullText, imagePath, discoveryTrigger
  usage: Create 20-30 new instances in LoreFactory following this exact structure

- file: cpp-qt-rpg/src/game/CodexManager.h
  why: Discovery logic and event handlers
  pattern: Lines 20-30 loadLoreEntries(), checkDiscoveryTriggers(), unlockEntry(), event handlers
  critical: Line 33 loreUnlocked signal must connect to LogDisplay for notifications

- file: cpp-qt-rpg/src/game/CodexManager.cpp
  why: Implementation of discovery triggers and unlock logic
  pattern: Lines 77-99 event handlers (onEnemyKilled, onQuestCompleted, onItemCollected)
  gotcha: Line 42-44 prevents duplicate unlocks, line 50 emits loreUnlocked signal

- file: cpp-qt-rpg/src/game/factories/LoreFactory.h
  why: Entry creation and caching patterns
  pattern: Lines 12-18 createLoreEntry(), getAllLoreEntries(), getLoreByCategory()
  usage: Add 20-30 new entry definitions following existing pattern

- file: cpp-qt-rpg/src/game/factories/LoreFactory.cpp
  why: Existing 11 entries as templates for new content
  pattern: Lines 15-349 show entry structure with raw string literals for fullText
  expand: Add new entries after line 349 before closing brace
  note: Static cache pattern (line 7) - entries never deleted

- file: cpp-qt-rpg/src/views/LoreBookPage.h
  why: UI structure for enhancements (search, progress, sorting)
  pattern: Lines 24-43 QTabWidget (categories), QListWidget (entries), QTextEdit (details)
  enhance: Add QLineEdit searchBar (line 44), QLabel progressLabels (line 45-49)

- file: cpp-qt-rpg/src/views/LoreBookPage.cpp
  why: Category display, entry rendering, keyboard shortcuts
  pattern: Lines 220-252 handleCategoryChanged(), lines 254-282 handleEntryClicked()
  enhance: Add search filtering logic, progress calculation, locked entry display

# Item-Lore Integration (NEEDS IMPLEMENTATION)
- file: cpp-qt-rpg/src/models/Item.h
  why: Add loreId field for linking items to lore
  current: Lines 15-24 define 10 existing fields (no lore field)
  add: QString loreId; after line 24 (before serialization operators)
  pattern: Follow existing QString fields (name, description, slot)

- file: cpp-qt-rpg/src/models/Item.cpp
  why: Update serialization for loreId field (version 2)
  current: Lines 18-32 serialize/deserialize all fields
  modify: Line 18 operator<< - increment version to 2, add loreId after description
  modify: Line 26 operator>> - conditional deserialization: if (version >= 2) in >> i.loreId;
  gotcha: MUST preserve backward compatibility for version 1 saves

- file: cpp-qt-rpg/src/game/factories/ItemFactory.cpp
  why: Assign loreId to legendary/rare items during creation
  locations: Line 51 (weapons), line 57 (armor), line 64-65 (accessories) in generateRandomItem()
  locations: Lines 77-95 (shop items) in getShopItems()
  pattern: After creating item, set item->loreId = "lore_entry_id"
  example: legendary->loreId = "ancient_blade_lore";

# Lore Unlock Hooks (INTEGRATION POINTS)
- file: cpp-qt-rpg/src/game/Game.cpp
  why: Item loot drops trigger lore unlocks
  location: Line 470 player->inventory.append(loot) - after item added
  add: if (loot->loreId && m_codexManager) { m_codexManager->unlockEntry(loot->loreId); }
  location: Line 484 legendary drop - same pattern for boss legendary

- file: cpp-qt-rpg/src/views/ShopPage.cpp
  why: Shop purchases trigger lore unlocks
  location: Line 218 after m_currentPlayer->inventory.append(purchasedItem)
  add: Need access to CodexManager - emit signal or pass reference in constructor

- file: cpp-qt-rpg/src/game/DialogueManager.cpp
  why: Dialogue rewards trigger lore unlocks
  location: Line 157 after m_player->inventory.append(item)
  add: if (item->loreId) { m_player->unlockLore(item->loreId); }

- file: cpp-qt-rpg/src/game/QuestManager.cpp
  why: Quest rewards trigger lore unlocks
  location: Line 345 after m_player->inventory.append(item)
  add: if (item->loreId) { m_player->unlockLore(item->loreId); }

# Notification Integration (ALREADY CONNECTED)
- file: cpp-qt-rpg/src/MainWindow.cpp
  why: CodexManager signal already connected to UI
  verify: Lines 753-757 connect loreUnlocked to handleLoreDiscovery
  implementation: handleLoreDiscovery() should add message to LogDisplay
  pattern: Similar to handleQuestCompleted() which updates UI

- file: cpp-qt-rpg/src/components/LogDisplay.h
  why: Combat log for non-intrusive notifications
  pattern: addMessage(QString message) method
  usage: logDisplay->addMessage(QString("New Codex Entry: %1").arg(loreTitle));

- file: cpp-qt-rpg/src/theme/Theme.h
  why: Color constants for notification styling
  pattern: Theme::PRIMARY for lore notification highlights
  usage: LogDisplay can use PRIMARY color for "New Codex Entry:" prefix

# Testing Patterns (COMPREHENSIVE DOCUMENTATION)
- file: cpp-qt-rpg/tests/test_models.cpp
  why: Model testing pattern with QTest framework
  pattern: Lines 20-99 show class structure, QCOMPARE, QVERIFY macros
  usage: test_lore_discovery.cpp follows this structure

- file: cpp-qt-rpg/tests/test_persistence.cpp
  why: Save/load round-trip testing pattern
  pattern: Lines 39-302 show serialization validation, slot testing, cleanup
  usage: test_item_lore.cpp tests loreId serialization following this pattern

- file: cpp-qt-rpg/tests/test_mainwindow.cpp
  why: UI interaction and signal testing pattern
  pattern: Lines 32-54 animation timing with QTest::qWait(300)
  pattern: Lines 170-199 keyboard shortcut testing with QTest::keyClick()
  usage: test_lore_notification.cpp uses similar signal spy and timing patterns

- file: cpp-qt-rpg/tests/test_quest_system.cpp
  why: Integration testing with event propagation
  pattern: Lines 140-198 show event simulation (onCombatEnd, onLevelUp)
  usage: test_lore_integration.cpp simulates game events triggering lore unlocks

- file: cpp-qt-rpg/CMakeLists.txt
  why: How to add new test executables
  pattern: Lines 268-282 test_quest_models executable definition
  critical: Add new test files to add_executable(), link Qt6::Test, add_test() command
  naming: test_lore_discovery, test_item_lore, test_lore_notification, test_lore_integration

# UI Enhancement Patterns
- file: cpp-qt-rpg/src/views/InventoryPage.cpp
  why: Search bar and filtering pattern
  pattern: QLineEdit with textChanged signal filtering QListWidget items
  usage: LoreBookPage search bar uses similar filtering approach

- file: cpp-qt-rpg/src/views/SaveLoadPage.cpp
  why: Progress indicator pattern ("X/Y slots used")
  pattern: QLabel with formatted string showing counts
  usage: LoreBookPage category progress "3/12 unlocked"

# External Research Citations
- url: https://kreonit.com/idea-generation-and-game-design/game-lore/
  why: Lore writing best practices (environmental storytelling, interconnected narrative)
  critical: Brief entries > lengthy prose, actionable content, mystery/questions

- url: https://www.memoryofeternity.com/write-rpg-lore/
  why: Content structure guidelines (100-300 words ideal, focus areas)
  critical: Build worlds first, characters as products of environment

- url: https://pinglestudio.com/knowledge-base/how-to-test-for-game-balance
  why: Boss balancing methodology (iterative playtesting, metrics collection)
  critical: Win/loss ratios, player feedback integration, gradual difficulty increase

- url: https://www.qable.io/blog/role-playing-game-testing
  why: Quest testing checklist (progression blockers, dialogue functionality, edge cases)
  critical: Test all decision branches, verify no dead-ends, validate outcomes

# Serialization Pattern (Version Migration)
- file: cpp-qt-rpg/src/models/Player.cpp
  why: Versioned save format with backward compatibility
  pattern: Lines 62-161 show version 3 serialization with conditional loading
  usage: Item serialization follows same pattern (version 1 → version 2)
  critical: if (version >= 2) conditional prevents crashes on old saves

# Boss Balancing Reference (FROM PHASE 4)
- file: PRPs/storyline-quest-system-phase4.md
  why: Final boss mechanics and tuning approach
  section: Lines 860-923 FinalBoss class, phase mechanics, attack multipliers
  metrics: 3-5 attempts for skilled player, 5-7 minute fight duration
  adjust: Modify FinalBoss.cpp constructor stats based on playtesting feedback
```

### Current Codebase Tree

```bash
cpp-qt-rpg/
├── src/
│   ├── models/
│   │   ├── LoreEntry.h                # COMPLETE - 8-field structure
│   │   ├── Item.h/.cpp                # NEEDS loreId field added
│   │   ├── Player.h/.cpp              # unlockedLoreEntries tracking (complete)
│   │   └── [other models]
│   ├── game/
│   │   ├── CodexManager.h/.cpp        # COMPLETE - discovery logic implemented
│   │   ├── QuestManager.h/.cpp        # Quest-lore integration points
│   │   ├── DialogueManager.h/.cpp     # Dialogue reward hooks
│   │   └── factories/
│   │       ├── LoreFactory.h/.cpp     # NEEDS 20-30 new entries
│   │       └── ItemFactory.h/.cpp     # NEEDS loreId assignments
│   ├── views/
│   │   └── LoreBookPage.h/.cpp        # NEEDS UI enhancements (search, progress, sorting)
│   ├── components/
│   │   └── LogDisplay.h/.cpp          # Notification display (ready to use)
│   ├── persistence/
│   │   └── SaveManager.h/.cpp         # Handles lore persistence via Player
│   └── theme/
│       └── Theme.h                     # Color constants for UI
├── tests/
│   ├── test_models.cpp                # Model testing pattern
│   ├── test_persistence.cpp           # Save/load pattern
│   ├── test_mainwindow.cpp            # UI testing pattern
│   ├── test_quest_system.cpp          # Integration testing pattern
│   └── [NEEDS 4 new lore test files]
└── CMakeLists.txt                     # NEEDS test executable additions
```

### Desired Codebase Tree (Files to Modify/Add)

```bash
cpp-qt-rpg/
├── src/
│   ├── models/
│   │   └── Item.h/.cpp                # MODIFY: Add loreId, update serialization v2
│   ├── game/
│   │   ├── Game.cpp                   # MODIFY: Add lore unlock hooks (lines 470, 484)
│   │   └── factories/
│   │       ├── LoreFactory.cpp        # MODIFY: Add 20-30 new lore entries
│   │       └── ItemFactory.cpp        # MODIFY: Assign loreId to 15-20 items
│   ├── views/
│   │   ├── LoreBookPage.h/.cpp        # MODIFY: Add search, progress, sorting, locked previews
│   │   ├── ShopPage.cpp               # MODIFY: Add lore unlock on purchase
│   │   ├── DialogueManager.cpp        # MODIFY: Add lore unlock on item reward
│   │   └── QuestManager.cpp           # MODIFY: Add lore unlock on quest item reward
│   └── MainWindow.cpp                 # MODIFY: Enhance handleLoreDiscovery for LogDisplay
├── tests/
│   ├── test_lore_discovery.cpp        # CREATE: Lore unlock testing (6 tests)
│   ├── test_item_lore.cpp             # CREATE: Item-lore integration (5 tests)
│   ├── test_lore_notification.cpp     # CREATE: Notification display (4 tests)
│   └── test_lore_integration.cpp      # CREATE: End-to-end integration (6 tests)
├── CMakeLists.txt                     # MODIFY: Add 4 new test executables
├── CLAUDE.md                          # MODIFY: Add lore system documentation
└── README.md                          # MODIFY: Add player lore discovery guide
```

### Known Gotchas & Library Quirks

```cpp
// CRITICAL: Item Serialization Version Migration
// Item.cpp operator<< and operator>> MUST increment version to 2
// Old version 1 saves MUST load without errors (no loreId)

// operator<< (saving) - Item.cpp
QDataStream &operator<<(QDataStream &out, const Item &i)
{
    out << quint32(2);  // Version 2: Added loreId field
    out << i.name << i.itemType << i.rarity << i.slot
        << i.attackBonus << i.defenseBonus << i.effect
        << i.power << i.value << i.description
        << i.loreId;  // NEW in version 2
    return out;
}

// operator>> (loading) - Item.cpp
QDataStream &operator>>(QDataStream &in, Item &i)
{
    quint32 version;
    in >> version;

    in >> i.name >> i.itemType >> i.rarity >> i.slot
       >> i.attackBonus >> i.defenseBonus >> i.effect
       >> i.power >> i.value >> i.description;

    // Backward compatibility: only load loreId if version 2+
    if (version >= 2) {
        in >> i.loreId;
    } else {
        i.loreId = "";  // Default for old saves
    }

    return in;
}

// CRITICAL: Lore Unlock Hooks - Check for null pointers
// Game.cpp line 470 (after loot drop)
if (loot && loot->loreId && !loot->loreId.isEmpty() && m_codexManager) {
    m_codexManager->unlockEntry(loot->loreId);
}

// GOTCHA: CodexManager Signal Connection
// MainWindow.cpp already connects loreUnlocked signal (lines 753-757)
// Verify handleLoreDiscovery() implementation adds LogDisplay message
void MainWindow::handleLoreDiscovery(const QString &loreId, const QString &loreTitle)
{
    if (m_logDisplay) {
        QString message = QString("<span style='color:%1'>New Codex Entry:</span> %2")
            .arg(Theme::PRIMARY.name())
            .arg(loreTitle);
        m_logDisplay->addMessage(message);
    }
}

// CRITICAL: LoreFactory Entry ID Naming Convention
// Use consistent namespace_name format for easy searching
// Bestiary: bestiary_goblin, bestiary_shadow_wolf, bestiary_orc_warrior
// Items: item_ancient_blade, item_healing_potion, item_magic_staff
// World: world_ancient_war, world_whispering_woods, world_shadow_realm
// Characters: character_elder_aldwin, character_marcus_merchant
// Locations: location_thornhaven, location_forgotten_ruins

// GOTCHA: LoreFactory Static Cache
// All LoreEntry* pointers owned by static factory cache (line 7)
// Never delete entries - they persist for entire application lifetime
// This is intentional design to prevent re-allocation

// CRITICAL: Discovery Trigger Format
// CodexManager event handlers generate specific trigger strings
// kill_EnemyName_Count: e.g., "kill_Goblin_5" (5th goblin kill)
// quest_complete_QuestId: e.g., "quest_complete_main_quest_01"
// item_get_ItemName: e.g., "item_get_Healing Potion"
// Ensure LoreEntry discoveryTrigger matches these exact patterns

// GOTCHA: LoreBookPage Search Implementation
// Use QString::contains(searchText, Qt::CaseInsensitive) for filtering
// Filter on both title and fullText for comprehensive search
// Update entry list when search text changes via textChanged signal

// CRITICAL: Testing Pattern - QTest::qWait() for Animations
// UI tests MUST wait for animations before assertions
// MainWindow.cpp line 54: QTest::qWait(300) for overlay hide animation
// Pattern: Action → qWait(300ms) → Assertion
overlay.hideOverlay();
QTest::qWait(300);  // REQUIRED for animation completion
QVERIFY(!overlay.isVisible());

// GOTCHA: CMakeLists.txt Test Dependencies
// Each test executable needs ALL dependencies of tested class
// test_lore_discovery.cpp needs:
//   - src/game/CodexManager.cpp
//   - src/models/LoreEntry.h (header-only, no .cpp)
//   - src/models/Player.cpp
//   - src/models/Character.cpp
//   - src/game/QuestManager.cpp
//   - src/models/Quest.cpp
//   - All factory dependencies

// CRITICAL: Boss Balancing Metrics
// Collect during playtesting:
// - Win/loss ratio (target: 40-60% win rate)
// - Average attempts to win (target: 3-5 attempts)
// - Fight duration (target: 5-7 minutes)
// - Phase 4 deaths (should be 50%+ of player deaths)

// GOTCHA: Lore Content Voice/Tone
// Maintain consistent dark fantasy atmosphere across all entries
// Use active voice ("Shadow wolves emerged from...") not passive
// Brief summaries (1-2 sentences) in shortDescription
// Full narrative (100-300 words) in fullText
// Leave mystery - questions drive player curiosity

// CRITICAL: Progress Indicator Calculation
// LoreBookPage category progress shows "X/Y unlocked"
int totalEntries = codexManager->getAllEntriesInCategory(category).size();
int unlockedCount = codexManager->getUnlockedEntries(category).size();
QString progressText = QString("%1/%2 unlocked").arg(unlockedCount).arg(totalEntries);

// GOTCHA: Locked Entry Preview
// Show "???" for locked entries with unlock hint
// Hint derived from discoveryTrigger parsing:
// "kill_Goblin_3" → "Defeat more Goblins (0/3)"
// "quest_complete_main_quest_01" → "Complete 'A Dark Omen' quest"
// "item_get_Ancient Blade" → "Acquire Ancient Blade"

// CRITICAL: Documentation Markdown Formatting
// Use mermaid diagrams for architecture documentation
// Use code blocks with language hints for API examples
// Use YAML for configuration/data structure examples
// Keep sections concise with headers for easy navigation
```

## Implementation Blueprint

### Data Models and Structure

**Item Lore Extension**:
```cpp
// Item.h additions (after line 24)
class Item {
public:
    // Existing fields (lines 15-24)
    QString name;
    QString itemType;
    QString rarity;
    QString slot;
    int attackBonus;
    int defenseBonus;
    QString effect;
    int power;
    int value;
    QString description;

    // NEW: Lore system integration
    QString loreId;  // Links to LoreEntry (e.g., "item_ancient_blade")

    // Serialization operators (update to version 2)
    friend QDataStream &operator<<(QDataStream &out, const Item &i);
    friend QDataStream &operator>>(QDataStream &in, Item &i);
};
```

**Lore Content Structure**:
```cpp
// Example entry in LoreFactory.cpp (add 20-30 of these)
entries["bestiary_shadow_wolf"] = new LoreEntry{
    "bestiary_shadow_wolf",                              // entryId
    "Bestiary",                                          // category
    "Shadow Wolves",                                     // title
    "Twisted creatures born from dark magic, hunting in packs through cursed forests.",  // shortDescription (1-2 sentences)
    R"(Shadow Wolves are not natural creatures. During the Ancient War, desperate mages
attempted to merge wolves with shadow essence to create the perfect hunters. The ritual
succeeded beyond their nightmares.

These cursed beasts hunt in packs of three to five, their eyes glowing crimson in the darkness.
They strike from shadows, materializing mere feet from their prey. Survivors speak of an
unnatural intelligence behind their coordinated attacks.

The transformation is irreversible. Once a wolf becomes shadow-touched, no magic can restore
its original form. They are bound to the Whispering Woods, forever hunting those who dare
enter their domain.)",                                   // fullText (100-300 words)
    "",                                                   // imagePath (future asset)
    "kill_Shadow Wolf_3"                                 // discoveryTrigger (3rd kill)
};
```

### Implementation Tasks (Ordered by Dependencies)

```yaml
Task 1: UPDATE src/models/Item.h
  MODIFY: Add loreId field
  LOCATION: After line 24 (after description field)
  ADDITIONS:
    - QString loreId;  // Empty string if no associated lore
  DEPENDENCIES: None
  PLACEMENT: Before serialization operators (line 26)

Task 2: UPDATE src/models/Item.cpp
  MODIFY: Serialization operators for version 2
  CHANGES:
    1. operator<< (line 18): Increment version to 2
       out << quint32(2);  // Version 2: Added loreId
    2. operator<< (line 24): Add loreId after description
       out << ... << i.description << i.loreId;
    3. operator>> (line 26): Read version, then fields
    4. operator>> (after line 31): Conditional loreId load
       if (version >= 2) {
           in >> i.loreId;
       } else {
           i.loreId = "";
       }
  CRITICAL: Backward compatibility MUST work for version 1 saves
  DEPENDENCIES: Item.h updated (Task 1)

Task 3: EXPAND src/game/factories/LoreFactory.cpp
  IMPLEMENT: 20-30 new lore entry definitions
  LOCATION: After line 349 (after existing 11 entries, before closing brace)
  CONTENT breakdown:
    - 8 Bestiary entries (Shadow Wolf, Goblin, Orc, Dark Mage, Stone Golem, Corrupted Guardian, Final Boss, Secret Boss)
    - 6 Item entries (Ancient Blade, Healing Potion, Mana Potion, Legendary Armor, Magic Staff, Cursed Ring)
    - 6 World History entries (Ancient War, Shadow Corruption, First Kingdom, Fall of Thornhaven, The Prophecy, The Void)
    - 5 Character entries (Elder Aldwin, Marcus Merchant, Wandering Scholar, Dark Lord, Lost Hero)
    - 5 Location entries (Whispering Woods, Thornhaven Village, Forgotten Ruins, Shadow Realm, Final Dungeon)
  PATTERN:
    - entryId follows namespace_name (e.g., bestiary_goblin, item_ancient_blade)
    - shortDescription: 1-2 sentences for list view
    - fullText: 100-300 words with R"(...)" raw string literal
    - discoveryTrigger matches CodexManager patterns (kill_X_Count, quest_complete_X, item_get_X)
  VOICE/TONE: Dark fantasy, active voice, mysterious, interconnected references
  DEPENDENCIES: LoreEntry.h (existing), LoreFactory.h (existing)

Task 4: UPDATE src/game/factories/ItemFactory.cpp
  MODIFY: Assign loreId to legendary/rare items
  LOCATIONS:
    1. generateRandomItem() method:
       - Line 51 (weapons): After item creation, add item->loreId = "item_X"
       - Line 57 (armor): Same pattern
       - Line 64-65 (accessories): Same pattern
       - Example: if (rarity == "Legendary") { item->loreId = "item_ancient_" + itemName.toLower().replace(" ", "_"); }
    2. getShopItems() method:
       - Lines 77-95: Assign loreId to shop items
       - Line 83 Iron Sword: item->loreId = "item_iron_sword"
       - Line 85 Magic Staff: item->loreId = "item_magic_staff"
       - (5 total shop items get lore)
  TOTAL: 15-20 items with loreId assigned
  DEPENDENCIES: Item.h updated (Task 1), LoreFactory expanded (Task 3)

Task 5: UPDATE src/game/Game.cpp
  MODIFY: Add lore unlock hooks on item acquisition
  CHANGES:
    1. Line 470 (after player->inventory.append(loot)):
       if (loot && !loot->loreId.isEmpty() && m_codexManager) {
           m_codexManager->unlockEntry(loot->loreId);
       }
    2. Line 484 (after legendary boss drop):
       if (legendary && !legendary->loreId.isEmpty() && m_codexManager) {
           m_codexManager->unlockEntry(legendary->loreId);
       }
  CRITICAL: Null checks prevent crashes if CodexManager not initialized
  DEPENDENCIES: Item.h updated (Task 1), ItemFactory updated (Task 4)

Task 6: UPDATE src/views/ShopPage.cpp
  MODIFY: Add lore unlock on shop item purchase
  CHALLENGE: ShopPage doesn't have CodexManager reference
  SOLUTIONS:
    Option A: Add CodexManager* to ShopPage constructor
    Option B: Emit signal that MainWindow connects to CodexManager
    Option C: Access via Player::unlockLore() (simpler, already exists)
  RECOMMENDED: Option C
  LOCATION: Line 218 (after m_currentPlayer->inventory.append(purchasedItem))
  CODE:
    if (purchasedItem && !purchasedItem->loreId.isEmpty()) {
        m_currentPlayer->unlockLore(purchasedItem->loreId);
    }
  DEPENDENCIES: Item.h updated (Task 1)

Task 7: UPDATE src/game/DialogueManager.cpp
  MODIFY: Add lore unlock on dialogue item reward
  LOCATION: Line 157 (after m_player->inventory.append(item))
  CODE:
    if (item && !item->loreId.isEmpty()) {
        m_player->unlockLore(item->loreId);
    }
  DEPENDENCIES: Item.h updated (Task 1)

Task 8: UPDATE src/game/QuestManager.cpp
  MODIFY: Add lore unlock on quest item reward
  LOCATION: Line 345 (after m_player->inventory.append(item))
  CODE:
    if (item && !item->loreId.isEmpty()) {
        m_player->unlockLore(item->loreId);
    }
  DEPENDENCIES: Item.h updated (Task 1)

Task 9: UPDATE src/MainWindow.cpp
  MODIFY: Enhance handleLoreDiscovery() for LogDisplay notifications
  VERIFY: Lines 753-757 already connect CodexManager::loreUnlocked
  IMPLEMENT: handleLoreDiscovery() method (if not exists, add to MainWindow.h slot)
  CODE:
    void MainWindow::handleLoreDiscovery(const QString &loreId, const QString &loreTitle)
    {
        if (m_combatPage && m_combatPage->getLogDisplay()) {
            QString message = QString("<span style='color:%1'>New Codex Entry:</span> %2")
                .arg(Theme::PRIMARY.name())
                .arg(loreTitle);
            m_combatPage->getLogDisplay()->addMessage(message);
        }
    }
  DEPENDENCIES: LogDisplay.h (existing), Theme.h (existing)

Task 10: ENHANCE src/views/LoreBookPage.h
  ADD: UI components for search, progress, sorting
  ADDITIONS:
    - QLineEdit* m_searchBar; (line 44)
    - QMap<QString, QLabel*> m_progressLabels; (line 45) - one per category
    - QComboBox* m_sortComboBox; (line 46) - sorting options
    - void handleSearchTextChanged(const QString &text); (private slot)
    - void handleSortChanged(int index); (private slot)
  PLACEMENT: Add members after existing m_currentCategory (line 43)
  DEPENDENCIES: None

Task 11: ENHANCE src/views/LoreBookPage.cpp
  IMPLEMENT: Search, progress, sorting, locked entry features
  CHANGES:
    1. setupUi() (add after line 40):
       - Create QLineEdit for search bar at top
       - Create QComboBox with "Alphabetical" and "Discovery Order" options
       - Add progress labels to each category tab header
    2. handleCategoryChanged() (modify lines 220-252):
       - Calculate progress: unlockedCount / totalCount
       - Update progress label: "3/12 unlocked"
       - Apply search filter to entry list
    3. handleSearchTextChanged() (new method):
       - Filter entry list by search text (case-insensitive)
       - Search in title AND fullText
    4. handleSortChanged() (new method):
       - Sort entry list alphabetically or by discovery order
    5. Locked entry display (in entry list population):
       - If entry not unlocked, show "???" with hint
       - Parse discoveryTrigger for hint text
  STYLING: Use Theme constants for all colors, spacing
  DEPENDENCIES: LoreBookPage.h updated (Task 10), CodexManager.h (existing)

Task 12: CREATE tests/test_lore_discovery.cpp
  IMPLEMENT: Unit tests for lore unlock mechanics
  FOLLOW pattern: tests/test_quest_system.cpp (integration with event handlers)
  TEST cases:
    - testLoreUnlockOnQuestComplete(): Quest completion triggers lore unlock
    - testLoreUnlockOnCombatKill(): Enemy kill count triggers unlock
    - testLoreUnlockOnItemAcquisition(): Item pickup triggers unlock
    - testLoreUnlockSignalEmitted(): Verify loreUnlocked signal
    - testDuplicateUnlockPrevention(): Can't unlock same entry twice
    - testLoreStatePersistence(): Save and load preserves unlocked state
  STRUCTURE:
    - #include <QtTest/QtTest>
    - #include "game/CodexManager.h"
    - #include "models/Player.h"
    - #include "game/QuestManager.h"
    - class TestLoreDiscovery : public QObject { Q_OBJECT private slots: ... };
    - QTEST_MAIN(TestLoreDiscovery)
    - #include "test_lore_discovery.moc"
  PLACEMENT: cpp-qt-rpg/tests/test_lore_discovery.cpp
  DEPENDENCIES: CodexManager, Player, QuestManager implementations

Task 13: CREATE tests/test_item_lore.cpp
  IMPLEMENT: Unit tests for item-lore integration
  FOLLOW pattern: tests/test_persistence.cpp (serialization testing)
  TEST cases:
    - testItemWithLoreId(): Create item with loreId, verify field
    - testItemLoreSerialization(): Save and load item with loreId (version 2)
    - testBackwardCompatibility(): Load version 1 item (no loreId crashes)
    - testLoreUnlockOnItemPickup(): Item acquisition unlocks associated lore
    - testShopItemLore(): Shop items have loreId populated
  STRUCTURE: Same as test_lore_discovery.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_item_lore.cpp
  DEPENDENCIES: Item, ItemFactory, SaveManager implementations

Task 14: CREATE tests/test_lore_notification.cpp
  IMPLEMENT: Unit tests for notification display
  FOLLOW pattern: tests/test_mainwindow.cpp (UI and signal testing)
  TEST cases:
    - testNotificationSignal(): CodexManager emits loreUnlocked
    - testLogDisplayMessage(): LogDisplay shows notification message
    - testMultipleNotificationQueue(): Sequential unlocks don't overlap
    - testNotificationFormatting(): Message uses Theme::PRIMARY color
  STRUCTURE: Same as test_lore_discovery.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_lore_notification.cpp
  DEPENDENCIES: CodexManager, LogDisplay, MainWindow implementations

Task 15: CREATE tests/test_lore_integration.cpp
  IMPLEMENT: End-to-end integration tests
  FOLLOW pattern: tests/test_quest_system.cpp + tests/test_persistence.cpp combined
  TEST cases:
    - testQuestToLoreFlow(): Quest completion → Lore unlock → Notification → Save → Load
    - testCombatToLoreFlow(): Enemy kill → Lore unlock → Notification → Save → Load
    - testItemToLoreFlow(): Item pickup → Lore unlock → Notification → Save → Load
    - testMultipleLoreUnlocks(): Chain of events unlocking multiple entries
    - testLoreAfterBossDefeat(): Final boss drops legendary with lore
    - testFullCodexCompletion(): Unlock all entries, save, load, verify
  STRUCTURE: Same as test_lore_discovery.cpp
  PLACEMENT: cpp-qt-rpg/tests/test_lore_integration.cpp
  DEPENDENCIES: Full game stack (Game, QuestManager, CodexManager, SaveManager, Player, Item)

Task 16: UPDATE cpp-qt-rpg/CMakeLists.txt
  ADD: Four new test executables
  FOLLOW pattern: Lines 268-282 (test_quest_models example)
  ADDITIONS (after existing tests, around line 350):
    1. add_executable(test_lore_discovery
           tests/test_lore_discovery.cpp
           src/game/CodexManager.cpp
           src/models/Player.cpp
           src/models/Character.cpp
           src/game/QuestManager.cpp
           src/models/Quest.cpp
           src/game/factories/QuestFactory.cpp
           src/game/factories/LoreFactory.cpp
       )
       target_link_libraries(test_lore_discovery PRIVATE Qt6::Widgets Qt6::Test)
       target_include_directories(test_lore_discovery PRIVATE src)
       add_test(NAME LoreDiscoveryTest COMMAND test_lore_discovery)

    2. test_item_lore executable (similar pattern with Item, ItemFactory, SaveManager)
    3. test_lore_notification executable (with LogDisplay, MainWindow, CodexManager)
    4. test_lore_integration executable (with FULL game stack)
  CRITICAL: Alphabetical order within add_executable() for maintainability
  DEPENDENCIES: All test files created (Tasks 12-15)

Task 17: BALANCE src/models/FinalBoss.cpp
  MODIFY: Tune boss stats based on playtesting
  PLAYTESTING protocol:
    1. Playtest at level 20 (minimum level) - 3 attempts
    2. Playtest at level 22 (above minimum) - 3 attempts
    3. Collect metrics: win/loss, attempts to win, fight duration, phase 4 deaths
  ADJUSTMENTS based on metrics:
    - If too easy (win rate > 70%): Increase maxHealth by 10-20%, increase attack multipliers
    - If too hard (win rate < 30%): Decrease maxHealth by 10-20%, decrease phase 4 multiplier
    - Target: 40-60% win rate, 3-5 attempts, 5-7 minute fight
  CHANGES (FinalBoss.cpp constructor):
    - Line 11: health = 500 + (playerLevel * X) - adjust X multiplier
    - Line 13: attack = 30 + (playerLevel * Y) - adjust Y multiplier
  DOCUMENTATION: Record playtesting notes in PRPs/phase5-playtesting-notes.md
  DEPENDENCIES: FinalBoss class (from Phase 4), Game combat system

Task 18: UPDATE CLAUDE.md
  ADD: Lore System Architecture section
  LOCATION: After "Quest System Architecture" section
  CONTENT:
    1. Component overview diagram (mermaid)
       LoreEntry → LoreFactory → CodexManager → Player persistence
    2. Data flow description (discovery triggers → unlock → notification → save)
    3. LoreEntry structure documentation (8 fields)
    4. CodexManager API reference (loadLoreEntries, unlockEntry, getUnlockedEntries)
    5. Discovery trigger format specification (kill_X_Count, quest_complete_X, item_get_X)
    6. Item-lore integration explanation (loreId field, unlock hooks)
  MARKDOWN format: Use mermaid diagrams, code blocks, YAML examples
  DEPENDENCIES: All lore system implementation complete

Task 19: UPDATE README.md
  ADD: Lore Discovery Guide for players
  LOCATION: After "Game Controls" section
  CONTENT:
    1. What is the Codex?: "Collection of lore entries about world, enemies, items, characters"
    2. How to access: "Press L key to open Lore Book"
    3. How to unlock lore: "Defeat enemies, complete quests, find rare items"
    4. Categories explanation: "Bestiary (enemies), Items, World (history), Characters, Locations"
    5. Notifications: "Watch combat log for 'New Codex Entry' messages"
    6. Progress tracking: "Each category shows unlocked/total entries"
  MARKDOWN format: Simple bullets, clear instructions
  DEPENDENCIES: LoreBookPage implementation complete

Task 20: FINAL TESTING & VALIDATION
  RUN: All test suites and manual testing
  COMMANDS:
    1. cd cpp-qt-rpg/build && cmake .. && make
    2. ctest --verbose (all tests pass)
    3. ./test_lore_discovery
    4. ./test_item_lore
    5. ./test_lore_notification
    6. ./test_lore_integration
    7. ./pyrpg-qt (manual playthrough)
  MANUAL testing checklist:
    - Create new game, defeat enemy, verify lore unlock notification
    - Open Lore Book (L key), verify entry visible
    - Save game, close, load, verify lore persists
    - Acquire shop item with loreId, verify unlock
    - Complete quest with lore reward, verify unlock
    - Search codex for keyword, verify filtering works
    - Check category progress indicators show correct counts
    - Defeat final boss, verify legendary lore unlocks
    - Load old save (version 1), verify no crashes
  VALIDATION: All 20 success criteria checkboxes marked complete
  DEPENDENCIES: All previous tasks complete
```

### Implementation Patterns & Key Details

```cpp
// ============================================================================
// PATTERN 1: Item Lore Field and Serialization Version 2
// ============================================================================
// File: src/models/Item.h
// Add loreId field to link items to lore entries

class Item {
public:
    // Existing fields
    QString name;
    QString itemType;
    QString rarity;
    QString slot;
    int attackBonus;
    int defenseBonus;
    QString effect;
    int power;
    int value;
    QString description;

    // NEW: Lore integration
    QString loreId;  // Empty string if no associated lore

    // Constructors
    Item();
    Item(const QString &name, const QString &itemType, const QString &rarity,
         const QString &slot, int attackBonus, int defenseBonus,
         const QString &effect, int power, int value, const QString &description,
         const QString &loreId = "");  // Add loreId parameter with default

    // Serialization
    friend QDataStream &operator<<(QDataStream &out, const Item &i);
    friend QDataStream &operator>>(QDataStream &in, Item &i);
};

// File: src/models/Item.cpp
// Update serialization operators for version 2

// Constructor with loreId
Item::Item(const QString &name, const QString &itemType, const QString &rarity,
           const QString &slot, int attackBonus, int defenseBonus,
           const QString &effect, int power, int value, const QString &description,
           const QString &loreId)
    : name(name), itemType(itemType), rarity(rarity), slot(slot),
      attackBonus(attackBonus), defenseBonus(defenseBonus), effect(effect),
      power(power), value(value), description(description), loreId(loreId)
{
}

// Serialization - Version 2
QDataStream &operator<<(QDataStream &out, const Item &i)
{
    out << quint32(2);  // Version 2: Added loreId field
    out << i.name << i.itemType << i.rarity << i.slot
        << i.attackBonus << i.defenseBonus << i.effect
        << i.power << i.value << i.description
        << i.loreId;  // NEW in version 2
    return out;
}

QDataStream &operator>>(QDataStream &in, Item &i)
{
    quint32 version;
    in >> version;

    in >> i.name >> i.itemType >> i.rarity >> i.slot
       >> i.attackBonus >> i.defenseBonus >> i.effect
       >> i.power >> i.value >> i.description;

    // CRITICAL: Backward compatibility for version 1 saves
    if (version >= 2) {
        in >> i.loreId;
    } else {
        i.loreId = "";  // Default for old saves (no crash)
    }

    return in;
}

// ============================================================================
// PATTERN 2: Lore Content Authoring in LoreFactory
// ============================================================================
// File: src/game/factories/LoreFactory.cpp
// Add 20-30 entries following this pattern

// BESTIARY ENTRIES (8 total)
entries["bestiary_shadow_wolf"] = new LoreEntry{
    "bestiary_shadow_wolf",
    "Bestiary",
    "Shadow Wolves",
    "Twisted creatures born from dark magic, hunting in packs through cursed forests.",
    R"(Shadow Wolves are not natural creatures. During the Ancient War, desperate mages
attempted to merge wolves with shadow essence to create the perfect hunters. The ritual
succeeded beyond their nightmares.

These cursed beasts hunt in packs of three to five, their eyes glowing crimson in the darkness.
They strike from shadows, materializing mere feet from their prey. Survivors speak of an
unnatural intelligence behind their coordinated attacks.

The transformation is irreversible. Once a wolf becomes shadow-touched, no magic can restore
its original form. They are bound to the Whispering Woods, forever hunting those who dare
enter their domain.)",
    "",  // Future image: ":/assets/lore/shadow_wolf.png"
    "kill_Shadow Wolf_3"  // Unlocks on 3rd Shadow Wolf kill
};

// ITEM ENTRIES (6 total)
entries["item_ancient_blade"] = new LoreEntry{
    "item_ancient_blade",
    "Items",
    "The Ancient Blade",
    "A sword forged in the First War, said to cut through darkness itself.",
    R"(The Ancient Blade was forged by Master Smith Aldric during the final days of the First War.
When shadow corruption threatened to consume the kingdom, Aldric created twelve legendary weapons
infused with purifying light.

This blade is one of the lost twelve. Its edge never dulls, and wounds dealt by it heal slowly,
even for creatures of shadow. The runes along the blade glow faint blue when darkness approaches,
warning its wielder of nearby corruption.

Aldric died defending the forge, but his blades survived. Scattered across the realm, they wait
for heroes brave enough to wield them against the encroaching shadows.)",
    "",
    "item_get_Ancient Blade"  // Unlocks when player acquires this item
};

// WORLD HISTORY ENTRIES (6 total)
entries["world_ancient_war"] = new LoreEntry{
    "world_ancient_war",
    "World",
    "The Ancient War",
    "A conflict that nearly destroyed the realm, when shadow magic first emerged.",
    R"(Three centuries ago, a cabal of mages discovered a source of immense power deep beneath
the Forgotten Ruins. They called it the Shadowwell—a font of dark energy that could reshape
reality itself.

The mages sought to harness this power for the kingdom's glory. Instead, they unleashed
corruption that spread like plague. Crops withered, animals transformed into twisted monsters,
and entire villages vanished into shadow.

The resulting war lasted twenty years. Brave warriors, led by the hero Thornhaven, fought
against shadow-corrupted forces. The war ended when Thornhaven sealed the Shadowwell,
sacrificing himself in the process.

Or so the legends claim. Recent disturbances suggest the seal may be weakening.)",
    "",
    "quest_complete_main_quest_02"  // Unlocks after completing second main quest
};

// CHARACTER ENTRIES (5 total)
entries["character_elder_aldwin"] = new LoreEntry{
    "character_elder_aldwin",
    "Characters",
    "Elder Aldwin",
    "The village elder, keeper of ancient knowledge and survivor of the Shadow War.",
    R"(Elder Aldwin has led Thornhaven Village for forty years, but few know the weight of
his past. In his youth, he fought alongside the hero Thornhaven during the final battles
of the Ancient War.

Aldwin witnessed horrors that changed him forever. He saw entire battalions consumed by
shadow corruption, watched friends transform into the very monsters they fought. The
experience left him with nightmares that persist to this day.

After the war, Aldwin devoted himself to scholarship, studying ancient texts to understand
the shadow threat. He believes the corruption is not destroyed—merely sleeping. His constant
vigilance keeps the village prepared for the darkness he knows will return.

The elder's advanced age and grim demeanor hide a fierce determination. He will do whatever
necessary to prevent another Shadow War, even if it requires sacrifices others find unacceptable.)",
    "",
    "quest_complete_main_quest_01"
};

// LOCATION ENTRIES (5 total)
entries["location_whispering_woods"] = new LoreEntry{
    "location_whispering_woods",
    "Locations",
    "The Whispering Woods",
    "A cursed forest where shadows move of their own accord and whispers echo through the trees.",
    R"(The Whispering Woods were once the Forest of Tranquility, a peaceful hunting ground for
Thornhaven's people. That changed during the Ancient War when shadow corruption seeped into
the soil, transforming the forest forever.

Travelers report hearing whispers that speak their names, see shadows that don't match their
sources, and feel watched by unseen eyes. Those who linger too long emerge changed—speaking
of visions and prophecies, or not emerging at all.

The forest's trees are ancient and twisted, their bark blackened as if burned from within.
No birds sing here, no normal animals remain. Only shadow-touched creatures prowl beneath
the canopy.

Yet the village depends on the woods. Rare herbs grow nowhere else, and the forest provides
a natural barrier against threats from the east. Villagers venture in cautiously, always in
groups, never after dark.)",
    "",
    "manual"  // Unlocked at game start or via dialogue
};

// ============================================================================
// PATTERN 3: ItemFactory Lore ID Assignment
// ============================================================================
// File: src/game/factories/ItemFactory.cpp

// In generateRandomItem() - assign loreId to legendary/rare items
Item* ItemFactory::generateRandomItem(int enemyLevel)
{
    // ... existing rarity determination code (lines 9-38) ...

    // Weapon generation (around line 48)
    if (itemType == "weapon") {
        QStringList weaponNames = {"Iron Sword", "Steel Blade", "Battle Axe",
                                   "War Hammer", "Long Spear", "Magic Staff"};
        QString name = weaponNames[rand() % weaponNames.size()];
        int attackBonus = (basePower + rand() % (basePower / 2));

        Item* weapon = new Item(name, "weapon", rarity, "weapon",
                                attackBonus, 0, "", 0, value,
                                QString("+%1 Attack").arg(attackBonus));

        // NEW: Assign loreId to legendary/rare weapons
        if (rarity == "Legendary") {
            weapon->loreId = "item_" + name.toLower().replace(" ", "_");
        } else if (rarity == "Rare" && rand() % 100 < 30) {  // 30% of rare items
            weapon->loreId = "item_common_" + weapon->itemType;
        }

        return weapon;
    }

    // Similar patterns for armor and accessories
}

// In getShopItems() - assign loreId to special shop items
QMap<QString, Item*> ItemFactory::getShopItems()
{
    static QMap<QString, Item*> shopItems;

    if (shopItems.isEmpty()) {
        // Potions (lines 77-80)
        shopItems["Healing Potion"] = new Item("Healing Potion", "consumable",
            "Common", "consumable", 0, 0, "heal", 50, 20,
            "Restores 50 HP", "item_healing_potion");  // NEW: loreId added

        // Weapons (lines 83-86)
        shopItems["Iron Sword"] = new Item("Iron Sword", "weapon", "Common",
            "weapon", 10, 0, "", 0, 50,
            "+10 Attack Power", "item_iron_sword");  // NEW: loreId added

        shopItems["Magic Staff"] = new Item("Magic Staff", "weapon", "Uncommon",
            "weapon", 15, 0, "mana", 10, 100,
            "+15 Attack, +10 Mana", "item_magic_staff");  // NEW: loreId added

        // ... similar for other shop items ...
    }

    return shopItems;
}

// ============================================================================
// PATTERN 4: Lore Unlock Hooks in Game Events
// ============================================================================
// File: src/game/Game.cpp

// Combat loot drop lore unlock (after line 470)
void Game::giveCombatRewards()
{
    // ... existing loot generation code ...

    // Line 467-477: Random loot drop
    if (rand() % 100 < 30) {
        Item* loot = ItemFactory::generateRandomItem(currentMonster->level);
        player->inventory.append(loot);
        combatLog += QString("\nFound loot: %1").arg(loot->name);

        // Quest manager item collection (existing)
        if (m_questManager) {
            m_questManager->onItemCollected(loot->name);
        }

        // NEW: Codex unlock for item lore
        if (loot && !loot->loreId.isEmpty() && m_codexManager) {
            m_codexManager->unlockEntry(loot->loreId);
        }
    }

    // Line 480-487: Final boss legendary drop
    if (currentMonster && currentMonster->enemyType == "final_boss") {
        Item* legendary = ItemFactory::generateRandomItem(player->level + 5);
        legendary->rarity = "Legendary";
        player->inventory.append(legendary);
        combatLog += QString("\n⭐ Legendary Drop: %1 ⭐").arg(legendary->name);

        // NEW: Legendary items always unlock lore
        if (legendary && !legendary->loreId.isEmpty() && m_codexManager) {
            m_codexManager->unlockEntry(legendary->loreId);
        }
    }
}

// ============================================================================
// PATTERN 5: LogDisplay Notification Integration
// ============================================================================
// File: src/MainWindow.cpp

// Enhance handleLoreDiscovery() (verify connection at lines 753-757)
void MainWindow::handleLoreDiscovery(const QString &loreId, const QString &loreTitle)
{
    // Add to combat log (non-intrusive notification)
    if (m_combatPage && m_combatPage->getLogDisplay()) {
        QString message = QString("<span style='color:%1'>New Codex Entry:</span> %2")
            .arg(Theme::PRIMARY.name())
            .arg(loreTitle);
        m_combatPage->getLogDisplay()->addMessage(message);
    }

    // Optional: Also show in menu overlay stats
    if (m_menuOverlay) {
        m_menuOverlay->showNotification(QString("Lore Unlocked: %1").arg(loreTitle));
    }
}

// ============================================================================
// PATTERN 6: LoreBookPage Search and Progress Implementation
// ============================================================================
// File: src/views/LoreBookPage.cpp

void LoreBookPage::setupUi()
{
    // ... existing title and tab widget setup (lines 21-81) ...

    // NEW: Add search bar at top (before tabs)
    m_searchBar = new QLineEdit(this);
    m_searchBar->setPlaceholderText("Search lore entries...");
    m_searchBar->setStyleSheet(QString(
        "background-color: %1; "
        "color: %2; "
        "border: 1px solid %3; "
        "border-radius: %4px; "
        "padding: %5px;"
    ).arg(Theme::CARD.name())
     .arg(Theme::TEXT.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD)
     .arg(Theme::SPACING_SM));
    connect(m_searchBar, &QLineEdit::textChanged, this, &LoreBookPage::handleSearchTextChanged);
    mainLayout->addWidget(m_searchBar);

    // ... existing tab widget and entry list setup ...

    // NEW: Add progress labels to category tabs
    for (const QString &category : QStringList{"Bestiary", "Items", "World", "Characters", "Locations"}) {
        QLabel *progressLabel = new QLabel(this);
        progressLabel->setStyleSheet(QString("color: %1; font-size: %2px;")
            .arg(Theme::TEXT_SECONDARY.name())
            .arg(Theme::FONT_SIZE_SM));
        m_progressLabels[category] = progressLabel;

        // Add progress label to tab (requires custom tab widget)
        // For simplicity, can append to tab text: "Bestiary (3/12)"
    }
}

void LoreBookPage::updateCategoryProgress(const QString &category)
{
    if (!m_codexManager || !m_player) return;

    int totalEntries = m_codexManager->getAllEntriesInCategory(category).size();
    int unlockedCount = m_codexManager->getUnlockedEntries(category).size();

    QString progressText = QString("(%1/%2)").arg(unlockedCount).arg(totalEntries);

    // Update tab text to include progress
    for (int i = 0; i < m_categoryTabs->count(); ++i) {
        if (m_categoryTabs->tabText(i).startsWith(category)) {
            m_categoryTabs->setTabText(i, category + " " + progressText);
            break;
        }
    }
}

void LoreBookPage::handleSearchTextChanged(const QString &searchText)
{
    if (!m_codexManager || !m_entryList) return;

    m_entryList->clear();

    QList<LoreEntry*> entries = m_codexManager->getUnlockedEntries(m_currentCategory);

    for (LoreEntry *entry : entries) {
        // Search in both title and fullText (case-insensitive)
        bool matches = searchText.isEmpty() ||
                       entry->title.contains(searchText, Qt::CaseInsensitive) ||
                       entry->fullText.contains(searchText, Qt::CaseInsensitive);

        if (matches) {
            QListWidgetItem *item = new QListWidgetItem(entry->title);
            item->setData(Qt::UserRole, QVariant::fromValue(entry));
            m_entryList->addItem(item);
        }
    }

    // Update details to show search results count
    if (m_entryList->count() == 0) {
        m_detailsText->setHtml(QString("<p style='color:%1'>No entries found matching '%2'</p>")
            .arg(Theme::TEXT_SECONDARY.name())
            .arg(searchText));
    }
}

// ============================================================================
// PATTERN 7: Comprehensive Testing Pattern
// ============================================================================
// File: tests/test_lore_discovery.cpp

#include <QtTest>
#include <QSignalSpy>
#include "game/CodexManager.h"
#include "models/Player.h"
#include "game/QuestManager.h"

class TestLoreDiscovery : public QObject
{
    Q_OBJECT

private slots:
    void testLoreUnlockOnQuestComplete();
    void testLoreUnlockOnCombatKill();
    void testLoreUnlockOnItemAcquisition();
    void testLoreUnlockSignalEmitted();
    void testDuplicateUnlockPrevention();
    void testLoreStatePersistence();
};

void TestLoreDiscovery::testLoreUnlockOnQuestComplete()
{
    // Setup
    Player player("TestHero", "Warrior");
    CodexManager codexManager(&player);
    codexManager.loadLoreEntries();

    QSignalSpy spy(&codexManager, &CodexManager::loreUnlocked);

    // Trigger quest complete event
    codexManager.onQuestCompleted("main_quest_01");

    // Verify lore unlock signal emitted
    QVERIFY(spy.count() > 0);  // At least one lore entry unlocked

    // Verify specific lore entry unlocked (if main_quest_01 unlocks "world_ancient_war")
    QVERIFY(player.hasUnlockedLore("world_ancient_war"));

    // Verify signal parameters (first emit)
    QString unlockedId = spy.at(0).at(0).toString();
    QString unlockedTitle = spy.at(0).at(1).toString();
    QCOMPARE(unlockedId, QString("world_ancient_war"));
    QVERIFY(!unlockedTitle.isEmpty());
}

void TestLoreDiscovery::testLoreUnlockOnCombatKill()
{
    Player player("TestHero", "Warrior");
    CodexManager codexManager(&player);
    codexManager.loadLoreEntries();

    QSignalSpy spy(&codexManager, &CodexManager::loreUnlocked);

    // Kill Shadow Wolf 3 times (trigger: kill_Shadow Wolf_3)
    codexManager.onEnemyKilled("Shadow Wolf");
    QCOMPARE(spy.count(), 0);  // No unlock yet

    codexManager.onEnemyKilled("Shadow Wolf");
    QCOMPARE(spy.count(), 0);  // Still no unlock

    codexManager.onEnemyKilled("Shadow Wolf");
    QCOMPARE(spy.count(), 1);  // Unlock on 3rd kill

    // Verify specific lore unlocked
    QVERIFY(player.hasUnlockedLore("bestiary_shadow_wolf"));
}

void TestLoreDiscovery::testDuplicateUnlockPrevention()
{
    Player player("TestHero", "Warrior");
    CodexManager codexManager(&player);
    codexManager.loadLoreEntries();

    // Unlock lore entry
    codexManager.unlockEntry("bestiary_goblin");
    QVERIFY(player.hasUnlockedLore("bestiary_goblin"));

    int initialCount = player.getUnlockedLoreEntries().size();

    // Try to unlock same entry again
    codexManager.unlockEntry("bestiary_goblin");

    // Verify count didn't increase (no duplicate)
    QCOMPARE(player.getUnlockedLoreEntries().size(), initialCount);
}

void TestLoreDiscovery::testLoreStatePersistence()
{
    // Create and save player with lore
    Player *original = new Player("TestHero", "Warrior");
    original->unlockLore("bestiary_goblin");
    original->unlockLore("world_ancient_war");

    SaveManager manager;
    bool saved = manager.saveToSlot(original, 1);
    QVERIFY(saved);

    // Load player from save
    Player *loaded = manager.loadFromSlot(1);
    QVERIFY(loaded != nullptr);

    // Verify lore state persisted
    QVERIFY(loaded->hasUnlockedLore("bestiary_goblin"));
    QVERIFY(loaded->hasUnlockedLore("world_ancient_war"));
    QCOMPARE(loaded->getUnlockedLoreEntries().size(), 2);

    // Cleanup
    delete original;
    delete loaded;
    manager.deleteSlot(1);
}

QTEST_MAIN(TestLoreDiscovery)
#include "test_lore_discovery.moc"
```

### Integration Points

```yaml
ITEM_LORE_LINKAGE:
  - location: src/models/Item.h line 25 (after description)
  - add: QString loreId field
  - update: Constructor to accept loreId parameter
  - update: Serialization operators to version 2 with backward compatibility

LORE_UNLOCK_HOOKS:
  - Game.cpp line 470: Combat loot drop → codexManager->unlockEntry(loot->loreId)
  - Game.cpp line 484: Boss legendary → codexManager->unlockEntry(legendary->loreId)
  - ShopPage.cpp line 218: Shop purchase → player->unlockLore(item->loreId)
  - DialogueManager.cpp line 157: Dialogue reward → player->unlockLore(item->loreId)
  - QuestManager.cpp line 345: Quest reward → player->unlockLore(item->loreId)

NOTIFICATION_DISPLAY:
  - MainWindow.cpp lines 753-757: CodexManager::loreUnlocked signal connected
  - MainWindow.cpp handleLoreDiscovery(): Add LogDisplay message with Theme::PRIMARY color
  - LogDisplay.cpp: Message format "<span style='color:PRIMARY'>New Codex Entry:</span> Title"

LOREBOOK_UI_ENHANCEMENTS:
  - LoreBookPage.h line 44: Add QLineEdit* m_searchBar member
  - LoreBookPage.cpp setupUi(): Create search bar with textChanged signal
  - LoreBookPage.cpp handleSearchTextChanged(): Filter entries by title/fullText
  - LoreBookPage.cpp updateCategoryProgress(): Calculate and display "X/Y unlocked"

TESTING_INTEGRATION:
  - CMakeLists.txt after line 350: Add 4 new test executables
  - tests/test_lore_discovery.cpp: Quest/combat/item unlock flow testing
  - tests/test_item_lore.cpp: Item serialization and lore linkage testing
  - tests/test_lore_notification.cpp: Notification display testing
  - tests/test_lore_integration.cpp: End-to-end integration testing

DOCUMENTATION_UPDATES:
  - CLAUDE.md: Add "Lore System Architecture" section with mermaid diagram
  - CLAUDE.md: Document LoreEntry structure, CodexManager API, discovery triggers
  - README.md: Add "Lore Discovery Guide" for players with L key shortcut
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Build after Item model changes
cd cpp-qt-rpg/build
cmake ..
make

# Verify Item.cpp compiles with version 2 serialization
make src/models/Item.cpp

# Verify LoreFactory expanded entries compile
make src/game/factories/LoreFactory.cpp

# Verify all lore unlock hooks compile
make src/game/Game.cpp
make src/views/ShopPage.cpp
make src/game/DialogueManager.cpp
make src/game/QuestManager.cpp

# Verify LoreBookPage enhancements compile
make src/views/LoreBookPage.cpp

# Full build
cd cpp-qt-rpg/build
cmake .. && make

# Expected: Zero compile errors, zero warnings
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test lore discovery mechanics
cd cpp-qt-rpg/build
./test_lore_discovery

# Expected output:
# PASS : TestLoreDiscovery::testLoreUnlockOnQuestComplete()
# PASS : TestLoreDiscovery::testLoreUnlockOnCombatKill()
# PASS : TestLoreDiscovery::testLoreUnlockOnItemAcquisition()
# PASS : TestLoreDiscovery::testLoreUnlockSignalEmitted()
# PASS : TestLoreDiscovery::testDuplicateUnlockPrevention()
# PASS : TestLoreDiscovery::testLoreStatePersistence()

# Test item-lore integration
./test_item_lore

# Expected output:
# PASS : TestItemLore::testItemWithLoreId()
# PASS : TestItemLore::testItemLoreSerialization()
# PASS : TestItemLore::testBackwardCompatibility()
# PASS : TestItemLore::testLoreUnlockOnItemPickup()
# PASS : TestItemLore::testShopItemLore()

# Test lore notifications
./test_lore_notification

# Expected output:
# PASS : TestLoreNotification::testNotificationSignal()
# PASS : TestLoreNotification::testLogDisplayMessage()
# PASS : TestLoreNotification::testMultipleNotificationQueue()
# PASS : TestLoreNotification::testNotificationFormatting()

# Test lore integration (end-to-end)
./test_lore_integration

# Expected output:
# PASS : TestLoreIntegration::testQuestToLoreFlow()
# PASS : TestLoreIntegration::testCombatToLoreFlow()
# PASS : TestLoreIntegration::testItemToLoreFlow()
# PASS : TestLoreIntegration::testMultipleLoreUnlocks()
# PASS : TestLoreIntegration::testLoreAfterBossDefeat()
# PASS : TestLoreIntegration::testFullCodexCompletion()

# Run all tests
ctest

# Expected: All tests pass (0 failures)
```

### Level 3: Integration Testing (System Validation)

```bash
# Run the game
cd cpp-qt-rpg/build
./pyrpg-qt

# Manual test flow - LORE DISCOVERY:
# 1. Start New Game, create character
# 2. Defeat Shadow Wolf enemy (1st kill)
#    - Verify: No lore notification yet
# 3. Defeat Shadow Wolf (2nd kill)
#    - Verify: Still no notification
# 4. Defeat Shadow Wolf (3rd kill)
#    - Verify: Combat log shows "New Codex Entry: Shadow Wolves"
# 5. Press L key to open Lore Book
#    - Verify: LoreBookPage opens
#    - Verify: Bestiary tab shows "(1/8)" or similar progress
#    - Verify: "Shadow Wolves" entry visible in list
# 6. Click "Shadow Wolves" entry
#    - Verify: Full lore text displays in right panel
#    - Verify: Formatting and readability are good
# 7. Close Lore Book (ESC), continue playing
# 8. Complete first main quest
#    - Verify: Combat log shows "New Codex Entry: [quest-related lore]"
# 9. Visit shop, buy "Magic Staff" (if has loreId)
#    - Verify: Lore unlock notification appears
# 10. Open Lore Book again
#    - Verify: Multiple categories show unlocked entries
#    - Verify: Progress indicators updated (e.g., "Bestiary (2/8)")
# 11. Use search bar: type "shadow"
#    - Verify: Only shadow-related entries shown
#    - Verify: Entries from multiple categories appear
# 12. Save game (slot 1)
# 13. Close game, relaunch, load slot 1
#    - Verify: All unlocked lore persists
#    - Verify: Progress indicators show same counts
# 14. Test backward compatibility:
#    - Find old save (version 1, before Phase 5)
#    - Load old save
#    - Verify: Game loads without crashing
#    - Verify: Items have empty loreId (no errors)

# Manual test flow - FINAL BOSS BALANCING:
# 1. Create level 20 character (or level up to 20)
# 2. Equip best available gear
# 3. Stock healing items (10+ Health Potions)
# 4. Accept final quest, confirm "Point of No Return"
# 5. Engage final boss combat
#    - Record: Time when combat starts
# 6. Monitor phase transitions:
#    - Phase 1 (100-76% HP): Baseline difficulty
#    - Phase 2 (75-51% HP): +25% attack - noticeable increase?
#    - Phase 3 (50-26% HP): +50% attack - challenging but survivable?
#    - Phase 4 (25-0% HP): +75% attack - desperate, requires strategy?
# 7. If player dies:
#    - Record: Which phase killed player
#    - Record: Total attempts
#    - Adjust boss stats if too hard/easy
# 8. If player wins:
#    - Record: Time to victory (target: 5-7 minutes)
#    - Record: Healing items used
#    - Record: Player health at victory
# 9. Repeat with 3-5 different playthroughs
# 10. Calculate metrics:
#    - Win rate (target: 40-60%)
#    - Average attempts (target: 3-5)
#    - Average fight duration (target: 5-7 minutes)
# 11. Tune FinalBoss.cpp stats based on metrics

# Expected: All manual tests pass, balanced boss difficulty
```

### Level 4: Content Quality & Experience Validation

```bash
# Lore content quality review:

# 1. Voice/Tone Consistency:
#    - Read all 30+ lore entries
#    - Verify: Dark fantasy atmosphere maintained
#    - Verify: Active voice ("wolves emerged") not passive
#    - Verify: Consistent terminology (e.g., "Shadow War" not "War of Shadows")
#    - Expected: All entries feel like same narrator

# 2. Interconnected Narrative:
#    - Map lore entry cross-references
#    - Verify: "Shadow Wolves" entry mentions "Ancient War"
#    - Verify: "Ancient Blade" entry references "Master Smith Aldric"
#    - Verify: Character entries connect to location/world entries
#    - Expected: Lore tells cohesive overarching story

# 3. Discovery Pacing:
#    - Track lore unlocks during typical playthrough
#    - Verify: Player unlocks 3-5 entries per hour
#    - Verify: Not overwhelming (max 3 unlocks per quest)
#    - Verify: Natural progression (easier enemies unlock first)
#    - Expected: Steady discovery without flooding

# 4. Search Functionality:
#    - Search for "shadow" → Results from Bestiary, World, Items
#    - Search for "war" → Results include Ancient War, weapon lore
#    - Search for character names → Character entries appear
#    - Expected: Intuitive search, helpful results

# 5. Progress Indicators:
#    - Bestiary tab shows "3/8 unlocked"
#    - Items tab shows "2/6 unlocked"
#    - All categories update dynamically
#    - Expected: Clear progression tracking, motivates collection

# 6. Locked Entry Previews:
#    - View locked Bestiary entry
#    - Verify: Shows "???" with hint "Defeat more Goblins (1/5)"
#    - Verify: Hint is actionable, not cryptic
#    - Expected: Player knows how to unlock, motivated to explore

# 7. UI/UX Polish:
#    - LoreBookPage loads instantly (< 100ms)
#    - Search updates results in real-time (< 50ms per keystroke)
#    - Tab switching is smooth (no lag)
#    - Entry display formatted with proper spacing, readability
#    - Expected: Polished, professional UI experience

# 8. Documentation Accuracy:
#    - Read CLAUDE.md "Lore System Architecture" section
#    - Verify: Diagram matches actual implementation
#    - Verify: API examples work as documented
#    - Expected: Documentation enables future developers

# 9. Player-Facing Documentation:
#    - Read README.md "Lore Discovery Guide"
#    - Verify: Clear instructions for new players
#    - Verify: Explains L key, categories, discovery triggers
#    - Expected: Players understand lore system without trial-and-error
```

## Final Validation Checklist

### Technical Validation

- [ ] All files compile without warnings
- [ ] Unit tests pass: test_lore_discovery (6 tests)
- [ ] Unit tests pass: test_item_lore (5 tests)
- [ ] Unit tests pass: test_lore_notification (4 tests)
- [ ] Integration tests pass: test_lore_integration (6 tests)
- [ ] All existing tests still pass (no regressions)
- [ ] ctest shows 0 failures across all 14+ test suites
- [ ] No memory leaks (run with valgrind or similar)
- [ ] Save/load works with version 2 Item serialization
- [ ] Backward compatibility: version 1 saves load without crashes

### Lore Content Validation

- [ ] 20-30 lore entries authored (8 Bestiary, 6 Items, 6 World, 5 Characters, 5 Locations)
- [ ] All entries have entryId, category, title, shortDescription, fullText
- [ ] Discovery triggers assigned and tested
- [ ] Voice/tone consistent across all entries (dark fantasy)
- [ ] Entries interconnected (cross-references present)
- [ ] No spelling/grammar errors in lore text
- [ ] Entry lengths appropriate (100-300 words for fullText)

### Item-Lore Integration Validation

- [ ] Item.h has loreId field
- [ ] Item.cpp serialization version 2 implemented
- [ ] Backward compatibility verified (version 1 saves load)
- [ ] 15-20 items have loreId assigned
- [ ] Shop items with loreId unlock correctly
- [ ] Combat loot with loreId unlocks correctly
- [ ] Dialogue/quest reward items unlock lore

### Lore Discovery Validation

- [ ] CodexManager::loreUnlocked signal emits on unlock
- [ ] Combat log shows "New Codex Entry: {title}" notifications
- [ ] Notifications use Theme::PRIMARY color
- [ ] Multiple unlocks queue sequentially without overlap
- [ ] Duplicate unlocks prevented (no repeat notifications)
- [ ] Lore state persists through save/load

### UI/UX Polish Validation

- [ ] LoreBookPage search bar functional
- [ ] Search filters by title and fullText (case-insensitive)
- [ ] Category progress indicators show "X/Y unlocked"
- [ ] Progress updates dynamically on new unlocks
- [ ] Locked entries show "???" with unlock hints
- [ ] Sorting options work (Alphabetical, Discovery Order)
- [ ] New entry highlight (5 second fade) implemented
- [ ] Images display if imagePath populated (future feature)
- [ ] UI responsive (< 100ms for all interactions)

### Testing Validation

- [ ] test_lore_discovery.cpp created with 6 tests (all pass)
- [ ] test_item_lore.cpp created with 5 tests (all pass)
- [ ] test_lore_notification.cpp created with 4 tests (all pass)
- [ ] test_lore_integration.cpp created with 6 tests (all pass)
- [ ] Edge cases covered: quest corruption, dialogue replay, version migration
- [ ] CMakeLists.txt updated with 4 new test executables
- [ ] All test dependencies correctly specified

### Final Boss Balancing Validation

- [ ] 3-5 playtests completed at level 20
- [ ] Win rate collected (target: 40-60%)
- [ ] Average attempts to win collected (target: 3-5)
- [ ] Average fight duration collected (target: 5-7 minutes)
- [ ] Phase transitions feel dramatic and meaningful
- [ ] Attack damage tuned based on playtesting
- [ ] Boss difficulty appropriate for level 20+ with healing items
- [ ] Playtesting notes documented in PRPs/phase5-playtesting-notes.md

### Documentation Validation

- [ ] CLAUDE.md "Lore System Architecture" section added
- [ ] CLAUDE.md includes mermaid component diagram
- [ ] CLAUDE.md documents LoreEntry structure with all 8 fields
- [ ] CLAUDE.md documents CodexManager API (loadLoreEntries, unlockEntry, etc.)
- [ ] CLAUDE.md explains discovery trigger format patterns
- [ ] CLAUDE.md describes Item-lore integration
- [ ] README.md "Lore Discovery Guide" added
- [ ] README.md explains L key, categories, unlock mechanics
- [ ] README.md instructions clear for new players
- [ ] All code docstrings added (LoreFactory.h, CodexManager.h)

## Anti-Patterns to Avoid

- ❌ Don't hardcode lore text in UI code - always use LoreFactory for content
- ❌ Don't skip backward compatibility - version 1 Item saves MUST load without errors
- ❌ Don't unlock lore without null checks - crashes if CodexManager not initialized
- ❌ Don't duplicate lore unlocks - always check hasUnlockedLore() first
- ❌ Don't forget to emit loreUnlocked signal - UI won't update otherwise
- ❌ Don't write entries in passive voice - "wolves were created" should be "mages created wolves"
- ❌ Don't make lore entries too long - 300 words max for fullText
- ❌ Don't make discovery triggers too obscure - player should understand how to unlock
- ❌ Don't skip interconnected references - isolated lore feels disconnected
- ❌ Don't ignore voice/tone consistency - all entries should feel like same narrator
- ❌ Don't make search case-sensitive - use Qt::CaseInsensitive flag
- ❌ Don't forget to update progress indicators - static counts feel broken
- ❌ Don't show locked entries without hints - player needs guidance on how to unlock
- ❌ Don't skip playtesting final boss - balance cannot be determined theoretically
- ❌ Don't tune boss based on one playthrough - collect 3-5 attempts minimum
- ❌ Don't make boss unbeatable - 40-60% win rate is target, not 0%
- ❌ Don't make boss too easy - should require 3-5 attempts, not 1
- ❌ Don't skip documentation - future developers need architecture guide
- ❌ Don't write documentation for developers only - players need guides too
- ❌ Don't forget to test with old saves - backward compatibility is critical

---

## Confidence Score: 9/10

**Rationale**: This PRP has comprehensive context from deep research:
- ✅ Complete lore infrastructure analysis (Phase 3 fully implemented - LoreEntry, CodexManager, LoreBookPage, LoreFactory)
- ✅ Full Item system analysis with exact hooks for lore integration (5 acquisition points identified)
- ✅ Notification patterns documented (LogDisplay integration ready, MainWindow.cpp lines 753-757 verified)
- ✅ Comprehensive testing patterns (4 test suites with code examples from existing tests)
- ✅ External research citations (RPG lore design, content writing, balancing methodologies from industry sources)
- ✅ Serialization versioning strategy (Item v1→v2 with backward compatibility pattern)
- ✅ UI enhancement patterns (search, progress, sorting from existing codebase)
- ✅ Boss balancing methodology (playtesting metrics, iteration approach from Phase 4)
- ✅ Documentation templates (CLAUDE.md structure, README player guide format)
- ✅ All file paths with line numbers for integration points

**Deduction (-1)**: Minor uncertainty around exact lore content quality - writing 20-30 interconnected lore entries with consistent voice requires creative iteration, though framework and guidelines provide all necessary tools.

**Validation**: An AI agent can implement this successfully with:
1. This PRP
2. Access to codebase files (all paths and line numbers provided)
3. Training data for Qt6/C++, RPG design, and content writing

All patterns, integration hooks, test structures, content guidelines, and quality gates are explicitly documented with research-backed recommendations and exact code examples.
