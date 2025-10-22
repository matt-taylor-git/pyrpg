# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyrpgQt is a turn-based RPG game built with Qt6 (C++17) featuring character creation, combat, inventory management, and save/load functionality. The application uses a QStackedWidget-based architecture for view navigation and implements the Qt Widgets framework with custom styling via QSS.

## Build System

This project uses CMake with Qt6 automation features:
- **CMAKE_AUTOMOC**: Automatically runs Qt's Meta-Object Compiler
- **CMAKE_AUTOUIC**: Automatically processes Qt UI files
- **CMAKE_AUTORCC**: Automatically compiles Qt Resource files

### Common Commands

```bash
# Configure and build
mkdir -p build && cd build
cmake ..
make

# Run the application
./pyrpg-qt

# Run all tests
ctest

# Run specific test
./test_models
./test_mainwindow
./test_persistence

# Build from root directory
cmake --build build

# Clean build
rm -rf build && mkdir build && cd build && cmake .. && make
```

## Architecture

### Core Components

**MainWindow** (`src/MainWindow.h/cpp`)
- Central controller managing all game views via QStackedWidget
- Handles navigation between different game screens
- Owns the Game instance and coordinates game state with UI updates
- Connects view signals to game logic handlers

**Game** (`src/game/Game.h/cpp`)
- Core game logic controller (QObject-based)
- Manages Player, Monster instances, and combat state
- Interfaces with SaveManager for persistence
- Provides combat flow: startCombat(), playerAttack(), monsterAttack(), isCombatOver()

**SaveManager** (`src/persistence/SaveManager.h/cpp`)
- Handles game serialization/deserialization using QDataStream
- Save/load operations for Player state including inventory, equipment, stats
- All model classes (Character, Player, Monster, Item, Skill) implement QDataStream operators

### Data Model Hierarchy

```
Character (base class)
├── Player (adds mana, stats, inventory, equipment, experience)
└── Monster (enemy entities)

Item (equipment, consumables, with QDataStream support)
Skill (player abilities)
```

**Player** inherits from **Character** and adds:
- Stats: strength, dexterity, intelligence, vitality, mana
- Inventory system: QList<Item*> inventory, QMap<QString, Item*> equipment
- Progression: experience, skillPoints, statPoints, gold

### View Layer

All views inherit from QWidget and are managed by MainWindow's QStackedWidget:

- **MainMenu**: Entry point (New Game, Load Game, Exit)
- **NewGameView**: Character name input and class selection
- **CharacterCustomizationPage**: Character creation UI
- **AdventurePage**: Main exploration hub (Explore, Rest, Save/Load, Shop, Stats)
- **CombatPage**: Turn-based combat interface
- **InventoryPage**: Player inventory management
- **StatsPage**: Character statistics display
- **MonsterStatsPage**: Enemy information display
- **SaveLoadPage**: Save/load game UI
- **ShopPage**: Item purchasing interface

### Custom Components

Located in `src/components/`:
- **AnimatedProgressBar**: Animated health/mana bars
- **ShadowedProgressBar**: Progress bars with shadow effects
- **ItemCard**: Visual item representation
- **ItemSelectionOverlay**: Item interaction overlay
- **LogDisplay**: Combat/event log display
- **ParticleSystem**: Visual effects system
- **StatusIndicator**: Character status display
- **ValidationLabel**: Input validation feedback
- **CharacterPreviewWidget**: Character appearance preview
- **CustomizationSection**: Character customization controls
- **ScalablePixmapLabel**: Image scaling widget

### Asset Management

**Qt Resource System** (`assets.qrc`):
- All assets embedded in the executable via Qt's resource system
- Access pattern: `":/assets/filename.ext"`
- Includes: images (character sprites, items, backgrounds), styles.qss
- Resources are compiled into the binary via CMAKE_AUTORCC

**Styling**: Global QSS stylesheet at `assets/styles.qss` loaded in main.cpp
- Theme constants defined in `src/theme/Theme.h` (colors, spacing, fonts)
- Dark theme with crimson accent color (#dc3545)

### Factory Pattern

**ItemFactory** (`src/game/factories/ItemFactory.h/cpp`):
- Static methods for item creation
- `generateRandomItem(int enemyLevel)`: Procedural loot generation
- `getShopItems()`: Returns predefined shop inventory
- `createItem(const QString &name)`: Named item instantiation

## Testing

Uses Qt Test framework (Qt6::Test). Three test suites:

1. **test_models**: Tests Player, Monster, ItemFactory
2. **test_mainwindow**: Integration tests for UI and game flow
3. **test_persistence**: SaveManager serialization tests

Test files must include the moc file: `#include "test_filename.moc"` and use `QTEST_MAIN(TestClassName)` macro.

## Important Implementation Details

### Adding New Source Files

When adding .cpp files, update **CMakeLists.txt** in relevant sections:
- Main executable: `add_executable(pyrpg-qt ...)`
- Test executables: Each test target needs dependencies
- All tests must link against `Qt6::Widgets Qt6::Test`
- Include directories: `target_include_directories(... PRIVATE src)`

### Resource File Updates

When adding assets:
1. Place file in `assets/` directory
2. Add entry to `assets.qrc` within `<qresource prefix="/">` tags
3. Access in code via `":/assets/filename"`
4. Rebuild (CMAKE_AUTORCC will recompile resources)

### Serialization

Models requiring persistence must implement:
```cpp
friend QDataStream &operator<<(QDataStream &out, const ClassName &obj);
friend QDataStream &operator>>(QDataStream &in, ClassName &obj);
```

### Signal/Slot Connections

Views emit signals that MainWindow connects to handler methods:
- Pattern: `void handleActionClicked()` slot methods in MainWindow
- Navigation: Switch stackedWidget page in handler
- State updates: Call Game methods and refresh UI accordingly

## Dependencies

- **Qt6**: Widgets (GUI), Test (unit testing)
- **C++17**: Standard library features
- **CMake 3.16+**: Build system
