
class Item:
    """Represents items in the game world."""

    def __init__(self, name, item_type, rarity='common', slot=None, attack_bonus=0,
                 defense_bonus=0, effect=None, power=0, value=0, description=""):
        self.name = name
        self.item_type = item_type  # 'weapon', 'armor', 'accessory', 'consumable'
        self.rarity = rarity  # 'common', 'uncommon', 'rare', 'epic', 'legendary'
        self.slot = slot  # 'weapon', 'armor', 'accessory' for equipment
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.effect = effect  # 'heal', 'restore_mana', etc. for consumables
        self.power = power  # Power of the effect
        self.value = value  # Gold value
        self.description = description

    def get_rarity_color(self):
        """Get color code for item rarity."""
        colors = {
            'common': '#ffffff',
            'uncommon': '#00ff00',
            'rare': '#0088ff',
            'epic': '#aa00ff',
            'legendary': '#ffaa00'
        }
        return colors.get(self.rarity, '#ffffff')
