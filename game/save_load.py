# -*- coding: utf-8 -*-
"""
Save/Load Game State Management
Handles serialization and deserialization of game state to/from JSON files
"""

import json
import os
from collections import OrderedDict
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union


class GameState:
    """
    Represents the complete game state for save/load operations.

    Encapsulates all game data that needs to be persisted between sessions:
    - Hero character stats and customization
    - Inventory and equipment
    - Game progress and achievements
    - Settings and preferences
    """

    def __init__(self):
        """Initialize a new game state."""
        self.hero = None
        self.inventory = []
        self.equipment = {}
        self.game_progress = {}
        self.settings = {}
        self.session_stats = {}
        self.metadata = {}

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load game state from dictionary.

        Args:
            data: Dictionary containing serialized game state
        """
        # Load hero (import locally to avoid circular imports)
        if 'hero' in data:
            # Local import to avoid circular dependency
            from game.models import Hero
            self.hero = Hero.from_dict(data['hero'])

        # Load inventory
        self.inventory = data.get('inventory', [])

        # Load equipment
        self.equipment = data.get('equipment', {})

        # Load game progress
        self.game_progress = data.get('game_progress', {})

        # Load settings
        self.settings = data.get('settings', {})

        # Load session stats
        self.session_stats = data.get('session_stats', {})

        # Load metadata
        self.metadata = data.get('metadata', {})

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize game state to dictionary.

        Returns:
            Dictionary containing complete game state
        """
        data = OrderedDict()

        # Add metadata first
        data['metadata'] = self.metadata.copy()
        data['metadata']['last_saved'] = datetime.now(timezone.utc).isoformat()

        # Add hero
        data['hero'] = self.hero.to_dict() if self.hero else None

        # Add inventory
        data['inventory'] = self.inventory.copy()

        # Add equipment
        data['equipment'] = self.equipment.copy()

        # Add game progress
        data['game_progress'] = self.game_progress.copy()

        # Add settings
        data['settings'] = self.settings.copy()

        # Add session stats
        data['session_stats'] = self.session_stats.copy()

        return dict(data)

    def is_valid(self) -> bool:
        """
        Validate that the game state contains required elements.

        Returns:
            True if game state is valid for loading
        """
        if self.hero is None:
            return False

        # Import locally to avoid circular dependency
        from game.models import Hero
        return isinstance(self.hero, Hero)


