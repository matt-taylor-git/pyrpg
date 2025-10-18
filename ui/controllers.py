# -*- coding: utf-8 -*-
"""
Controller classes to separate UI logic from business logic following MVC pattern.
These controllers handle the interaction between UI components and game models.
"""
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox


class BaseController(QObject):
    """Base controller class providing common functionality"""

    # Common signals
    error_occurred = Signal(str, str)  # (title, message)
    status_message = Signal(str)  # message

    def __init__(self, parent=None):
        super().__init__(parent)


class AdventureController(BaseController):
    """Controller handling adventure/game exploration logic"""

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model

    def explore_wilderness(self):
        """Handle exploration logic"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return

        self.status_message.emit("You venture into the wilderness...")

        # Exploration logic would go here
        # For now, just emit that we're starting exploration

    def rest_at_camp(self):
        """Handle resting logic"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return

        self.hero.health = self.hero.max_health
        self.status_message.emit("You rest and restore your health!")


class CombatController(BaseController):
    """Controller handling combat logic and UI state"""

    battle_started = Signal(object)  # enemy
    battle_ended = Signal()
    turn_processed = Signal(dict)   # turn_data

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model
        self.current_enemy = None

    def start_battle(self, enemy):
        """Initialize battle state"""
        self.current_enemy = enemy
        self.battle_started.emit(enemy)

    def process_player_turn(self, action):
        """Process player's combat action"""
        if not self.hero or not self.current_enemy:
            return

        # Process combat logic here
        turn_data = {
            'action': action,
            'hero_health': self.hero.health,
            'enemy_health': self.current_enemy.health
        }

        self.turn_processed.emit(turn_data)

    def end_battle(self):
        """Clean up battle state"""
        self.current_enemy = None
        self.battle_ended.emit()


class ShopController(BaseController):
    """Controller handling shop transactions and inventory management"""

    transaction_completed = Signal(object)  # item
    gold_updated = Signal(int)  # new_gold_amount

    def __init__(self, hero_model, shop_items, parent=None):
        super().__init__(parent)
        self.hero = hero_model
        self.shop_items = shop_items

    def purchase_item(self, item):
        """Process item purchase"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return

        if self.hero.gold >= item.value:
            self.hero.gold -= item.value
            self.hero.add_item(item)
            self.transaction_completed.emit(item)
            self.gold_updated.emit(self.hero.gold)
            self.status_message.emit(f"💰 Purchased {item.name}!")
        else:
            self.error_occurred.emit("Not Enough Gold",
                                   f"You need {item.value} gold to buy {item.name}. You have {self.hero.gold} gold.")

    def sell_item(self, item):
        """Process item sales"""
        if not self.hero:
            return

        sell_value = item.value // 2
        self.hero.inventory.remove(item)
        self.hero.gold += sell_value
        self.gold_updated.emit(self.hero.gold)
        self.status_message.emit(f"Sold {item.name} for {sell_value} gold!")


class InventoryController(BaseController):
    """Controller handling inventory management and equipment"""

    item_used = Signal(object)      # item
    item_equipped = Signal(object)  # item

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model

    def use_consumable_item(self, item):
        """Use a consumable item"""
        if item.item_type != 'consumable':
            return

        message = self.hero.use_item(item)
        if message:
            self.hero.inventory.remove(item)
            self.item_used.emit(item)
            self.status_message.emit(f"\U0001f9ea {message}")

    def equip_item(self, item):
        """Equip equipment items"""
        if item.item_type not in ['weapon', 'armor', 'accessory']:
            return

        # Remove item from inventory and equip
        self.hero.inventory.remove(item)

        # Get previously equipped item (if any)
        old_item = self.hero.equip_item(item)

        # Add old item back to inventory
        if old_item:
            self.hero.inventory.append(old_item)

        self.item_equipped.emit(item)
        self.status_message.emit(f"\u2694\ufe0f Equipped {item.name}!")


class StatsController(BaseController):
    """Controller handling character stat allocation"""

    stat_increased = Signal(str)  # stat_name

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model

    def increase_stat(self, stat_name):
        """Increase hero's stats if points available"""
        if not self.hero or self.hero.stat_points <= 0:
            self.error_occurred.emit("No Stat Points", "You have no available stat points to allocate.")
            return

        # Increase the stat
        if stat_name == 'strength':
            self.hero.strength += 1
            self.hero.attack_power = self.hero.calculate_attack_power()
        elif stat_name == 'defense':
            self.hero.defense += 1
        elif stat_name == 'magic':
            self.hero.intelligence += 1
            self.hero.magic_power = self.hero.calculate_magic_power()
        elif stat_name == 'speed':
            self.hero.dexterity += 1
            # Recalculate crit/dodge chances
            self.hero.update_secondary_stats()
        else:
            return

        # Consume stat point
        self.hero.stat_points -= 1

        self.stat_increased.emit(stat_name)
        self.status_message.emit(f"🏋️ Increased {stat_name}!")


