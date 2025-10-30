# Developer Onboarding Guide - PyRPG Qt Project

Welcome to PyRPG Qt! This comprehensive guide will help you get started contributing to this turn-based RPG game project.

## 1. Project Overview

### Project Purpose
PyRPG Qt is a modern turn-based RPG game built with Qt6 and C++17. Originally developed in Python/PySide6, it was refactored to C++ for improved performance and native platform integration. The game features character creation, turn-based combat, inventory management, equipment systems, and a shop interface with a professional dark theme UI.

### Tech Stack

**Core Technologies:**
- **Language**: C++17 (modern standard with std library features)
- **GUI Framework**: Qt6 Widgets (cross-platform GUI)
- **Build System**: CMake 3.16+ with Qt automation (AUTOMOC, AUTOUIC, AUTORCC)
- **Testing**: Qt Test framework
- **Serialization**: QDataStream for save/load functionality
- **Version Control**: Git

**Key Dependencies:**
- Qt6::Widgets - Main GUI framework
- Qt6::Test - Unit testing framework
- Qt6 on macOS typically installed via Homebrew at `/opt/homebrew/lib/cmake/Qt6`

### Architecture Pattern
The project follows a **layered MVC-inspired architecture** with Qt's signal/slot pattern:

- **Model Layer**: Game entities (Player, Monster, Item, Skill, Character)
- **View Layer**: UI pages managed by QStackedWidget navigation
- **Controller Layer**: MainWindow orchestrates views, Game manages logic
- **Persistence Layer**: SaveManager handles serialization

### Main Functionality
- Character creation with class selection and customization
- Turn-based combat system with attacks, skills, and items
- Inventory management with equipment slots
- Shop system for buying/selling items
- Save/load game functionality with 10 save slots
- Character progression with leveling, stats, and experience
- Item rarity system (Common, Uncommon, Rare, Epic, Legendary)

---

## 2. Repository Structure

### Top-Level Directories

```
pyrpg/take2/
├── cpp-qt-rpg/          # Main C++ Qt application
│   ├── src/            # All source code
│   ├── assets/         # Game assets (images, stylesheets)
│   ├── tests/          # Unit tests (Qt Test framework)
│   ├── build/          # Build output directory (git-ignored)
│   ├── CMakeLists.txt  # Build configuration
│   └── CLAUDE.md       # Development guide for AI assistants
├── assets/             # Additional project assets
├── PRPs/               # Product Requirement Prompts (AI dev workflow)
│   ├── ai_docs/       # Library documentation for AI reference
│   └── *.md           # PRP templates and specifications
├── tasks/              # Task management files
├── tests/              # Root-level test utilities
├── venv/               # Python virtual environment (legacy from Python version)
├── .agents/            # Agent configuration
├── .claude/            # Claude Code configuration
├── .github/            # Would contain CI/CD (not currently present)
└── README.md           # Project overview
```

### C++ Source Code Organization (`cpp-qt-rpg/src/`)

```
src/
├── main.cpp                    # Application entry point
├── MainWindow.h/.cpp          # Central UI controller
├── models/                    # Data models
│   ├── Character.h/.cpp      # Base character class
│   ├── Player.h/.cpp         # Player character with inventory, stats
│   ├── Monster.h/.cpp        # Enemy entities
│   ├── Item.h/.cpp           # Equipment and consumables
│   └── Skill.h/.cpp          # Player abilities
├── game/                      # Game logic
│   ├── Game.h/.cpp           # Core game controller
│   └── factories/            # Factory pattern for entity creation
│       ├── ItemFactory.h/.cpp
│       ├── MonsterFactory.h/.cpp
│       └── SkillFactory.h/.cpp
├── views/                     # UI pages/screens
│   ├── MainMenu.h/.cpp
│   ├── NewGameView.h/.cpp
│   ├── CharacterCustomizationPage.h/.cpp
│   ├── CombatPage.h/.cpp
│   ├── InventoryPage.h/.cpp
│   ├── StatsPage.h/.cpp
│   ├── MonsterStatsPage.h/.cpp
│   ├── ShopPage.h/.cpp
│   └── SaveLoadPage.h/.cpp
├── components/                # Reusable UI components
│   ├── AnimatedProgressBar.h/.cpp
│   ├── ItemCard.h/.cpp
│   ├── LogDisplay.h/.cpp
│   ├── MenuOverlay.h/.cpp
│   ├── AnimationManager.h/.cpp
│   └── [many other components]
├── persistence/               # Save/load system
│   └── SaveManager.h/.cpp
└── theme/                     # Styling constants
    └── Theme.h               # Color definitions, spacing constants
```

