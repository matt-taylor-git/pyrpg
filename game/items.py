
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

    def to_dict(self) -> dict:
        """
        Serialize Item object to dictionary for saving.

        Returns:
            Dictionary containing all item state
        """
        return {
            'name': self.name,
            'item_type': self.item_type,
            'rarity': self.rarity,
            'slot': self.slot,
            'attack_bonus': self.attack_bonus,
            'defense_bonus': self.defense_bonus,
            'effect': self.effect,
            'power': self.power,
            'value': self.value,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Deserialize Item object from dictionary.

        Args:
            data: Dictionary containing item state

        Returns:
            Item instance
        """
        return cls(
            name=data['name'],
            item_type=data['item_type'],
            rarity=data.get('rarity', 'common'),
            slot=data.get('slot'),
            attack_bonus=data.get('attack_bonus', 0),
            defense_bonus=data.get('defense_bonus', 0),
            effect=data.get('effect'),
            power=data.get('power', 0),
            value=data.get('value', 0),
            description=data.get('description', '')
        )
