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
    src/main.cpp
    src/MainWindow.cpp
)

# Link against the Qt modules
target_link_libraries(pyrpg-qt PRIVATE Qt6::Widgets)

target_include_directories(pyrpg-qt PRIVATE src)

# --- Tests ---
add_executable(run-tests
    tests/test_main.cpp
    src/MainWindow.cpp
    src/MainWindow.h
)
target_link_libraries(run-tests PRIVATE Qt6::Widgets Qt6::Test)
target_include_directories(run-tests PRIVATE src)

add_test(NAME basic_tests COMMAND run-tests)