### Test Structure (`cpp-qt-rpg/tests/`)

Each test file targets specific functionality:
- `test_models.cpp` - Model layer tests (Player, Monster, Items)
- `test_mainwindow.cpp` - UI integration tests
- `test_persistence.cpp` - Save/load functionality
- `test_combat_page_dual_mode.cpp` - Combat UI tests
- `test_navigation_flow.cpp` - View navigation tests
- `test_inventory_shortcuts.cpp` - Keyboard shortcut tests
- `test_shop_shortcuts.cpp` - Shop keyboard tests
- `test_saveload_shortcuts.cpp` - Save/load keyboard tests

### Non-Standard Patterns

**PRP Workflow**: This project uses "Product Requirement Prompts" (PRPs) - a structured approach to AI-assisted development. The `PRPs/` directory contains:
- Detailed feature specifications with context
- AI documentation references (`ai_docs/`)
- Implementation strategies and validation gates
- See `PRPs/README.md` for the PRP philosophy

**AGENTS.md**: Contains quick-reference information for AI coding assistants (build commands, architecture summary, code style guidelines).

**CLAUDE.md**: Located in `cpp-qt-rpg/`, provides detailed architectural guidance specifically for Claude Code.

---

## 3. Getting Started

### Prerequisites

**Required Software:**
- **C++ Compiler**: C++17 compatible (GCC 7+, Clang 5+, MSVC 2017+)
- **CMake**: Version 3.16 or higher
- **Qt6**: Qt6 Widgets module
  - macOS: `brew install qt@6` (typically installs to `/opt/homebrew/`)
  - Linux: `sudo apt install qt6-base-dev` (Ubuntu/Debian)
  - Windows: Download from qt.io or use vcpkg

**Optional:**
- **Python 3.13+**: For legacy Python version exploration (in venv)
- **Git**: For version control

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pyrpg/take2
   ```

2. **Verify Qt6 installation:**
   ```bash
   # macOS
   ls /opt/homebrew/lib/cmake/Qt6

   # Linux
   pkg-config --modversion Qt6Widgets
   ```

3. **Configure Qt6 path** (if not in standard location):
   Edit `cpp-qt-rpg/CMakeLists.txt` line 17:
   ```cmake
   set(Qt6_DIR /your/path/to/Qt6)
   ```

### Installing Dependencies

**macOS:**
```bash
brew install cmake qt@6
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install cmake qt6-base-dev qt6-base-dev-tools libqt6widgets6
```

**Windows:**
- Install Qt6 from qt.io or use vcpkg
- Install CMake from cmake.org or via chocolatey: `choco install cmake`

### Building the Project

```bash
# Navigate to the C++ project directory
cd cpp-qt-rpg

# Create and enter build directory
mkdir -p build
cd build

# Configure with CMake
cmake ..

# Build the project
make

# On Windows, use:
# cmake --build . --config Release
```

**Expected build output:**
- Executable: `build/pyrpg-qt`
- Test executables: `build/test_*`

### Running the Project Locally

```bash
# From the build directory
./pyrpg-qt

# Or from the root directory
cd cpp-qt-rpg && ./build/pyrpg-qt
```

### Running Tests

```bash
# From the build directory
ctest                    # Run all tests
ctest --verbose          # Run with detailed output

# Or run individual test executables
./test_models
./test_mainwindow
./test_persistence
```

### Building for Production

```bash
# Release build
cd cpp-qt-rpg
mkdir -p build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make

