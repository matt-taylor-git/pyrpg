# -*- coding: utf-8 -*-
"""
Monster stats viewer page for PyRPG Adventure
Displays detailed information about enemies for player reference
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                               QGroupBox, QScrollArea, QTextEdit, QListWidget,
                               QListWidgetItem, QGridLayout)
from PySide6.QtCore import Qt
from ..theme import Theme
from ..widgets import Card
from game.models import Enemy


class MonsterStatsViewer(QWidget):
    """Comprehensive monster stats viewer displaying detailed enemy information."""

    def __init__(self, parent=None, enemy=None):
        super().__init__(parent)
        self.current_enemy = enemy or Enemy("Sample Monster", 1, "normal")
        self.init_ui()

    def init_ui(self):
        """Initialize the monster stats viewer UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.SPACING_LG, Theme.SPACING_LG,
                                      Theme.SPACING_LG, Theme.SPACING_LG)
        main_layout.setSpacing(Theme.SPACING_MD)

        # Monster header with image and basic info
        self.create_header_section(main_layout)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Theme.BACKGROUND};
            }}
            QScrollBar:vertical {{
                width: 12px;
                background: {Theme.CARD};
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.MUTED};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(Theme.SPACING_MD)

        # Combat stats section
        self.create_combat_stats_section(content_layout)

        # Physical traits section
        self.create_physical_traits_section(content_layout)

        # Elemental properties section
        self.create_elemental_section(content_layout)

        # Abilities section
        self.create_abilities_section(content_layout)

        # Behavior section
        self.create_behavior_section(content_layout)

        # Miscellaneous info
        self.create_misc_info_section(content_layout)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Load initial enemy data
        self.display_enemy_stats(self.current_enemy)

    def create_header_section(self, parent_layout):
        """Create the header section with monster image and basic info."""
        header_card = Card()
        header_layout = QHBoxLayout()
        header_layout.setSpacing(Theme.SPACING_LG)

        # Monster image placeholder
        image_frame = QFrame()
        image_frame.setFixedSize(100, 100)
        image_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.MUTED};
                border: 2px solid {Theme.BORDER};
                border-radius: 8px;
            }}
        """)

        image_label = QLabel("👹")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("font-size: 48px; color: #dc3545;")

        frame_layout = QVBoxLayout(image_frame)
        frame_layout.addWidget(image_label)

        header_layout.addWidget(image_frame)

        # Monster info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(Theme.SPACING_XS)

        self.name_label = QLabel("Monster Name")
        self.name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: bold;
                color: {Theme.FOREGROUND};
                text-decoration: underline;
            }}
        """)
        info_layout.addWidget(self.name_label)

        self.level_label = QLabel("Level 1 - Rarity")
        self.level_label.setStyleSheet(f"color: {Theme.FOREGROUND}; font-size: 14px;")
        info_layout.addWidget(self.level_label)

        self.type_size_label = QLabel("Type - Size Category")
        self.type_size_label.setStyleSheet(f"color: {Theme.MUTED_FOREGROUND};")
        info_layout.addWidget(self.type_size_label)

        info_layout.addStretch()
        header_layout.addLayout(info_layout)

        header_layout.addStretch()
        header_card.setLayout(header_layout)
        parent_layout.addWidget(header_card)

    def create_combat_stats_section(self, parent_layout):
        """Create combat statistics section."""
        section = self.create_stat_section("⚔️ Combat Statistics")

        grid = QGridLayout()
        grid.setSpacing(Theme.SPACING_MD)

        # Health
        grid.addWidget(self.create_stat_label("Health:"), 0, 0)
        self.health_label = self.create_value_label("???/???")
        grid.addWidget(self.health_label, 0, 1)

        # Physical Attack
        grid.addWidget(self.create_stat_label("Physical Attack:"), 1, 0)
        self.attack_range_label = self.create_value_label("???-???")
        grid.addWidget(self.attack_range_label, 1, 1)

        # Magic Attack
        grid.addWidget(self.create_stat_label("Magic Attack:"), 2, 0)
        self.magic_range_label = self.create_value_label("???-???")
        grid.addWidget(self.magic_range_label, 2, 1)

        # Defense
        grid.addWidget(self.create_stat_label("Defense:"), 3, 0)
        self.defense_label = self.create_value_label("???")
        grid.addWidget(self.defense_label, 3, 1)

        # Attack Speed & Crit
        grid.addWidget(self.create_stat_label("Attack Speed:"), 4, 0)
        self.speed_crit_label = self.create_value_label("??? (???% crit)")
        grid.addWidget(self.speed_crit_label, 4, 1)

        # Armor Type
        grid.addWidget(self.create_stat_label("Armor Type:"), 5, 0)
        self.armor_label = self.create_value_label("???")
        grid.addWidget(self.armor_label, 5, 1)

        # Special attacks
        grid.addWidget(self.create_stat_label("Special Attacks:"), 0, 2, Qt.AlignmentFlag.AlignTop)
        self.special_attacks_label = self.create_value_label("None")
        self.special_attacks_label.setWordWrap(True)
        grid.addWidget(self.special_attacks_label, 0, 3, 3, 1)

        # Combat style
        grid.addWidget(self.create_stat_label("Combat Style:"), 3, 2)
        self.combat_style_label = self.create_value_label("???")
        grid.addWidget(self.combat_style_label, 3, 3)

        # XP/Gold rewards
        grid.addWidget(self.create_stat_label("Rewards:"), 4, 2)
        self.rewards_label = self.create_value_label("??? XP, ??? Gold")
        grid.addWidget(self.rewards_label, 4, 3)

        # Threat level
        grid.addWidget(self.create_stat_label("Threat Level:"), 5, 2)
        self.threat_label = self.create_value_label("???")
        grid.addWidget(self.threat_label, 5, 3)

        section.layout().addLayout(grid)
        parent_layout.addWidget(section)

    def create_physical_traits_section(self, parent_layout):
        """Create physical traits section."""
        section = self.create_stat_section("🏋️ Physical Traits")

        content_layout = QHBoxLayout()
        content_layout.setSpacing(Theme.SPACING_LG)

        # Size and Speed
        traits_layout = QVBoxLayout()
        traits_layout.setSpacing(Theme.SPACING_SM)

        traits_layout.addWidget(self.create_stat_label("Size Category:"))
        self.size_label = self.create_value_label("???")
        traits_layout.addWidget(self.size_label)

        traits_layout.addWidget(self.create_stat_label("Speed Rating:"))
        self.speed_label = self.create_value_label("???")
        traits_layout.addWidget(self.speed_label)

        traits_layout.addWidget(self.create_stat_label("Movement Speed:"))
        self.movement_label = self.create_value_label("???x")
        traits_layout.addWidget(self.movement_label)

        content_layout.addLayout(traits_layout)

        # Intelligence
        traits_layout.addWidget(self.create_stat_label("Intelligence:"))
        self.intelligence_label = self.create_value_label("???")
        traits_layout.addWidget(self.intelligence_label)

        # Habitat
        habitat_layout = QVBoxLayout()
        habitat_layout.addWidget(self.create_stat_label("Habitat:"))
        self.habitat_label = QLabel("???")
        self.habitat_label.setWordWrap(True)
        self.habitat_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                font-size: 12px;
                background-color: {Theme.MUTED};
                padding: {Theme.SPACING_XS}px;
                border-radius: 4px;
                max-width: 300px;
            }}
        """)
        habitat_layout.addWidget(self.habitat_label)

        content_layout.addLayout(habitat_layout)
        content_layout.addStretch()

        section.layout().addLayout(content_layout)
        parent_layout.addWidget(section)

    def create_elemental_section(self, parent_layout):
        """Create elemental properties section."""
        section = self.create_stat_section("🔮 Elemental Properties")

        content_layout = QVBoxLayout()
        content_layout.setSpacing(Theme.SPACING_SM)

        # Elemental Type & Strength
        elemental_layout = QHBoxLayout()
        elemental_layout.addWidget(self.create_stat_label("Elemental Type:"))
        self.elemental_type_label = self.create_value_label("None (Strength: 0)")
        elemental_layout.addWidget(self.elemental_type_label)
        elemental_layout.addStretch()
        content_layout.addLayout(elemental_layout)

        # Weaknesses
        weaknesses_layout = QHBoxLayout()
        weaknesses_layout.addWidget(self.create_stat_label("Weaknesses:"))
        self.weaknesses_label = QLabel("None")
        self.weaknesses_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.DESTRUCTIVE};
                background-color: rgba(210, 58, 26, 0.1);
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        weaknesses_layout.addWidget(self.weaknesses_label)
        weaknesses_layout.addStretch()
        content_layout.addLayout(weaknesses_layout)

        # Resistances
        resistances_layout = QHBoxLayout()
        resistances_layout.addWidget(self.create_stat_label("Resistances:"))
        self.resistances_label = QLabel("None")
        self.resistances_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.ACCENT};
                background-color: rgba(140, 82, 255, 0.1);
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        resistances_layout.addWidget(self.resistances_label)
        resistances_layout.addStretch()
        content_layout.addLayout(resistances_layout)

        # Immunities
        immunities_layout = QHBoxLayout()
        immunities_layout.addWidget(self.create_stat_label("Immunities:"))
        self.immunities_label = QLabel("None")
        self.immunities_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.PRIMARY};
                background-color: rgba(102, 102, 255, 0.1);
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        immunities_layout.addWidget(self.immunities_label)
        immunities_layout.addStretch()
        content_layout.addLayout(immunities_layout)

        section.layout().addLayout(content_layout)
        parent_layout.addWidget(section)

    def create_abilities_section(self, parent_layout):
        """Create abilities and passive skills section."""
        section = self.create_stat_section("✨ Abilities & Skills")

        content_layout = QVBoxLayout()
        content_layout.setSpacing(Theme.SPACING_MD)

        # Special Abilities (initially hidden)
        special_section = QVBoxLayout()
        special_section.addWidget(self.create_stat_label("Special Abilities:"))

        self.special_abilities_text = QLabel("Loading...")
        self.special_abilities_text.setWordWrap(True)
        self.special_abilities_text.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                background-color: {Theme.MUTED};
                padding: {Theme.SPACING_SM}px;
                border-radius: 4px;
                font-size: 11px;
                line-height: 1.4;
            }}
        """)
        special_section.addWidget(self.special_abilities_text)
        content_layout.addLayout(special_section)

        # Passive Abilities
        passive_section = QVBoxLayout()
        passive_section.addWidget(self.create_stat_label("Passive Abilities:"))
        self.passive_abilities_label = QLabel("Basic combat training")
        self.passive_abilities_label.setWordWrap(True)
        self.passive_abilities_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                background-color: {Theme.MUTED};
                padding: {Theme.SPACING_SM}px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        passive_section.addWidget(self.passive_abilities_label)
        content_layout.addLayout(passive_section)

        section.layout().addLayout(content_layout)
        parent_layout.addWidget(section)

    def create_behavior_section(self, parent_layout):
        """Create behavior patterns section."""
        section = self.create_stat_section("🧠 Behavior Patterns")

        behavior_text = QLabel("Loading behavior data...")
        behavior_text.setWordWrap(True)
        behavior_text.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                background-color: {Theme.MUTED};
                padding: {Theme.SPACING_SM}px;
                border-radius: 4px;
                font-size: 11px;
                line-height: 1.4;
            }}
        """)
        self.behavior_patterns_label = behavior_text

        section.layout().addWidget(behavior_text)
        parent_layout.addWidget(section)

    def create_misc_info_section(self, parent_layout):
        """Create miscellaneous information section."""
        section = self.create_stat_section("📚 Additional Information")

        content_layout = QHBoxLayout()
        content_layout.setSpacing(Theme.SPACING_LG)

        # Description
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(self.create_stat_label("Description:"))
        self.description_label = QLabel("Loading...")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                background-color: {Theme.MUTED};
                padding: {Theme.SPACING_SM}px;
                border-radius: 4px;
                font-size: 11px;
                line-height: 1.4;
                max-width: 400px;
            }}
        """)
        desc_layout.addWidget(self.description_label)
        content_layout.addLayout(desc_layout)

        # Loot
        loot_layout = QVBoxLayout()
        loot_layout.addWidget(self.create_stat_label("Common Loot:"))
        self.loot_label = QLabel("Unknown")
        self.loot_label.setWordWrap(True)
        self.loot_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.SECONDARY};
                background-color: rgba(53, 46, 77, 0.1);
                padding: {Theme.SPACING_SM}px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        loot_layout.addWidget(self.loot_label)
        content_layout.addLayout(loot_layout)

        content_layout.addStretch()
        section.layout().addLayout(content_layout)
        parent_layout.addWidget(section)

    def create_stat_section(self, title):
        """Create a standardized stat section group box."""
        section = QGroupBox(title)
        section.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {Theme.BORDER};
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
                color: {Theme.FOREGROUND};
                background-color: {Theme.CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                color: #dc3545;
                font-size: 14px;
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(Theme.SPACING_MD, Theme.SPACING_MD,
                                 Theme.SPACING_MD, Theme.SPACING_MD)
        layout.setSpacing(Theme.SPACING_SM)

        return section

    def create_stat_label(self, text):
        """Create a standardized stat label."""
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.FOREGROUND};
                font-weight: bold;
                font-size: 12px;
            }}
        """)
        return label

    def create_value_label(self, text):
        """Create a standardized value label."""
        label = QLabel(text)
        label.setStyleSheet(f"color: {Theme.FOREGROUND}; font-size: 12px;")
        return label

    def display_enemy_stats(self, enemy):
        """Display detailed stats for the given enemy."""
        if not enemy:
            return

        self.current_enemy = enemy

        # Header information
        self.name_label.setText(enemy.name)
        self.level_label.setText(f"Level {enemy.level} - {enemy.rarity.title()}")

        # Type and size
        enemy_type_display = enemy.enemy_type.title() if enemy.enemy_type != 'normal' else 'Common'
        self.type_size_label.setText(f"{enemy_type_display} - {enemy.size_category.title()}")

        # Combat stats
        self.health_label.setText(f"{enemy.health}/{enemy.max_health}")
        self.attack_range_label.setText(f"{enemy.attack_min}-{enemy.attack_max}")
        self.magic_range_label.setText(f"{enemy.magic_attack_min}-{enemy.magic_attack_max}")
        self.defense_label.setText(str(enemy.defense))
        self.speed_crit_label.setText(f"{enemy.attack_speed:.1f}x speed ({enemy.crit_chance:.0f}% crit)")
        self.armor_label.setText(enemy.armor_type.title())

        # Special attacks
        special_attacks_text = ", ".join(enemy.special_attacks) if enemy.special_attacks else "None"
        self.special_attacks_label.setText(special_attacks_text)
        self.combat_style_label.setText(enemy.combat_style.title())
        self.rewards_label.setText(f"{enemy.exp_reward} XP, {enemy.gold_reward} Gold")
        self.threat_label.setText(enemy.threat_level.title())

        # Physical traits
        self.size_label.setText(enemy.size_category.title())
        self.speed_label.setText(enemy.speed_rating.title())
        self.movement_label.setText(f"{enemy.movement_speed:.1f}x")
        self.intelligence_label.setText(enemy.intelligence.title())
        self.habitat_label.setText(enemy.habitat or "Unknown")

        # Elemental properties
        elemental_strength = f" (Strength: {enemy.elemental_strength})" if enemy.elemental_strength > 0 else ""
        self.elemental_type_label.setText(f"{enemy.elemental_type.title()}{elemental_strength}")
        self.weaknesses_label.setText(", ".join(enemy.elemental_weakness).title() or "None")
        self.resistances_label.setText(", ".join(enemy.elemental_resistance).title() or "None")
        self.immunities_label.setText(", ".join(enemy.elemental_immunity).title() or "None")

        # Abilities
        if enemy.special_abilities:
            abilities_text = ""
            for ability in enemy.special_abilities:
                abilities_text += f"• {ability['name']}: {ability['description']}\n"
            self.special_abilities_text.setText(abilities_text.strip())

        passive_text = ", ".join(enemy.passive_abilities) if enemy.passive_abilities else "Basic combat training"
        self.passive_abilities_label.setText(passive_text)

        # Behavior patterns
        behavior_text = "\n".join([f"• {pattern}" for pattern in enemy.behavior_patterns]) if enemy.behavior_patterns else "Standard enemy behavior patterns."
        self.behavior_patterns_label.setText(behavior_text)

        # Misc info
        self.description_label.setText(enemy.description)
        loot_text = ", ".join(enemy.loot_drops) if enemy.loot_drops else "Nothing special"
        self.loot_label.setText(loot_text)

    def set_enemy(self, enemy):
        """Set a new enemy to display."""
        self.display_enemy_stats(enemy)
