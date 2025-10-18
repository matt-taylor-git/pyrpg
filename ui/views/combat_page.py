# -*- coding: utf-8 -*-
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QTextEdit, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from ..widgets import Card, StyledButton, StyledProgressBar
from ..theme import Theme

class CombatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.battle_log = ["A wild enemy appears!", "Prepare for battle!"]
        self.init_ui()
        self.setup_accessibility()

    def setup_accessibility(self):
        """Set up accessibility features for the combat page"""
        self.setAccessibleName("Combat Interface")
        self.setAccessibleDescription("Battle arena where you fight enemies")

        # Combat buttons accessibility
        self.attack_btn.setAccessibleName("Attack button")
        self.attack_btn.setAccessibleDescription("Attack the enemy (A)")

        self.use_skill_btn.setAccessibleName("Use skill button")
        self.use_skill_btn.setAccessibleDescription("Use a special skill (S)")

        self.use_item_btn.setAccessibleName("Use item button")
        self.use_item_btn.setAccessibleDescription("Use a consumable item (I)")

        self.run_btn.setAccessibleName("Run away button")
        self.run_btn.setAccessibleDescription("Attempt to escape from battle (R)")

        # Health bars accessibility
        self.hero_combat_health_bar.setAccessibleName("Hero health bar")
        self.hero_combat_health_bar.setAccessibleDescription("Current hero health status")

        self.enemy_combat_health_bar.setAccessibleName("Enemy health bar")
        self.enemy_combat_health_bar.setAccessibleDescription("Current enemy health status")

        # Enable keyboard navigation
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Left Column: Battle Arena
        arena_card = self._create_arena_card()
        main_layout.addWidget(arena_card, 2)

        # Right Column: Battle Log
        log_card = self._create_log_card()
        main_layout.addWidget(log_card, 1)

    def _create_arena_card(self):
        card = Card()
        layout = QVBoxLayout()

        # Title with improved styling
        title = QLabel("⚔️ Battle Arena")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.PRIMARY.name()}; margin-bottom: {Theme.SPACING_SM}px;")
        title.setAccessibleName("Battle Arena Title")
        title.setAccessibleDescription("Combat zone header")
        layout.addWidget(title)

        # Sprites container with better visual hierarchy
        sprites_container = QFrame()
        sprites_container.setFrameShape(QFrame.Shape.Box)
        sprites_container.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {Theme.BORDER.name()};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                background-color: {Theme.CARD.name()};
                padding: {Theme.SPACING_MD}px;
            }}
        """)

        sprites_layout = QHBoxLayout(sprites_container)
        sprites_layout.setSpacing(Theme.SPACING_MD)

        # Hero sprite with actual character images
        self.hero_sprite_label = QLabel()
        self.hero_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hero_sprite_label.setMinimumSize(80, 80)
        self.hero_sprite_label.setStyleSheet(f"""
            QLabel {{
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                background-color: {Theme.SECONDARY.name()};
            }}
        """)
        self.load_hero_sprite()  # Load hero sprite from assets
        self.hero_sprite_label.setToolTip("Your character's sprite during battle")
        self.hero_sprite_label.setAccessibleName("Hero sprite")
        self.hero_sprite_label.setAccessibleDescription("Representation of your character in battle")

        # VS indicator
        vs_label = QLabel("⚔️")
        vs_font = QFont()
        vs_font.setPointSize(24)
        vs_label.setFont(vs_font)
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vs_label.setAccessibleName("Versus indicator")

        # Enemy sprite with better formatting
        self.enemy_sprite_label = QLabel()
        self.enemy_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enemy_sprite_label.setMinimumSize(80, 80)
        self.enemy_sprite_label.setStyleSheet(f"""
            QLabel {{
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                background-color: {Theme.DESTRUCTIVE.name()};
            }}
        """)
        self.enemy_sprite_label.setToolTip("The enemy's sprite during battle")
        self.enemy_sprite_label.setAccessibleName("Enemy sprite")
        self.enemy_sprite_label.setAccessibleDescription("Representation of the enemy in battle")

        sprites_layout.addWidget(self.hero_sprite_label)
        sprites_layout.addWidget(vs_label, alignment=Qt.AlignmentFlag.AlignCenter)
        sprites_layout.addWidget(self.enemy_sprite_label)

        layout.addWidget(sprites_container)

        # Health Bars with better labels and styling
        health_bars_layout = QVBoxLayout()
        health_bars_layout.setSpacing(Theme.SPACING_SM)

        # Hero health section
        hero_health_layout = QVBoxLayout()
        hero_health_label = QLabel("❤️ Hero Health")
        hero_health_label.setStyleSheet(f"color: {Theme.FOREGROUND.name()}; font-weight: bold;")
        hero_health_label.setAccessibleName("Hero health section")
        hero_health_label.setAccessibleDescription("Hero's current health status")

        self.hero_combat_health_bar = StyledProgressBar(variant="health")
        self.hero_combat_health_bar.setAccessibleName("Hero health progress bar")
        self.hero_combat_health_bar.setAccessibleDescription("Visual indicator of hero's remaining health")

        hero_health_layout.addWidget(hero_health_label)
        hero_health_layout.addWidget(self.hero_combat_health_bar)
        health_bars_layout.addLayout(hero_health_layout)

        # Enemy health section
        enemy_health_layout = QVBoxLayout()
        enemy_health_label = QLabel("💀 Enemy Health")
        enemy_health_label.setStyleSheet(f"color: {Theme.FOREGROUND.name()}; font-weight: bold;")
        enemy_health_label.setAccessibleName("Enemy health section")
        enemy_health_label.setAccessibleDescription("Enemy's current health status")

        self.enemy_combat_health_bar = StyledProgressBar(variant="health")
        self.enemy_combat_health_bar.setAccessibleName("Enemy health progress bar")
        self.enemy_combat_health_bar.setAccessibleDescription("Visual indicator of enemy's remaining health")

        enemy_health_layout.addWidget(enemy_health_label)
        enemy_health_layout.addWidget(self.enemy_combat_health_bar)
        health_bars_layout.addLayout(enemy_health_layout)

        layout.addLayout(health_bars_layout)

        # Action Buttons with improved tooltips
        actions_layout = QGridLayout()
        actions_layout.setSpacing(Theme.SPACING_SM)

        self.attack_btn = StyledButton("⚔️ Attack", variant="primary")
        self.attack_btn.setToolTip("Attack the enemy with your weapon (A)")

        self.use_skill_btn = StyledButton("✨ Use Skill", variant="secondary")
        self.use_skill_btn.setToolTip("Use a special skill or spell (S)")

        self.use_item_btn = StyledButton("🧪 Use Item", variant="secondary")
        self.use_item_btn.setToolTip("Use a consumable item (I)")

        self.view_stats_btn = StyledButton("📖 View Stats", variant="secondary")
        self.view_stats_btn.setToolTip("View detailed enemy statistics and tactics (V)")

        # Add accessibility information for the view stats button
        self.view_stats_btn.setAccessibleName("View enemy stats button")
        self.view_stats_btn.setAccessibleDescription("View detailed enemy statistics and tactics (V)")

        self.run_btn = StyledButton("🏃 Run", variant="destructive")
        self.run_btn.setToolTip("Attempt to flee from battle (R)")

        actions_layout.addWidget(self.attack_btn, 0, 0)
        actions_layout.addWidget(self.use_skill_btn, 0, 1)
        actions_layout.addWidget(self.use_item_btn, 1, 0)
        actions_layout.addWidget(self.view_stats_btn, 1, 1)
        actions_layout.addWidget(self.run_btn, 2, 0, 1, 2)

        layout.addLayout(actions_layout)

        # Set layout on card and return
        card.setLayout(layout)
        return card

    def load_hero_sprite(self):
        """Load and display hero sprite image with proper Qt PySide scaling"""
        try:
            # Try to load Hero.png from assets
            hero_sprite_path = "assets/Hero.png"
            if os.path.exists(hero_sprite_path):
                self.hero_pixmap = QPixmap(hero_sprite_path)
                if not self.hero_pixmap.isNull():
                    # Don't scale immediately - wait for layout and resize events
                    # This follows Qt best practices for image scaling
                    self.rescale_hero_sprite()
                else:
                    print("Warning: Failed to load hero sprite pixmap")
                    self.hero_sprite_label.setText("🛡️ HERO")
            else:
                print(f"Warning: Hero sprite not found at {hero_sprite_path}")
                self.hero_sprite_label.setText("🛡️ HERO")
        except Exception as e:
            print(f"Warning: Error loading hero sprite: {e}")
            self.hero_sprite_label.setText("🛡️ HERO")

    def rescale_hero_sprite(self):
        """Properly scale hero sprite according to Qt PySide best practices"""
        if not hasattr(self, 'hero_pixmap') or self.hero_pixmap.isNull():
            return

        # Get the actual container dimensions for proper scaling
        # Use the parent container's size for more reliable calculations
        parent = self.hero_sprite_label.parentWidget()
        container_size = parent.size() if parent else self.hero_sprite_label.size()

        # Calculate target size based on container with proper padding
        # Use a reasonable size that's responsive but not too large
        available_width = max(60, min(140, container_size.width() - Theme.SPACING_MD * 2))
        available_height = max(60, min(140, container_size.height() - Theme.SPACING_MD * 2))

        target_size = min(available_width, available_height)
        target_size = max(target_size, 48)  # Minimum 48px for visibility

        try:
            # Scale with aspect ratio preserved - Qt PySide best practice
            scaled_pixmap = self.hero_pixmap.scaled(
                target_size, target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.hero_sprite_label.setPixmap(scaled_pixmap)
            self.hero_sprite_label.setScaledContents(False)
            self.hero_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print(f"Warning: Error scaling hero sprite: {e}")
            self.hero_sprite_label.setText("🛡️ HERO")

    def resizeEvent(self, event):
        """Handle resize events to rescale sprites properly"""
        super().resizeEvent(event)
        # Rescale hero sprite when container resizes - Qt best practice
        if hasattr(self, 'hero_sprite_label') and hasattr(self, 'hero_pixmap'):
            self.rescale_hero_sprite()

    def load_enemy_sprite(self, enemy):
        """Load and display enemy sprite based on enemy type"""
        try:
            # Map common enemy names to asset files
            enemy_sprite_map = {
                'Goblin': 'goblin.png',
                'Orc': 'Orc.png',
                'Golem': 'golem.png',
                'Mage': 'mage.png',
                'Rogue': 'rogue.png'
            }

            enemy_name = getattr(enemy, 'name', '').split(' ')[0]  # Get first word (type)
            sprite_file = enemy_sprite_map.get(enemy_name, 'goblin.png')  # Default to goblin
            enemy_sprite_path = f"assets/{sprite_file}"

            if os.path.exists(enemy_sprite_path):
                pixmap = QPixmap(enemy_sprite_path)
                if not pixmap.isNull():
                    # Get the actual size for proper scaling
                    target_size = self.enemy_sprite_label.size()
                    scaled_pixmap = pixmap.scaled(
                        target_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.enemy_sprite_label.setPixmap(scaled_pixmap)
                    self.enemy_sprite_label.setScaledContents(False)
                else:
                    print(f"Warning: Failed to load enemy sprite pixmap for {enemy_name}")
                    self.enemy_sprite_label.setText(f"👹 {getattr(enemy, 'name', 'ENEMY')}")
            else:
                print(f"Warning: Enemy sprite not found at {enemy_sprite_path}")
                self.enemy_sprite_label.setText(f"👹 {getattr(enemy, 'name', 'ENEMY')}")
        except Exception as e:
            print(f"Warning: Error loading enemy sprite: {e}")
            self.enemy_sprite_label.setText(f"👹 {getattr(enemy, 'name', 'ENEMY')}")

    def _create_log_card(self):
        card = Card()
        layout = QVBoxLayout()

        # Title with styling
        title = QLabel("📜 Battle Log")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.PRIMARY.name()}; margin-bottom: {Theme.SPACING_SM}px;")
        title.setAccessibleName("Battle Log Title")
        title.setAccessibleDescription("Combat events and messages header")
        layout.addWidget(title)

        # Battle log display with improved styling
        self.battle_log_display = QTextEdit()
        self.battle_log_display.setReadOnly(True)
        self.battle_log_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Theme.CARD.name()};
                color: {Theme.FOREGROUND.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                font-family: monospace;
                font-size: 12px;
                padding: {Theme.SPACING_SM}px;
            }}
        """)
        self.battle_log_display.setAccessibleName("Battle log")
        self.battle_log_display.setAccessibleDescription("Chronological list of combat events and messages")
        layout.addWidget(self.battle_log_display)

        card.setLayout(layout)
        return card

    def update_combat_ui(self, hero, enemy):
        if not hero or not enemy:
            return

        # Update hero health with animation
        hero_health_percent = int((hero.health / hero.max_health) * 100)
        self.hero_combat_health_bar.setValue(hero_health_percent)
        self.hero_combat_health_bar.setFormat(f"{hero.health} / {hero.max_health} HP")

        # Update enemy health with animation
        enemy_health_percent = int((enemy.health / enemy.max_health) * 100)
        self.enemy_combat_health_bar.setValue(enemy_health_percent)
        self.enemy_combat_health_bar.setFormat(f"{enemy.health} / {enemy.max_health} HP")

        # Load dynamic sprites for enemies
        self.load_enemy_sprite(enemy)

        self.update_battle_log_display()

    def add_battle_log_message(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > 20:
            self.battle_log = self.battle_log[-20:]
        self.update_battle_log_display()

    def update_battle_log_display(self):
        if hasattr(self, 'battle_log_display'):
            log_html = f"<div style='line-height: 1.6; color: {Theme.FOREGROUND.name()};'>"
            for msg in self.battle_log[-10:]:
                # Color messages based on content
                if any(word in msg.lower() for word in ["critical", "damage", "attack"]):
                    msg_color = Theme.PRIMARY.name()
                elif any(word in msg.lower() for word in ["defeated", "victory"]):
                    msg_color = Theme.ACCENT.name()
                elif any(word in msg.lower() for word in ["healing", "restored", "recovered"]):
                    msg_color = Theme.SECONDARY.name()
                else:
                    msg_color = Theme.MUTED_FOREGROUND.name()

                log_html += f"<div style='border-left: 3px solid {Theme.PRIMARY.name()}; padding-left: 8px; margin: 4px 0; color: {msg_color};'>{msg}</div>"
            log_html += "</div>"
            self.battle_log_display.setHtml(log_html)

            # Auto-scroll to bottom
            scrollbar = self.battle_log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