# Create distributable package (uses CPack)
cpack
```

**Platform-specific packages:**
- **macOS**: Creates a `.dmg` drag-and-drop installer
- **Linux**: Creates a `.deb` package
- **Windows**: Creates an NSIS installer

---

## 4. Key Components

### Entry Point
**File**: `cpp-qt-rpg/src/main.cpp`

Responsibilities:
- Initializes QApplication
- Loads global stylesheet from Qt resources (`:/assets/styles.qss`)
- Creates and shows MainWindow
- Enters Qt event loop

```cpp
QApplication app(argc, argv);
// Load stylesheet
MainWindow window;
window.show();
return app.exec();
```

### Core Business Logic

**Game Controller** (`src/game/Game.h/.cpp`)
- QObject-based controller managing game state
- Owns Player and Monster instances
- Provides combat flow: `startCombat()`, `playerAttack()`, `monsterAttack()`, `isCombatOver()`
- Interfaces with SaveManager for persistence
- Emits `combatEnded(bool playerWon)` signal when combat completes

**MainWindow** (`src/MainWindow.h/.cpp`)
- Central UI controller managing all views via QStackedWidget
- Owns the Game instance
- Connects view signals to game logic handlers
- Navigation between screens via slot methods (e.g., `handleExploreClicked()`)
- Implements keyboard shortcuts via `keyPressEvent()` override

### Database Models/Schemas

**Character Hierarchy** (`src/models/`)

Base class `Character`:
- Common properties: name, level, health, maxHealth, attack, defense
- Virtual methods for serialization

`Player` (inherits Character):
- Additional stats: mana, strength, dexterity, intelligence, vitality
- Inventory: `QList<Item*> inventory`
- Equipment: `QMap<QString, Item*> equipment` (slots: weapon, armor, accessory)
- Progression: experience, experienceToLevel, skillPoints, statPoints, gold
- Skills: `QList<Skill*> skills`
- Methods: `equipItem()`, `useItem()`, `gainExperience()`, `levelUp()`

`Monster` (inherits Character):
- Simplified enemy entities
- Used for combat encounters

`Item` (`src/models/Item.h`):
- Properties: name, description, type (weapon/armor/consumable/accessory)
- Stats: attack, defense, healthBonus, value (gold cost)
- Rarity: ItemRarity enum (Common, Uncommon, Rare, Epic, Legendary)
- Item slots: itemSlot (weapon, armor, accessory)

`Skill` (`src/models/Skill.h`):
- name, description, manaCost, damage, cooldown
- Skill types and effects

### API Endpoints / Routes
This is a desktop application without REST APIs. Navigation is handled internally via MainWindow's QStackedWidget:

**View Navigation Pattern:**
```cpp
// In MainWindow slot handlers
void MainWindow::handleExploreClicked() {
    m_game->startCombat();           // Update game state
    m_combatPage->updateDisplay();   // Refresh view
    stackedWidget->setCurrentWidget(m_combatPage);  // Navigate
}
```

### Configuration Management
- **Qt Resource System** (`assets.qrc`): Assets embedded in executable
- **Stylesheet**: `assets/styles.qss` (dark theme with crimson accents)
- **Theme Constants**: `src/theme/Theme.h` defines colors, spacing, fonts
- **CMake Configuration**: `CMakeLists.txt` sets Qt6 path, build options, test targets

### Authentication/Authorization
Not applicable - single-player desktop game with local save files.

### Persistence Layer

**SaveManager** (`src/persistence/SaveManager.h/.cpp`)
- 10 save slots system
- Save location: OS-specific (QStandardPaths::AppDataLocation)
  - macOS: `~/Library/Application Support/Gemini/Pyrpg-Qt/`
  - Linux: `~/.local/share/Gemini/Pyrpg-Qt/`
  - Windows: `%APPDATA%/Gemini/Pyrpg-Qt/`
- Serialization via QDataStream (binary format)
- Methods: `saveToSlot()`, `loadFromSlot()`, `deleteSaveSlot()`, `getSaveSlots()`

**Serialization Pattern:**
All persistent models implement:
```cpp
friend QDataStream &operator<<(QDataStream &out, const ClassName &obj);
friend QDataStream &operator>>(QDataStream &in, ClassName &obj);
```

---

## 5. Development Workflow

### Git Branch Naming Conventions
Currently, the project uses a simple workflow:
- **master**: Main development branch (also main branch for PRs)
- Feature branches: No strict convention currently enforced

**Recommended conventions** (if adopting):
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `test/description` - Test additions/improvements

### Creating a New Feature

**Step-by-step workflow:**

1. **Create a branch** (recommended):
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes to code:**
   - Add/modify source files in `cpp-qt-rpg/src/`
   - Update `CMakeLists.txt` if adding new .cpp files
   - Add assets to `assets/` and `assets.qrc` if needed

3. **Build and test locally:**
   ```bash
   cd cpp-qt-rpg/build
   cmake .. && make
   ./pyrpg-qt        # Manual testing
   ctest              # Run automated tests
   ```

4. **Write/update tests:**
   - Add test cases to relevant `tests/test_*.cpp` file
   - Or create a new test file (update CMakeLists.txt accordingly)

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: descriptive message about changes"
   ```

6. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub targeting master branch
   ```

### Testing Requirements

**Test Coverage Expectations:**
- All new model methods should have unit tests in `test_models.cpp`
- UI changes should be verified in `test_mainwindow.cpp` or relevant UI test
- Persistence changes require tests in `test_persistence.cpp`

**Running Tests:**
```bash
cd cpp-qt-rpg/build
ctest              # All tests
ctest -R Models    # Only model tests
ctest -V           # Verbose output
./test_models      # Direct execution for detailed output
```

**Test Structure:**
```cpp
#include <QtTest/QtTest>
class TestModels : public QObject {
    Q_OBJECT
private slots:
    void testPlayerCreation();
    void testItemEquipping();
    // ...
};
QTEST_MAIN(TestModels)
#include "test_models.moc"
```

### Code Style / Linting Rules

**Qt Conventions:**
- **Classes**: PascalCase (e.g., `MainWindow`, `SaveManager`)
- **Methods**: camelCase (e.g., `handleAttackClicked()`, `saveGame()`)
- **Member Variables**: m_ prefix for class members (e.g., `m_player`, `m_combatPage`)
- **Signals/Slots**: Use Qt signal/slot pattern with descriptive names
- **File Naming**: Match class names (e.g., `MainWindow.h` and `MainWindow.cpp`)

**C++ Style:**
- Use C++17 features where appropriate
- Prefer smart pointers (though Qt uses raw pointers with parent-child ownership)
- RAII principles
- Const correctness
- Descriptive variable/method names

**No automated linters currently configured**, but maintain consistency with existing code.

### PR Process and Review Guidelines

**Current Setup:**
- No formal PR template or CI/CD pipeline in place
- Reviews are manual

**Recommended PR Checklist:**
1. All tests pass (`ctest` succeeds)
2. Code builds without warnings
3. Changes are tested manually
4. New functionality includes tests
5. Code follows existing style conventions
6. CMakeLists.txt updated if new files added
7. Assets added to assets.qrc if needed

### CI/CD Pipeline Overview

**Current Status**: No automated CI/CD configured

**Recommendation**: Set up GitHub Actions workflow:
- Build on push/PR (Linux, macOS, Windows)
- Run ctest suite
- Check for build warnings
- Create release artifacts (optional)

Example workflow location: `.github/workflows/ci.yml`

---

## 6. Architecture Decisions

### Design Patterns Used

**1. MVC-Inspired Layered Architecture**
- **Why**: Clear separation of concerns; Qt's signal/slot pattern fits naturally
- **Implementation**: Models (data), Views (UI), MainWindow+Game (controllers)

**2. Factory Pattern**
- **Files**: `src/game/factories/ItemFactory.cpp`, `MonsterFactory.cpp`, `SkillFactory.cpp`
- **Why**: Centralized entity creation; supports procedural generation
- **Example**: `ItemFactory::generateRandomItem(enemyLevel)` for loot drops

**3. Signal/Slot Pattern (Qt)**
- **Why**: Loose coupling between UI and logic; event-driven architecture
- **Example**: Views emit signals → MainWindow slots handle → Update game state → Refresh UI

**4. QStackedWidget Navigation**
- **Why**: Simple page-based navigation; single window application
- **Implementation**: MainWindow manages all views in a stack, switches via `setCurrentWidget()`

### State Management Approach

**Game State**: Centralized in `Game` class (QObject)
- Player instance (with inventory, stats, equipment)
- Current monster (combat state)
- Combat active flag

**UI State**: Each view maintains local UI state
- Views query Game/Player for data when displayed
- Updates triggered by signals from Game

**Persistence**: SaveManager serializes entire Player state
- Binary format via QDataStream
- No database; file-based saves

### Error Handling Strategy

**Qt Framework Approach**:
- Signals for asynchronous error reporting
- Boolean return values for sync operations
- Qt's parent-child ownership prevents memory leaks

**Examples:**
- `SaveManager::saveGame()` returns `bool` (success/failure)
- `Game::combatEnded(bool playerWon)` signal for combat results
- Qt debug messages: `qDebug()`, `qWarning()` (not heavily used in code)

**No formal exception handling** - Qt style favors return codes and signals.

### Logging and Monitoring Setup

**Current Logging**:
- Combat log displayed in UI (`LogDisplay` component)
- In-game event messages shown to player

**Debug Logging**:
- Qt provides `qDebug()`, `qWarning()`, `qCritical()` (not extensively used)
- No structured logging framework

**Recommendation**: Add qDebug statements for development, consider Qt logging categories for production.

### Security Measures

**Save File Integrity**: No encryption or tampering prevention
- Save files can be manually edited
- Suitable for single-player offline game

**Recommendations** (if needed):
- Add checksum validation to save files
- Implement basic obfuscation for save data

### Performance Optimizations

**Asset Loading**: Qt Resource System embeds assets in binary
- Fast loading; no file I/O at runtime
- Trade-off: Larger executable size

**UI Rendering**: Qt's double-buffering and hardware acceleration
- Smooth animations via QPropertyAnimation
- Custom components like AnimatedProgressBar use Qt animations

**Memory Management**: Qt's parent-child ownership
- Automatic cleanup when parent widget destroyed
- Manual management for model objects (Items, Skills)

---

## 7. Common Tasks

### How to Add a New API Endpoint
**Not applicable** - this is a desktop application, not a web service.

For adding a new game action:
1. Add method to `Game` class (e.g., `void Game::restPlayer()`)
2. Add signal if async result needed (e.g., `signal void restCompleted()`)
3. Add slot handler in MainWindow (e.g., `void MainWindow::handleRestClicked()`)
4. Connect view signal to MainWindow slot in MainWindow constructor
5. Update game state in handler, refresh UI

### How to Create a New Database Model

**Example: Adding a "Quest" model**

1. **Create header file** (`src/models/Quest.h`):
   ```cpp
   #ifndef QUEST_H
   #define QUEST_H

   #include <QString>
   #include <QDataStream>

   class Quest {
   public:
       Quest(const QString &name, const QString &description);

       QString name;
       QString description;
       bool completed;
       int rewardGold;

       friend QDataStream &operator<<(QDataStream &out, const Quest &q);
       friend QDataStream &operator>>(QDataStream &in, Quest &q);
   };

   #endif
   ```

2. **Create implementation file** (`src/models/Quest.cpp`):
   ```cpp
   #include "Quest.h"

   Quest::Quest(const QString &name, const QString &description)
       : name(name), description(description), completed(false), rewardGold(0) {}

   QDataStream &operator<<(QDataStream &out, const Quest &q) {
       out << q.name << q.description << q.completed << q.rewardGold;
       return out;
   }

   QDataStream &operator>>(QDataStream &in, Quest &q) {
       in >> q.name >> q.description >> q.completed >> q.rewardGold;
       return in;
   }
   ```

3. **Update CMakeLists.txt**:
   Add `src/models/Quest.cpp` to the executable and relevant tests.

4. **Add to Player** (if needed):
   ```cpp
   // In Player.h
   QList<Quest*> quests;
   ```

5. **Update serialization** in `Player` operators to include quests.

### How to Add a New Test

**Example: Testing a new feature**

1. **Decide test file**:
   - Model tests → `tests/test_models.cpp`
   - UI tests → `tests/test_mainwindow.cpp`
   - New feature → Create `tests/test_myfeature.cpp`

2. **Create test file** (if new):
   ```cpp
   #include <QtTest/QtTest>
   #include "models/Player.h"

   class TestMyFeature : public QObject {
       Q_OBJECT
   private slots:
       void testFeatureFunction();
   };

   void TestMyFeature::testFeatureFunction() {
       Player player("Hero", "Warrior");
       QVERIFY(player.name == "Hero");
       // More assertions...
   }

   QTEST_MAIN(TestMyFeature)
   #include "test_myfeature.moc"
   ```

3. **Update CMakeLists.txt**:
   ```cmake
   add_executable(test_myfeature tests/test_myfeature.cpp
       src/models/Player.cpp
       # Add dependencies...
   )
   target_link_libraries(test_myfeature PRIVATE Qt6::Widgets Qt6::Test)
   target_include_directories(test_myfeature PRIVATE src)
   add_test(NAME MyFeatureTest COMMAND test_myfeature)
   ```

4. **Run test**:
   ```bash
   cd build && cmake .. && make
   ./test_myfeature
   ctest -R MyFeature
   ```

### How to Debug Common Issues

**Build Fails - Missing Qt6:**
```
CMake Error: Could not find a package configuration file provided by "Qt6"
```
**Solution**: Verify Qt6 installation and update Qt6_DIR in CMakeLists.txt (line 17).

**Undefined Reference Errors:**
```
undefined reference to `Player::equipItem(Item*)'
```
**Solution**: Add the .cpp file containing the implementation to CMakeLists.txt.

