# PRP: Battle Arena Animations - Phase 3: Polish and Expansion

## Goal

**Feature Goal**: To enhance the visual richness of the battle arena by adding monster attack animations and expanding the variety of skill effects.

**Deliverable**: Monster attacks are visually animated, and a diverse set of particle effects are available for different skill types, further immersing the player in combat.

**Success Definition**: When a monster attacks, its sprite animates towards the player and returns. Different skill types (e.g., fire, ice, healing) display distinct and appropriate particle effects. The overall combat experience feels more dynamic and visually appealing.

## All Needed Context

### Context Completeness Check

_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_ - **Yes.** This document provides the complete plan, building upon the existing animation system.

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://doc.qt.io/qt-6/qpropertyanimation.html
  why: Continues to be the core for sprite movement and property changes.
  critical: Understanding how to reverse animations or create mirrored movements for monster attacks.

- url: https://doc.qt.io/qt-6/qsequentialanimationgroup.html
  why: For orchestrating monster attack sequences (move, pause, return).
  critical: Reusing patterns established in Phase 1 for player attacks.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/components/AnimationManager.cpp
  why: The central class for managing animations. Will be extended with methods for monster attack animations and more varied skill particle effects.
  pattern: Existing `playPlayerAttackAnimation` provides a template for `playMonsterAttackAnimation`.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/components/Particle.cpp
  why: The custom particle class. Will be modified or extended to allow for different visual styles.
  pattern: The `Particle` constructor and `advance` method can be adapted for different particle behaviors (e.g., color, size, velocity).

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/MainWindow.cpp
  why: Contains the main combat logic and state machine. Will need updates to trigger monster attack animations.
  pattern: The `onAnimationFinished` slot's state machine will be extended to handle `MonsterTurn` animations.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/game/Game.cpp
  why: Contains the game logic for monster attacks and skill effects. May need to expose more information about skill types to the `AnimationManager`.
  pattern: Observe how `playerAttack()` and `monsterAttack()` are called.
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
cpp-qt-rpg/
└── src/
    ├── components/
    │   ├── AnimationManager.h   # (MODIFY) Add new animation methods for monster attacks and varied skill effects.
    │   ├── AnimationManager.cpp # (MODIFY) Implement new animation methods.
    │   ├── Particle.h           # (MODIFY) Potentially add parameters for varied particle types.
    │   └── Particle.cpp         # (MODIFY) Implement varied particle behaviors.
    └── MainWindow.h             # (MODIFY) Update CombatState enum if needed.
    └── MainWindow.cpp           # (MODIFY) Update state machine to trigger monster attack animations.
```

## Implementation Blueprint

### Data models and structure

No new core data models are introduced. Existing `Player`, `Monster`, and `Skill` models will be used.

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: MODIFY src/components/AnimationManager.h
  - ADD: New public method: `void playMonsterAttackAnimation();`.
  - MODIFY: `playSkillParticleEffect(const QPointF& targetPos, Skill::SkillType skillType);` to accept a skill type for varied effects.

Task 2: MODIFY src/components/AnimationManager.cpp
  - IMPLEMENT: `playMonsterAttackAnimation()`:
    - Get the enemy and hero sprite labels from `CombatPage`.
    - Create a `QSequentialAnimationGroup`.
    - Create a `QPropertyAnimation` to animate the enemy's "pos" property towards the hero's position.
    - Add a pause.
    - Create a second `QPropertyAnimation` to animate the enemy's "pos" back to its original position.
    - Connect the group's `finished()` signal to `AnimationManager::animationFinished()`.
    - Start the group.
  - MODIFY: `playSkillParticleEffect()`:
    - Use a `switch` statement or `if/else if` based on `skillType` to create different particle configurations (e.g., color, size, velocity, lifetime).
    - Example: Fire skill -> red/orange particles, Ice skill -> blue/white particles, Healing skill -> green/yellow particles.

Task 3: MODIFY src/MainWindow.h
  - No changes to `CombatState` enum are strictly necessary if `MonsterTurn` already exists.

Task 4: MODIFY src/MainWindow.cpp
  - MODIFY: `onAnimationFinished()`:
    - In the `case MonsterTurn` block, before executing `m_game->monsterAttack()`:
      - Trigger `m_animationManager->playMonsterAttackAnimation();`.
      - Change `m_combatState` to `MonsterAttackAnimation`.
      - The `onAnimationFinished` will then be called again after the monster attack animation completes.
    - Add a new `case MonsterAttackAnimation`:
      - Execute the monster's attack logic (`QString monsterLog = m_game->monsterAttack();`).
      - Update UI.
      - Check if combat is over. If so, change state to `CombatEnded` and call `handleCombatEnded()`.
      - If not over, change state back to `Idle` and re-enable combat buttons: `m_combatPage->setCombatActive(true);`.
  - MODIFY: `handleSkillClicked()`:
    - Pass the `selectedSkill->skillType` to `m_animationManager->playSkillParticleEffect()`.

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
# No new unit tests are strictly required for this phase, but existing ones should not break.
# From the `cpp-qt-rpg/build` directory:
make test
# Expected: All existing tests should still pass.
```

### Level 3: Manual Feature Validation

1.  Build and run the application from the `cpp-qt-rpg/build` directory: `./pyrpg-qt`.
2.  Start a new game.
3.  Click "Explore" to enter combat.
4.  **VERIFY**: When the monster attacks, its sprite moves towards the player and returns.
5.  **VERIFY**: When the player uses different skills, distinct particle effects are displayed (e.g., different colors, sizes, or behaviors).
6.  **VERIFY**: The game correctly waits for monster attack animations and skill effects to complete before proceeding.

## Final Validation Checklist

- [ ] All validation levels completed successfully.
- [ ] The application compiles without errors.
- [ ] Monster attack animations are implemented and play correctly.
- [ ] Skill effects vary based on skill type.
- [ ] The combat flow correctly integrates monster attack animations and varied skill effects.
- [ ] `AnimationManager` includes methods for monster attack animations and handles skill types for particle effects.
- [ ] `MainWindow`'s state machine correctly handles `MonsterAttackAnimation` state.
