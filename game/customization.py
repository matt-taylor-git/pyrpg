"""
Character customization options and data structures.
Provides customization categories, options, and default settings for character appearance.
"""

class CharacterCustomization:
    """Manages all character customization options and settings."""

    def __init__(self):
        self.appearance_options = self._load_appearance_options()
        self.cosmetic_options = self._load_cosmetic_options()
        self.name_limits = (1, 20)  # Min/max character length for names

    def _load_appearance_options(self):
        """Load available appearance customization options."""
        return {
            'hair_color': [
                {'id': 'black', 'name': 'Black', 'color': '#1a1a1a'},
                {'id': 'brown', 'name': 'Brown', 'color': '#8B4513'},
                {'id': 'blonde', 'name': 'Blonde', 'color': '#FFD700'},
                {'id': 'red', 'name': 'Red', 'color': '#DC143C'},
                {'id': 'gray', 'name': 'Gray', 'color': '#808080'},
                {'id': 'white', 'name': 'White', 'color': '#FFFFFF'}
            ],
            'hair_style': [
                {'id': 'short', 'name': 'Short'},
                {'id': 'long', 'name': 'Long'},
                {'id': 'medium', 'name': 'Medium'},
                {'id': 'buzzcut', 'name': 'Buzz Cut'},
                {'id': 'ponytail', 'name': 'Ponytail'}
            ],
            'skin_tone': [
                {'id': 'pale', 'name': 'Pale', 'color': '#F5DEB3'},
                {'id': 'fair', 'name': 'Fair', 'color': '#DEB887'},
                {'id': 'medium', 'name': 'Medium', 'color': '#D2B48C'},
                {'id': 'tan', 'name': 'Tan', 'color': '#CD853F'},
                {'id': 'olive', 'name': 'Olive', 'color': '#BCB88A'},
                {'id': 'dark', 'name': 'Dark', 'color': '#8B4513'}
            ],
            'eye_color': [
                {'id': 'brown', 'name': 'Brown', 'color': '#8B4513'},
                {'id': 'blue', 'name': 'Blue', 'color': '#4169E1'},
                {'id': 'green', 'name': 'Green', 'color': '#228B22'},
                {'id': 'hazel', 'name': 'Hazel', 'color': '#8B7355'},
                {'id': 'gray', 'name': 'Gray', 'color': '#708090'}
            ]
        }

    def _load_cosmetic_options(self):
        """Load available cosmetic customization options."""
        return {
            'headgear': [
                {'id': 'none', 'name': 'None', 'unlocked': True},
                {'id': 'cap', 'name': 'Baseball Cap', 'unlocked': True},
                {'id': 'helmet', 'name': 'Warrior Helmet', 'unlocked': False},
                {'id': 'crown', 'name': 'Golden Crown', 'unlocked': False}
            ],
            'accessory': [
                {'id': 'none', 'name': 'None', 'unlocked': True},
                {'id': 'scarf', 'name': 'Silk Scarf', 'unlocked': True},
                {'id': 'necklace', 'name': 'Silver Necklace', 'unlocked': False},
                {'id': 'cape', 'name': 'Hero Cape', 'unlocked': False}
            ],
            'facial_hair': [
                {'id': 'none', 'name': 'None', 'unlocked': True},
                {'id': 'beard', 'name': 'Beard', 'unlocked': True},
                {'id': 'mustache', 'name': 'Mustache', 'unlocked': True}
            ]
        }

    def get_default_customization(self):
        """Get default customization settings."""
        return {
            'name': 'Hero',
            'appearance': {
                'hair_color': 'brown',
                'hair_style': 'medium',
                'skin_tone': 'medium',
                'eye_color': 'brown'
            },
            'cosmetic': {
                'headgear': 'none',
                'accessory': 'none',
                'facial_hair': 'none'
            }
        }

    def validate_customization(self, customization_data):
        """Validate customization data structure."""
        required_keys = ['name', 'appearance', 'cosmetic']

        # Check required top-level keys
        if not all(key in customization_data for key in required_keys):
            return False, "Missing required customization keys"

        # Validate name
        name = customization_data['name']
        if not isinstance(name, str) or not self.name_limits[0] <= len(name) <= self.name_limits[1]:
            return False, f"Name must be {self.name_limits[0]}-{self.name_limits[1]} characters"

        # Validate letters/numbers/space/-/underscore only
        if not all(c.isalnum() or c in (' ', '-', '_') for c in name):
            return False, "Name can only contain letters, numbers, spaces, hyphens, and underscores"

        # Validate appearance options
        appearance = customization_data['appearance']
        for category in ['hair_color', 'hair_style', 'skin_tone', 'eye_color']:
            if category not in appearance:
                return False, f"Missing appearance category: {category}"
            option_ids = [opt['id'] for opt in self.appearance_options[category]]
            if appearance[category] not in option_ids:
                return False, f"Invalid {category} option: {appearance[category]}"

        # Validate cosmetic options (only check if unlocked)
        cosmetic = customization_data['cosmetic']
        for category in ['headgear', 'accessory', 'facial_hair']:
            if category not in cosmetic:
                return False, f"Missing cosmetic category: {category}"

            option = next((opt for opt in self.cosmetic_options[category]
                          if opt['id'] == cosmetic[category]), None)
            if not option:
                return False, f"Invalid {category} option: {cosmetic[category]}"

        return True, "Customization is valid"

    def get_option_details(self, category, option_id):
        """Get detailed information about a specific customization option."""
        if category in self.appearance_options:
            return next((opt for opt in self.appearance_options[category]
                        if opt['id'] == option_id), None)
        elif category in self.cosmetic_options:
            return next((opt for opt in self.cosmetic_options[category]
                        if opt['id'] == option_id), None)
        return None

    def get_unlocked_options(self, category):
        """Get all unlocked options for a cosmetic category."""
        if category not in self.cosmetic_options:
            return []

        return [opt for opt in self.cosmetic_options[category] if opt['unlocked']]


# Global customization instance
customization_system = CharacterCustomization()
