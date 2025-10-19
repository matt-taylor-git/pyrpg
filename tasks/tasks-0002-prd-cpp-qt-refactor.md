## Relevant Files

Since this is a new C++ project, all files will be created from scratch. The Python project files should be used as a reference.

- `CMakeLists.txt` - The main build script for CMake to configure and build the project.
- `assets.qrc` - Qt resource file to bundle all game assets (images, styles) into the executable.
- `src/main.cpp` - The main entry point for the C++ application.
- `src/MainWindow.h` / `src/MainWindow.cpp` - The main application window that will contain and manage all other UI views.
- `src/models/` - Directory for C++ data models (e.g., `Player.h`, `Item.h`, `Monster.h`) corresponding to `game/models.py`.
- `src/game/` - Directory for core game logic (e.g., `Game.h`, `CombatEngine.h`) corresponding to `game/game.py`.
- `src/views/` - Directory for all the different game screens/pages (e.g., `CharacterCustomizationPage.h`, `CombatPage.h`).
- `src/components/` - Directory for reusable custom widgets (e.g., `ValidationLabel.h`, `StatusIndicator.h`).
- `src/persistence/` - Directory for save/load logic (e.g., `SaveManager.h`).
- `tests/` - Directory for unit tests.
  - `tests/test_models.cpp` - Unit tests for data models.
  - `tests/test_combat.cpp` - Unit tests for the combat engine.

### Notes

- The project will be built using CMake and a C++ compiler (like GCC, Clang, or MSVC).
- Qt's signals and slots mechanism should be used for communication between UI components and game logic.
- Unit tests can be implemented using a framework like Google Test or the built-in Qt Test framework.

## Tasks

- [x] 1.0 Project Setup and Foundation
  - [x] 1.1 Initialize a new directory structure for the C++ project (`src`, `include`, `assets`, `tests`).
  - [x] 1.2 Create a root `CMakeLists.txt` file.
  - [x] 1.3 Configure CMake to find and link the required Qt6 modules (Core, GUI, Widgets).
  - [x] 1.4 Create a basic `main.cpp` that initializes a `QApplication`.
  - [x] 1.5 Create a placeholder `MainWindow` class and display it.

- [x] 2.0 Port Core Game Logic and Data Models
  - [x] 2.1 Create C++ header files (`.h`) for all data models (Player, Character, Monster, Item) based on `game/models.py`.
  - [x] 2.2 Implement the corresponding source files (`.cpp`) for the data models.
  - [x] 2.3 Port the core game logic from `game/game.py` into a `Game` class in C++.
  - [x] 2.4 Port item definitions and logic from `game/items.py`.
  - [x] 2.5 Add basic unit tests for the data models and core game logic.

- [x] 3.0 Implement UI Shell and Core Components
  - [x] 3.1 Implement the `MainWindow` to use a `QStackedWidget` to manage the different game views.
  - [x] 3.2 Re-implement the custom widgets from `ui/custom_widgets.py` and `ui/components/` in C++/Qt.
  - [x] 3.3 Load and apply the existing `styles.qss` stylesheet to the `QApplication`.

- [ ] 4.0 Implement Game Views and UI Logic
  - [ ] 4.1 Create C++ classes for each view from the `ui/views/` directory (e.g., `NewGameView`, `CharacterCustomizationPage`, `CombatPage`).
  - [ ] 4.2 Implement the UI layout and widgets for each view, mirroring the Python implementation.
  - [ ] 4.3 Connect UI element signals (e.g., button clicks) to slots in the game logic or view controllers.
  - [ ] 4.4 Port the UI controller logic from `ui/controllers.py` into the respective view classes or dedicated C++ controller classes.

- [ ] 5.0 Implement Persistence and Asset Management
  - [ ] 5.1 Implement a `SaveManager` class with `saveGame` and `loadGame` methods using `QDataStream` for binary serialization.
  - [ ] 5.2 Integrate the `SaveManager` with the UI (e.g., Save/Load buttons in the main menu).
  - [ ] 5.3 Create a Qt Resource file (`assets.qrc`) and add all game assets to it.
  - [ ] 5.4 Modify the UI code to load images and other resources from the Qt resource system.

- [ ] 6.0 Finalize, Package, and Test
  - [ ] 6.1 Replace generic file dialogs with `QFileDialog` for native save/load prompts.
  - [ ] 6.2 Configure CPack within the `CMakeLists.txt` to generate platform-specific installers/packages.
  - [ ] 6.3 Build and run the application on Windows, macOS, and Linux to ensure cross-platform compatibility.
  - [ ] 6.4 Conduct a full manual test of the application, comparing it against the original Python version to ensure feature parity.
