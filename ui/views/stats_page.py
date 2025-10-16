# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton)
from PySide6.QtCore import Qt
from ..widgets import Card, StyledProgressBar, StyledButton
from ..theme import Theme

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hero = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Left Column: Character Info
        char_info_card = self._create_character_info_card()
        main_layout.addWidget(char_info_card, 1)

        # Right Column: Stats Allocation
        stats_alloc_card = self._create_stats_allocation_card()
        main_layout.addWidget(stats_alloc_card, 1)

    def _create_character_info_card(self):
        card = Card()
        layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Character Info")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.level_badge = QLabel("Level 1")
        self.level_badge.setStyleSheet("font-size: 14px; color: #9a96a5;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.level_badge)
        layout.addLayout(header_layout)

        # Avatar and Name
        self.char_name_label = QLabel("Hero")
        self.char_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.char_name_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.char_name_label.setToolTip("Your character's name and level")
        layout.addWidget(self.char_name_label)

        # Progress Bars
        self.exp_bar = StyledProgressBar(variant="experience")
        self.health_bar = StyledProgressBar(variant="health")
        self.mana_bar = StyledProgressBar(variant="mana")
        layout.addWidget(QLabel("Experience"))
        layout.addWidget(self.exp_bar)
        layout.addWidget(QLabel("Health"))
        layout.addWidget(self.health_bar)
        layout.addWidget(QLabel("Mana"))
        layout.addWidget(self.mana_bar)

        # Gold
        self.gold_label = QLabel("Gold: 0")
        self.gold_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e5c07b;")
        layout.addWidget(self.gold_label)

        card.setLayout(layout)
        return card

    def _create_stats_allocation_card(self):
        card = Card()
        layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Character Stats")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.points_badge = QLabel("0 Points Available")
        self.points_badge.setStyleSheet("font-size: 14px; color: #9a96a5;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.points_badge)
        layout.addLayout(header_layout)

        # Stat Rows
        self.strength_row, self.strength_value, self.strength_plus_btn = self._create_stat_row("Strength", "Increases physical damage")
        self.defense_row, self.defense_value, self.defense_plus_btn = self._create_stat_row("Defense", "Reduces damage taken")
        self.magic_row, self.magic_value, self.magic_plus_btn = self._create_stat_row("Magic", "Enhances spell power")
        self.speed_row, self.speed_value, self.speed_plus_btn = self._create_stat_row("Speed", "Determines turn order")

        layout.addWidget(self.strength_row)
        layout.addWidget(self.defense_row)
        layout.addWidget(self.magic_row)
        layout.addWidget(self.speed_row)

        card.setLayout(layout)
        return card

    def _create_stat_row(self, name, description):
        row_widget = QWidget()
        row_layout = QGridLayout(row_widget)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold;")
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #9a96a5;")

        value_label = QLabel("0")
        value_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        plus_button = StyledButton("+", size="sm")

        row_layout.addWidget(name_label, 0, 0)
        row_layout.addWidget(value_label, 0, 1, 2, 1, Qt.AlignmentFlag.AlignRight)
        row_layout.addWidget(plus_button, 0, 2, 2, 1, Qt.AlignmentFlag.AlignRight)
        row_layout.addWidget(desc_label, 1, 0)

        return row_widget, value_label, plus_button

    def update_stats_display(self, hero=None):
        if hero:
            self.hero = hero
        if not self.hero:
            return

        self.level_badge.setText(f"Level {self.hero.level}")
        self.char_name_label.setText(self.hero.name)

        exp_percent = int((self.hero.experience / self.hero.experience_to_level) * 100) if self.hero.experience_to_level > 0 else 0
        self.exp_bar.setValue(exp_percent)
        self.exp_bar.setFormat(f"{self.hero.experience} / {self.hero.experience_to_level} XP")

        health_percent = int((self.hero.health / self.hero.max_health) * 100) if self.hero.max_health > 0 else 0
        self.health_bar.setValue(health_percent)
        self.health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health} HP")

        mana_percent = int((self.hero.mana / self.hero.max_mana) * 100) if self.hero.max_mana > 0 else 0
        self.mana_bar.setValue(mana_percent)
        self.mana_bar.setFormat(f"{self.hero.mana} / {self.hero.max_mana} MP")

        self.gold_label.setText(f"Gold: {self.hero.gold}")

        self.points_badge.setText(f"{self.hero.stat_points} Points Available")
        
        self.strength_value.setText(str(self.hero.strength))
        self.defense_value.setText(str(self.hero.defense))
        self.magic_value.setText(str(self.hero.intelligence))
        self.speed_value.setText(str(self.hero.dexterity))

        can_upgrade = self.hero.stat_points > 0
        self.strength_plus_btn.setEnabled(can_upgrade)
        self.defense_plus_btn.setEnabled(can_upgrade)
        self.magic_plus_btn.setEnabled(can_upgrade)
        self.speed_plus_btn.setEnabled(can_upgrade)