class CustomizationController(BaseController):
    """Controller handling character customization logic"""

    customization_saved = Signal()    # Emitted when customization is saved
    customization_loaded = Signal()   # Emitted when customization is loaded

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model
        self.customization_file = "customization.json"

    def save_customization(self, customization_data=None):
        """Save current customization settings"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return False

        try:
            import json
            import os

            # Use provided data or current hero customization
            if customization_data is None:
                customization_data = self.hero.get_customization()

            # Ensure the directory exists
            os.makedirs("saves", exist_ok=True)
            file_path = os.path.join("saves", self.customization_file)

            # Save customization to file
            with open(file_path, 'w') as f:
                json.dump(customization_data, f, indent=2)

            self.customization_saved.emit()
            self.status_message.emit("💾 Character customization saved!")
            return True

        except Exception as e:
            self.error_occurred.emit("Save Failed", f"Could not save customization: {str(e)}")
            return False

    def load_customization(self):
        """Load customization settings from file"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return False

        try:
            import json
            import os

            file_path = os.path.join("saves", self.customization_file)

            if not os.path.exists(file_path):
                self.error_occurred.emit("No Saved Customization", "No customization file found to load.")
                return False

            # Load customization from file
            with open(file_path, 'r') as f:
                customization_data = json.load(f)

            # Validate the loaded data
            from game.customization import customization_system
            is_valid, message = customization_system.validate_customization(customization_data)

            if not is_valid:
                self.error_occurred.emit("Invalid Customization", f"Loaded customization is invalid: {message}")
                return False

            # Apply customization to hero
            self.hero.set_customization(customization_data)

            self.customization_loaded.emit()
            self.status_message.emit("📁 Character customization loaded!")
            return True

        except json.JSONDecodeError:
            self.error_occurred.emit("Load Failed", "Customization file is corrupted.")
            return False
        except Exception as e:
            self.error_occurred.emit("Load Failed", f"Could not load customization: {str(e)}")
            return False

    def apply_customization(self, customization_data):
        """Apply customization changes to hero"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return False

        try:
            # Validate before applying
            from game.customization import customization_system
            is_valid, message = customization_system.validate_customization(customization_data)

            if not is_valid:
                self.error_occurred.emit("Invalid Customization", message)
                return False

            # Apply changes
            self.hero.set_customization(customization_data)

            self.status_message.emit("✅ Character customization updated!")
            return True

        except Exception as e:
            self.error_occurred.emit("Update Failed", f"Could not apply customization: {str(e)}")
            return False

    def get_current_customization(self):
        """Get hero's current customization settings"""
        if not self.hero:
            return None
        return self.hero.get_customization()

    def reset_customization(self):
        """Reset customization to default settings"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return False

        try:
            from game.customization import customization_system
            default_customization = customization_system.get_default_customization()
            # Keep the hero's current name
            default_customization['name'] = self.hero.name

            self.hero.set_customization(default_customization)

            self.status_message.emit("🔄 Character customization reset to default!")
            return True

        except Exception as e:
            self.error_occurred.emit("Reset Failed", f"Could not reset customization: {str(e)}")
            return False

    def update_customization_name(self, new_name):
        """Update only the character name"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded!")
            return False

        try:
            self.hero.update_customization_name(new_name)
            self.status_message.emit(f"✏️ Character name updated to '{new_name}'!")
            return True

        except ValueError as e:
            self.error_occurred.emit("Invalid Name", str(e))
            return False
        except Exception as e:
            self.error_occurred.emit("Update Failed", f"Could not update name: {str(e)}")
            return False


