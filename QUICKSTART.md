# PyRPG Qt - Quick Start Guide

Get up and running with PyRPG Qt in 5 minutes!

## Prerequisites

Install these before starting:

**macOS:**
```bash
brew install cmake qt@6
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install cmake qt6-base-dev libqt6widgets6
```

**Windows:**
- Install Qt6 from [qt.io](https://www.qt.io/download) or use vcpkg
- Install CMake from [cmake.org](https://cmake.org/download/)

## Quick Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pyrpg/take2
```

### 2. Verify Qt6 Path (macOS/Linux)
Check if Qt6 is at the expected location:

**macOS:**
```bash
ls /opt/homebrew/lib/cmake/Qt6
```

**Linux:**
```bash
pkg-config --modversion Qt6Widgets
```

If Qt6 is installed elsewhere, edit `cpp-qt-rpg/CMakeLists.txt` line 17 to point to your Qt6 installation.

### 3. Build the Project
```bash
cd cpp-qt-rpg
mkdir -p build
cd build
cmake ..
make
```

On Windows, use:
```bash
cmake --build . --config Release
```

### 4. Run the Game
```bash
./pyrpg-qt
```

On Windows:
```bash
.\Release\pyrpg-qt.exe
```

### 5. Run Tests (Optional)
```bash
ctest
```

Or run individual tests:
```bash
./test_models
./test_mainwindow
./test_persistence
```

## First Time Playing

1. **New Game**: Click "New Game" from the main menu
2. **Character Creation**: Enter a name and select a character class
3. **Explore**: Click "Explore" to encounter enemies
4. **Combat**: Use Attack, Skills, or Items to defeat monsters
5. **Level Up**: Gain experience and level up your character
6. **Shop**: Visit the shop to buy better equipment
7. **Save**: Use the Save/Load page to save your progress

## Common Build Issues

### Qt6 Not Found
```
CMake Error: Could not find a package configuration file provided by "Qt6"
```

**Solution**: Update the Qt6 path in `cpp-qt-rpg/CMakeLists.txt` line 17:
```cmake
set(Qt6_DIR /path/to/your/Qt6/lib/cmake/Qt6)
```

### Build Directory Missing
**Solution**: Always create the build directory first:
```bash
mkdir -p cpp-qt-rpg/build
cd cpp-qt-rpg/build
```

### Make Command Not Found (Windows)
**Solution**: Use CMake's build command instead:
```bash
cmake --build . --config Release
```

## Project Structure (Quick Reference)

```
pyrpg/take2/cpp-qt-rpg/
├── src/
│   ├── main.cpp              # Application entry point
│   ├── MainWindow.h/.cpp     # Main UI controller
│   ├── models/               # Game data (Player, Monster, Item, Skill)
│   ├── game/                 # Game logic and factories
│   ├── views/                # UI screens (Combat, Inventory, Shop, etc.)
│   ├── components/           # Reusable UI components
│   ├── persistence/          # Save/load system
│   └── theme/                # UI styling
├── assets/                   # Images and stylesheets
├── tests/                    # Unit tests
└── CMakeLists.txt           # Build configuration
```

## Key Commands

**Build:**
```bash
cd cpp-qt-rpg/build && cmake .. && make
```

**Run:**
```bash
cd cpp-qt-rpg/build && ./pyrpg-qt
```

**Test:**
```bash
cd cpp-qt-rpg/build && ctest
```

**Clean Build:**
```bash
cd cpp-qt-rpg
rm -rf build
mkdir build && cd build
cmake .. && make
```

## Making Your First Change

### Example: Change Starting Gold

1. Open `cpp-qt-rpg/src/models/Player.cpp`
2. Find the Player constructor
3. Change the `gold` initialization value
4. Rebuild:
   ```bash
   cd cpp-qt-rpg/build && make
   ```
5. Run and create a new character to see your change

### Example: Add a Test

1. Open `cpp-qt-rpg/tests/test_models.cpp`
2. Add a new test method:
   ```cpp
   void TestModels::testNewFeature() {
       Player player("Test", "Warrior");
       QVERIFY(player.gold > 0);
   }
   ```
3. Rebuild and run tests:
   ```bash
   cd cpp-qt-rpg/build
   cmake .. && make
   ./test_models
   ```

## Next Steps

For comprehensive documentation, see:
- **ONBOARDING.md** - Complete developer guide
- **cpp-qt-rpg/CLAUDE.md** - Architecture and implementation details
- **AGENTS.md** - Quick command reference
- **README.md** - Project overview

## Game Controls

### Keyboard Shortcuts

**Global Navigation:**
- `I` - Inventory
- `S` - Stats
- `H` - Shop
- `L` - Save/Load
- `Esc` - Menu overlay
- `1-9` - Quick actions (context-specific)

**Combat:**
- `A` - Attack
- `K` - Use Skill
- `I` - Use Item
- `R` - Run

**Inventory:**
- Number keys (`1-9`) - Use item in slot

**Shop:**
- Number keys (`1-9`) - Buy item

**Save/Load:**
- Number keys (`1-9`) - Quick save/load slot

## Troubleshooting

### Game Won't Launch
- Check that all Qt6 libraries are installed
- On Linux, try: `ldd ./pyrpg-qt` to check dependencies
- On macOS, ensure Qt6 is in the library path

### Tests Fail
- Make sure you're in the build directory
- Run `cmake ..` again to regenerate build files
- Check that all test dependencies compiled successfully

### Changes Not Showing
- Make sure you ran `make` after editing code
- If editing assets or .qrc file, do a clean build: `rm -rf build && mkdir build && cd build && cmake .. && make`

## Getting Help

For more detailed information:
1. Check the **ONBOARDING.md** section "How to Debug Common Issues"
2. Review the Qt6 documentation: https://doc.qt.io/qt-6/
3. Look at existing code examples in the `src/` directory

Happy coding!
