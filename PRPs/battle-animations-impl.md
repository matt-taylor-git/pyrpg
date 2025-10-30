
# PRP: Battle Arena Animations - Phase 1

## Goal

**Feature Goal**: To implement the core animation system for the battle arena, making the combat sequence asynchronous and providing initial visual feedback for player attacks.

**Deliverable**: A functional integration of a new `AnimationManager` class that plays a player attack animation (sprite movement) and a damage animation (sprite flash) within a refactored, asynchronous combat turn sequence in `MainWindow`.

**Success Definition**: When the player clicks "Attack", the hero sprite animates moving towards the enemy, the enemy flashes to indicate damage, and the monster's turn only begins after these animations are complete. The application remains responsive throughout the animation sequence.

## All Needed Context

### Context Completeness Check

_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_ - **Yes.** This document provides the complete plan, from file creation to the refactoring of the core combat loop, with specific code patterns and external documentation.

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://doc.qt.io/qt-6/qpropertyanimation.html
  why: This is the core class for all animations. Understand how to set the target object, property name (e.g., "pos", "geometry"), duration, and start/end values.
  critical: The property to be animated must have a setter with the `Q_PROPERTY` macro, or be a known `QWidget` property like "pos".

- url: https://doc.qt.io/qt-6/qsequentialanimationgroup.html
  why: This class is essential for playing animations one after another, which is required for the attack -> damage -> return sequence.
  critical: Animations added to this group are owned by the group. You don't need to delete them manually if the group has a parent.

- url: https://doc.qt.io/qt-6/qeasingcurve.html
  why: Easing curves make animations look natural (e.g., speeding up or slowing down) instead of linear and robotic.
  critical: Review the different curve types to select appropriate ones for attack (e.g., `InOutQuad`) and damage effects.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/MainWindow.cpp
  why: This file contains the main application and combat logic. The `handleAttackClicked` method is the entry point for the synchronous combat that needs to be refactored.
  pattern: Observe how signals from UI pages (like `m_combatPage`) are connected to handler slots in `MainWindow`. This pattern will be extended for animation signals.
  gotcha: The current `handleAttackClicked` function executes the entire player and monster turn in one go. This synchronous execution will block any animations, which is the core problem to solve.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/views/CombatPage.cpp
  why: This file defines the UI of the battle arena. It's where the sprites (`m_heroSpriteLabel`, `m_enemySpriteLabel`) that need to be animated are located.
  pattern: UI elements are created and placed in the `setupUi` and `createArenaCard` methods.
  gotcha: The sprite labels are raw `QLabel*` pointers. The `AnimationManager` will need direct access to them to apply animations.
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
cpp-qt-rpg/
└── src/
    ├── components/
    │   ├── AnimationManager.h   # (NEW) Header for the animation management class.
    │   └── AnimationManager.cpp # (NEW) Implementation of the animation logic.
    ├── views/
    │   ├── CombatPage.h         # (MODIFY) Add accessors for UI elements.
    │   └── CombatPage.cpp         # (MODIFY) Implement accessors.
    └── MainWindow.h             # (MODIFY) Add AnimationManager and combat state machine.
    └── MainWindow.cpp           # (MODIFY) Refactor combat logic to be asynchronous.
