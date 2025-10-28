name: "BASE PRP - Implement Keyboard Shortcuts for Shop, Inventory, and Save/Load Screens"

description: |

---

## Goal

**Feature Goal**: Add keyboard shortcuts to open and navigate shop, inventory, and save/load screens in the PyrpgQt RPG game.

**Deliverable**: Functional keyboard shortcuts allowing users to:
- Press 'I' to open inventory from game screen
- Press 'S' to open shop from game screen  
- Press 'L' to open save/load from game screen
- Navigate within screens using arrow keys, Enter, and ESC

**Success Definition**: All shortcuts work without conflicts, navigation is intuitive, and no regressions in existing mouse functionality.

## User Persona (if applicable)

**Target User**: Keyboard-focused gamers who prefer not using mouse for menu navigation.

**Use Case**: Player in main game screen wants to quickly access inventory, shop, or save game without mouse clicks.

**Pain Points Addressed**: Slow menu navigation via mouse, accessibility issues for keyboard users.

## Why

- Improve user experience for keyboard users
- Add accessibility features
- Follow common RPG game conventions (I for inventory, etc.)
- Enable faster gameplay flow

## What

### User-visible behavior and technical requirements

- Global shortcuts active only in CombatPage (main game screen)
- 'I' opens inventory, 'S' opens shop, 'L' opens save/load
- Within screens: arrow keys navigate, Enter selects, ESC closes
- Shortcuts only work when not in combat or menus
- Visual feedback when shortcuts trigger
- No conflicts with existing controls

### Success Criteria

- [ ] 'I' key opens inventory from CombatPage
- [ ] 'S' key opens shop from CombatPage  
- [ ] 'L' key opens save/load from CombatPage
- [ ] Arrow key navigation works in all three screens
- [ ] Enter key selects/activates items in screens
- [ ] ESC key closes screens and returns to game
- [ ] Shortcuts disabled during combat
- [ ] No conflicts with existing ESC menu functionality

## All Needed Context

### Context Completeness Check

_Before writing this PRP, validate: "If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://doc.qt.io/qt-6/qkeyevent.html
  why: Official Qt documentation for QKeyEvent class and keyPressEvent handling
  critical: Understanding event acceptance, key constants, and focus requirements

- file: PRPs/ai_docs/qt_key_handling.md
  why: Comprehensive guide to Qt key handling patterns with examples
  pattern: Shows QKeyEvent vs QShortcut usage, best practices, common gotchas
  gotcha: Focus requirements, event propagation, modifier handling

- file: src/MainWindow.cpp lines 413-436
  why: Existing keyPressEvent implementation handling ESC for menu
  pattern: How global shortcuts are currently implemented in MainWindow
  gotcha: Only handles ESC when in CombatPage, calls parent for other keys

- file: src/MainWindow.h lines 58-60
  why: Current keyPressEvent override declaration
  pattern: Protected virtual method override pattern

- file: tests/test_mainwindow.cpp lines 102-109
  why: Existing test pattern for ESC key handling
  pattern: QTest::keyClick usage and QKeyEvent simulation for testing

# NICE TO HAVE - Additional context if needed
- url: https://doc.qt.io/qt-6/qshortcut.html
  why: Alternative QShortcut class for reference (not primary approach)
  critical: When QShortcut might be better than keyPressEvent

- url: https://www.reddit.com/r/gamedev/comments/56ton6/keyboard_controls_what_default_keys_should_i_use/
  why: Game dev discussion on common key bindings
  critical: Common RPG shortcuts like I for inventory, S for shop
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```
cpp-qt-rpg/
├── src/
│   ├── MainWindow.h/cpp          # Central UI controller with keyPressEvent
│   ├── views/
│   │   ├── CombatPage.h/cpp      # Main game screen (target for shortcuts)
│   │   ├── InventoryPage.h/cpp   # Inventory screen to extend with navigation
│   │   ├── ShopPage.h/cpp        # Shop screen to extend with navigation
│   │   └── SaveLoadPage.h/cpp    # Save/load screen to extend with navigation
│   ├── game/
│   │   └── Game.h/cpp           # Game state management
│   └── components/
│       └── MenuOverlay.h/cpp     # Existing menu system (ensure no conflicts)
├── tests/
│   └── test_mainwindow.cpp       # Existing tests to extend
└── CMakeLists.txt               # Build configuration
```

### Desired Codebase tree with files to be added and responsibility of file

```
cpp-qt-rpg/
├── src/
│   ├── MainWindow.h/cpp          # MODIFIED: Extend keyPressEvent for global shortcuts
│   ├── views/
│   │   ├── InventoryPage.h/cpp   # MODIFIED: Add keyPressEvent for navigation
│   │   ├── ShopPage.h/cpp        # MODIFIED: Add keyPressEvent for navigation
│   │   └── SaveLoadPage.h/cpp    # MODIFIED: Add keyPressEvent for navigation
├── tests/
│   ├── test_mainwindow.cpp       # MODIFIED: Add shortcut tests
│   ├── test_inventory_shortcuts.cpp    # NEW: Navigation tests
│   ├── test_shop_shortcuts.cpp         # NEW: Navigation tests
│   └── test_saveload_shortcuts.cpp     # NEW: Navigation tests
```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: Qt key events require widget focus
# Gotcha: keyPressEvent only triggers on focused widgets
# Solution: Ensure CombatPage has focus for global shortcuts

