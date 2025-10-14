# -*- coding: utf-8 -*-
import random
from .items import Item

class Hero:
    """Advanced player character with comprehensive RPG mechanics."""

    def __init__(self, name):
        self.name = name
        self.level = 1

        # Core stats
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50

        # Combat stats
        self.strength = 12      # Affects physical damage
        self.dexterity = 10     # Affects crit chance and dodge
        self.intelligence = 8   # Affects magic damage and mana
        self.vitality = 10      # Affects health and defense

        # Equipment and inventory - Start with basic gear
        # Create starting equipment
        starter_weapon = Item("Rusty Sword", 'weapon', 'common', 'weapon',
                             attack_bonus=3, value=10,
                             description="A worn but functional blade")
        starter_armor = Item("Cloth Tunic", 'armor', 'common', 'armor',
                            defense_bonus=2, value=8,
                            description="Simple protective clothing")

        self.equipment = {
            'weapon': starter_weapon,
            'armor': starter_armor,
            'accessory': None
        }
        self.inventory = []
        self.gold = 100

        # Progression
        self.experience = 0
        self.experience_to_level = 100
        self.skill_points = 0
        self.stat_points = 0

        # Status effects
        self.status_effects = []
        self.buffs = []

        # Skills and abilities
        self.unlocked_skills = [
            Skill("Power Strike", "physical", 20, 10, "A powerful physical attack."),
            Skill("Fireball", "magic", 30, 20, "A fiery magic attack.")
        ]
        self.skill_cooldowns = {}

        # Initialize derived stats after equipment is set up
        self.refresh_derived_stats()

    def calculate_attack_power(self):
        """Calculate total attack power including equipment."""
        base = self.strength + (self.level * 2)
        weapon_bonus = 0
        if self.equipment['weapon']:
            weapon_bonus = self.equipment['weapon'].attack_bonus
        return base + weapon_bonus

    def calculate_magic_power(self):
        """Calculate total magic power."""
        return self.intelligence + (self.level * 1.5)

    def calculate_defense(self):
        """Calculate total defense including equipment."""
        base = self.vitality + (self.level * 1.5)
        armor_bonus = 0
        if self.equipment['armor']:
            armor_bonus = self.equipment['armor'].defense_bonus
        return int(base + armor_bonus)

    def calculate_crit_chance(self):
        """Calculate critical hit chance."""
        return min(50, self.dexterity * 0.5 + (self.level * 0.2))

    def calculate_dodge_chance(self):
        """Calculate dodge chance."""
        return min(30, self.dexterity * 0.3 + (self.level * 0.1))

    def take_damage(self, damage, damage_type='physical'):
        """Advanced damage calculation with type considerations."""
        if random.random() * 100 < self.dodge_chance:
            return 0, "dodged"

        actual_damage = max(1, damage - self.defense)

        # Apply damage type modifiers
        if damage_type == 'magic':
            actual_damage = int(actual_damage * 1.2)  # Magic does 20% more damage
        elif damage_type == 'poison':
            actual_damage = int(actual_damage * 0.8)  # Poison does 20% less damage

        self.health -= actual_damage

        # Apply status effects based on damage type
        if damage_type == 'poison' and random.random() < 0.3:
            self.add_status_effect('poisoned', 3)

        return actual_damage, "hit"

    def add_status_effect(self, effect, duration):
        """Add a status effect to the hero."""
        self.status_effects.append({
            'type': effect,
            'duration': duration,
            'name': effect.title()
        })

    def remove_status_effect(self, effect_type):
        """Remove a specific status effect."""
        self.status_effects = [e for e in self.status_effects if e['type'] != effect_type]

    def process_status_effects(self):
        """Process and update all status effects."""
        damage_this_turn = 0
        effects_to_remove = []

        for effect in self.status_effects[:]:  # Copy to avoid modification during iteration
            if effect['type'] == 'poisoned':
                poison_damage = max(1, self.max_health // 20)
                self.health -= poison_damage
                damage_this_turn += poison_damage
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    effects_to_remove.append(effect)

            elif effect['type'] == 'stunned':
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    effects_to_remove.append(effect)

        # Remove expired effects
        for effect in effects_to_remove:
            self.status_effects.remove(effect)

        return damage_this_turn

    def is_alive(self):
        """Check if the hero is still alive."""
        return self.health > 0

    def can_act(self):
        """Check if hero can perform actions (not stunned, etc.)."""
        for effect in self.status_effects:
            if effect['type'] == 'stunned':
                return False
        return True

    def gain_experience(self, exp):
        """Advanced experience gain with multiple level ups."""
        self.experience += exp
        leveled_up = False
        levels_gained = 0

        while self.experience >= self.experience_to_level:
            self.level_up()
            leveled_up = True
            levels_gained += 1

        if leveled_up:
            self.stat_points += levels_gained * 3  # 3 stat points per level
            self.skill_points += levels_gained    # 1 skill point per level

        return leveled_up, levels_gained

    def level_up(self):
        """Advanced level up with diminishing returns."""
        self.level += 1
        self.experience -= self.experience_to_level

        # Increasing experience requirements
        if self.level <= 10:
            self.experience_to_level = int(self.experience_to_level * 1.4)
        elif self.level <= 25:
            self.experience_to_level = int(self.experience_to_level * 1.3)
        else:
            self.experience_to_level = int(self.experience_to_level * 1.2)

        # Stat increases based on primary attributes
        self.max_health += self.vitality
        self.max_mana += self.intelligence // 2
        self.health = self.max_health
        self.mana = self.max_mana

        # Recalculate derived stats
        self.refresh_derived_stats()

    def refresh_derived_stats(self):
        """Recalculate all derived stats."""
        self.attack_power = self.calculate_attack_power()
        self.magic_power = self.calculate_magic_power()
        self.defense = self.calculate_defense()
        self.crit_chance = self.calculate_crit_chance()
        self.dodge_chance = self.calculate_dodge_chance()

    def equip_item(self, item):
        """Equip an item and apply its bonuses.
        Returns the previously equipped item if there was one, None otherwise.
        Caller is responsible for managing inventory."""
        slot = item.slot
        old_item = self.equipment[slot]
        self.equipment[slot] = item
        self.refresh_derived_stats()
        return old_item

    def unequip_item(self, slot):
        """Unequip an item from the specified slot and return it.
        Returns the unequipped item if there was one, None otherwise.
        Caller is responsible for managing inventory."""
        if self.equipment[slot]:
            old_item = self.equipment[slot]
            self.equipment[slot] = None
            self.refresh_derived_stats()
            return old_item
        return None

    def add_item(self, item):
        """Add item to inventory."""
        self.inventory.append(item)

    def remove_item(self, item):
        """Remove item from inventory."""
        if item in self.inventory:
            self.inventory.remove(item)

    def use_item(self, item):
        """Use a consumable item."""
        if item.item_type == 'consumable':
            if item.effect == 'heal':
                heal_amount = min(item.power, self.max_health - self.health)
                self.health += heal_amount
                return f"Restored {heal_amount} health!"
            elif item.effect == 'restore_mana':
                mana_amount = min(item.power, self.max_mana - self.mana)
                self.mana += mana_amount
                return f"Restored {mana_amount} mana!"

        return None

    def get_level_up_message(self):
        """Get detailed level up message."""
        return (f"🎉 {self.name} reached level {self.level}!\n"
                f"📈 Gained +{self.vitality} Max Health\n"
                f"🔮 Gained +{self.intelligence//2} Max Mana\n"
                f"⭐ Earned 3 Stat Points and 1 Skill Point!")

    def get_stats_text(self):
        """Get comprehensive stats display."""
        lines = [
            f"Name: {self.name} (Level {self.level})",
            f"Health: {self.health}/{self.max_health}",
            f"Mana: {self.mana}/{self.max_mana}",
            f"Strength: {self.strength} (Physical Power)",
            f"Dexterity: {self.dexterity} (Crit: {self.crit_chance:.1f}%)",
            f"Intelligence: {self.intelligence} (Magic Power)",
            f"Vitality: {self.vitality} (Defense: {self.defense})",
            f"Attack Power: {self.attack_power}",
            f"Magic Power: {self.magic_power:.1f}",
            f"Dodge Chance: {self.dodge_chance:.1f}%",
            f"Experience: {self.experience}/{self.experience_to_level}",
            f"Gold: {self.gold}",
            f"Stat Points: {self.stat_points}",
            f"Skill Points: {self.skill_points}"
        ]

        # Equipment display
        equipment_text = "Equipment: "
        for slot, item in self.equipment.items():
            if item:
                equipment_text += f"{slot.title()}: {item.name}, "
            else:
                equipment_text += f"{slot.title()}: None, "
        lines.append(equipment_text.rstrip(", "))

        # Status effects
        if self.status_effects:
            effects = [effect['name'] for effect in self.status_effects]
            lines.append(f"Status: {', '.join(effects)}")

        # Inventory (first 5 items)
        if self.inventory:
            inv_items = [item.name for item in self.inventory[:5]]
            lines.append(f"Inventory: {', '.join(inv_items)}")
            if len(self.inventory) > 5:
                lines.append(f"... and {len(self.inventory) - 5} more items")
        else:
            lines.append("Inventory: Empty")

        return "\n".join(lines)

    def get_combat_stats_text(self):
        """Get simplified stats for combat display."""
        return (f"{self.name} (Lv.{self.level})\n"
                f"HP: {self.health}/{self.max_health}\n"
                f"MP: {self.mana}/{self.max_mana}\n"
                f"ATK: {self.attack_power} | DEF: {self.defense}")

class Enemy:
    """Advanced enemy with sophisticated combat mechanics."""

    def __init__(self, name, level, enemy_type='normal'):
        self.name = name
        self.level = level
        self.enemy_type = enemy_type

        # Scale stats based on level
        self.max_health = 50 + (level * 15)
        self.health = self.max_health
        self.attack = 8 + (level * 2)
        self.defense = int(3 + (level * 1.5))
        self.magic_attack = int(5 + (level * 1.5))

        # Experience and gold rewards
        self.exp_reward = level * 25
        self.gold_reward = level * (5 + random.randint(0, 5))

        # Special abilities
        self.special_attacks = []
        self.status_effects = []

        # Initialize enemy type specific traits
        self.initialize_enemy_type()

    def initialize_enemy_type(self):
        """Initialize enemy-specific traits and abilities."""
        if self.enemy_type == 'warrior':
            self.attack += 3
            self.defense += 2
            self.special_attacks = ['power_strike']
        elif self.enemy_type == 'mage':
            self.magic_attack += 5
            self.attack -= 2
            self.special_attacks = ['magic_missile', 'fireball']
        elif self.enemy_type == 'rogue':
            self.attack += 2
            self.special_attacks = ['backstab', 'poison_strike']
        elif self.enemy_type == 'tank':
            self.max_health += 30
            self.defense += 5
            self.attack -= 2
            self.health = self.max_health
            self.special_attacks = ['shield_bash']

    def take_damage(self, damage, damage_type='physical'):
        """Advanced damage taking with type considerations."""
        actual_damage = max(1, damage - self.defense)

        # Apply damage type modifiers
        if damage_type == 'magic':
            actual_damage = int(actual_damage * 1.1)  # Magic slightly more effective

        self.health -= actual_damage
        return actual_damage

    def perform_special_attack(self):
        """Perform a special attack if available."""
        if not self.special_attacks:
            return None, 0

        attack = random.choice(self.special_attacks)

        if attack == 'power_strike':
            damage = int(self.attack * 1.5)
            return 'physical', damage
        elif attack == 'magic_missile':
            damage = int(self.magic_attack * 1.2)
            return 'magic', damage
        elif attack == 'fireball':
            damage = int(self.magic_attack * 1.8)
            return 'magic', damage
        elif attack == 'backstab':
            damage = int(self.attack * 2.0)
            return 'physical', damage
        elif attack == 'poison_strike':
            damage = int(self.attack * 1.3)
            return 'poison', damage
        elif attack == 'shield_bash':
            damage = int(self.attack * 1.2)
            return 'physical', damage

        return 'physical', self.attack

    def is_alive(self):
        """Check if the enemy is still alive."""
        return self.health > 0

    def get_combat_display_text(self):
        """Get text representation for combat display."""
        return f"{self.name} (Lv.{self.level})\nHP: {self.health}/{self.max_health}"

class Skill:
    """Represents a skill or ability."""
    def __init__(self, name, skill_type, damage, mana_cost, description=""):
        self.name = name
        self.skill_type = skill_type  # 'physical', 'magic'
        self.damage = damage
        self.mana_cost = mana_cost
        self.description = description