**Resource Not Found at Runtime:**
```
QPixmap: Cannot open file :/assets/hero.png
```
**Solution**: Add asset to `assets.qrc`, then rebuild to recompile resources.

**Segmentation Fault:**
- Check for null pointers (e.g., `Item*` in inventory)
- Verify Qt parent-child relationships for widgets
- Use debugger: `gdb ./pyrpg-qt` or `lldb ./pyrpg-qt`

**Tests Fail to Build:**
- Ensure all dependencies are listed in test target's CMakeLists.txt section
- Include `#include "test_name.moc"` at end of test file

### How to Update Dependencies

**Updating Qt Version:**

1. Install new Qt version (via package manager or qt.io)
2. Update `Qt6_DIR` in CMakeLists.txt if path changed
3. Update `find_package(Qt6 REQUIRED COMPONENTS ...)` if API changes
4. Rebuild: `rm -rf build && mkdir build && cd build && cmake .. && make`
5. Test thoroughly for API deprecations

**Adding a New Qt Module:**

Example: Adding Qt6::Network
1. Update CMakeLists.txt line 18:
   ```cmake
   find_package(Qt6 REQUIRED COMPONENTS Widgets Test Network)
   ```
2. Link to executable:
   ```cmake
   target_link_libraries(pyrpg-qt PRIVATE Qt6::Widgets Qt6::Network)
   ```
