cmake_minimum_required(VERSION 3.16)
project(PyrpgQt VERSION 1.0)

# Set the path to the Qt installation
set(CMAKE_PREFIX_PATH "/opt/homebrew/opt/qt")

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Automatically run moc, uic, and rcc
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Find the required Qt modules
find_package(Qt6 REQUIRED COMPONENTS Widgets Test)

enable_testing()

# Add the executable
add_executable(pyrpg-qt
    assets.qrc
    src/main.cpp
    src/MainWindow.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/models/Character.cpp
    src/models/Player.cpp
    src/models/Monster.cpp
    src/game/Game.cpp
    src/game/factories/ItemFactory.cpp
    src/persistence/SaveManager.cpp
    src/components/ValidationLabel.cpp
    src/components/AnimatedProgressBar.cpp
    src/components/ShadowedProgressBar.cpp
    src/components/ScalablePixmapLabel.cpp
    src/components/LogDisplay.cpp
    src/components/ParticleSystem.cpp
    src/components/ItemCard.cpp
    src/components/ItemSelectionOverlay.cpp
    src/components/CharacterPreviewWidget.cpp
    src/components/CustomizationSection.cpp
    src/components/ScalablePixmapLabel.cpp
    src/components/LogDisplay.cpp
    src/components/StatusIndicator.cpp
    src/views/AdventurePage.cpp
    src/views/CharacterCustomizationPage.cpp
    src/views/CombatPage.cpp
    src/views/InventoryPage.cpp
    src/views/MonsterStatsPage.cpp
    src/views/NewGameView.cpp
    src/views/SaveLoadPage.cpp
    src/views/ShopPage.cpp
    src/views/StatsPage.cpp
)

# Link against the Qt modules
target_link_libraries(pyrpg-qt PRIVATE Qt6::Widgets)

target_include_directories(pyrpg-qt PRIVATE src)

# --- Tests ---
enable_testing()

# Test for MainWindow
add_executable(test_mainwindow tests/test_mainwindow.cpp src/MainWindow.cpp
    src/views/NewGameView.cpp
    src/views/AdventurePage.cpp
    src/views/CharacterCustomizationPage.cpp
    src/views/CombatPage.cpp
    src/views/InventoryPage.cpp
    src/views/MonsterStatsPage.cpp
    src/views/SaveLoadPage.cpp
    src/views/ShopPage.cpp
    src/views/StatsPage.cpp
    src/components/ValidationLabel.cpp
    src/components/CharacterPreviewWidget.cpp
    src/components/CustomizationSection.cpp
    src/game/Game.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Monster.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
    src/persistence/SaveManager.cpp
)
target_link_libraries(test_mainwindow PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_mainwindow PRIVATE src)
add_test(NAME MainWindowTest COMMAND test_mainwindow)

# Test for Data Models
add_executable(test_models tests/test_models.cpp src/models/Item.cpp src/models/Skill.cpp src/models/Character.cpp src/models/Player.cpp src/models/Monster.cpp src/game/factories/ItemFactory.cpp)
target_link_libraries(test_models PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_models PRIVATE src)
add_test(NAME ModelsTest COMMAND test_models)

# Test for Persistence
add_executable(test_persistence tests/test_persistence.cpp
    src/persistence/SaveManager.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Monster.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
)
target_link_libraries(test_persistence PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_persistence PRIVATE src)
add_test(NAME PersistenceTest COMMAND test_persistence)


