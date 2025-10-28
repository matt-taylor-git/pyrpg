cmake_minimum_required(VERSION 3.16)
project(PyrpgQt VERSION 1.0)

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
    src/game/factories/SkillFactory.cpp
    src/game/factories/MonsterFactory.cpp
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
    src/components/SkillSelectionDialog.cpp
    src/components/CombatItemDialog.cpp
    src/components/CombatResultDialog.cpp
    src/components/MenuOverlay.cpp
    src/components/AnimationManager.cpp
    src/views/MainMenu.cpp
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
    src/views/MainMenu.cpp
    src/views/NewGameView.cpp
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
    src/components/SkillSelectionDialog.cpp
    src/components/CombatItemDialog.cpp
    src/components/CombatResultDialog.cpp
    src/components/MenuOverlay.cpp
    src/components/AnimationManager.cpp
    src/game/Game.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Monster.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
    src/game/factories/SkillFactory.cpp
    src/game/factories/MonsterFactory.cpp
    src/persistence/SaveManager.cpp
)
target_link_libraries(test_mainwindow PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_mainwindow PRIVATE src)
add_test(NAME MainWindowTest COMMAND test_mainwindow)

# Test for Data Models
add_executable(test_models tests/test_models.cpp src/models/Item.cpp src/models/Skill.cpp src/models/Character.cpp src/models/Player.cpp src/models/Monster.cpp src/game/factories/ItemFactory.cpp src/game/factories/SkillFactory.cpp src/game/factories/MonsterFactory.cpp src/game/Game.cpp src/persistence/SaveManager.cpp)
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
    src/game/factories/SkillFactory.cpp
    src/game/factories/MonsterFactory.cpp
)
target_link_libraries(test_persistence PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_persistence PRIVATE src)
add_test(NAME PersistenceTest COMMAND test_persistence)

# Test for CombatPage dual mode
add_executable(test_combat_page_dual_mode tests/test_combat_page_dual_mode.cpp src/views/CombatPage.cpp src/models/Player.cpp src/models/Character.cpp src/models/Monster.cpp src/models/Item.cpp src/models/Skill.cpp)
target_link_libraries(test_combat_page_dual_mode PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_combat_page_dual_mode PRIVATE src)
add_test(NAME CombatPageDualModeTest COMMAND test_combat_page_dual_mode)

# Test for Navigation Flow
add_executable(test_navigation_flow tests/test_navigation_flow.cpp src/MainWindow.cpp
    src/views/MainMenu.cpp
    src/views/NewGameView.cpp
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
    src/components/SkillSelectionDialog.cpp
    src/components/CombatItemDialog.cpp
    src/components/CombatResultDialog.cpp
    src/components/MenuOverlay.cpp
    src/components/AnimationManager.cpp
    src/game/Game.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Monster.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
    src/game/factories/SkillFactory.cpp
    src/game/factories/MonsterFactory.cpp
    src/persistence/SaveManager.cpp
)
target_link_libraries(test_navigation_flow PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_navigation_flow PRIVATE src)
add_test(NAME NavigationFlowTest COMMAND test_navigation_flow)

# Test for Inventory Shortcuts
add_executable(test_inventory_shortcuts tests/test_inventory_shortcuts.cpp
    src/views/InventoryPage.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
)
target_link_libraries(test_inventory_shortcuts PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_inventory_shortcuts PRIVATE src)
add_test(NAME InventoryShortcutsTest COMMAND test_inventory_shortcuts)

# Test for Shop Shortcuts
add_executable(test_shop_shortcuts tests/test_shop_shortcuts.cpp
    src/views/ShopPage.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
)
target_link_libraries(test_shop_shortcuts PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_shop_shortcuts PRIVATE src)
add_test(NAME ShopShortcutsTest COMMAND test_shop_shortcuts)

# Test for SaveLoad Shortcuts
add_executable(test_saveload_shortcuts tests/test_saveload_shortcuts.cpp
    src/views/SaveLoadPage.cpp
    src/persistence/SaveManager.cpp
    src/models/Player.cpp
    src/models/Character.cpp
    src/models/Monster.cpp
    src/models/Item.cpp
    src/models/Skill.cpp
    src/game/factories/ItemFactory.cpp
    src/game/factories/SkillFactory.cpp
    src/game/factories/MonsterFactory.cpp
)
target_link_libraries(test_saveload_shortcuts PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(test_saveload_shortcuts PRIVATE src)
add_test(NAME SaveLoadShortcutsTest COMMAND test_saveload_shortcuts)

# --- Packaging ---

include(CPack)

set(CPACK_PACKAGE_NAME "PyrpgQt")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A turn-based RPG game")
set(CPACK_PACKAGE_VENDOR "Gemini")
set(CPACK_PACKAGE_CONTACT "support@gemini.com")

# Platform-specific configurations
if(WIN32)
    set(CPACK_GENERATOR "NSIS")
    set(CPACK_NSIS_DISPLAY_NAME "PyrpgQt")
    set(CPACK_NSIS_PACKAGE_NAME "PyrpgQt")
    set(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL ON)
elseif(APPLE)
    set(CPACK_GENERATOR "DragNDrop")
    set(CPACK_DMG_VOLUME_NAME "PyrpgQt")
    set(CPACK_DMG_FORMAT "UDBZ")
else() # Linux
    set(CPACK_GENERATOR "DEB")
    set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Gemini")
    set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6widgets6 (>= 6.0), libqt6core6 (>= 6.0)")
endif()


