# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from ..custom_widgets import AnimatedProgressBar, ScalablePixmapLabel

class CombatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        page = self
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Top section for combatants
        combatants_layout = QHBoxLayout()

        # Hero Side
        hero_combat_layout = QVBoxLayout()
        hero_combat_layout.setAlignment(Qt.AlignCenter)
        
        self.hero_combat_name = QLabel("Hero")
        self.hero_combat_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #61afef;")
        self.hero_combat_name.setAlignment(Qt.AlignCenter)
        
        self.hero_sprite_label = ScalablePixmapLabel()
        self.hero_sprite_label.setAlignment(Qt.AlignCenter)
        
        self.hero_combat_health_bar = AnimatedProgressBar()
        self.hero_combat_health_bar.setMaximumHeight(20)
        self.hero_combat_health_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #98c379; }
        """)

        self.hero_combat_mana_bar = AnimatedProgressBar()
        self.hero_combat_mana_bar.setMaximumHeight(20)
        self.hero_combat_mana_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #61afef; }
        """)

        hero_combat_layout.addWidget(self.hero_combat_name)
        hero_combat_layout.addWidget(self.hero_sprite_label)
        hero_combat_layout.addWidget(self.hero_combat_health_bar)
        hero_combat_layout.addWidget(self.hero_combat_mana_bar)
        combatants_layout.addLayout(hero_combat_layout)

        # VS Label
        vs_label = QLabel("VS")
        vs_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e5c07b;")
        vs_label.setAlignment(Qt.AlignCenter)
        combatants_layout.addWidget(vs_label)

        # Enemy Side
        enemy_combat_layout = QVBoxLayout()
        enemy_combat_layout.setAlignment(Qt.AlignCenter)

        self.enemy_combat_name = QLabel("Enemy")
        self.enemy_combat_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #e06c75;")
        self.enemy_combat_name.setAlignment(Qt.AlignCenter)

        self.enemy_sprite_label = ScalablePixmapLabel()
        self.enemy_sprite_label.setAlignment(Qt.AlignCenter)

        self.enemy_combat_health_bar = AnimatedProgressBar()
        self.enemy_combat_health_bar.setMaximumHeight(20)
        self.enemy_combat_health_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #e06c75; }
        """)

        enemy_combat_layout.addWidget(self.enemy_combat_name)
        enemy_combat_layout.addWidget(self.enemy_sprite_label)
        enemy_combat_layout.addWidget(self.enemy_combat_health_bar)
        combatants_layout.addLayout(enemy_combat_layout)

        layout.addLayout(combatants_layout)
        layout.addStretch()

        # Combat buttons
        combat_buttons_layout = QGridLayout()
        combat_buttons_layout.setSpacing(10)

        self.attack_btn = QPushButton("⚔️ Attack")
        self.attack_btn.setObjectName("attack_btn")
        self.attack_btn.setToolTip("Strike the enemy with your weapon!")
        self.attack_btn.setMinimumHeight(60)

        self.use_skill_btn = QPushButton("✨ Use Skill")
        self.use_skill_btn.setObjectName("use_skill_btn")
        self.use_skill_btn.setToolTip("Use a special skill or magic spell")
        self.use_skill_btn.setMinimumHeight(60)
        self.use_skill_btn.setStyleSheet("""
            QPushButton#use_skill_btn {
                background-color: #282c34;
                color: #c678dd;
                border: 1px solid #c678dd;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton#use_skill_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)

        self.use_item_btn = QPushButton("🧪 Use Item")
        self.use_item_btn.setObjectName("use_item_btn")
        self.use_item_btn.setToolTip("Use a consumable item from your inventory")
        self.use_item_btn.setMinimumHeight(60)
        self.use_item_btn.setStyleSheet("""
            QPushButton#use_item_btn {
                background-color: #282c34;
                color: #98c379;
                border: 1px solid #98c379;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton#use_item_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)

        self.run_btn = QPushButton("🏃 Run")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.setToolTip("Attempt to escape the battle")
        self.run_btn.setMinimumHeight(60)

        for btn in [self.attack_btn, self.use_skill_btn, self.use_item_btn, self.run_btn]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(5)
            shadow.setColor(QColor(0, 0, 0, 150))
            btn.setGraphicsEffect(shadow)

        combat_buttons_layout.addWidget(self.attack_btn, 0, 0)
        combat_buttons_layout.addWidget(self.use_skill_btn, 0, 1)
        combat_buttons_layout.addWidget(self.use_item_btn, 1, 0)
        combat_buttons_layout.addWidget(self.run_btn, 1, 1)

        layout.addLayout(combat_buttons_layout)