# PRD 0002: Python RPG Refactor to C++/Qt

## 1. Introduction/Overview

This document outlines the requirements for refactoring the existing Python-based RPG application to C++ using the Qt framework. The primary goal is to create a native, high-performance, cross-platform desktop application that mirrors the functionality of the original Python version. The refactor will focus on improving deployment, maintainability, and performance while retaining the existing feature set and user experience.

## 2. Goals

*   **Feature Parity:** Achieve a 1:1 port of all features from the Python application to the C++ version.
*   **Cross-Platform Compatibility:** Ensure the application compiles, runs, and is distributable on Windows, macOS, and major Linux distributions.
*   **Native Performance:** Leverage the performance benefits of C++ and Qt for a more responsive and efficient application.
*   **Idiomatic C++:** Implement the application using modern C++ (C++17 or newer) and Qt best practices, rather than a direct line-by-line translation of Python code.

## 3. User Stories

The user stories remain the same as the original application. Key stories include:

*   **As a player,** I want to start a new game and create a character by customizing its name, class, and stats.
*   **As a player,** I want to save my game progress to a file so I can resume it later.
*   **As a player,** I want to load a previously saved game from the main menu.
*   **As a player,** I want to navigate between different screens, including the main menu, character creation, adventure, combat, and inventory.
*   **As a player,** I want to engage in turn-based combat with randomly encountered monsters.
*   **As a player,** I want to manage my character's inventory, equipping and unequipping items.

## 4. Functional Requirements

1.  **UI Implementation:** The entire user interface shall be rebuilt using C++ and the Qt Widgets module. All existing UI components, views, and layouts must be replicated.
2.  **Game Logic Port:** All game logic, including character creation, combat mechanics, item management, and game state progression, shall be ported to C++.
3.  **Save/Load System:** A new save/load system shall be implemented using C++ native serialization methods (e.g., `QDataStream` for binary files or a lightweight SQL database like SQLite). This will replace the current JSON-based system.
4.  **Build System:** The project shall use CMake as its build system to facilitate cross-platform compilation.
5.  **Asset Management:** All game assets (images, stylesheets) shall be managed through Qt's resource system (`.qrc`) to ensure they are bundled into the final executable.
6.  **Platform Integration:** The application should use native file dialogs for saving and loading games and correctly handle windowing and user input on all target platforms.

## 5. Non-Goals (Out of Scope)

*   **New Features:** No new gameplay features, characters, items, or UI elements will be added during this refactoring project.
*   **UI Redesign:** The existing UI/UX design will be replicated, not redesigned.
*   **Mobile Support:** The initial scope does not include support for mobile platforms like iOS or Android.

## 6. Design Considerations

*   The visual appearance of the Python application, defined in `styles.qss`, should be preserved by using Qt Style Sheets in the new application.
*   The application's window size, layout, and component hierarchy should closely match the original version.

## 7. Technical Considerations

*   **C++ Standard:** The project will use a modern C++ standard (C++17 or newer).
*   **Qt Version:** The project should target a recent, stable version of Qt (e.g., Qt 6).
*   **Project Structure:** The C++ source code should be organized into a logical structure, separating UI code, game logic, and data models.

## 8. Success Metrics

*   The C++ application is feature-complete and behaves identically to the Python version from a user's perspective.
*   The application successfully builds and runs on target versions of Windows, macOS, and a designated Linux distribution (e.g., Ubuntu 22.04).
*   The new save/load system is robust and works consistently across all supported platforms.
*   The final application can be packaged into distributable formats for each target platform (e.g., `.exe`, `.dmg`, `.AppImage`).

## 9. Open Questions

*   Should a migration tool or import function be developed to convert existing `.json` save files to the new C++ native format?
*   Are there any specific third-party C++ libraries that should be considered or avoided?
