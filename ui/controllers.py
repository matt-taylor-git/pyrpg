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
