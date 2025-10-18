# -*- coding: utf-8 -*-
import random
from .items import Item
from .customization import customization_system

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

        # Character customization - appearance and cosmetic choices
        self.customization = customization_system.get_default_customization()
        self.customization['name'] = name  # Override default name with hero's actual name

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

    def get_customization(self):
        """Get the current character customization settings."""
        return self.customization.copy()

    def set_customization(self, customization):
        """Set character customization settings."""
        # Validate customization before setting
        is_valid, message = customization_system.validate_customization(customization)
        if not is_valid:
            raise ValueError(f"Invalid customization: {message}")

        # Update internal customization
        self.customization = customization.copy()

        # Update hero name if it changed
        if customization['name'] != self.name:
            self.name = customization['name']

    def update_customization_name(self, new_name):
        """Update only the character name in customization."""
        # Validate name
        name = new_name.strip()
        if not customization_system.name_limits[0] <= len(name) <= customization_system.name_limits[1]:
            raise ValueError(f"Name must be {customization_system.name_limits[0]}-{customization_system.name_limits[1]} characters")

        # Validate allowed characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-")
        if not all(c in valid_chars for c in name):
            raise ValueError("Name can only contain letters, numbers, spaces, hyphens, and underscores")

        # Update both hero name and customization
        self.customization['name'] = name
        self.name = name

