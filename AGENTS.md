# AGENTS.md

## Build/Lint/Test Commands
- **Build**: `cd cpp-qt-rpg && mkdir -p build && cd build && cmake .. && make`
- **Run**: `./pyrpg-qt` (from build dir)
- **All tests**: `ctest` (from build dir)
- **Single test**: `./test_models`, `./test_mainwindow`, `./test_persistence`, `./test_combat_page_dual_mode`, `./test_navigation_flow`

## Architecture & Structure
Qt6/C++17 turn-based RPG with QStackedWidget navigation. MainWindow controls views, Game manages logic, SaveManager handles persistence via QDataStream. Models: Character→Player/Monster, Item, Skill. Views in src/views/, components in src/components/, Qt resources via assets.qrc.

## Code Style Guidelines
- Qt conventions: camelCase methods, PascalCase classes, signals/slots pattern
- Serialization: Implement `friend QDataStream &operator<<(QDataStream &out, const ClassName &obj);` for persistent models
- Naming: Descriptive names, consistent Qt patterns (handleActionClicked() slots)
- Structure: Header (.h) and implementation (.cpp) files, proper includes
- Error handling: Qt's QObject framework with signals for UI updates

## Rules Files
- **.clinerules/pyside-qt.md**: qt-pyside-ux-validator agent for Qt UI/UX validation (despite C++ focus, UI principles apply)
