# -*- coding: utf-8 -*-
"""
Character customization page for PyRPG Adventure
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                               QPushButton, QFrame, QGroupBox, QScrollArea, QLineEdit)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from ..theme import Theme
from ..widgets import Card, StyledButton
from ..components.validation_label import ValidationLabel
from game.customization import customization_system
import os


class CharacterPreviewWidget(QFrame):
    """Character preview widget displaying current customization"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.customization = customization_system.get_default_customization()
        self.init_ui()

    def init_ui(self):
        """Initialize the character preview UI"""
        self.setFixedSize(250, 250)
        self.setStyleSheet(f"""
            CharacterPreviewWidget {{
                background-color: {Theme.CARD};
                border: 2px solid {Theme.BORDER};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Character Preview")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Sprite display
        self.sprite_label = QLabel()
        self.sprite_label.setMinimumSize(150, 150)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.sprite_label)

        # Current name display
        self.name_label = QLabel(f"Name: {self.customization['name']}")
        self.name_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                font-size: 12px;
                text-align: center;
                font-weight: bold;
            }}
        """)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        # Update initial display
        self.update_preview()

    def set_customization(self, customization):
        """Update the current customization and refresh preview"""
        self.customization = customization.copy()
        self.update_preview()

    def update_preview(self):
        """Update the preview display based on current customization"""
        # Update name
        self.name_label.setText(f"Name: {self.customization['name']}")

        # Load and display sprite (using Hero.png for now, could be enhanced with character-specific sprites)
        try:
            pixmap = QPixmap(os.path.join("assets", "Hero.png"))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
                self.sprite_label.setPixmap(scaled_pixmap)
            else:
                self.sprite_label.setText("👤")
                self.sprite_label.setStyleSheet("font-size: 48px; color: #dc3545;")
        except Exception:
            self.sprite_label.setText("👤")
            self.sprite_label.setStyleSheet("font-size: 48px; color: #dc3545;")