# CRITICAL: Event propagation in Qt
# Gotcha: Unhandled key events bubble up to parent widgets
# Solution: Always call parent keyPressEvent for unhandled keys

# CRITICAL: Existing ESC handling
# Gotcha: ESC already shows MenuOverlay from CombatPage
# Solution: Ensure new shortcuts don't conflict, ESC still works for menu

# CRITICAL: Qt::Key constants
# Gotcha: Must use Qt::Key_I, not just 'I'
# Solution: Reference qt_key_handling.md for correct constants

# CRITICAL: Combat state checking
# Gotcha: Shortcuts should only work when not in combat
# Solution: Check game state before handling shortcuts
```

## Implementation Blueprint

### Data models and structure

No new data models needed. Extend existing QWidget classes with keyPressEvent overrides.

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: MODIFY src/MainWindow.cpp keyPressEvent
  - ADD: Check for global shortcuts (I, S, L) when current widget is CombatPage
  - ADD: Call existing navigation slots (handleInventoryBack, etc.) to open screens
  - ADD: Disable shortcuts during combat (check game state)
  - FOLLOW pattern: src/MainWindow.cpp lines 413-436 (existing keyPressEvent)
  - NAMING: Extend existing keyPressEvent method
  - PLACEMENT: Inside existing keyPressEvent override
  - DEPENDENCIES: None

Task 2: MODIFY src/views/InventoryPage.cpp
  - ADD: keyPressEvent override for navigation
  - ADD: Arrow key handling for item selection
  - ADD: Enter key for item activation
  - ADD: ESC key to close (emit backRequested)
  - FOLLOW pattern: PRPs/ai_docs/qt_key_handling.md (keyPressEvent examples)
  - NAMING: void InventoryPage::keyPressEvent(QKeyEvent *event)
  - PLACEMENT: Private section of InventoryPage class
  - DEPENDENCIES: Task 1

Task 3: MODIFY src/views/ShopPage.cpp
  - ADD: keyPressEvent override for shop navigation
  - ADD: Arrow keys for item browsing
  - ADD: Enter key for purchasing
  - ADD: ESC key to leave (emit leaveRequested)
  - FOLLOW pattern: PRPs/ai_docs/qt_key_handling.md
  - NAMING: void ShopPage::keyPressEvent(QKeyEvent *event)
  - PLACEMENT: Private section of ShopPage class
  - DEPENDENCIES: Task 1

Task 4: MODIFY src/views/SaveLoadPage.cpp
  - ADD: keyPressEvent override for save/load navigation
  - ADD: Number keys (1-9) for slot selection
  - ADD: Enter key for save/load confirmation
  - ADD: ESC key to back (emit backRequested)
  - FOLLOW pattern: PRPs/ai_docs/qt_key_handling.md
  - NAMING: void SaveLoadPage::keyPressEvent(QKeyEvent *event)
  - PLACEMENT: Private section of SaveLoadPage class
  - DEPENDENCIES: Task 1

Task 5: MODIFY src/MainWindow.h
  - ADD: Include <QKeyEvent> if not present
  - VERIFY: keyPressEvent declaration exists
  - PLACEMENT: Header includes and protected methods
  - DEPENDENCIES: None

Task 6: MODIFY tests/test_mainwindow.cpp
  - ADD: Tests for global shortcuts (I, S, L keys)
  - ADD: Test shortcut disabled during combat
  - ADD: Test no conflict with ESC menu
  - FOLLOW pattern: tests/test_mainwindow.cpp lines 102-109 (existing key test)
  - NAMING: testGlobalShortcuts, testShortcutCombatDisabled, etc.
  - PLACEMENT: Add to TestMainWindow class
  - DEPENDENCIES: Task 1

Task 7: CREATE tests/test_inventory_shortcuts.cpp
  - IMPLEMENT: Unit tests for inventory key navigation
  - TEST: Arrow key selection changes
  - TEST: Enter key activates item
  - TEST: ESC key emits backRequested
  - FOLLOW pattern: tests/test_mainwindow.cpp (QTest framework usage)
  - NAMING: TestInventoryShortcuts class
  - PLACEMENT: tests/ directory
  - DEPENDENCIES: Task 2

Task 8: CREATE tests/test_shop_shortcuts.cpp
  - IMPLEMENT: Unit tests for shop key navigation
  - TEST: Arrow key browsing
  - TEST: Enter key purchases
  - TEST: ESC key emits leaveRequested
  - FOLLOW pattern: tests/test_mainwindow.cpp
  - NAMING: TestShopShortcuts class
  - PLACEMENT: tests/ directory
  - DEPENDENCIES: Task 3

Task 9: CREATE tests/test_saveload_shortcuts.cpp
  - IMPLEMENT: Unit tests for save/load key navigation
  - TEST: Number keys select slots
  - TEST: Enter key confirms action
  - TEST: ESC key emits backRequested
  - FOLLOW pattern: tests/test_mainwindow.cpp
  - NAMING: TestSaveLoadShortcuts class
  - PLACEMENT: tests/ directory
  - DEPENDENCIES: Task 4

Task 10: UPDATE CMakeLists.txt
  - ADD: New test executables to build system
  - ADD: Link Qt6::Test to new test targets
  - FOLLOW pattern: Existing test target definitions
  - PLACEMENT: Test section of CMakeLists.txt
  - DEPENDENCIES: Tasks 7-9
```

