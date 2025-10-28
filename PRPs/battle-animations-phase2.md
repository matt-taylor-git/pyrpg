# PRP: Battle Arena Animations - Phase 2: Health Bar and Skill Effects

## Goal

**Feature Goal**: To implement animated health bar updates and a basic particle effect system for skill usage, enhancing visual feedback during combat.

**Deliverable**: Animated health and mana bars that smoothly transition to new values, and a visual particle effect that plays when a player uses a skill, integrated into the asynchronous combat flow.

**Success Definition**: When a character takes damage or uses mana, their respective health/mana bar animates down to the new value. When a skill is used, a particle effect appears at the target's location, and the game waits for the effect to complete before proceeding with the next combat step.

## All Needed Context

### Context Completeness Check

_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_ - **Yes.** This document provides the complete plan, from file modifications to new class implementations, with specific code patterns and external documentation.

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://doc.qt.io/qt-6/qpropertyanimation.html
  why: Core class for animating properties like QProgressBar's 'value'.
  critical: The property to be animated must have a setter. QProgressBar's 'value' property is suitable.

- url: https://doc.qt.io/qt-6/qsequentialanimationgroup.html
  why: To orchestrate multiple animations (e.g., skill particle effect followed by damage animation).
  critical: Animations added to this group are owned by the group.

- url: https://doc.qt.io/qt-6/qgraphicsview.html
  why: Provides a canvas for managing and interacting with a large number of 2D graphical items, suitable for particle systems.
  critical: QGraphicsView works with QGraphicsScene and QGraphicsItem. It needs to be integrated into the existing QWidget-based UI.

- url: https://doc.qt.io/qt-6/qgraphicsscene.html
  why: Manages the graphical items. Particles will be QGraphicsItems added to this scene.
  critical: The scene is the container for all graphical items.

- url: https://doc.qt.io/qt-6/qgraphicsitem.html
  why: Base class for all graphical items in a QGraphicsScene. Custom particle classes will inherit from this.
  critical: Custom items need to implement paint() and boundingRect().

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/MainWindow.cpp
  why: Contains the main combat logic and state machine. Will need updates to trigger skill animations and handle health bar updates.
  pattern: Observe how signals from UI pages (like `m_combatPage`) are connected to handler slots in `MainWindow`.
  gotcha: The `handleSkillClicked` method currently processes skill logic synchronously. This needs to be refactored to be asynchronous, similar to `handleAttackClicked`.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/views/CombatPage.cpp
  why: Defines the battle arena UI. Will need to expose QProgressBar elements and potentially a QGraphicsView for particle effects.
  pattern: UI elements are created and placed in the `setupUi` and `createArenaCard` methods.
  gotcha: Integrating QGraphicsView into an existing QWidget layout requires careful management of layout and sizing.

- file: /home/matt/code/pyrpg/cpp-qt-rpg/src/components/AnimationManager.cpp
  why: The central class for managing animations. Will be extended with methods for health bar animations and skill particle effects.
  pattern: Existing `playPlayerAttackAnimation` shows how to use `QSequentialAnimationGroup`.
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
cpp-qt-rpg/
└── src/
    ├── components/
    │   ├── AnimationManager.h   # (MODIFY) Add new animation methods.
    │   ├── AnimationManager.cpp # (MODIFY) Implement new animation methods.
    │   ├── Particle.h           # (NEW) Header for a custom QGraphicsItem for particles.
    │   └── Particle.cpp         # (NEW) Implementation of the custom particle.
    ├── views/
    │   ├── CombatPage.h         # (MODIFY) Add accessors for QProgressBars and QGraphicsView.
    │   └── CombatPage.cpp         # (MODIFY) Implement accessors and integrate QGraphicsView.
    └── MainWindow.h             # (MODIFY) Update CombatState enum and add new slots.
    └── MainWindow.cpp           # (MODIFY) Refactor skill logic, update state machine.