3. Use in code:
   ```cpp
   #include <QNetworkAccessManager>
   ```

---

## 8. Potential Gotchas

### Non-Obvious Configurations

**Qt6 Path on macOS:**
- Homebrew installs to `/opt/homebrew/lib/cmake/Qt6` (Apple Silicon) or `/usr/local/lib/cmake/Qt6` (Intel)
- CMakeLists.txt hardcodes the path (line 17); update if your installation differs

**Build Directory:**
- `build/` is git-ignored; you must create it manually first time
- CMake generates build files in-tree; don't commit them

**assets.qrc:**
- Changes to this file require full rebuild (CMake must re-run AUTORCC)
- Resource paths must start with `:/` in C++ code

### Required Environment Variables
**None required** for basic building/running.

Optional:
- `QT_DEBUG_PLUGINS=1` - Debug Qt plugin loading issues
- `QT_QPA_PLATFORM=offscreen` - Useful for headless testing (Linux)

### External Service Dependencies
**None** - this is a fully offline, standalone application.

### Known Issues or Workarounds

**Issue 1: CMakeLists.txt Duplicated Entries**
- Lines 47-48 duplicate entries from lines 40-41, 48-49
- **Workaround**: Benign; no impact on build
- **Fix**: Remove duplicate lines (cosmetic cleanup)

**Issue 2: No Automated CI/CD**
- Tests must be run manually before merging
- **Workaround**: Always run `ctest` before pushing
- **Recommendation**: Set up GitHub Actions

**Issue 3: Save File Compatibility**
- Save format is binary QDataStream; changes to model classes break old saves
- **Workaround**: Version save files if making serialization changes
- **Future**: Implement versioned serialization

