# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QTextEdit)
from PySide6.QtCore import Qt
from ..widgets import Card, StyledButton, StyledProgressBar
from ..theme import Theme

class CombatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.battle_log = ["A wild enemy appears!", "Prepare for battle!"]
        self.init_ui()

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

        # Title
        title = QLabel("Battle Arena")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Sprites
        sprites_layout = QHBoxLayout()
        self.hero_sprite_label = QLabel("HERO")
        self.hero_sprite_label.setAlignment(Qt.AlignCenter)
        self.hero_sprite_label.setToolTip("Your character's sprite during battle")
        self.enemy_sprite_label = QLabel("ENEMY")
        self.enemy_sprite_label.setAlignment(Qt.AlignCenter)
        self.enemy_sprite_label.setToolTip("The enemy's sprite during battle")
        sprites_layout.addWidget(self.hero_sprite_label)
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignCenter)
        sprites_layout.addWidget(vs_label)
        sprites_layout.addWidget(self.enemy_sprite_label)
        layout.addLayout(sprites_layout)

        # Health Bars
        self.hero_combat_health_bar = StyledProgressBar(variant="health")
        self.enemy_combat_health_bar = StyledProgressBar(variant="health")
        layout.addWidget(self.hero_combat_health_bar)
        layout.addWidget(self.enemy_combat_health_bar)

        # Action Buttons
        actions_layout = QGridLayout()
        self.attack_btn = StyledButton("Attack", variant="primary")
        self.use_skill_btn = StyledButton("Use Skill", variant="secondary")
        self.use_item_btn = StyledButton("Use Item", variant="secondary")
        self.run_btn = StyledButton("Run", variant="destructive")
        actions_layout.addWidget(self.attack_btn, 0, 0)
        actions_layout.addWidget(self.use_skill_btn, 0, 1)
        actions_layout.addWidget(self.use_item_btn, 1, 0)
        actions_layout.addWidget(self.run_btn, 1, 1)
        layout.addLayout(actions_layout)

        card.setLayout(layout)
        return card

    def _create_log_card(self):
        card = Card()
        layout = QVBoxLayout()

        title = QLabel("Battle Log")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.battle_log_display = QTextEdit()
        self.battle_log_display.setReadOnly(True)
        layout.addWidget(self.battle_log_display)

        card.setLayout(layout)
        return card

    def update_combat_ui(self, hero, enemy):
        if not hero or not enemy:
            return

        self.hero_combat_health_bar.setValue(int((hero.health / hero.max_health) * 100))
        self.hero_combat_health_bar.setFormat(f"{hero.health} / {hero.max_health} HP")

        self.enemy_combat_health_bar.setValue(int((enemy.health / enemy.max_health) * 100))
        self.enemy_combat_health_bar.setFormat(f"{enemy.health} / {enemy.max_health} HP")

        # Update sprites (if you have them)
        # self.hero_sprite_label.setPixmap(QPixmap(hero.sprite_path).scaled(100, 100, Qt.KeepAspectRatio))
        # self.enemy_sprite_label.setPixmap(QPixmap(enemy.sprite_path).scaled(100, 100, Qt.KeepAspectRatio))

        self.update_battle_log_display()

    def add_battle_log_message(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > 20:
            self.battle_log = self.battle_log[-20:]
        self.update_battle_log_display()

    def update_battle_log_display(self):
        if hasattr(self, 'battle_log_display'):
            log_html = "<div style='line-height: 1.6;'>"
            for msg in self.battle_log[-10:]:
                log_html += f"<div style='border-left: 3px solid #dc3545; padding-left: 8px; margin: 4px 0;'>{msg}</div>"
            log_html += "</div>"
            self.battle_log_display.setHtml(log_html)
