import random
import time
from models import Hero, Enemy, Item

def get_random_enemy(hero_level):
    """Get a random enemy for encounters with varied types and levels."""
    enemy_types = ['warrior', 'mage', 'rogue', 'tank']
    enemy_names = {
        'warrior': ['Orc Warrior', 'Goblin Fighter', 'Bandit Chief', 'Knight'],
        'mage': ['Dark Sorcerer', 'Shadow Mage', 'Fire Wizard', 'Ice Witch'],
        'rogue': ['Assassin', 'Thief', 'Shadow Walker', 'Night Blade'],
        'tank': ['Stone Golem', 'Iron Guardian', 'Rock Beast', 'Earth Elemental']
    }

    enemy_type = random.choice(enemy_types)
    name = random.choice(enemy_names[enemy_type])
    level = max(1, min(hero_level + random.randint(-2, 2), hero_level + 5))

    return Enemy(name, level, enemy_type)

def simulate_combat(hero, enemy):
    """Advanced combat simulation with special abilities and status effects."""
    combat_log = []

    # Process status effects at start of combat
    status_damage = hero.process_status_effects()
    if status_damage > 0:
        combat_log.append(f"You take {status_damage} damage from status effects!")

    turn_count = 0
    while hero.is_alive() and enemy.is_alive() and turn_count < 50:  # Prevent infinite combat
        turn_count += 1

        # Hero's turn
        if not hero.can_act():
            combat_log.append("You are stunned and cannot act!")
        else:
            # Calculate damage with critical hits
            base_damage = hero.attack_power
            if random.random() * 100 < hero.crit_chance:
                base_damage = int(base_damage * 1.5)
                combat_log.append("Critical hit!")

            actual_damage = enemy.take_damage(base_damage, 'physical')
            if actual_damage > 0:
                combat_log.append(f"You deal {actual_damage} damage to {enemy.name}!")
            else:
                combat_log.append(f"{enemy.name} dodges your attack!")

        if not enemy.is_alive():
            break

        # Enemy's turn - may use special attacks
        if random.random() < 0.3 and enemy.special_attacks:  # 30% chance for special attack
            damage_type, damage = enemy.perform_special_attack()
            actual_damage, hit_type = hero.take_damage(damage, damage_type)

            if hit_type == "dodged":
                combat_log.append(f"{enemy.name} uses {damage_type} attack, but you dodge!")
            else:
                combat_log.append(f"{enemy.name} uses special attack dealing {actual_damage} {damage_type} damage!")
        else:
            # Regular attack
            actual_damage, hit_type = hero.take_damage(enemy.attack, 'physical')
            if hit_type == "dodged":
                combat_log.append(f"{enemy.name} attacks, but you dodge!")
            else:
                combat_log.append(f"{enemy.name} deals {actual_damage} damage to you!")

        # Process status effects each turn
        status_damage = hero.process_status_effects()
        if status_damage > 0:
            combat_log.append(f"You take {status_damage} damage from status effects!")

    if hero.is_alive():
        leveled_up, levels_gained = hero.gain_experience(enemy.exp_reward)
        hero.gold += enemy.gold_reward

        combat_log.append(f"You defeated the {enemy.name}!")
        combat_log.append(f"Gained {enemy.exp_reward} experience and {enemy.gold_reward} gold!")

        if leveled_up:
            combat_log.append(hero.get_level_up_message())

        # Item drop chance based on enemy level and type
        drop_chance = 0.2 + (enemy.level * 0.05)  # 20% base + 5% per level
        if random.random() < min(drop_chance, 0.8):  # Max 80% drop chance
            item = generate_random_item(enemy.level)
            hero.add_item(item)
            combat_log.append(f"Found {item.name}!")

        return True, combat_log
    else:
        combat_log.append("You have been defeated...")
        return False, combat_log