**Issue 4: macOS App Bundles**
- Built executable is not a .app bundle; must use CPack for distribution
- **Workaround**: Use `cpack` to generate proper .dmg installer

**Issue 5: Python venv in Repo**
- Legacy `venv/` directory from Python version; not needed for C++ build
- **Workaround**: Ignore it; kept for historical reference
- Can be deleted if disk space is a concern

### Performance Bottlenecks

**Asset Loading:**
- All assets embedded in binary via Qt resources
- **Impact**: Larger executable, but faster runtime loading
- **Optimization**: If executable becomes too large, consider external asset loading

**Serialization:**
- QDataStream is straightforward but not optimized for large saves
- **Impact**: Minimal for current game complexity
- **Future**: Consider JSON or protobuf if save files grow large

**UI Redraws:**
- Qt handles this well with double-buffering
- **Potential issue**: Complex animations on older hardware
- **Mitigation**: AnimationManager uses Qt's efficient QPropertyAnimation

### Areas of Technical Debt

1. **No CI/CD Pipeline**
   - Manual testing only
   - **Priority**: Medium - Add GitHub Actions

2. **Inconsistent Error Handling**
   - Mix of bool returns and silent failures
   - **Priority**: Low - Functional but could be clearer

3. **Limited Input Validation**
   - Save file loading doesn't validate data thoroughly
   - **Priority**: Medium - Could lead to crashes with corrupted saves

4. **Hard-Coded Values**
   - Magic numbers in factories (e.g., item stats, spawn rates)
   - **Priority**: Low - Extract to config files for easier balancing

5. **Test Coverage Gaps**
   - Some UI flows not fully tested
   - **Priority**: Medium - Increase integration test coverage

6. **Documentation**
   - Inline comments are sparse in some files
   - **Priority**: Low - Code is fairly self-documenting

---

## 9. Documentation and Resources

### Existing Documentation

**Project Documentation:**
- `README.md` - Project overview, installation, basic usage
- `cpp-qt-rpg/CLAUDE.md` - Detailed architecture for AI assistants
- `AGENTS.md` - Quick reference (build commands, architecture summary)
- This file (`ONBOARDING.md`) - Comprehensive developer guide

**PRP Documentation:**
- `PRPs/README.md` - Product Requirement Prompt philosophy
- `PRPs/prp_spec.md` - PRP specification and structure
- `PRPs/*.md` - Various feature PRPs (keyboard shortcuts, animations, etc.)

### API Documentation
**No formal API docs** (not a library). Code is the documentation.

Key headers to understand:
- `src/game/Game.h` - Core game interface
- `src/MainWindow.h` - UI controller interface
- `src/models/Player.h` - Player data model
- `src/persistence/SaveManager.h` - Save/load interface

### Database Schemas
**File-based persistence** (no traditional database).

**Save File Structure** (QDataStream binary):
```
Player {
    Character base data (name, level, health, attack, defense)
    Stats (strength, dexterity, intelligence, vitality, mana)
    Experience, skillPoints, statPoints, gold
    Inventory (QList<Item*>)
    Equipment (QMap<QString, Item*>)
    Skills (QList<Skill*>)
}
```

Each nested object (Item, Skill) is also serialized recursively.

### Deployment Guides

**Desktop Distribution:**

1. **Build release version**:
   ```bash
   cmake -DCMAKE_BUILD_TYPE=Release ..
   make
   ```

2. **Package with CPack**:
   ```bash
   cpack
   ```

3. **Platform-specific outputs**:
   - **macOS**: `PyrpgQt-1.0.0-Darwin.dmg` (drag-and-drop installer)
   - **Linux**: `PyrpgQt-1.0.0-Linux.deb` (Debian package)
   - **Windows**: `PyrpgQt-1.0.0-win64.exe` (NSIS installer)

**Deployment considerations:**
- Users need Qt6 runtime libraries (either bundled or system-installed)
- macOS/Windows: Use Qt's `macdeployqt` / `windeployqt` tools to bundle Qt frameworks

**Not covered**: App Store / Steam deployment (would require additional setup)

### Team Conventions or Style Guides