```

## Implementation Blueprint

### Data models and structure

No new core data models are introduced in this phase. Existing `Player` and `Monster` models will be used.

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: MODIFY src/views/CombatPage.h
  - ADD: Public accessor methods for `m_heroHealthBar`, `m_heroManaBar`, `m_enemyHealthBar`.
  - ADD: A `QGraphicsView* m_graphicsView;` and `QGraphicsScene* m_graphicsScene;` members.
  - ADD: Public accessor methods for `m_graphicsView` and `m_graphicsScene`.

Task 2: MODIFY src/views/CombatPage.cpp
  - IMPLEMENT: The accessor methods for health/mana bars, graphics view, and graphics scene.
  - MODIFY: In `createArenaCard()`, initialize `m_graphicsScene` and `m_graphicsView`.
  - INTEGRATE: Add `m_graphicsView` to the `spritesLayout` or a suitable container within `createArenaCard()`.
  - CONFIGURE: Set `m_graphicsScene`'s scene rect and `m_graphicsView`'s render hints (e.g., `Antialiasing`).

Task 3: CREATE src/components/Particle.h
  - IMPLEMENT: A custom `QGraphicsItem` class named `Particle`.
  - INHERIT: From `QGraphicsEllipseItem` or `QGraphicsRectItem`.
  - MEMBERS: `QPointF m_velocity;`, `int m_lifetime;`, `QColor m_color;`.
  - METHODS: Constructor, `advance(int phase) override`, `bool isDead() const`.

Task 4: CREATE src/components/Particle.cpp
  - IMPLEMENT: The `Particle` class methods.
  - CONSTRUCTOR: Initialize position, velocity, lifetime, color, and set brush/pen.
  - advance(): Update particle position based on velocity, decrease lifetime, and optionally fade out.
  - isDead(): Return true if `m_lifetime <= 0`.

Task 5: MODIFY src/components/AnimationManager.h
  - ADD: New public methods: `playHealthBarAnimation(QProgressBar* bar, int startValue, int endValue);`, `playSkillParticleEffect(const QPointF& targetPos, const QColor& color);`.

Task 6: MODIFY src/components/AnimationManager.cpp
  - INCLUDE: `Particle.h`.
  - IMPLEMENT: `playHealthBarAnimation()`:
    - Create a `QPropertyAnimation` targeting the `bar`'s "value" property.
    - Set duration, start value, end value, and an easing curve (e.g., `OutCubic`).
    - Connect its `finished()` signal to `AnimationManager::animationFinished()`.
    - Start the animation.
  - IMPLEMENT: `playSkillParticleEffect()`:
    - Get `m_graphicsScene` from `CombatPage`.
    - Create and add multiple `Particle` objects to the scene at `targetPos` with specified `color` and random velocities/lifetimes.
    - Use a `QTimer` to periodically call `m_graphicsScene->advance()` and remove dead particles.
    - Connect the `QTimer`'s `timeout()` signal to a private slot (e.g., `_updateParticles()`) that handles particle emission and removal.
    - Emit `animationFinished()` after a fixed duration or when all particles are dead.

Task 7: MODIFY src/MainWindow.h
  - UPDATE: `enum CombatState` to include `PlayerSkillAnimation`, `MonsterSkillAnimation`.
  - ADD: A new private slot `void onSkillAnimationFinished();` (or integrate into `onAnimationFinished`).

Task 8: MODIFY src/MainWindow.cpp
  - REFRACTOR: `handleSkillClicked()`:
    - Remove synchronous skill logic.
    - Set `m_combatState = PlayerSkillAnimation;`.
    - Disable combat buttons.
    - Trigger `m_animationManager->playSkillParticleEffect(...)`.
  - MODIFY: `onAnimationFinished()`:
    - Add `case PlayerSkillAnimation`:
      - Execute player skill logic (`m_game->playerUseSkill(...)`).
      - Update UI (`m_combatPage->updateCombatState(...)`).
      - Trigger health bar animations for affected characters.
      - Transition to `PlayerDamage` or `MonsterTurn` state based on combat outcome.
    - Add logic to trigger health bar animations after `playerAttack()` and `monsterAttack()` calls.

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
# Consider adding unit tests for Particle class if its logic becomes complex.
# From the `cpp-qt-rpg/build` directory:
make test
# Expected: All existing tests should still pass.
```

### Level 3: Manual Feature Validation

1.  Build and run the application from the `cpp-qt-rpg/build` directory: `./pyrpg-qt`.
2.  Start a new game.
3.  Click "Explore" to enter combat.
4.  **VERIFY**: When a character takes damage, their health bar animates smoothly down to the new value.
5.  **VERIFY**: When a character uses mana, their mana bar animates smoothly down to the new value.
6.  Click the "Use Skill" button.
7.  Select a skill.
8.  **VERIFY**: A particle effect appears at the target's location.
9.  **VERIFY**: The game waits for the particle effect to complete before processing the monster's turn.
10. **VERIFY**: The action buttons are disabled during skill animation and re-enabled after the full combat sequence.

## Final Validation Checklist

- [ ] All validation levels completed successfully.
- [ ] The application compiles without errors.
- [ ] Health and mana bars animate smoothly.
- [ ] Skill usage triggers a visual particle effect.
- [ ] The combat flow correctly integrates skill animations and waits for their completion.
- [ ] `CombatPage.h` and `CombatPage.cpp` expose necessary UI elements for animation.
- [ ] `Particle.h` and `Particle.cpp` define a functional particle item.
- [ ] `AnimationManager` includes methods for health bar and skill particle animations.
- [ ] `MainWindow`'s state machine correctly handles `PlayerSkillAnimation` state.