class Enemy:
    """Advanced enemy with detailed stats and battle mechanics for monster viewer."""

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

        # Attack range and variability
        self.attack_min = max(1, self.attack - 3)
        self.attack_max = self.attack + 6
        self.crit_chance = min(20, 5 + (level * 0.5))
        self.crit_multiplier = 1.5

        # Magic attack range
        self.magic_attack_min = max(1, self.magic_attack - 2)
        self.magic_attack_max = self.magic_attack + 4

        # Combat behavior
        self.attack_speed = 1.0 + (level * 0.1)  # Attacks per turn (can be > 1)
        self.movement_speed = 1.0  # Speed multiplier
        self.intelligence = 'normal'  # low, normal, high, cunning

        # Elemental properties
        self.elemental_type = 'none'  # fire, ice, lightning, poison, etc.
        self.elemental_strength = 0  # Bonus damage with this element
        self.elemental_weakness = []  # Elements that do extra damage
        self.elemental_resistance = []  # Elements that do less damage
        self.elemental_immunity = []  # Elements that do no damage

        # Physical properties
        self.size_category = 'medium'  # small, medium, large, huge, colossal
        self.speed_rating = 'normal'  # slow, normal, fast, very_fast
        self.armor_type = 'light'  # light, medium, heavy, magical

        # Special abilities and attacks
        self.special_abilities = []
        self.special_attacks = []
        self.passive_abilities = []

        # Behavioral traits
        self.behavior_patterns = []
        self.combat_style = 'aggressive'  # aggressive, defensive, magical, supportive

        # Descriptive information
        self.description = ""
        self.habitat = ""
        self.rarity = 'common'  # common, uncommon, rare, legendary, boss
        self.loot_drops = []
        self.status_effects = []

        # Experience and gold rewards
        self.exp_reward = level * 25
        self.gold_reward = level * (5 + random.randint(0, 5))

        # Threat assessment
        self.threat_level = 'normal'  # weak, normal, tough, dangerous, deadly

        # Initialize enemy type specific traits
        self.initialize_enemy_type()

    def initialize_enemy_type(self):
        """Initialize enemy-specific traits and abilities."""
        if self.enemy_type == 'warrior':
            self.attack += 3
            self.defense += 2
            self.special_attacks = ['power_strike']

            # Detailed stats
            self.description = "A formidable warrior trained in the arts of melee combat. Their heavy armor provides excellent protection but slows their movement."
            self.habitat = "Castles, battlegrounds, and mountain outposts"
            self.size_category = 'medium'
            self.speed_rating = 'slow'
            self.armor_type = 'heavy'
            self.combat_style = 'aggressive'
            self.elemental_weakness = ['lightning', 'magic']
            self.elemental_resistance = ['physical']
            self.behavior_patterns = ['charges at start of combat', 'uses power strikes when health is high', 'defends when wounded']
            self.special_abilities = [
                {'name': 'Power Strike', 'description': 'A devastating overhead attack that deals 150% damage'},
                {'name': 'Warrior Spirit', 'description': 'Passive: Increased defense when health drops below 50%'}
            ]
            self.passive_abilities = ['heavy armor expertise', 'melee weapon mastery']
            self.rarity = 'uncommon'
            self.threat_level = 'normal'
            self.loot_drops = ['iron_sword', 'heavy_helmet', 'chainmail']

        elif self.enemy_type == 'mage':
            self.magic_attack += 5
            self.attack -= 2
            self.special_attacks = ['magic_missile', 'fireball']

            # Detailed stats
            self.description = "A scholarly practitioner of arcane arts. They wield powerful spells but are physically weak without proper protection."
            self.habitat = "Ancient libraries, magical towers, and ritual chambers"
            self.size_category = 'medium'
            self.speed_rating = 'normal'
            self.armor_type = 'light'
            self.combat_style = 'magical'
            self.elemental_weakness = ['physical', 'poison']
            self.elemental_resistance = ['magic', 'fire', 'ice']
            self.elemental_type = 'fire'  # Has innate fire magic
            self.elemental_strength = 2
            self.behavior_patterns = ['stays at range during combat', 'focuses on spell casting', 'vulnerable when mana is depleted']
            self.special_abilities = [
                {'name': 'Fireball', 'description': 'Launches a ball of flame that deals fire damage and may burn the target'},
                {'name': 'Magic Missile', 'description': 'Fires multiple homing magical projectiles'},
                {'name': 'Mana Shield', 'description': 'Passive: Converts some incoming damage to mana drain'}
            ]
            self.passive_abilities = ['spell focus', 'arcane knowledge']
            self.rarity = 'rare'
            self.threat_level = 'dangerous'
            self.loot_drops = ['mage_robe', 'magic_staff', 'mana_crystal']

        elif self.enemy_type == 'rogue':
            self.attack += 2
            self.special_attacks = ['backstab', 'poison_strike']

            # Detailed stats
            self.description = "A stealthy assassin who strikes from the shadows. They are masters of ambush tactics and poison-based attacks."
            self.habitat = "Dark alleys, forests, thieves' dens, and abandoned ruins"
            self.size_category = 'medium'
            self.speed_rating = 'fast'
            self.armor_type = 'light'
            self.combat_style = 'aggressive'
            self.elemental_weakness = ['pure', 'magic']
            self.elemental_resistance = ['poison']
            self.behavior_patterns = ['avoids direct confrontation', 'strikes from behind', 'uses poison to weaken enemies']
            self.special_abilities = [
                {'name': 'Backstab', 'description': 'Attacks from behind for double damage'},
                {'name': 'Poison Strike', 'description': 'Coats weapon in poison, causing damage over time'},
                {'name': 'Smoke Bomb', 'description': 'Creates obscuring smoke to hide or escape'}
            ]
            self.passive_abilities = ['stealth', 'poison resistance']
            self.rarity = 'uncommon'
            self.threat_level = 'tough'
            self.loot_drops = ['serrated_dagger', 'leather_boots', 'poison_vial']

        elif self.enemy_type == 'tank':
            self.max_health += 30
            self.defense += 5
            self.attack -= 2
            self.health = self.max_health
            self.special_attacks = ['shield_bash']

            # Detailed stats
            self.description = "A heavily armored defender built for endurance rather than speed. Their massive shields make them nearly impervious to damage."
            self.habitat = "Fortresses, defensive walls, and siege encampments"
            self.size_category = 'large'
            self.speed_rating = 'slow'
            self.armor_type = 'heavy'
            self.combat_style = 'defensive'
            self.elemental_weakness = ['lightning', 'corrosion']
            self.elemental_resistance = ['physical']
            self.elemental_immunity = ['fear']
            self.behavior_patterns = ['holds defensive positions', 'absorbs damage for allies', 'stuns attackers with shield blows']
            self.special_abilities = [
                {'name': 'Shield Bash', 'description': 'Slams enemy with shield, dealing damage and chance to stun'},
                {'name': 'Guardian Aura', 'description': 'Passive: Reduces damage to nearby allies'},
                {'name': 'Fortress Stance', 'description': 'Greatly increased defense for one turn but cannot attack'}
            ]
            self.passive_abilities = ['iron constitution', 'shield mastery']
            self.rarity = 'rare'
            self.threat_level = 'tough'
            self.loot_drops = ['tower_shield', 'plate_armor', 'health_potion']

        elif self.enemy_type == 'giant':
            self.max_health += 50
            self.attack += 5
            self.defense += 3
            self.health = self.max_health
            self.special_attacks = ['ground_slam', 'rock_throw']

            # Detailed stats
            self.description = "An enormous beast that towers over lesser foes. Their raw strength is unmatched, capable of shaking the ground itself."
            self.habitat = "Mountain peaks, giant caves, and ancient ruins"
            self.size_category = 'huge'
            self.speed_rating = 'slow'
            self.armor_type = 'medium'
            self.combat_style = 'aggressive'
            self.elemental_weakness = ['lightning', 'ice']
            self.elemental_resistance = ['physical']
            self.behavior_patterns = ['crushes smaller enemies', 'throws environmental objects', 'feared by smaller creatures']
            self.special_abilities = [
                {'name': 'Ground Slam', 'description': 'Slams fists into ground, causing area damage and stun'},
                {'name': 'Rock Throw', 'description': 'Hurls massive boulders at distant targets'},
                {'name': 'Giant Strength', 'description': 'Passive: Can throw or destroy obstacles'}
            ]
            self.passive_abilities = ['tremor sense', 'enormous strength']
            self.rarity = 'rare'
            self.threat_level = 'dangerous'
            self.loot_drops = ['giant_club', 'boulder', 'treasure_chest']

        elif self.enemy_type == 'undead':
            self.attack += 1
            self.special_attacks = ['life_drain', 'curse']
            self.elemental_weakness = ['holy', 'fire']
            self.elemental_immunity = ['poison', 'fear']

            # Detailed stats
            self.description = "A corrupted corpse animated by dark magic. Immune to pain and fear, they exist only to destroy the living."
            self.habitat = "Graveyards, haunted ruins, and cursed battlefields"
            self.size_category = 'medium'
            self.speed_rating = 'slow'
            self.armor_type = 'light'
            self.combat_style = 'magical'
            self.behavior_patterns = ['slow but relentless', 'sustained by dark energy', 'vulnerable to holy cleansing']
            self.special_abilities = [
                {'name': 'Life Drain', 'description': 'Siphons health from the living to sustain itself'},
                {'name': 'Curse', 'description': 'Afflicts enemies with debilitating ailments'},
                {'name': 'Unholy Resilience', 'description': 'Passive: Regenerates health slowly while in darkness'}
            ]
            self.passive_abilities = ['undead fortitude', 'curse immunity']
            self.rarity = 'uncommon'
            self.threat_level = 'tough'
            self.loot_drops = ['tainted_armor', 'dark_amulet', 'sun_blessed_weapon']

        elif self.enemy_type == 'beast':
            self.attack += 4
            self.attack_speed = 1.2
            self.special_attacks = ['savage_bite', 'pounce']
            self.movement_speed = 1.5

            # Detailed stats
            self.description = "A feral beast driven by instinct and hunger. They are incredibly fast and strike with animalistic ferocity."
            self.habitat = "Forests, caves, and wild plains where prey is abundant"
            self.size_category = 'large'
            self.speed_rating = 'very_fast'
            self.armor_type = 'light'
            self.combat_style = 'aggressive'
            self.elemental_weakness = ['fire', 'cold_iron']
            self.elemental_resistance = ['nature']
            self.behavior_patterns = ['circles prey rapidly', 'strikes unpredictably', 'retreats when injured']
            self.special_abilities = [
                {'name': 'Savage Bite', 'description': 'Sinks teeth into flesh, causing bleeding and disease risk'},
                {'name': 'Pounce', 'description': 'Leaps great distances to surprise prey'},
                {'name': 'Animal Instinct', 'description': 'Passive: Can detect hidden or invisible enemies'}
            ]
            self.passive_abilities = ['keen_senses', 'four-legged_speed']
            self.rarity = 'common'
            self.threat_level = 'normal'
            self.loot_drops = ['beast_hide', 'sharp_claws', 'raw_meat']

        elif self.enemy_type == 'elemental':
            self.magic_attack += 10
            self.elemental_type = random.choice(['fire', 'ice', 'lightning', 'earth'])
            self.special_attacks = ['elemental_burst', 'summon_minions']
            self.elemental_strength = 5
            self.elemental_immunity = [self.elemental_type]

            # Detailed stats
            specific_descriptions = {
                'fire': "A living inferno of pure elemental energy. Burns bright and hot, consuming all in its path.",
                'ice': "A chilling embodiment of winter's wrath. Freezes its victims and shrouds them in ice.",
                'lightning': "A crackling force of electrical energy. Strikes with blinding speed and paralyzing force.",
                'earth': "A massive construct of stone and mineral. Unyielding stone given malicious will."
            }
            self.description = specific_descriptions.get(self.elemental_type, "A manifestation of pure elemental power.")
            self.habitat = f"Planes of {self.elemental_type}, corrupted natural areas, and magical rifts"
            self.size_category = 'large'
            self.speed_rating = {'fire': 'very_fast', 'ice': 'slow', 'lightning': 'very_fast', 'earth': 'slow'}[self.elemental_type]
            self.armor_type = 'magical'
            self.combat_style = 'magical'
            self.elemental_weakness = [self.get_elemental_weakness()]
            self.behavior_patterns = [f'draws power from {self.elemental_type} sources', 'weakens when elemental energy is disrupted', 'can be banished to elemental planes']
            self.special_abilities = [
                {'name': 'Elemental Burst', 'description': f'Explosion of {self.elemental_type} energy dealing massive damage'},
                {'name': 'Summon Minions', 'description': f'Creates lesser {self.elemental_type} elementals to aid in battle'},
                {'name': f'{self.elemental_type.title()} Affinity', 'description': f'Immune to {self.elemental_type} and deals bonus {self.elemental_type} damage'}
            ]
            self.rarity = 'legendary'
            self.threat_level = 'deadly'
            self.loot_drops = [f'elemental_essence_{self.elemental_type}', f'storm_heart', f'elemental_breaker']

        else:  # Default 'normal' enemy
            self.description = "A common adversary encountered in the wild. Not particularly remarkable, but still dangerous in numbers."
            self.habitat = "Roads, fields, and forests throughout the realm"
            self.size_category = 'medium'
            self.speed_rating = 'normal'
            self.armor_type = 'light'
            self.combat_style = 'aggressive'
            self.behavior_patterns = ['fights directly', 'forms groups for safety', 'flees when outnumbered']
            self.special_abilities = []
            self.passive_abilities = ['basic_combat_training']
            self.rarity = 'common'
            self.threat_level = 'weak'
            self.loot_drops = ['basic_sword', 'cloth_armor', 'copper_coins']

        # Calculate attack ranges after enemy type modifications
        self.attack_min = max(1, self.attack - 3)
        self.attack_max = self.attack + 6
        self.magic_attack_min = max(1, self.magic_attack - 2)
        self.magic_attack_max = self.magic_attack + 4

    def get_elemental_weakness(self):
        """Get the opposing elemental weakness based on elemental type."""
        elemental_opposites = {
            'fire': 'water',
            'ice': 'fire',
            'lightning': 'earth',
            'earth': 'lightning',
            'water': 'lightning',
            'poison': 'holy',
            'holy': 'dark',
            'dark': 'holy',
            'nature': 'fire'
        }
        return elemental_opposites.get(self.elemental_type, 'none')

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