**Current Conventions:**
- Follow Qt coding style (camelCase methods, PascalCase classes)
- Use Qt containers (QList, QMap) over STL when interfacing with Qt
- Member variables prefixed with `m_`
- Signal/slot naming: descriptive action-based names

**File Organization:**
- Each class in its own .h/.cpp pair
- Headers include only necessary dependencies (forward declarations preferred)
- Implementation files include full headers

**Git Commit Messages:**
- No strict convention enforced
- **Recommended**: Conventional Commits (feat:, fix:, refactor:, test:, docs:)

**Code Reviews:**
- No formal process documented
- **Recommended**: At least one reviewer approval before merge

---

## 10. Next Steps - Onboarding Checklist

Welcome aboard! Complete these steps to get fully oriented:

### 1. Set Up Development Environment
- [ ] Clone the repository
- [ ] Install Qt6, CMake, and C++ compiler
- [ ] Verify Qt6_DIR path in `cpp-qt-rpg/CMakeLists.txt` matches your installation
- [ ] Build the project successfully: `cd cpp-qt-rpg && mkdir build && cd build && cmake .. && make`

### 2. Run the Project Successfully
- [ ] Execute `./pyrpg-qt` from the build directory
- [ ] Create a new character and play through the tutorial
- [ ] Explore the main game loop: combat, inventory, shop, stats
- [ ] Save and load a game

### 3. Make a Small Test Change
- [ ] Modify `src/main.cpp` to change the application name
- [ ] Or change a stat value in `src/game/factories/ItemFactory.cpp`
- [ ] Rebuild and verify your change appears in the running game
- [ ] Revert your test change

### 4. Run the Test Suite
- [ ] Execute `ctest` from the build directory
- [ ] Verify all tests pass
- [ ] Run an individual test: `./test_models` to see detailed output
- [ ] Review test code in `tests/test_models.cpp` to understand testing patterns

### 5. Understand the Main User Flow
- [ ] Read through `src/MainWindow.cpp` to see how views are connected
- [ ] Trace the combat flow: `handleExploreClicked()` → `Game::startCombat()` → `CombatPage` display
- [ ] Study the save/load flow: `SaveLoadPage` → `MainWindow::handleSaveToSlot()` → `Game::saveToSlot()` → `SaveManager`
- [ ] Map out the navigation between views in your notes

### 6. Explore the Codebase Structure
- [ ] Browse the `src/models/` directory and understand the data models
- [ ] Look at `src/views/` and see how each game screen is implemented
- [ ] Review `src/components/` to see reusable UI components
- [ ] Check out `src/game/factories/` to understand entity creation

### 7. Read Key Documentation
- [ ] Read `cpp-qt-rpg/CLAUDE.md` for architectural details
- [ ] Skim `PRPs/README.md` to understand the PRP workflow (if contributing via AI-assisted development)
- [ ] Review `AGENTS.md` for quick command references

### 8. Identify Area to Start Contributing
- [ ] Look at open issues (if any) or areas of technical debt listed in section 8
- [ ] Pick a small task: add a new test, improve a component, or fix a known issue
- [ ] Set up a feature branch: `git checkout -b feature/my-first-contribution`

### 9. Ask Questions
- [ ] Reach out to team members if you're stuck
- [ ] Review the "How to Debug Common Issues" section (Section 7) if you encounter problems

### 10. Make Your First Contribution
- [ ] Implement a small feature or fix
- [ ] Write tests for your changes
- [ ] Run `ctest` to ensure all tests pass
- [ ] Commit your changes with a clear message
- [ ] Submit a PR for review

---

## Additional Resources

**Qt6 Documentation:**
- Official Docs: https://doc.qt.io/qt-6/
- Qt Widgets: https://doc.qt.io/qt-6/qtwidgets-index.html
- Qt Test: https://doc.qt.io/qt-6/qttest-index.html

**C++17 Reference:**
- https://en.cppreference.com/w/cpp/17

**CMake Documentation:**
- https://cmake.org/cmake/help/latest/

**PRP Methodology:**
- See `PRPs/README.md` for the team's approach to AI-assisted development

---

**Welcome to the team!** If you have questions or suggestions for improving this onboarding guide, please reach out or submit a PR.
