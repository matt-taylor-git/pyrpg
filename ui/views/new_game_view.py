# -*- coding: utf-8 -*-
"""
Enhanced animated character creation view for PyRPG
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QFrame, QProgressBar, QGraphicsDropShadowEffect,
                               QApplication)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PySide6.QtGui import QFont, QPixmap
from ..widgets import Card, StyledButton
from ..theme import Theme
from ..custom_widgets import ScalablePixmapLabel
from ..components.validation_label import ValidationLabel
import os
import random


class CharacterPreview(QFrame):
    """Animated character preview widget with sprite animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_class = "hero"
        self.animation_frame = 0
        self.animation_timer = None
        self.sprite_cycle = ["idle", "walk1", "idle", "walk2"]
        self.init_ui()
        self.start_sprite_animation()

    def init_ui(self):
        """Initialize the character preview UI"""
        self.setFixedSize(200, 200)
        self.setStyleSheet(f"""
            CharacterPreview {{
                background-color: {Theme.CARD};
                border: 2px solid {Theme.BORDER};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Character Preview")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Sprite container
        self.sprite_container = QWidget()
        sprite_layout = QVBoxLayout(self.sprite_container)

        self.sprite_label = ScalablePixmapLabel()
        self.sprite_label.setMinimumSize(120, 120)
        self.sprite_label.setAlignment(Qt.AlignCenter)
        self.sprite_label.setStyleSheet("border: none; background: transparent;")
        sprite_layout.addWidget(self.sprite_label)

        layout.addWidget(self.sprite_container)

        # Class selector buttons
        class_layout = QHBoxLayout()

        classes = ["hero", "mage", "rogue"]
        self.class_buttons = {}

        for class_name in classes:
            btn = StyledButton(class_name.title(), size="sm")
            btn.clicked.connect(lambda checked=False, name=class_name: self.set_character_class(name))
            class_layout.addWidget(btn)
            self.class_buttons[class_name] = btn

        layout.addLayout(class_layout)

        # Set initial class
        self.set_character_class("hero")

    def set_character_class(self, class_name):
        """Change the character class and update sprite"""
        self.current_class = class_name

        # Update button states
        for name, btn in self.class_buttons.items():
            if name == class_name:
                btn.setVariant("primary")
            else:
                btn.setVariant("default")

        # Update sprite immediately
        self.update_sprite()

    def start_sprite_animation(self):
        """Start the idle sprite animation"""
        if self.animation_timer:
            self.animation_timer.stop()

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.next_animation_frame)
        self.animation_timer.start(800)  # Change sprite every 800ms
        self.update_sprite()

    def next_animation_frame(self):
        """Cycle to next animation frame"""
        self.animation_frame = (self.animation_frame + 1) % len(self.sprite_cycle)
        self.update_sprite()

    def update_sprite(self):
        """Update the sprite image based on current class and frame"""
        sprite_name = f"{self.current_class}_idle.png"
        sprite_cycle = self.sprite_cycle[self.animation_frame]

        # Map to actual asset names
        sprite_map = {
            ("hero", "idle"): "Hero.png",
            ("hero", "walk1"): "Hero.png",
            ("hero", "walk2"): "Hero.png",
            ("mage", "idle"): "mage.png",
            ("mage", "walk1"): "mage.png",
            ("mage", "walk2"): "mage.png",
            ("rogue", "idle"): "rogue.png",
            ("rogue", "walk1"): "rogue.png",
            ("rogue", "walk2"): "rogue.png",
        }

        asset_name = sprite_map.get((self.current_class, sprite_cycle), "Hero.png")

        try:
            pixmap = QPixmap(os.path.join("assets", asset_name))
            if not pixmap.isNull():
                # Scale and center the sprite with proper fallbacks
                scaled_pixmap = pixmap.scaledToHeight(120, Qt.SmoothTransformation)
                self.sprite_label.setOriginalPixmap(scaled_pixmap)
            else:
                # Fallback to text representation
                self.sprite_label.setText(f"👤 {self.current_class.title()}")
                self.sprite_label.setStyleSheet("font-size: 48px; color: #dc3545;")
        except Exception as e:
            self.sprite_label.setText(f"👤 {self.current_class.title()}")
            self.sprite_label.setStyleSheet("font-size: 48px; color: #dc3545;")


class NewGameView(QWidget):
    """Enhanced animated character creation view for PyRPG"""
    character_created = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations_active = False
        self.init_ui()
        self.start_entry_animation()

    def init_ui(self):
        """Initialize the enhanced character creation UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Title with animation
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)

        # Main title
        self.main_title = QLabel("🌟 R E A L M   O F   L E G E N D S 🌟")
        self.main_title.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #dc3545;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        """)
        self.main_title.setAlignment(Qt.AlignCenter)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(2)
        shadow.setYOffset(4)
        shadow.setColor(Qt.black)
        self.main_title.setGraphicsEffect(shadow)

        title_layout.addWidget(self.main_title)

        # Subtitle
        subtitle = QLabel("Forge Your Destiny")
        subtitle.setStyleSheet("font-size: 18px; color: #9a96a5; margin-top: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)

        main_layout.addLayout(title_layout)

        # Character creation card
        self.create_card = Card()
        self.create_card.setMinimumWidth(600)
        self.create_card.setMaximumWidth(800)

        create_layout = QHBoxLayout()
        create_layout.setSpacing(30)

        # Character preview (left side)
        self.char_preview = CharacterPreview()
        create_layout.addWidget(self.char_preview)

        # Character details (right side)
        details_layout = QVBoxLayout()
        details_layout.setSpacing(15)

        # Name input section with animation
        name_section = QWidget()
        name_layout = QVBoxLayout(name_section)

        name_title = QLabel("Choose Your Name")
        name_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f1f0f2;")
        name_layout.addWidget(name_title)

        # Name input with styling and validation
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your hero's name...")
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                font-size: 14px;
                padding: 12px;
                border: 2px solid {Theme.BORDER};
                border-radius: 8px;
                background-color: {Theme.CARD};
                color: {Theme.FOREGROUND};
                font-weight: 500;
            }}
            QLineEdit:focus {{
                border-color: {Theme.PRIMARY.name()};
                background-color: {Theme.MUTED.name()};
            }}
        """)
        self.name_input.setMaxLength(20)  # Enforce limit visually
        self.name_input.textChanged.connect(self.validate_name_input)
        name_layout.addWidget(self.name_input)

        # Validation feedback label
        self.validation_label = ValidationLabel()
        name_layout.addWidget(self.validation_label)

        details_layout.addWidget(name_section)

        # Character stats preview
        stats_section = QWidget()
        stats_layout = QVBoxLayout(stats_section)

        stats_title = QLabel("Starting Stats")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f1f0f2;")
        stats_layout.addWidget(stats_title)

        # Stats display
        stats_info = QLabel("""
        <html>
        <body>
            <div style='line-height: 1.6; color: #abb2bf;'>
                <div>🏋️ Strength: <b>8</b></div>
                <div>🏃 Dexterity: <b>6</b></div>
                <div>🔮 Intelligence: <b>4</b></div>
                <div>❤️ Vitality: <b>10</b></div>
            </div>
        </body>
        </html>
        """)
        stats_info.setTextFormat(Qt.RichText)
        stats_layout.addWidget(stats_info)

        details_layout.addWidget(stats_section)

        # Action buttons
        button_section = QWidget()
        button_layout = QVBoxLayout(button_section)

        # Create adventure button with enhanced styling
        self.start_btn = StyledButton("✨ Begin Your Quest", variant="primary", size="lg")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.clicked.connect(self.start_game)

        # Add glow effect to start button
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(25)
        glow.setXOffset(0)
        glow.setYOffset(0)
        glow.setColor(Qt.GlobalColor.darkYellow)
        self.start_btn.setGraphicsEffect(glow)

        button_layout.addWidget(self.start_btn)

        details_layout.addWidget(button_section)

        create_layout.addLayout(details_layout)

        self.create_card.main_layout.addLayout(create_layout)
        main_layout.addWidget(self.create_card)

        # Footer with fade animation
        self.footer_label = QLabel("Press Enter to create your character instantly")
        self.footer_label.setStyleSheet("color: #6c757d; font-size: 12px; margin-top: 20px;")
        self.footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.footer_label)

    def start_entry_animation(self):
        """Start the entry animations"""
        if self.animations_active:
            return

        self.animations_active = True

        # Animate title from above
        title_anim = QPropertyAnimation(self.main_title, b"pos")
        title_anim.setStartValue(self.main_title.pos() + QPoint(0, -100))
        title_anim.setEndValue(self.main_title.pos())
        title_anim.setDuration(1200)
        title_anim.setEasingCurve(QEasingCurve.OutBounce)

        # Animate card from right
        card_anim = QPropertyAnimation(self.create_card, b"pos")
        card_anim.setStartValue(self.create_card.pos() + QPoint(800, 0))
        card_anim.setEndValue(self.create_card.pos())
        card_anim.setDuration(1000)
        card_anim.setEasingCurve(QEasingCurve.OutBack)

        # Start animations
        title_anim.start()
        card_anim.start()

        # Keep references to prevent garbage collection
        self._animations = [title_anim, card_anim]

    def validate_name_input(self):
        """Validate character name input and show inline feedback"""
        char_name = self.name_input.text().strip()

        # Clear previous validation
        self.validation_label.clear_validation()

        # Basic validation rules
        if not char_name:
            self.validation_label.show_warning("A hero needs a name!")
            self.start_btn.setEnabled(False)
            return

        if len(char_name) > 20:
            self.validation_label.show_error("Name is too long (max 20 characters)")
            self.start_btn.setEnabled(False)
            return

        # Check for invalid characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-")
        if not all(c in valid_chars for c in char_name):
            self.validation_label.show_error("Only letters, numbers, spaces, hyphens, and underscores allowed")
            self.start_btn.setEnabled(False)
            return

        # Check for spaces at start/end
        if char_name.startswith(' ') or char_name.endswith(' '):
            self.validation_label.show_warning("Name shouldn't start or end with spaces")
            self.start_btn.setEnabled(False)
            return

        # All validation passed
        if len(char_name) >= 3:
            self.validation_label.show_success("That's a heroic name!")
            self.start_btn.setEnabled(True)
        else:
            self.validation_label.show_warning("Make it at least 3 characters long")
            self.start_btn.setEnabled(False)

    def start_game(self):
        """Handle character creation and transition"""
        char_name = self.name_input.text().strip()

        # Use inline validation instead of QMessageBox
        if self.validation_label.isVisible() and "error" in self.validation_label.styleSheet().lower():
            # Error feedback is already shown, don't proceed
            return

        # Additional final validation
        if not char_name or len(char_name) < 3 or len(char_name) > 20:
            self.validate_name_input()  # This will show appropriate error
            return

        # Disable button to prevent double-clicking
        self.start_btn.setEnabled(False)
        self.start_btn.setText("🌀 Creating Character...")

        # Clear validation feedback
        self.validation_label.clear_validation()

        # Animate out before emitting signal
        exit_anim = QPropertyAnimation(self.create_card, b"pos")
        exit_anim.setStartValue(self.create_card.pos())
        exit_anim.setEndValue(self.create_card.pos() + QPoint(0, -600))
        exit_anim.setDuration(800)
        exit_anim.setEasingCurve(QEasingCurve.InBack)
        exit_anim.finished.connect(lambda: self.character_created.emit(char_name))
        exit_anim.start()

        self._exit_anim = exit_anim

    def keyPressEvent(self, event):
        """Handle Enter key for quick creation"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.name_input.hasFocus():
                self.start_game()
        super().keyPressEvent(event)
