# PyRPG Adventure

A modern Python RPG game with a beautiful GUI built using PySide6 (Qt for Python).

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

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pyrpg.git
cd pyrpg
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On macOS/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

4. Install dependencies:
```bash
pip install PySide6
```

## Usage

Run the game:
```bash
python main.py
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

## Technologies

- **Python 3.x**
- **PySide6** - Qt for Python GUI framework
- **Object-Oriented Design** - Clean MVC architecture
- **Modern UI Components** - Custom widgets and overlays

## Project Structure

```
pyrpg/
├── main.py              # Main application entry point
├── models.py            # Hero, Enemy, and Item classes
├── game.py              # Game logic and utilities
├── ui_components.py     # Reusable UI components
└── README.md
```

## License

This project is open source and available for educational purposes.