### Implementation Patterns & Key Details

```python
# Show critical patterns and gotchas - keep concise, focus on non-obvious details

# MainWindow global shortcut pattern
void MainWindow::keyPressEvent(QKeyEvent *event) {
    // CHECK: Only handle shortcuts in game screen
    if (stackedWidget->currentWidget() == m_combatPage) {
        switch (event->key()) {
            case Qt::Key_I:
                // CALL: Existing slot to open inventory
                handleInventoryBack();  // Wait, this closes - need to find open slot
                // TODO: Find the correct slot to open inventory
                event->accept();
                return;
            // Similar for S and L
        }
    }
    
    // GOTCHA: Always call existing ESC handling first
    if (event->key() == Qt::Key_Escape) {
        // Existing menu logic...
    }
    
    QMainWindow::keyPressEvent(event);
}

# View navigation pattern
void InventoryPage::keyPressEvent(QKeyEvent *event) {
    switch (event->key()) {
        case Qt::Key_Up:
            selectPreviousItem();
            break;
        case Qt::Key_Down:
            selectNextItem();
            break;
        case Qt::Key_Return:
            activateSelectedItem();
            break;
        case Qt::Key_Escape:
            emit backRequested();
            break;
        default:
            QWidget::keyPressEvent(event);
    }
}

# CRITICAL: Focus management
# Pattern: Ensure widgets get focus when switched to
void MainWindow::switchToInventory() {
    stackedWidget->setCurrentWidget(m_inventoryPage);
    m_inventoryPage->setFocus();  // CRITICAL: Enable key events
}
```

### Integration Points

```yaml
EXISTING_SLOTS:
  - MainWindow::handleInventoryBack() closes inventory
  - Need to find/create slots to OPEN screens
  - Check CombatPage for existing open slots

FOCUS_MANAGEMENT:
  - Add setFocus() calls when switching widgets
  - Ensure CombatPage has focus for global shortcuts

COMBAT_CHECK:
  - Add game state checking before shortcuts
  - Disable during active combat
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file modification - fix before proceeding
cd cpp-qt-rpg
make clean && cmake .. && make

# Check for compilation errors
# Expected: Clean compile with no errors
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component as it's created
cd cpp-qt-rpg
./test_mainwindow
./test_inventory_shortcuts
./test_shop_shortcuts  
./test_saveload_shortcuts

# Expected: All tests pass
```

### Level 3: Integration Testing (System Validation)

```bash
# Build and run full application
cd cpp-qt-rpg
./pyrpg-qt

# Manual testing:
# 1. Start game, reach CombatPage
# 2. Press I - inventory opens
# 3. Use arrow keys to navigate inventory
# 4. Press Enter to select item
# 5. Press ESC to close inventory
# 6. Repeat for S (shop) and L (save/load)

# Expected: All shortcuts work as specified
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Test during different game states
# 1. Test shortcuts only work in CombatPage
# 2. Test disabled during combat
# 3. Test no conflicts with ESC menu
# 4. Test on different screen sizes

# Performance test - rapid key presses don't crash
# Accessibility test - keyboard-only navigation works
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All new tests pass: `./test_*_shortcuts`
- [ ] No compilation errors in modified files
- [ ] Code follows existing Qt/C++ patterns
- [ ] No memory leaks from new event handlers

### Feature Validation

- [ ] All success criteria from "What" section met
- [ ] Manual testing successful: shortcuts work in game
- [ ] Error cases handled gracefully (combat state, etc.)
- [ ] Integration points work as specified
- [ ] No regressions in existing mouse functionality

### Code Quality Validation

- [ ] Follows existing codebase patterns and naming conventions
- [ ] File placement matches desired codebase tree structure
- [ ] keyPressEvent overrides properly implemented
- [ ] Event acceptance and propagation handled correctly
- [ ] Focus management implemented

---

## Anti-Patterns to Avoid

- ❌ Don't use QShortcut when keyPressEvent is more appropriate for navigation
- ❌ Don't forget to call parent keyPressEvent for unhandled keys
- ❌ Don't implement shortcuts without checking current widget context
- ❌ Don't hardcode key codes - use Qt::Key constants
- ❌ Don't add shortcuts that conflict with existing ESC menu
- ❌ Don't implement navigation without proper focus management