def generate_random_item(enemy_level):
    """Generate a random item based on enemy level."""
    item_types = ['weapon', 'armor', 'accessory', 'consumable']
    item_type = random.choice(item_types)

    if item_type == 'consumable':
        consumables = [
            Item("Health Potion", 'consumable', 'common', effect='heal', power=50, value=25),
            Item("Mana Potion", 'consumable', 'common', effect='restore_mana', power=30, value=20),
            Item("Greater Health Potion", 'consumable', 'uncommon', effect='heal', power=100, value=50),
        ]
        return random.choice(consumables)

    # Equipment generation
    rarity_chance = min(0.1 + (enemy_level * 0.02), 0.5)  # Better items at higher levels
    if random.random() < rarity_chance:
        rarity = 'rare' if random.random() < 0.3 else 'uncommon'
    else:
        rarity = 'common'

    # Rarity multipliers
    rarity_multipliers = {
        'common': 1.0,
        'uncommon': 1.5,
        'rare': 2.0,
        'epic': 3.0,
        'legendary': 5.0
    }

    multiplier = rarity_multipliers[rarity]

    if item_type == 'weapon':
        attack_bonus = int((5 + enemy_level) * multiplier)
        names = ['Iron Sword', 'Steel Blade', 'Magic Sword', 'Enchanted Blade', 'Legendary Sword']
        name = random.choice(names)
        return Item(name, 'weapon', rarity, 'weapon', attack_bonus=attack_bonus,
                   value=int(50 * multiplier))

    elif item_type == 'armor':
        defense_bonus = int((3 + enemy_level) * multiplier)
        names = ['Leather Armor', 'Chain Mail', 'Plate Armor', 'Magic Armor', 'Legendary Armor']
        name = random.choice(names)
        return Item(name, 'armor', rarity, 'armor', defense_bonus=defense_bonus,
                   value=int(40 * multiplier))

    elif item_type == 'accessory':
        attack_bonus = int((2 + enemy_level * 0.5) * multiplier)
        defense_bonus = int((2 + enemy_level * 0.5) * multiplier)
        names = ['Silver Ring', 'Gold Amulet', 'Magic Pendant', 'Enchanted Gem', 'Legendary Artifact']
        name = random.choice(names)
        return Item(name, 'accessory', rarity, 'accessory', attack_bonus=attack_bonus,
                   defense_bonus=defense_bonus, value=int(60 * multiplier))

def random_encounter(hero):
    """Generate a random enemy encounter and return results."""
    enemy = get_random_enemy()
    success, combat_log = simulate_combat(hero, enemy)
    return success, combat_log

def get_shop_items():
    """Get available shop items with proper Item objects."""
    return {
        "Health Potion": Item("Health Potion", 'consumable', 'common', effect='heal', power=50, value=25, description="Restores 50 HP"),
        "Mana Potion": Item("Mana Potion", 'consumable', 'common', effect='restore_mana', power=30, value=20, description="Restores 30 MP"),
        "Iron Sword": Item("Iron Sword", 'weapon', 'common', 'weapon', attack_bonus=8, value=75, description="+8 Attack Power"),
        "Steel Sword": Item("Steel Sword", 'weapon', 'uncommon', 'weapon', attack_bonus=15, value=150, description="+15 Attack Power"),
        "Leather Armor": Item("Leather Armor", 'armor', 'common', 'armor', defense_bonus=5, value=60, description="+5 Defense"),
        "Chain Mail": Item("Chain Mail", 'armor', 'uncommon', 'armor', defense_bonus=12, value=120, description="+12 Defense"),
        "Silver Ring": Item("Silver Ring", 'accessory', 'common', 'accessory', attack_bonus=3, defense_bonus=3, value=80, description="+3 Attack, +3 Defense"),
        "Gold Ring": Item("Gold Ring", 'accessory', 'uncommon', 'accessory', attack_bonus=6, defense_bonus=6, value=160, description="+6 Attack, +6 Defense"),
    }

def apply_item_effects(hero, item):
    """Apply effects of equipped items."""
    if item.item_type in ['weapon', 'armor', 'accessory']:
        hero.equip_item(item)
    elif item.item_type == 'consumable':
        message = hero.use_item(item)
        if message:
            return message
    return None

def get_enemy_types():
    """Get available enemy types for different areas."""
    return {
        'forest': ['goblin', 'wolf', 'bandit', 'archer'],
        'cave': ['skeleton', 'spider', 'orc', 'bat'],
        'tower': ['mage', 'apprentice', 'guardian', 'elemental'],
        'dungeon': ['warrior', 'rogue', 'knight', 'boss']
    }