class MonsterStatsController(BaseController):
    """Controller handling monster stats viewing logic"""

    enemy_displayed = Signal(object)  # enemy object
    enemy_comparison_requested = Signal(object, object)  # hero, enemy pair

    def __init__(self, hero_model, parent=None):
        super().__init__(parent)
        self.hero = hero_model
        self.current_enemy = None
        self.known_monsters = {}  # Cache of monsters we've encountered
        self.monster_database = {}  # Comprehensive monster encyclopedia

    def view_enemy_stats(self, enemy, viewing_mode='detailed'):
        """Display enemy statistics in the monster stats viewer"""
        if not enemy:
            self.error_occurred.emit("Error", "No enemy selected to view.")
            return

        self.current_enemy = enemy

        # Mark this monster as known for future reference
        self._add_to_known_monsters(enemy)

        self.enemy_displayed.emit(enemy)
        self.status_message.emit(f"📊 Viewing stats for {enemy.name}")

    def load_monster_by_name(self, monster_name, level=1):
        """Load and display a monster by name and level"""
        try:
            # Create a basic enemy of the specified type and level
            enemy = self._create_enemy_from_name(monster_name, level)

            if enemy:
                self.view_enemy_stats(enemy)
                return True
            else:
                self.error_occurred.emit("Monster Not Found", f"Could not find monster: {monster_name}")
                return False

        except Exception as e:
            self.error_occurred.emit("Load Error", f"Could not load monster: {str(e)}")
            return False

    def compare_with_hero(self, enemy=None):
        """Compare enemy stats with current hero"""
        if not self.hero:
            self.error_occurred.emit("Error", "No hero loaded for comparison.")
            return

        compare_enemy = enemy or self.current_enemy
        if not compare_enemy:
            self.error_occurred.emit("Error", "No enemy selected for comparison.")
            return

        self.enemy_comparison_requested.emit(self.hero, compare_enemy)
        self.status_message.emit(f"⚖️ Comparing {self.hero.name} vs {compare_enemy.name}")

    def get_encounter_preview(self, enemy, immediate_danger=False):
        """Get quick stats preview for encounter decision"""
        if not enemy:
            return None

        preview_data = {
            'name': enemy.name,
            'level': enemy.level,
            'health': f"{enemy.health}/{enemy.max_health}",
            'attack': f"{enemy.attack_min}-{enemy.attack_max}",
            'weaknesses': enemy.elemental_weakness[:3],  # Show top 3 weaknesses
            'threat_level': self._calculate_encounter_threat(self.hero, enemy),
            'immediate_danger': immediate_danger
        }

        return preview_data

    def get_known_monsters(self):
        """Get list of all known monsters for browsing"""
        return list(self.known_monsters.values())

    def get_monsters_by_rarity(self, rarity):
        """Get monsters filtered by rarity"""
        return [monster for monster in self.known_monsters.values() if monster.rarity == rarity]

    def get_monsters_by_type(self, enemy_type):
        """Get monsters filtered by type"""
        return [monster for monster in self.known_monsters.values() if monster.enemy_type == enemy_type]

    def get_bestiary_completion(self):
        """Get completion statistics for monster encyclopedia"""
        if not self.known_monsters:
            return {
                'total_known': 0,
                'completion_percentage': 0,
                'by_rarity': {},
                'by_type': {}
            }

        # In a real implementation, this would compare against a full monster database
        # For now, we'll calculate stats from known monsters

        by_rarity = {}
        by_type = {}

        for monster in self.known_monsters.values():
            by_rarity[monster.rarity] = by_rarity.get(monster.rarity, 0) + 1
            by_type[monster.enemy_type] = by_type.get(monster.enemy_type, 0) + 1

        total_known = len(self.known_monsters)
        # Mock completion percentage - in reality this would be vs database size
        completion_percentage = min(100, total_known * 10)

        return {
            'total_known': total_known,
            'completion_percentage': completion_percentage,
            'by_rarity': by_rarity,
            'by_type': by_type
        }

    def _add_to_known_monsters(self, enemy):
        """Add enemy to known monsters cache"""
        key = f"{enemy.enemy_type}_{enemy.level}_{enemy.name}"

        if key not in self.known_monsters:
            # Create a copy for the database to avoid modifying original
            monster_copy = self._duplicate_enemy(enemy)
            self.known_monsters[key] = monster_copy

    def _duplicate_enemy(self, enemy):
        """Create a duplicate of an enemy for safe storage"""
        # For now, create a new enemy instance - in reality you might want to serialize/deserialize
        return enemy.__class__(enemy.name, enemy.level, enemy.enemy_type)

    def _create_enemy_from_name(self, name, level=1):
        """Create an enemy instance from a name string"""
        # This is a simplified implementation - in a real game you'd have a monster database

        name_to_type = {
            'goblin': 'normal',
            'orc': 'warrior',
            'wolf': 'beast',
            'skeleton': 'undead',
            'fire elemental': 'elemental',
            'ice mage': 'mage',
            'troll': 'tank',
            'dragon': 'giant',
            'assassin': 'rogue'
        }

        enemy_type = name_to_type.get(name.lower(), 'normal')

        # Create enemy with appropriate type
        from game.models import Enemy
        return Enemy(name.title(), level, enemy_type)

    def _calculate_encounter_threat(self, hero, enemy):
        """Calculate threat level of encounter"""
        if not hero or not enemy:
            return "unknown"

        # Simple threat calculation based on level difference and enemy type
        level_diff = enemy.level - hero.level

        if enemy.enemy_type == 'elemental':
            base_threat = 'deadly'
        elif enemy.enemy_type == 'dragon':
            base_threat = 'deadly'
        elif enemy.enemy_type in ['undead', 'beast']:
            base_threat = 'dangerous'
        elif enemy.enemy_type in ['warrior', 'mage', 'rogue']:
            base_threat = 'normal'
        elif enemy.enemy_type == 'giant':
            base_threat = 'tough'
        else:
            base_threat = 'weak'

        # Adjust based on level difference
        if level_diff >= 3:
            base_threat = 'deadly'
        elif level_diff >= 1:
            if base_threat == 'weak':
                base_threat = 'normal'
            elif base_threat != 'deadly':
                base_threat = 'dangerous'
        elif level_diff <= -3:
            if base_threat == 'deadly':
                base_threat = 'dangerous'
            elif base_threat == 'dangerous':
                base_threat = 'normal'
            else:
                base_threat = 'weak'

        return base_threat