```

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE src/components/AnimationManager.h
  - IMPLEMENT: The `AnimationManager` class definition.
  - API: Include a constructor that takes a `CombatPage*`, public methods `playPlayerAttackAnimation()` and `playDamageAnimation(QLabel* target)`, and a public signal `animationFinished()`.
  - FOLLOW pattern: Use standard Qt `QObject` conventions with the `Q_OBJECT` macro.

Task 2: CREATE src/components/AnimationManager.cpp
  - IMPLEMENT: The `AnimationManager` methods.
  - playPlayerAttackAnimation():
    - Get the hero and enemy sprite labels from `CombatPage`.
    - Create a `QSequentialAnimationGroup`.
    - Create a `QPropertyAnimation` to animate the hero's "pos" property from its current position to the enemy's position. Use an `QEasingCurve::InOutQuad`.
    - Add a pause to the group using `addAnimation(new QPauseAnimation(100));`.
    - Create a second `QPropertyAnimation` to animate the hero's "pos" back to its original position.
    - Add both animations and the pause to the sequential group.
    - Connect the group's `finished()` signal to the `AnimationManager`'s `animationFinished()` signal.
    - Start the group.
  - playDamageAnimation():
    - This is a placeholder for now. For Phase 1, a simple sprite flash is enough. We will implement a more complex version later.
    - For now, just emit `animationFinished()` immediately.

Task 3: MODIFY src/views/CombatPage.h
  - ADD: Public accessor methods to get the sprite labels.
  - API: `QLabel* getHeroSpriteLabel();` and `QLabel* getEnemySpriteLabel();`.

Task 4: MODIFY src/views/CombatPage.cpp
  - IMPLEMENT: The accessor methods defined in the header. They should simply return the corresponding member variables (`m_heroSpriteLabel`, `m_enemySpriteLabel`).

Task 5: MODIFY src/MainWindow.h
  - INCLUDE: `AnimationManager.h`.
  - ADD: A private member `AnimationManager* m_animationManager;`.
  - ADD: An enum to manage the combat state: `enum CombatState { Idle, PlayerAttacking, PlayerDamage, MonsterTurn, CombatEnded };`.
  - ADD: A private member `CombatState m_combatState;`.
  - ADD: A new private slot `void onAnimationFinished();`.

Task 6: MODIFY src/MainWindow.cpp
  - INCLUDE: `AnimationManager.h`.
  - INSTANTIATE: In the `MainWindow` constructor, create the `AnimationManager`: `m_animationManager = new AnimationManager(m_combatPage, this);`.
  - CONNECT: In the constructor, connect the animation manager's signal to the new slot: `connect(m_animationManager, &AnimationManager::animationFinished, this, &MainWindow::onAnimationFinished);`.
  - REFACTOR: `handleAttackClicked()`:
    - Remove all existing logic.
    - Set the combat state: `m_combatState = PlayerAttacking;`.
    - Disable combat buttons to prevent user input during animation: `m_combatPage->setCombatActive(false);`.
    - Start the animation: `m_animationManager->playPlayerAttackAnimation();`.
  - IMPLEMENT: `onAnimationFinished()` slot:
    - Use a `switch` statement on `m_combatState`.
    - `case PlayerAttacking`:
        - Execute the player's attack logic (the code that was originally in `handleAttackClicked`): `QString log = m_game->playerAttack();`.
        - Update the UI: `m_combatPage->updateCombatState(...)`.
        - Check if combat is over. If so, change state to `CombatEnded` and call `handleCombatEnded()`.
        - If not over, change state to `PlayerDamage` and trigger the damage animation: `m_animationManager->playDamageAnimation(m_combatPage->getEnemySpriteLabel());`.
    - `case PlayerDamage`:
        - Now it's the monster's turn. Change state to `MonsterTurn`.
        - Execute the monster's attack logic: `QString monsterLog = m_game->monsterAttack();`.
        - Update UI.
        - Check if combat is over. If so, change state to `CombatEnded` and call `handleCombatEnded()`.
        - If not over, change state back to `Idle` and re-enable combat buttons: `m_combatPage->setCombatActive(true);`.
    - `default`: break.

```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# After creating/modifying files, run the build process.
# The project uses CMake. From the `cpp-qt-rpg/build` directory:
cmake ..
make
# Expected: Clean compile with no errors or warnings.
```

### Level 2: Unit Tests (Component Validation)

```bash
# No new unit tests are required for this phase, but existing ones should not break.
# From the `cpp-qt-rpg/build` directory:
make test
# Expected: All existing tests should still pass.
```

### Level 3: Manual Feature Validation

1.  Build and run the application from the `cpp-qt-rpg/build` directory: `./pyrpg-qt`.
2.  Start a new game.
3.  Click "Explore" to enter combat.
4.  Click the "Attack" button.
5.  **VERIFY**: The hero sprite moves smoothly to the enemy sprite's location.
6.  **VERIFY**: The hero sprite pauses briefly and then returns to its original position.
7.  **VERIFY**: Immediately after the hero returns, the enemy's health bar updates.
8.  **VERIFY**: The monster's attack log appears *after* the player's attack animation is fully complete.
9.  **VERIFY**: The action buttons ("Attack", "Skill", etc.) are disabled during the animation and are re-enabled once the entire sequence (player attack + monster attack) is finished.

## Final Validation Checklist

- [ ] All validation levels completed successfully.
- [ ] The application compiles without errors.
- [ ] The player attack sequence animates correctly as per the manual validation steps.
- [ ] The combat flow is asynchronous and the UI remains responsive.
- [ ] The `handleAttackClicked` method has been refactored and no longer contains synchronous game logic.
- [ ] The new `onAnimationFinished` slot correctly handles the combat state machine.
- [ ] The new files `AnimationManager.h` and `AnimationManager.cpp` are created in the correct location (`src/components/`).
- [ ] `CombatPage.h` and `MainWindow.h` have been modified as specified.
