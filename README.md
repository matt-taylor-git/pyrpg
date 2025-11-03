# PyRPG Qt - C++ Edition

A modern turn-based RPG game built with Qt6 and C++17. This project was refactored from Python/PySide6 to C++ for improved performance and native platform integration.

## Features

- **Modern UI Design** - Professional dark theme with One Dark Pro color scheme
- **Sidebar Navigation** - Easy navigation between Adventure, Stats, Inventory, and Shop pages
- **Combat System** - Turn-based combat with critical hits, dodging, and special attacks
- **Character Progression** - Level up system with stat increases and skill points
- **Equipment System** - Collect and equip weapons, armor, and accessories
- **Inventory Management** - Grid-based inventory with item cards
- **Shop System** - Buy and sell items with a beautiful card-based interface
- **Item Rarity** - Common, Uncommon, Rare, Epic, and Legendary items with color-coding
- **Animated Overlays** - Smooth transitions and modern UI interactions

## Screenshots

The game features:
- Character creation with custom overlay
- Real-time combat visualization
- Detailed stats page with comprehensive hero information
- Interactive inventory with item cards
- Shop with visual item browsing

## Installation

### Prerequisites
- Qt6 (Widgets module)
- CMake 3.16 or higher
- C++17 compatible compiler

### Building

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pyrpg.git
cd pyrpg/cpp-qt-rpg
```

2. Build the project:
```bash
mkdir -p build && cd build
cmake ..
make
```

3. Run the game:
```bash
./pyrpg-qt
```

### Running Tests
```bash
cd build
ctest
```

## Game Controls

- **New Game** - Create a new character and start your adventure
- **Explore** - Venture into the wilderness to encounter enemies
- **Shop** - Visit the merchant to buy equipment and sell items
- **Stats** - View detailed character statistics
- **Inventory** - Manage your items and equipment
- **Rest** - Restore your health to maximum

## Combat

During combat you can:
- **Attack** - Deal damage to enemies
- **Use Item** - Use consumables like potions
- **Run** - Attempt to escape from battle

## Lore & Codex System

Discover the rich history and lore of the world through the **Codex** - a collection of entries about enemies, items, characters, locations, and world events.

### How to Access

- Press **L** key during gameplay to open the Lore Book
- Navigate through 5 categories:
  - **Bestiary** - Information about creatures you've encountered
  - **Items** - Backstories of legendary equipment and artifacts
  - **World** - Historical events and world lore
  - **Characters** - Biographies of important NPCs
  - **Locations** - Details about places in the world

### How to Unlock Lore

Lore entries unlock automatically as you play:

- **Defeat Enemies** - After defeating certain enemies multiple times, unlock bestiary entries
- **Find Rare Items** - Discover legendary or rare items to unlock their lore
- **Complete Quests** - Major quest completions reveal world history and character backgrounds
- **Explore** - Visiting new locations and progressing the story unlocks new entries

### Notifications

Watch the **combat log** for notifications when you unlock new lore:
- "**New Codex Entry: Shadow Wolves**" appears when a new entry is discovered
- All unlocked lore persists through save/load

### Tips

- Defeat the same enemy type multiple times to unlock their bestiary entry
- Purchase special items from the shop to discover their lore
- Complete all main quests to unlock the full world history
- Save your game regularly to preserve your lore discoveries

**Total Entries**: 30 lore entries across 5 categories wait to be discovered!

## Technologies

- **C++17** - Modern C++ standard
- **Qt6 Widgets** - Cross-platform GUI framework
- **CMake** - Build system with Qt automation (AUTOMOC, AUTOUIC, AUTORCC)
- **Qt Test** - Unit testing framework
- **QDataStream** - Game state serialization

## Project Structure

```
pyrpg/
└── cpp-qt-rpg/
    ├── src/              # Source code
    │   ├── game/        # Game logic (Player, Monster, Game controller)
    │   ├── views/       # UI views (Combat, Inventory, Stats, Shop, etc.)
    │   ├── components/  # Custom UI components
    │   ├── persistence/ # Save/load system
    │   └── theme/       # Styling and theme constants
    ├── assets/          # Game assets (images, stylesheets)
    ├── tests/           # Unit tests
    ├── CMakeLists.txt   # Build configuration
    └── CLAUDE.md        # Development guide
```

## Development

For detailed development information, architecture overview, and coding guidelines, see [cpp-qt-rpg/CLAUDE.md](cpp-qt-rpg/CLAUDE.md).

## History

This project was originally developed in Python with PySide6 and has been refactored to C++ with Qt6 for improved performance. The Python implementation is preserved in the git history.

## License

This project is open source and available for educational purposes.