class CustomizationSection(QGroupBox):
    """Section containing customization options for a category"""

    def __init__(self, title, category_type, parent=None):
        super().__init__(title, parent)
        self.category_type = category_type
        self.options_changed = Signal(dict)  # Emits customization changes
        self.init_ui()

    def init_ui(self):
        """Initialize the customization section UI"""
        self.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {Theme.BORDER};
                border-radius: 8px;
                margin-top: 8px;
                padding: 8px;
                color: {Theme.FOREGROUND};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #dc3545;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING_MD)

    def add_option(self, label_text, option_key, options_list):
        """Add a customization option dropdown"""
        option_layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet(f"color: {Theme.FOREGROUND}; font-size: 14px;")
        option_layout.addWidget(label)

        combo = QComboBox()
        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.CARD};
                border: 1px solid {Theme.BORDER};
                border-radius: 4px;
                padding: 4px;
                color: {Theme.FOREGROUND};
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {Theme.FOREGROUND};
                margin-right: 8px;
            }}
        """)

        # Populate dropdown
        for option in options_list:
            display_text = option['name']
            combo.addItem(display_text, option['id'])

        # Connect change signal
        combo.currentIndexChanged.connect(lambda: self.on_option_changed(option_key, combo))

        option_layout.addWidget(combo)
        self.layout().addLayout(option_layout)

        # Store reference for updates
        setattr(self, f"{option_key}_combo", combo)

    def on_option_changed(self, option_key, combo):
        """Handle option change and emit signal"""
        option_id = combo.currentData()
        change = {option_key: option_id}
        self.options_changed.emit(change)

    def set_option_value(self, option_key, option_id):
        """Set the value of a specific option"""
        combo = getattr(self, f"{option_key}_combo", None)
        if combo:
            for i in range(combo.count()):
                if combo.itemData(i) == option_id:
                    combo.setCurrentIndex(i)
                    break


class CharacterCustomizationPage(QWidget):
    """Main character customization page"""
    customization_changed = Signal(dict)  # Emits full customization dict
    save_requested = Signal(dict)  # Emits when save is requested
    load_requested = Signal()  # Emits when load is requested

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_customization = customization_system.get_default_customization()
        self.init_ui()

    def init_ui(self):
        """Initialize the character customization page UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Left side: Character preview
        self.preview_widget = CharacterPreviewWidget()
        main_layout.addWidget(self.preview_widget)

        # Right side: Customization options
        options_layout = QVBoxLayout()
        options_layout.setSpacing(Theme.SPACING_MD)

        # Name customization
        name_section = Card()
        name_layout = QVBoxLayout()

        name_label = QLabel("Character Name")
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #dc3545;")
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit(self.current_customization['name'])
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                font-size: 14px;
                padding: 8px;
                border: 1px solid {Theme.BORDER};
                border-radius: 4px;
                background-color: {Theme.CARD};
                color: {Theme.FOREGROUND};
            }}
            QLineEdit:focus {{
                border-color: {Theme.PRIMARY};
            }}
        """)
        self.name_input.textChanged.connect(self.on_name_changed)
        name_layout.addWidget(self.name_input)

        # Name validation
        self.name_validation = ValidationLabel()
        name_layout.addWidget(self.name_validation)

        name_section.main_layout.addLayout(name_layout)
        options_layout.addWidget(name_section)

        # Appearance customization
        self.appearance_section = CustomizationSection("Appearance", "appearance")
        self.appearance_section.options_changed.connect(self.on_appearance_changed)

        # Add appearance options
        appearance_data = customization_system.appearance_options
        self.appearance_section.add_option("Hair Color", "hair_color", appearance_data['hair_color'])
        self.appearance_section.add_option("Hair Style", "hair_style", appearance_data['hair_style'])
        self.appearance_section.add_option("Skin Tone", "skin_tone", appearance_data['skin_tone'])
        self.appearance_section.add_option("Eye Color", "eye_color", appearance_data['eye_color'])

        options_layout.addWidget(self.appearance_section)

        # Cosmetic customization
        self.cosmetic_section = CustomizationSection("Cosmetics", "cosmetic")
        self.cosmetic_section.options_changed.connect(self.on_cosmetic_changed)

        # Add cosmetic options (filter to unlocked)
        cosmetic_data = customization_system.cosmetic_options
        for category in ['headgear', 'accessory', 'facial_hair']:
            unlocked_options = customization_system.get_unlocked_options(category)
            if unlocked_options:
                display_name = category.replace('_', ' ').title()
                self.cosmetic_section.add_option(display_name, category, unlocked_options)

        options_layout.addWidget(self.cosmetic_section)

        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(Theme.SPACING_MD)

        self.save_btn = StyledButton("💾 Save", variant="primary")
        self.save_btn.clicked.connect(self.on_save_requested)
        actions_layout.addWidget(self.save_btn)

        self.load_btn = StyledButton("📁 Load", variant="secondary")
        self.load_btn.clicked.connect(self.on_load_requested)
        actions_layout.addWidget(self.load_btn)

        self.reset_btn = StyledButton("🔄 Reset", variant="secondary")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        actions_layout.addWidget(self.reset_btn)

        options_layout.addLayout(actions_layout)

        # Add stretch to push everything to top
        options_layout.addStretch()

        main_layout.addLayout(options_layout)

        # Load initial settings
        self.load_customization(self.current_customization)

    def on_name_changed(self, text):
        """Handle name input changes"""
        self.current_customization['name'] = text.strip()

        # Validate name
        is_valid, message = customization_system.validate_customization(self.current_customization)
        if is_valid:
            self.name_validation.clear_validation()
        else:
            # Find name-specific errors
            if "Name must be" in message or "Name can only" in message:
                self.name_validation.show_error(message.split(": ", 1)[1] if ": " in message else message)
            else:
                self.name_validation.clear_validation()

        self.emit_customization_change()

    def on_appearance_changed(self, changes):
        """Handle appearance option changes"""
        self.current_customization['appearance'].update(changes)
        self.emit_customization_change()

    def on_cosmetic_changed(self, changes):
        """Handle cosmetic option changes"""
        self.current_customization['cosmetic'].update(changes)
        self.emit_customization_change()

    def emit_customization_change(self):
        """Emit the current customization state"""
        self.preview_widget.set_customization(self.current_customization)
        self.customization_changed.emit(self.current_customization.copy())

    def load_customization(self, customization):
        """Load a customization configuration"""
        self.current_customization = customization.copy()

        # Update UI elements
        self.name_input.setText(customization['name'])

        # Update appearance options
        for key, value in customization['appearance'].items():
            self.appearance_section.set_option_value(key, value)

        # Update cosmetic options
        for key, value in customization['cosmetic'].items():
            self.cosmetic_section.set_option_value(key, value)

        # Update preview
        self.preview_widget.set_customization(customization)

    def reset_to_defaults(self):
        """Reset customization to default values"""
        default_customization = customization_system.get_default_customization()
        self.load_customization(default_customization)

    def on_save_requested(self):
        """Handle save button click"""
        # Validate before saving
        is_valid, message = customization_system.validate_customization(self.current_customization)
        if not is_valid:
            self.name_validation.show_error(message)
            return

        self.save_requested.emit(self.current_customization.copy())

    def on_load_requested(self):
        """Handle load button click"""
        self.load_requested.emit()

    def get_current_customization(self):
        """Get the current customization state"""
        return self.current_customization.copy()

    def set_customization_preview(self, customization):
        """Update preview without changing current state"""
        self.preview_widget.set_customization(customization)