class SaveLoadManager:
    """
    Manages save and load operations for game states.

    Provides high-level interface for saving/loading game states to/from
    JSON files with proper error handling and validation.
    """

    def __init__(self, save_directory: str = "saves"):
        """
        Initialize the save/load manager.

        Args:
            save_directory: Directory to store save files (default: "saves")
        """
        self.save_directory = save_directory
        self._ensure_save_directory()

    def _ensure_save_directory(self) -> None:
        """Ensure the save directory exists."""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def save_game(self, game_state: GameState, slot_name: str) -> bool:
        """
        Save game state to a slot.

        Args:
            game_state: GameState object to save
            slot_name: Name of the save slot (without .json extension)

        Returns:
            True if save was successful, False otherwise
        """
        if not isinstance(game_state, GameState):
            print(f"Error: Expected GameState object, got {type(game_state)}")
            return False

        if not game_state.is_valid():
            print("Error: Game state is not valid for saving")
            return False

        filename = self._get_save_filename(slot_name)

        try:
            # Serialize to dictionary
            data = game_state.to_dict()

            # Write to file with pretty printing
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Game saved successfully to {filename}")
            return True

        except Exception as e:
            print(f"Error saving game to {filename}: {e}")
            return False

    def load_game(self, slot_name: str) -> Optional[GameState]:
        """
        Load game state from a slot.

        Args:
            slot_name: Name of the save slot (without .json extension)

        Returns:
            GameState object if loaded successfully, None otherwise
        """
        filename = self._get_save_filename(slot_name)

        if not os.path.exists(filename):
            print(f"Save file {filename} does not exist")
            return None

        try:
            # Read from file
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Deserialize to GameState
            game_state = GameState()
            game_state.from_dict(data)

            if not game_state.is_valid():
                print(f"Error: Save file {filename} contains invalid game state")
                return None

            print(f"Game loaded successfully from {filename}")
            return game_state

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {filename}: {e}")
            return None
        except Exception as e:
            print(f"Error loading game from {filename}: {e}")
            return None

    def list_saves(self) -> List[Dict[str, Any]]:
        """
        List all available save files with metadata.

        Returns:
            List of dictionaries containing save file information
        """
        saves = []

        try:
            for filename in os.listdir(self.save_directory):
                if filename.endswith('.json'):
                    slot_name = filename[:-5]  # Remove .json extension
                    filepath = os.path.join(self.save_directory, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Extract metadata
                        metadata = data.get('metadata', {})
                        hero_data = data.get('hero', {})

                        save_info = {
                            'slot': slot_name,
                            'filename': filename,
                            'last_saved': metadata.get('last_saved', 'Unknown'),
                            'hero_name': hero_data.get('name', 'Unknown'),
                            'hero_level': hero_data.get('level', 1),
                            'hero_class': hero_data.get('character_class', 'Unknown'),
                            'playtime': metadata.get('total_playtime', 0),
                        }

                        saves.append(save_info)

                    except Exception as e:
                        print(f"Error reading save file {filename}: {e}")
                        continue

        except Exception as e:
            print(f"Error listing save files: {e}")

        # Sort saves by last saved date (newest first)
        saves.sort(key=lambda x: x.get('last_saved', ''), reverse=True)
        return saves

    def delete_save(self, slot_name: str) -> bool:
        """
        Delete a save file.

        Args:
            slot_name: Name of the save slot to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        filename = self._get_save_filename(slot_name)

        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Save file {filename} deleted successfully")
                return True
            else:
                print(f"Save file {filename} does not exist")
                return False

        except Exception as e:
            print(f"Error deleting save file {filename}: {e}")
            return False

    def _get_save_filename(self, slot_name: str) -> str:
        """
        Get the full path for a save slot.

        Args:
            slot_name: Name of the save slot

        Returns:
            Full path to the save file
        """
        # Sanitize slot name to prevent directory traversal
        safe_name = "".join(c for c in slot_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            safe_name = "default"

        return os.path.join(self.save_directory, f"{safe_name}.json")


# Global save/load manager instance
save_load_manager = SaveLoadManager()


def save_game_state(game_state: GameState, slot_name: str = "auto") -> bool:
    """
    Convenience function to save game state.

    Args:
        game_state: GameState object to save
        slot_name: Save slot name (default: "auto")

    Returns:
        True if save was successful
    """
    return save_load_manager.save_game(game_state, slot_name)


def load_game_state(slot_name: str) -> Optional[GameState]:
    """
    Convenience function to load game state.

    Args:
        slot_name: Save slot name

    Returns:
        GameState object if loaded successfully, None otherwise
    """
    return save_load_manager.load_game(slot_name)


def get_available_saves() -> List[Dict[str, Any]]:
    """
    Get list of available save files.

    Returns:
        List of save file information dictionaries
    """
    return save_load_manager.list_saves()


# Auto-save functionality
auto_save_interval = 300  # 5 minutes in seconds
last_auto_save = 0

def should_auto_save(current_time: float) -> bool:
    """
    Check if auto-save should trigger based on time interval.

    Args:
        current_time: Current timestamp

    Returns:
        True if auto-save should occur
    """
    global last_auto_save
    return (current_time - last_auto_save) >= auto_save_interval


def perform_auto_save(game_state: GameState) -> bool:
    """
    Perform an automatic save.

    Args:
        game_state: GameState to auto-save

    Returns:
        True if auto-save was successful
    """
    global last_auto_save
    success = save_game_state(game_state, "auto")
    if success:
        last_auto_save = datetime.now(timezone.utc).timestamp()
    return success