def handle_combat_turn(hero, enemy, action):
    """
    Handles a single turn of combat.

    Args:
        hero (Hero): The player's character.
        enemy (Enemy): The enemy character.
        action (str): The action taken by the player ('attack', 'run', 'use_item').

    Returns:
        list: A list of combat event dictionaries.
        bool: True if the combat is over, False otherwise.
    """
    events = []
    combat_over = False

    if action == "attack":
        # Player attacks with critical chance
        base_damage = hero.attack_power
        is_critical = random.random() * 100 < hero.crit_chance

        if is_critical:
            base_damage = int(base_damage * 1.5)
            events.append({'type': 'critical_hit'})

        actual_damage = enemy.take_damage(base_damage, 'physical')
        if actual_damage > 0:
            events.append({'type': 'player_damage', 'damage': actual_damage, 'target': enemy.name})
        else:
            events.append({'type': 'player_miss', 'target': enemy.name})

        if not enemy.is_alive():
            # Enemy defeated
            leveled_up, levels_gained = hero.gain_experience(enemy.exp_reward)
            hero.gold += enemy.gold_reward

            events.append({'type': 'enemy_defeated', 'enemy_name': enemy.name})
            events.append({'type': 'gain_experience', 'amount': enemy.exp_reward})
            events.append({'type': 'gain_gold', 'amount': enemy.gold_reward})

            if leveled_up:
                events.append({'type': 'level_up', 'new_level': hero.level, 'message': hero.get_level_up_message()})

            # Item drop
            drop_chance = 0.2 + (enemy.level * 0.05)
            if random.random() < min(drop_chance, 0.8):
                item = generate_random_item(enemy.level)
                hero.add_item(item)
                events.append({'type': 'item_drop', 'item_name': item.name, 'rarity': item.rarity})
            
            combat_over = True
            return events, combat_over

    elif action[0] == "use_skill":
        skill = action[1]
        events.append({'type': 'use_skill', 'skill_name': skill.name})
        
        damage = skill.damage
        if skill.skill_type == 'physical':
            damage += hero.strength // 2
        elif skill.skill_type == 'magic':
            damage += hero.intelligence // 2

        actual_damage = enemy.take_damage(damage, skill.skill_type)
        if actual_damage > 0:
            events.append({'type': 'player_damage', 'damage': actual_damage, 'target': enemy.name})
        else:
            events.append({'type': 'player_miss', 'target': enemy.name})

        if not enemy.is_alive():
            # Enemy defeated
            leveled_up, levels_gained = hero.gain_experience(enemy.exp_reward)
            hero.gold += enemy.gold_reward

            events.append({'type': 'enemy_defeated', 'enemy_name': enemy.name})
            events.append({'type': 'gain_experience', 'amount': enemy.exp_reward})
            events.append({'type': 'gain_gold', 'amount': enemy.gold_reward})

            if leveled_up:
                events.append({'type': 'level_up', 'new_level': hero.level, 'message': hero.get_level_up_message()})

            # Item drop
            drop_chance = 0.2 + (enemy.level * 0.05)
            if random.random() < min(drop_chance, 0.8):
                item = generate_random_item(enemy.level)
                hero.add_item(item)
                events.append({'type': 'item_drop', 'item_name': item.name, 'rarity': item.rarity})
            
            combat_over = True
            return events, combat_over

    elif action == "run":
        # Try to escape
        if random.random() < 0.4:  # 40% chance to escape
            events.append({'type': 'escape_success'})
            combat_over = True
            return events, combat_over
        else:
            events.append({'type': 'escape_fail'})

    elif action == "use_item":
        # Item was already used, just process enemy turn
        pass

    # Enemy's turn
    if enemy.is_alive():
        if random.random() < 0.3 and enemy.special_attacks:  # 30% chance for special attack
            damage_type, damage = enemy.perform_special_attack()
            actual_damage, hit_type = hero.take_damage(damage, damage_type)

            if hit_type == "dodged":
                events.append({'type': 'enemy_miss', 'enemy_name': enemy.name, 'attack_type': damage_type})
            else:
                events.append({'type': 'enemy_damage', 'damage': actual_damage, 'enemy_name': enemy.name, 'attack_type': damage_type})
        else:
            # Regular attack
            actual_damage, hit_type = hero.take_damage(enemy.attack, 'physical')
            if hit_type == "dodged":
                events.append({'type': 'enemy_miss', 'enemy_name': enemy.name, 'attack_type': 'physical'})
            else:
                events.append({'type': 'enemy_damage', 'damage': actual_damage, 'enemy_name': enemy.name, 'attack_type': 'physical'})

        if not hero.is_alive():
            events.append({'type': 'player_defeated'})
            combat_over = True
            return events, combat_over

    # Process status effects
    status_damage = hero.process_status_effects()
    if status_damage > 0:
        events.append({'type': 'status_effect_damage', 'damage': status_damage})

    return events, combat_over
