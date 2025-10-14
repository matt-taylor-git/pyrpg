# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QGroupBox, QGraphicsDropShadowEffect)
from PySide6.QtGui import QColor
from ..custom_widgets import AnimatedProgressBar

class AdventurePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Enhanced Stats Panel with Progress Bars
        self.stats_group = QGroupBox("\u2694\ufe0f Hero Status")
        self.stats_group.setMinimumWidth(300)
        self.stats_layout = QVBoxLayout()

        # Hero name and level - Enhanced typography
        name_layout = QHBoxLayout()
        self.name_label = QLabel("Name: Not created")
        self.name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #61afef;
        """)
        self.level_label = QLabel("Level: -")
        self.level_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #98c379;
            background-color: #21252b;
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()
        name_layout.addWidget(self.level_label)
        self.stats_layout.addLayout(name_layout)

        # Health bar - Professional styling
        health_layout = QHBoxLayout()
        health_label = QLabel("\u2764\ufe0f Health:")
        health_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #abb2bf;")
        health_layout.addWidget(health_label)
        self.health_bar = AnimatedProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(100)
        self.health_bar.setFormat("100/100 HP")
        self.health_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                height: 26px;
                background-color: #21252b;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #98c379;
                width: 10px;
                margin: 0.5px;
            }
        """)
        health_layout.addWidget(self.health_bar)
        self.stats_layout.addLayout(health_layout)

        # Experience bar - Professional blue theme
        exp_layout = QHBoxLayout()
        exp_label = QLabel("\u2b50\ufe0f Experience:")
        exp_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #abb2bf;")
        exp_layout.addWidget(exp_label)
        self.exp_bar = AnimatedProgressBar()
        self.exp_bar.setRange(0, 100)
        self.exp_bar.setValue(0)
        self.exp_bar.setFormat("0/100 XP")
        self.exp_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                height: 26px;
                background-color: #21252b;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #61afef;
                width: 10px;
                margin: 0.5px;
            }
        """)
        exp_layout.addWidget(self.exp_bar)
        self.stats_layout.addLayout(exp_layout)

        # Combat stats grid - Enhanced styling
        combat_stats_layout = QGridLayout()
        combat_stats_layout.setSpacing(8)

        self.attack_label = QLabel("\u2694\ufe0f Attack: -")
        self.attack_label.setObjectName("attack_label")
        self.attack_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.attack_label, 0, 0)

        self.defense_label = QLabel("\U0001f6e1\ufe0f Defense: -")
        self.defense_label.setObjectName("defense_label")
        self.defense_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.defense_label, 0, 1)

        self.gold_label = QLabel("\U0001f4b0 Gold: -")
        self.gold_label.setObjectName("gold_label")
        self.gold_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.gold_label, 1, 0)

        self.inventory_label = QLabel("\U0001f392 Inventory: Empty")
        self.inventory_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
            color: #abb2bf;
        """)
        combat_stats_layout.addWidget(self.inventory_label, 1, 1)

        self.stats_layout.addLayout(combat_stats_layout)

        # Equipment display - Professional card
        equipment_group = QGroupBox("\u2694\ufe0f Equipment")
        equipment_layout = QVBoxLayout()

        self.weapon_label = QLabel("\U0001f5e1\ufe0f Weapon: None")
        self.weapon_label.setStyleSheet("font-size: 12px; color: #e06c75; padding: 4px;")
        self.armor_label = QLabel("\U0001f6e1\ufe0f Armor: None")
        self.armor_label.setStyleSheet("font-size: 12px; color: #61afef; padding: 4px;")
        self.accessory_label = QLabel("\U0001f48d Accessory: None")
        self.accessory_label.setStyleSheet("font-size: 12px; color: #c678dd; padding: 4px;")

        equipment_layout.addWidget(self.weapon_label)
        equipment_layout.addWidget(self.armor_label)
        equipment_layout.addWidget(self.accessory_label)

        equipment_group.setLayout(equipment_layout)
        self.stats_layout.addWidget(equipment_group)

        self.stats_group.setLayout(self.stats_layout)
        layout.addWidget(self.stats_group)

        layout.addStretch()

        # Action buttons
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(10)

        self.explore_btn = QPushButton("\U0001f50d Explore")
        self.explore_btn.setObjectName("explore_btn")
        self.explore_btn.setToolTip("Explore the wilderness and encounter enemies!")
        self.explore_btn.setMinimumHeight(50)

        self.rest_btn = QPushButton("\U0001f634 Rest")
        self.rest_btn.setObjectName("rest_btn")
        self.rest_btn.setToolTip("Rest to fully recover your health")
        self.rest_btn.setMinimumHeight(50)

        self.quit_btn = QPushButton("\u274c Quit")
        self.quit_btn.setObjectName("quit_btn")
        self.quit_btn.setToolTip("Exit the game")
        self.quit_btn.setMinimumHeight(50)

        # Add shadow effects to action buttons for depth
        for btn in [self.explore_btn, self.rest_btn, self.quit_btn]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 0, 0, 120))
            btn.setGraphicsEffect(shadow)

        self.button_layout.addWidget(self.explore_btn, 0, 0)
        self.button_layout.addWidget(self.rest_btn, 0, 1)
        self.button_layout.addWidget(self.quit_btn, 1, 0, 1, 2)

        layout.addLayout(self.button_layout)