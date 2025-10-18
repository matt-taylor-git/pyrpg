"""
Unit tests for character customization functionality.
"""
import unittest
import os
import json
import tempfile
from game.customization import CharacterCustomization, customization_system


class TestCharacterCustomization(unittest.TestCase):
    """Test cases for character customization system."""

    def setUp(self):
        """Set up test fixtures."""
        self.customization_system = CharacterCustomization()

    def test_default_customization_structure(self):
        """Test that default customization has correct structure."""
        default = self.customization_system.get_default_customization()

        # Check required keys
        required_keys = ['name', 'appearance', 'cosmetic']
        for key in required_keys:
            self.assertIn(key, default, f"Missing key: {key}")

        # Check appearance options
        appearance = default['appearance']
        appearance_keys = ['hair_color', 'hair_style', 'skin_tone', 'eye_color']
        for key in appearance_keys:
            self.assertIn(key, appearance, f"Missing appearance key: {key}")

        # Check cosmetic options
        cosmetic = default['cosmetic']
        cosmetic_keys = ['headgear', 'accessory', 'facial_hair']
        for key in cosmetic_keys:
            self.assertIn(key, cosmetic, f"Missing cosmetic key: {key}")

    def test_customization_validation_valid(self):
        """Test validation of valid customization data."""
        valid_customization = {
            'name': 'TestHero',
            'appearance': {
                'hair_color': 'brown',
                'hair_style': 'medium',
                'skin_tone': 'medium',
                'eye_color': 'blue'
            },
            'cosmetic': {
                'headgear': 'cap',
                'accessory': 'scarf',
                'facial_hair': 'none'
            }
        }

        is_valid, message = self.customization_system.validate_customization(valid_customization)
        self.assertTrue(is_valid, f"Valid customization rejected: {message}")
        self.assertEqual(message, "Customization is valid")

    def test_customization_validation_name_too_short(self):
        """Test validation rejects names that are too short."""
        invalid_customization = self.customization_system.get_default_customization()
        invalid_customization['name'] = ''  # Too short

        is_valid, message = self.customization_system.validate_customization(invalid_customization)
        self.assertFalse(is_valid, "Name too short should be rejected")
        self.assertIn("Name must be", message)

    def test_customization_validation_name_too_long(self):
        """Test validation rejects names that are too long."""
        invalid_customization = self.customization_system.get_default_customization()
        invalid_customization['name'] = 'A' * 21  # Too long

        is_valid, message = self.customization_system.validate_customization(invalid_customization)
        self.assertFalse(is_valid, "Name too long should be rejected")
        self.assertIn("Name must be", message)

    def test_customization_validation_invalid_characters(self):
        """Test validation rejects names with invalid characters."""
        invalid_customization = self.customization_system.get_default_customization()
        invalid_customization['name'] = 'Test@Hero'  # Invalid character

        is_valid, message = self.customization_system.validate_customization(invalid_customization)
        self.assertFalse(is_valid, "Invalid characters should be rejected")
        self.assertIn("Name can only contain", message)

    def test_customization_validation_missing_key(self):
        """Test validation rejects incomplete customization data."""
        invalid_customization = self.customization_system.get_default_customization()
        del invalid_customization['appearance']  # Remove required key

        is_valid, message = self.customization_system.validate_customization(invalid_customization)
        self.assertFalse(is_valid, "Missing key should be rejected")
        self.assertIn("Missing required", message)

    def test_customization_validation_invalid_appearance_option(self):
        """Test validation rejects invalid appearance options."""
        invalid_customization = self.customization_system.get_default_customization()
        invalid_customization['appearance']['hair_color'] = 'invalid_color'

        is_valid, message = self.customization_system.validate_customization(invalid_customization)
        self.assertFalse(is_valid, "Invalid appearance option should be rejected")
        self.assertIn("Invalid hair_color option", message)

    def test_get_option_details(self):
        """Test getting detailed option information."""
        # Test hair_color option (appearance)
        option_detail = self.customization_system.get_option_details('hair_color', 'brown')
        self.assertIsNotNone(option_detail, "Should return option details for valid hair_color option")
        self.assertEqual(option_detail['name'], 'Brown')

        # Test headgear option (cosmetic)
        cosmetic_detail = self.customization_system.get_option_details('headgear', 'cap')
        self.assertIsNotNone(cosmetic_detail, "Should return option details for valid headgear option")
        self.assertEqual(cosmetic_detail['name'], 'Baseball Cap')

        # Test invalid category/option
        self.assertIsNone(self.customization_system.get_option_details('invalid', 'brown'))
        self.assertIsNone(self.customization_system.get_option_details('hair_color', 'invalid'))

    def test_get_unlocked_cosmetic_options(self):
        """Test filtering cosmetic options to only unlocked ones."""
        unlocked_headgear = self.customization_system.get_unlocked_options('headgear')
        self.assertTrue(len(unlocked_headgear) > 0, "Should have unlocked headgear options")

        all_headgear = self.customization_system.cosmetic_options['headgear']
        unlocked_names = [opt['name'] for opt in unlocked_headgear]

        # Check that only unlocked options are returned
        for option in all_headgear:
            if option['unlocked']:
                self.assertIn(option['name'], unlocked_names, f"Unlocked option {option['name']} should be included")
            else:
                self.assertNotIn(option['name'], unlocked_names, f"Locked option {option['name']} should not be included")


class TestCustomizationPersistence(unittest.TestCase):
    """Test cases for customization save/load functionality."""

    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_saves_dir = None

        # Mock the saves directory for testing
        import game.customization
        self.original_saves_dir = game.customization.customization_system.__class__.customization_file
        # This is complex to mock, so we'll focus on core logic testing

    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original if needed
        pass


if __name__ == '__main__':
    unittest.main()
