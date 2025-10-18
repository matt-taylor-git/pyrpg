# -*- coding: utf-8 -*-
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTextEdit,
                               QGridLayout, QGroupBox, QInputDialog, QMessageBox,
                               QProgressBar, QListWidget, QListWidgetItem, QGraphicsDropShadowEffect,
                               QStackedWidget, QScrollArea, QFrame, QLineEdit, QSizePolicy, QTabWidget)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPropertyAnimation, QEasingCurve, QPoint, Property
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap, QKeySequence
import random
import time
from game.models import Hero, Enemy
from game.game import random_encounter, get_shop_items, apply_item_effects, handle_player_turn, handle_enemy_turn
from ui_components import ItemCard, ItemSelectionOverlay
from .constants import GameState, PageIndex
from .custom_widgets import AnimatedProgressBar, ShadowedProgressBar, ScalablePixmapLabel
from .views.adventure_page import AdventurePage
from .views.stats_page import StatsPage
from .views.inventory_page import InventoryPage
from .views.shop_page import ShopPage
from .views.combat_page import CombatPage
from .views.new_game_view import NewGameView
from .views.character_customization_page import CharacterCustomizationPage
from .components import AchievementSystem
from .controllers import (
    AdventureController,
    CombatController,
    ShopController,
    InventoryController,
    StatsController,
    CustomizationController,
    MonsterStatsController
)
from .components.log_display import LogDisplay
from .theme import Theme

from .widgets import Card, StyledButton



class RPGGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hero = None
        self.current_state = GameState.MENU
        self.current_enemy = None
        self.animations = []  # Store active animations
        self.current_view_index = 0  # Track current tab for transitions

        self.new_game_view = NewGameView()
        self.new_game_view.character_created.connect(self.start_new_game)
        self.setCentralWidget(self.new_game_view)

    def shake_widget(self, widget, duration=200, magnitude=10):
        """Create a shake animation for a widget using AnimationFactory"""
        from .widgets import AnimationFactory
        animation = AnimationFactory.shake_animation(widget, duration, magnitude)
        animation.start()
        self.animations.append(animation)  # Keep reference

    def flash_widget(self, widget, color, duration=300):
        """Create a flash effect using AnimationFactory"""
        from .widgets import AnimationFactory
        AnimationFactory.color_flash_animation(widget, color, duration)

    def resizeEvent(self, event):
        """Handle window resize to scale font size."""
        super().resizeEvent(event)
        # Scale font size of the log display based on window height - only if it exists
        if hasattr(self, 'log_display') and self.log_display:
            font_size = max(8, min(18, int(self.height() / 50)))
            font = self.log_display.font()
            font.setPointSize(font_size)
            self.log_display.setFont(font)


    def setup_game_interface(self):
        """Initialize the enhanced user interface with modern design"""
        self.setWindowTitle("PyRPG Adventure")
        self.resize(1200, 750)
        self.setMinimumSize(800, 600)

        # Remove splash screen and setup game interface components
        old_central = self.takeCentralWidget()
        if old_central:
            old_central.setParent(None)


        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Game log (top section) - Using modern LogDisplay component
        self.log_display = LogDisplay(max_entries=20)
        self.add_entry_to_log("Welcome to PyRPG Adventure! Type 'help' for commands.", "info")
        self.main_layout.addWidget(self.log_display, 1) # Add with stretch factor

        # Create tab widget (horizontal tabs at top, like React sample)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setAccessibleName("Main navigation tabs")
        self.tab_widget.setAccessibleDescription("Navigate between different game sections")
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {Theme.BACKGROUND.name()};
            }}
            QTabBar::tab {{
                background-color: {Theme.CARD.name()};
                color: {Theme.MUTED_FOREGROUND.name()};
                padding: {Theme.SPACING_MD}px {Theme.SPACING_LG}px;
                border: none;
                border-bottom: 3px solid transparent;
                font-size: 14px;
                font-weight: {Theme.FONT_WEIGHT_MEDIUM};
                margin-right: {Theme.SPACING_XS}px;
                border-radius: {Theme.BORDER_RADIUS_SM}px  {Theme.BORDER_RADIUS_SM}px 0 0;
            }}
            QTabBar::tab:hover {{
                background-color: {Theme.MUTED.name()};
                color: {Theme.FOREGROUND.name()};
            }}
            QTabBar::tab:selected {{
                background-color: {Theme.BACKGROUND.name()};
                color: {Theme.PRIMARY.name()};
                border-bottom-color: {Theme.PRIMARY.name()};
            }}
        """)

        # Create and add pages
        self.adventure_page = AdventurePage()
        self.stats_page = StatsPage()
        self.inventory_page = InventoryPage()
        self.shop_page = ShopPage()
        self.combat_page = CombatPage()
        self.customization_page = CharacterCustomizationPage()

        self.tab_widget.addTab(self.adventure_page, "🏠 Adventure")
        self.tab_widget.addTab(self.combat_page, "⚔️ Battle")
        self.tab_widget.addTab(self.stats_page, "📊 Stats")
        self.tab_widget.addTab(self.inventory_page, "🎒 Inventory")
        self.tab_widget.addTab(self.shop_page, "🏪 Shop")
        self.tab_widget.addTab(self.customization_page, "👤 Character")

        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        self.main_layout.addWidget(self.tab_widget, 4)  # Add with stretch factor

        # Initialize controllers (following MVC pattern)
        self.adventure_controller = AdventureController(self.hero)
        self.combat_controller = CombatController(self.hero)
        self.shop_controller = ShopController(self.hero, get_shop_items())
        self.inventory_controller = InventoryController(self.hero)
        self.stats_controller = StatsController(self.hero)
        self.customization_controller = CustomizationController(self.hero)
        self.monster_stats_controller = MonsterStatsController(self.hero)

        # Connect controller signals to UI updates
        self.adventure_controller.status_message.connect(self.log_message)
        self.adventure_controller.error_occurred.connect(lambda title, msg: QMessageBox.warning(self, title, msg))

        self.shop_controller.transaction_completed.connect(self._on_item_purchased)
        self.shop_controller.gold_updated.connect(self._update_gold_displays)
        self.shop_controller.error_occurred.connect(lambda title, msg: QMessageBox.warning(self, title, msg))

        self.inventory_controller.item_used.connect(self._on_item_used)
        self.inventory_controller.item_equipped.connect(self._on_item_equipped)

        self.stats_controller.stat_increased.connect(self._on_stat_increased)
        self.stats_controller.error_occurred.connect(lambda title, msg: QMessageBox.information(self, title, msg))

        self.customization_controller.error_occurred.connect(lambda title, msg: QMessageBox.warning(self, title, msg))
        self.customization_controller.status_message.connect(self.log_message)
        self.customization_controller.customization_saved.connect(self._on_customization_saved)
        self.customization_controller.customization_loaded.connect(self._on_customization_loaded)

        # Connect customization page to controller
        self.customization_page.customization_changed.connect(
            lambda data: self.customization_controller.apply_customization(data)
        )
        self.customization_page.save_requested.connect(
            lambda data: self.customization_controller.save_customization(data)
        )
        self.customization_page.load_requested.connect(
            self.customization_controller.load_customization
        )

        # Connect UI elements to controllers (clean separation)
        self.adventure_page.explore_btn.clicked.connect(self._explore_via_controller)
        self.adventure_page.rest_btn.clicked.connect(self._rest_via_controller)
        self.adventure_page.quit_btn.clicked.connect(self.quit_game)

        self.combat_page.attack_btn.clicked.connect(self.combat_attack)
        self.combat_page.use_skill_btn.clicked.connect(self.combat_use_skill)
        self.combat_page.use_item_btn.clicked.connect(self.combat_use_item)
        self.combat_page.view_stats_btn.clicked.connect(self.view_enemy_stats)
        self.combat_page.run_btn.clicked.connect(self.combat_run)

        self.shop_page.sell_btn.clicked.connect(self.sell_items)
        self.shop_page.leave_btn.clicked.connect(self.leave_shop)

        self.stats_page.strength_plus_btn.clicked.connect(lambda: self._increase_stat_via_controller('strength'))
        self.stats_page.defense_plus_btn.clicked.connect(lambda: self._increase_stat_via_controller('defense'))
        self.stats_page.magic_plus_btn.clicked.connect(lambda: self._increase_stat_via_controller('magic'))
        self.stats_page.speed_plus_btn.clicked.connect(lambda: self._increase_stat_via_controller('speed'))

        # Set up keyboard shortcuts
        self.setup_keyboard_shortcuts()

    def on_tab_changed(self, index):
        """Handle tab selection changes with smooth transitions"""
        if not self.hero and index != 0:  # 0 is Adventure tab
            self.tab_widget.setCurrentIndex(0)
            return

        # Animate tab transition fade
        self.animate_tab_transition(index)

        if self.hero:
            self.update_stats_display()
            if index == PageIndex.SHOP:
                self.shop_page.update_shop(self.hero, get_shop_items())
                for card in self.shop_page.item_cards:
                    card.action_clicked.connect(self.on_shop_item_clicked)
            elif index == PageIndex.INVENTORY:
                self.inventory_page.update_inventory(self.hero)
                for i in range(self.inventory_page.inventory_grid_layout.count()):
                    item = self.inventory_page.inventory_grid_layout.itemAt(i)
                    if item:
                        widget = item.widget()
                        if isinstance(widget, ItemCard):
                            widget.action_clicked.connect(self.on_inventory_item_clicked)

    def animate_tab_transition(self, new_index):
        """Animate tab transition with fade effect"""
        # Get current and target widgets
        current_widget = self.tab_widget.widget(self.current_view_index)
        target_widget = self.tab_widget.widget(new_index)

        if not current_widget or not target_widget or current_widget == target_widget:
            self.current_view_index = new_index
            return

        # Simple crossfade animation (fade out current, fade in new)
        fade_out = QPropertyAnimation(current_widget, b"windowOpacity")
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setDuration(150)

        fade_in = QPropertyAnimation(target_widget, b"windowOpacity")
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setDuration(150)

        fade_out.finished.connect(lambda: fade_in.start())

        fade_out.start()
        self.current_view_index = new_index

        # Keep references
        self._tab_animations = [fade_out, fade_in]

    def log_message(self, message):
        """Add a message to the game log with type-based coloring"""
        if hasattr(self, 'log_display') and isinstance(self.log_display, LogDisplay):
            # Determine message type based on content
            message_type = "info"
            if any(word in message.lower() for word in ["defeated", "damage", "critical", "died"]):
                message_type = "combat"
            elif any(word in message.lower() for word in ["gold", "purchased", "sold"]):
                message_type = "success"
            elif "error" in message.lower() or "failed" in message.lower():
                message_type = "error"

            self.log_display.add_entry(message, message_type)

    def add_entry_to_log(self, message, message_type="info"):
        """Direct method to add log entries with type"""
        if hasattr(self, 'log_display') and isinstance(self.log_display, LogDisplay):
            self.log_display.add_entry(message, message_type)


    def hide_main_log(self):
        """Hide the main game log widget"""
        if hasattr(self, 'log_display') and self.log_display:
            self.log_display.hide()  # Hide but keep widget for reuse

    def handle_event(self, event):
        """Processes a game event and logs a message."""
        event_type = event.get('type')
        params = event

        message = ""
        is_combat_event = False

        if event_type == 'critical_hit':
            message = "\U0001f4a5 Critical hit!"
            is_combat_event = True
        elif event_type == 'player_damage':
            message = f"\u2694\ufe0f You deal {params['damage']} damage to {params['target']}!"
            self.shake_widget(self.combat_page.enemy_sprite_label)
            is_combat_event = True
        elif event_type == 'player_miss':
            message = f"\U0001f6e1\ufe0f {params['target']} dodges your attack!"
            is_combat_event = True
        elif event_type == 'enemy_defeated':
            message = f"\U0001f389 You defeated the {params['enemy_name']}!"
            is_combat_event = True
        elif event_type == 'gain_experience':
            message = f"\u2b50\ufe0f Gained {params['amount']} experience!"
        elif event_type == 'gain_gold':
            message = f"\U0001f4b0 Gained {params['amount']} gold!"
        elif event_type == 'level_up':
            message = params['message']
        elif event_type == 'item_drop':
            message = f"\U0001f4e6 Found {params['item_name']} ({params['rarity']})!"
            is_combat_event = True
        elif event_type == 'escape_success':
            message = "\U0001f3c3 You successfully escaped!"
            is_combat_event = True
        elif event_type == 'escape_fail':
            message = "\u274c Failed to escape!"
            is_combat_event = True
        elif event_type == 'enemy_miss':
            message = f"\U0001f6e1\ufe0f {params['enemy_name']} attacks, but you dodge!"
            is_combat_event = True
        elif event_type == 'enemy_damage':
            message = f"\U0001f4a5 {params['enemy_name']} deals {params['damage']} damage to you!"
            self.shake_widget(self.combat_page.hero_sprite_label)
            is_combat_event = True
        elif event_type == 'player_defeated':
            message = "\U0001f480 You have been defeated..."
            is_combat_event = True
        elif event_type == 'status_effect_damage':
            message = f"\u2620\ufe0f You take {params['damage']} damage from status effects!"
            is_combat_event = True
        elif event_type == 'use_skill':
            message = f"\u2728 You used {params['skill_name']}!"
            is_combat_event = True
        elif event_type == 'healing_effect':
            message = f"💚 Recovered {params['amount']} HP!"
            # Flash healing effect
            QTimer.singleShot(200, lambda: self.flash_widget(self.combat_page.hero_sprite_label, "rgba(39, 174, 96, 0.4)", 300))
            is_combat_event = True
        elif event_type == 'mana_recovery':
            message = f"🔷 Recovered {params['amount']} MP!"
            # Flash mana effect
            QTimer.singleShot(200, lambda: self.flash_widget(self.combat_page.hero_sprite_label, "rgba(52, 152, 219, 0.4)", 300))
            is_combat_event = True

        if message:
            # If we're in combat and it's a combat event, show it in battle log
            if is_combat_event and self.current_state == GameState.COMBAT and hasattr(self.combat_page, 'add_battle_log_message'):
                self.combat_page.add_battle_log_message(message)
            else:
                # Otherwise, show in main log
                self.log_message(message)

    def start_new_game(self, hero_name):
        """Start new game from the NewGameView."""
        self.hero = Hero(hero_name)
        self.current_state = GameState.ADVENTURE
        self.setup_game_interface()
        self.update_stats_display()

    def show_menu(self):
        """Show the main menu"""
        self.current_state = GameState.MENU
        self.log_message("=== Welcome to PyRPG Adventure! ===")
        self.log_message("Click 'New Game' to start your adventure!")

        # Ensure we're on adventure tab
        self.tab_widget.setCurrentIndex(PageIndex.ADVENTURE)

        # Hide existing game buttons
        self.adventure_page.explore_btn.hide()
        self.adventure_page.rest_btn.hide()

        # Show new game button with professional styling
        self.new_game_btn = QPushButton("🎮 New Game")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                border: 2px solid #dc3545;
                color: #dc3545;
                font-size: 18px;
                font-weight: 600;
                padding: 20px 40px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)
        self.new_game_btn.clicked.connect(self.show_new_game_view)

        # Add shadow to new game button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.new_game_btn.setGraphicsEffect(shadow)

        # Replace explore button with new game button
        self.adventure_page.button_layout.addWidget(self.new_game_btn, 0, 0, 1, 2)


    def show_new_game_view(self):
        """Show the new game view."""
        self.new_game_view = NewGameView()
        self.new_game_view.character_created.connect(self.start_new_game)
        self.setCentralWidget(self.new_game_view)


    def _explore_via_controller(self):
        """Explore using controller pattern"""
        if not self.hero:
            return
        self.adventure_controller.explore_wilderness()
        # After controller logic, handle UI parts
        QApplication.processEvents()
        QTimer.singleShot(1000, self.trigger_random_encounter)

    def _rest_via_controller(self):
        """Rest using controller pattern"""
        if not self.hero:
            return
        self.adventure_controller.rest_at_camp()
        self.hero.health = self.hero.max_health
        self.update_stats_display()

    def _increase_stat_via_controller(self, stat_name):
        """Increase stat using controller pattern"""
        self.stats_controller.increase_stat(stat_name)

    def _on_item_purchased(self, item):
        """Handle item purchase completion"""
        if self.hero:
            self.hero.add_item(item)
            self.log_message(f"💰 Purchased {item.name}!")
            self.update_stats_display()

    def _on_item_used(self, item):
        """Handle item usage completion"""
        if self.hero:
            self.log_message(f"🧪 {self.hero.use_item(item)}")
            self.hero.remove_item(item)
            self.update_stats_display()

    def _on_item_equipped(self, item):
        """Handle item equip completion"""
        if self.hero:
            self.log_message(f"⚔️ Equipped {item.name}!")
            self.update_stats_display()

    def _on_stat_increased(self, stat_name):
        """Handle stat increase completion"""
        if self.hero:
            self.log_message(f"🏋️ Increased {stat_name}!")
            self.update_stats_display()

    def _on_customization_saved(self):
        """Handle customization save completion"""
        # Additional UI updates if needed
        pass

    def _on_customization_loaded(self):
        """Handle customization load completion"""
        # Refresh customization page display if necessary
        if hasattr(self, 'customization_page') and self.customization_page:
            current_customization = self.customization_controller.get_current_customization()
            if current_customization:
                self.customization_page.load_customization(current_customization)

    def _update_gold_displays(self, new_gold):
        """Update all gold displays when gold changes"""
        self.shop_page.gold_label.setText(f"Gold: {new_gold}")
        self.inventory_page.gold_label.setText(f"Gold: {new_gold}")

    def on_shop_item_clicked(self, item, action):
        if action == "buy":
            reply = QMessageBox.question(self, "Confirm Purchase",
                                       f"Buy {item.name} for {item.value} gold?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                success = self.shop_controller.purchase_item(item)
                if success:
                    self._on_item_purchased(item)
                    QTimer.singleShot(100, lambda: self.handle_consumable_auto_use(item))

    def handle_consumable_auto_use(self, item):
        """Handle automatic use of consumables after purchase"""
        if self.hero and item.item_type == 'consumable':
            message = self.hero.use_item(item)
            if message:
                self.log_message(f"🧪 {message}")
                self.hero.remove_item(item)
                self.update_stats_display()

    def update_stats_display(self):
        """Update the stats display with current hero stats"""
        if not self.hero:
            return

        # Update detailed stats page
        if hasattr(self.stats_page, 'update_stats_display'):
            self.stats_page.update_stats_display(self.hero)

        # Update gold labels on other pages
        self.shop_page.gold_label.setText(f"Gold: {self.hero.gold}")
        self.inventory_page.gold_label.setText(f"Gold: {self.hero.gold}")


    def format_stats_html(self):
        """Format hero stats as HTML for detailed stats page"""
        if not self.hero:
            return "No character created yet"

        return f"""
<div style='line-height: 1.6;'>
    <h2 style='color: #dc3545; border-bottom: 2px solid #3e4452; padding-bottom: 10px;'>\u2694\ufe0f {self.hero.name}</h2>

    <h3 style='color: #98c379; margin-top: 20px;'>\U0001f4ca Core Stats</h3>
    <div style='margin-left: 15px;'>
        <p><b>Level:</b> {self.hero.level}</p>
        <p><b>Experience:</b> {self.hero.experience} / {self.hero.experience_to_level}</p>
        <p><b>Health:</b> {self.hero.health} / {self.hero.max_health}</p>
        <p><b>Mana:</b> {self.hero.mana} / {self.hero.max_mana}</p>
        <p><b>Gold:</b> <span style='color: #e5c07b;'>{self.hero.gold}</span></p>
    </div>

    <h3 style='color: #e06c75; margin-top: 20px;'>\u26a1 Attributes</h3>
    <div style='margin-left: 15px;'>
        <p><b>Strength:</b> {self.hero.strength} (Physical damage)</p>
        <p><b>Dexterity:</b> {self.hero.dexterity} (Crit: {self.hero.crit_chance:.1f}%, Dodge: {self.hero.dodge_chance:.1f}%)</p>
        <p><b>Intelligence:</b> {self.hero.intelligence} (Magic power)</p>
        <p><b>Vitality:</b> {self.hero.vitality} (Defense)</p>
    </div>

    <h3 style='color: #dc3545; margin-top: 20px;'>\u2694\ufe0f Combat Stats</h3>
    <div style='margin-left: 15px;'>
        <p><b>Attack Power:</b> <span style='color: #e06c75;'>{self.hero.attack_power}</span></p>
        <p><b>Magic Power:</b> <span style='color: #c678dd;'>{self.hero.magic_power:.1f}</span></p>
        <p><b>Defense:</b> <span style='color: #dc3545;'>{self.hero.defense}</span></p>
        <p><b>Critical Chance:</b> {self.hero.crit_chance:.1f}%</p>
        <p><b>Dodge Chance:</b> {self.hero.dodge_chance:.1f}%</p>
    </div>

    <h3 style='color: #c678dd; margin-top: 20px;'>\U0001f392 Equipment</h3>
    <div style='margin-left: 15px;'>
        <p><b>Weapon:</b> {self.hero.equipment['weapon'].name if self.hero.equipment['weapon'] else 'None'}</p>
        <p><b>Armor:</b> {self.hero.equipment['armor'].name if self.hero.equipment['armor'] else 'None'}</p>
        <p><b>Accessory:</b> {self.hero.equipment['accessory'].name if self.hero.equipment['accessory'] else 'None'}</p>
    </div>

    <h3 style='color: #98c379; margin-top: 20px;'>\U0001f4e6 Inventory</h3>
    <div style='margin-left: 15px;'>
        <p><b>Items:</b> {len(self.hero.inventory)}</p>
        {''.join([f"<p style='margin-left: 15px;'>• {item.name} ({item.rarity})</p>" for item in self.hero.inventory]) if self.hero.inventory else '<p style="margin-left: 15px;">No items</p>'}
    </div>

    <h3 style='color: #e5c07b; margin-top: 20px;'>\u2b50\ufe0f Progression</h3>
    <div style='margin-left: 15px;'>
        <p><b>Stat Points:</b> {self.hero.stat_points}</p>
        <p><b>Skill Points:</b> {self.hero.skill_points}</p>
    </div>
</div>
"""


    def on_inventory_item_clicked(self, item, action):
        """Handle inventory item card clicks"""
        if self.hero:
            if action.lower() == "use" and item.item_type == 'consumable':
                # Use consumable
                message = self.hero.use_item(item)
                if message:
                    self.log_message(f"\U0001f9ea {message}")
                    self.hero.remove_item(item)
                    self.update_stats_display()
            elif action.lower() == "equip" and item.item_type in ['weapon', 'armor', 'accessory']:
                # Remove item from inventory
                self.hero.remove_item(item)
                # Equip the item and get the previously equipped item (if any)
                old_item = self.hero.equip_item(item)
                # Add the old item back to inventory if there was one
                if old_item:
                    self.hero.add_item(old_item)
                self.log_message(f"\u2694\ufe0f Equipped {item.name}!")
                self.update_stats_display()

    def explore(self):
        """Handle exploration and random encounters"""
        if not self.hero:
            return

        self.log_message("You venture into the wilderness...")
        QApplication.processEvents()

        # Simulate exploration delay
        QTimer.singleShot(1000, self.trigger_random_encounter)

    def trigger_random_encounter(self):
        """Trigger a random enemy encounter with encounter preview"""
        if self.hero:
            # Get a random enemy for this encounter
            from game.game import get_random_enemy
            self.encounter_enemy = get_random_enemy(self.hero.level)

            # Show encounter preview dialog
            self.show_encounter_preview()
            return

    def show_encounter_preview(self):
        """Show encounter preview dialog before entering combat"""
        if not self.encounter_enemy:
            self.show_combat_interface()
            return

        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
        from PySide6.QtCore import Qt

        # Create encounter dialog
        encounter_dialog = QDialog(self)
        encounter_dialog.setWindowTitle("⚠️ Enemy Encountered!")
        encounter_dialog.setModal(True)
        encounter_dialog.setFixedSize(500, 400)
        encounter_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {Theme.BACKGROUND.name()};
                border: 2px solid {Theme.BORDER.name()};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(encounter_dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Encounter title
        title_label = QLabel("⚠️ A Wild Enemy Approaches!")
        title_font = encounter_dialog.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {Theme.FOREGROUND.name()}; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Enemy info frame
        enemy_frame = QFrame()
        enemy_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {Theme.ACCENT.name()};
                border-radius: 8px;
                background-color: {Theme.CARD.name()};
                padding: 10px;
            }}
        """)

        frame_layout = QVBoxLayout(enemy_frame)

        # Enemy display
        enemy_display_layout = QHBoxLayout()

        # Enemy sprite/emoji
        enemy_sprite_label = QLabel("👹")
        sprite_font = encounter_dialog.font()
        sprite_font.setPointSize(48)
        enemy_sprite_label.setFont(sprite_font)
        enemy_sprite_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.DESTRUCTIVE.name()};
                padding: 10px;
                background-color: {Theme.MUTED.name()};
                border-radius: 8px;
                min-width: 80px;
                max-width: 80px;
                text-align: center;
            }}
        """)
        enemy_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        enemy_display_layout.addWidget(enemy_sprite_label)

        # Enemy info
        enemy_info_layout = QVBoxLayout()
        enemy_info_layout.setSpacing(5)

        enemy_name_label = QLabel(f"<b>{self.encounter_enemy.name}</b>")
        name_font = encounter_dialog.font()
        name_font.setPointSize(14)
        enemy_name_label.setFont(name_font)
        enemy_name_label.setStyleSheet(f"color: {Theme.FOREGROUND.name()};")
        enemy_info_layout.addWidget(enemy_name_label)

        enemy_level_label = QLabel(f"Level {self.encounter_enemy.level} • {self.encounter_enemy.enemy_type.title()}")
        enemy_level_label.setStyleSheet(f"color: {Theme.MUTED_FOREGROUND.name()};")
        enemy_info_layout.addWidget(enemy_level_label)

        # Quick stats preview
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        health_label = QLabel(f"❤️ Health: {self.encounter_enemy.health}/{self.encounter_enemy.max_health}")
        health_label.setStyleSheet(f"color: {Theme.SECONDARY.name()};")

        threat_label = QLabel(f"⚔️ Threat: {self.monster_stats_controller._calculate_encounter_threat(self.hero, self.encounter_enemy).title()}")
        threat_label.setStyleSheet(f"color: {Theme.DESTRUCTIVE.name()};")

        stats_layout.addWidget(health_label)
        stats_layout.addWidget(threat_label)
        stats_layout.addStretch()

        enemy_info_layout.addLayout(stats_layout)
        enemy_info_layout.addStretch()
        enemy_display_layout.addLayout(enemy_info_layout)

        frame_layout.addLayout(enemy_display_layout)

        # Quick elemental info if applicable
        if self.encounter_enemy.elemental_weakness or self.encounter_enemy.elemental_resistance:
            elemental_layout = QHBoxLayout()
            elemental_layout.setSpacing(10)

            if self.encounter_enemy.elemental_weakness:
                weaknesses = ", ".join(self.encounter_enemy.elemental_weakness[:2])  # Show top 2
                weak_label = QLabel(f"🤕 Weak to: {weaknesses}")
                weak_label.setStyleSheet(f"color: {Theme.DESTRUCTIVE.name()}; font-size: 11px;")
                elemental_layout.addWidget(weak_label)

            if self.encounter_enemy.elemental_resistance:
                resistances = ", ".join(self.encounter_enemy.elemental_resistance[:2])  # Show top 2
                res_label = QLabel(f"🛡️ Resistant: {resistances}")
                res_label.setStyleSheet(f"color: {Theme.ACCENT.name()}; font-size: 11px;")
                elemental_layout.addWidget(res_label)

            elemental_layout.addStretch()
            frame_layout.addLayout(elemental_layout)

        layout.addWidget(enemy_frame)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # View Details button
        view_details_btn = StyledButton("📖 View Details", variant="secondary")
        view_details_btn.setToolTip("View detailed monster statistics")
        view_details_btn.clicked.connect(lambda: self.show_encounter_details(encounter_dialog))
        buttons_layout.addWidget(view_details_btn)

        # Spacer
        buttons_layout.addStretch()

        # Fight button
        fight_btn = StyledButton("⚔️ Fight!", variant="primary")
        fight_btn.setToolTip("Engage the enemy in combat")
        fight_btn.clicked.connect(encounter_dialog.accept)  # Accept will close and proceed
        buttons_layout.addWidget(fight_btn)

        # Run button
        run_btn = StyledButton("🏃 Run Away", variant="destructive")
        run_btn.setToolTip("Avoid the encounter")
        run_btn.clicked.connect(encounter_dialog.reject)  # Reject will flee
        buttons_layout.addWidget(run_btn)

        layout.addLayout(buttons_layout)

        # Show dialog and handle result
        result = encounter_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Player chose to fight
            self.current_enemy = self.encounter_enemy
            self.show_combat_interface()
        else:
            # Player chose to run
            self.log_message("You avoid the encounter and continue exploring.")
            self.encounter_enemy = None

    def show_encounter_details(self, parent_dialog):
        """Show detailed monster stats from encounter preview"""
        if not self.encounter_enemy:
            return

        # Create monster stats viewer dialog
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        from ui.views.monster_stats_page import MonsterStatsViewer

        # Create details dialog
        details_dialog = QDialog(parent_dialog)
        details_dialog.setWindowTitle(f"{self.encounter_enemy.name} - Monster Details")
        details_dialog.setModal(True)
        details_dialog.setMinimumSize(600, 500)
        details_dialog.setMaximumSize(900, 700)

        # Create the monster stats viewer
        stats_viewer = MonsterStatsViewer(details_dialog, self.encounter_enemy)

        # Set up dialog layout
        layout = QVBoxLayout(details_dialog)
        layout.addWidget(stats_viewer)
        layout.setContentsMargins(0, 0, 0, 0)

        # Connect controller signals
        self.monster_stats_controller.enemy_displayed.connect(
            lambda enemy: stats_viewer.display_enemy_stats(enemy)
        )

        # Show the stats via controller
        self.monster_stats_controller.view_enemy_stats(self.encounter_enemy)

        # Show dialog
        details_dialog.exec()

    def show_combat_interface(self):
        """Show the combat interface with current enemy - Enhanced formatting"""
        if not self.hero or not self.current_enemy:
            return

        self.current_state = GameState.COMBAT
        self.tab_widget.setCurrentIndex(PageIndex.COMBAT)

        # Re-enable combat buttons for new fight
        self.set_combat_buttons_enabled(True)

        # Add to combat page battle log
        if hasattr(self.combat_page, 'add_battle_log_message'):
            self.combat_page.add_battle_log_message(f"A wild {self.current_enemy.name} appears!")

    def hide_combat_interface(self):
        """Hide combat interface and return to adventure"""
        self.tab_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.current_state = GameState.ADVENTURE
        self.current_enemy = None

    def process_combat_round(self, action):
        """Process the player's turn and schedule the enemy's turn."""
        if not self.hero or not self.current_enemy:
            return

        # Disable combat buttons during the turn
        self.set_combat_buttons_enabled(False)

        events, combat_over = handle_player_turn(self.hero, self.current_enemy, action)
        for event in events:
            self.handle_event(event)

        self.update_combat_ui()

        if combat_over:
            QTimer.singleShot(1500, self.hide_combat_interface)
            self.update_stats_display()
            return

        # Schedule the enemy's turn after a delay
        QTimer.singleShot(1000, self.execute_enemy_turn)

    def execute_enemy_turn(self):
        """Process the enemy's turn after a delay."""
        if not self.hero or not self.current_enemy:
            return

        events, combat_over = handle_enemy_turn(self.hero, self.current_enemy)
        for event in events:
            self.handle_event(event)

        self.update_combat_ui()

        if combat_over:
            if not self.hero.is_alive():
                QMessageBox.critical(self, "Defeat", "You have been defeated! Game Over.")
                self.quit_game()
            return

        # Re-enable combat buttons for the next player turn
        self.set_combat_buttons_enabled(True)

    def update_combat_ui(self):
        """Update all combat UI elements with smooth animations"""
        if self.hero and self.current_enemy:
            # Animate hero health bar
            if hasattr(self, 'combat_page') and self.combat_page:
                current_hero_health = self.combat_page.hero_combat_health_bar.value()
                target_hero_health = int((self.hero.health / self.hero.max_health) * 100)
                self.animate_progress_bar(self.combat_page.hero_combat_health_bar, current_hero_health, target_hero_health)
                self.combat_page.hero_combat_health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health}")

                # Animate enemy health bar
                current_enemy_health = self.combat_page.enemy_combat_health_bar.value()
                target_enemy_health = int((self.current_enemy.health / self.current_enemy.max_health) * 100)
                self.animate_progress_bar(self.combat_page.enemy_combat_health_bar, current_enemy_health, target_enemy_health)
                self.combat_page.enemy_combat_health_bar.setFormat(f"{self.current_enemy.health} / {self.current_enemy.max_health}")

        self.update_stats_display()

    def animate_progress_bar(self, progress_bar, start_value, end_value, duration=500):
        """Animate a progress bar smoothly from start to end value"""
        if hasattr(self, 'animations'):
            animation = QPropertyAnimation(progress_bar, b"value")
            animation.setStartValue(start_value)
            animation.setEndValue(end_value)
            animation.setDuration(duration)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()
            self.animations.append(animation)  # Keep reference

    def set_combat_buttons_enabled(self, enabled):
        """Enable or disable all combat action buttons."""
        self.combat_page.attack_btn.setEnabled(enabled)
        self.combat_page.use_skill_btn.setEnabled(enabled)
        self.combat_page.use_item_btn.setEnabled(enabled)
        self.combat_page.run_btn.setEnabled(enabled)

    def open_shop(self):
        """Open the shop interface"""
        if not self.hero:
            return

        self.current_state = GameState.SHOP
        self.tab_widget.setCurrentIndex(PageIndex.SHOP)

        self.log_message(f"You have {self.hero.gold} gold to spend!")

    def leave_shop(self):
        """Leave the shop"""
        self.current_state = GameState.ADVENTURE
        self.tab_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.log_message("You leave the shop.")

    def buy_item(self, item_name, price):
        """Buy an item from the shop"""
        if not self.hero:
            return

        # Get the actual Item object from the shop
        shop_items = get_shop_items()
        if item_name in shop_items:
            item = shop_items[item_name]

            if self.hero.gold >= item.value:
                self.hero.gold -= item.value
                self.hero.add_item(item)

                # Only use consumables immediately, equipment goes to inventory
                if item.item_type == 'consumable':
                    message = self.hero.use_item(item)
                    if message:
                        # Queued for async display
                        QTimer.singleShot(100, lambda: self.log_message(f"🧪 {message}"))
                        self.hero.remove_item(item)  # Remove after using

                self.update_stats_display()
                # Show purchase success message - only for equipment, consumables already shown above
                if item.item_type != 'consumable':
                    self.log_message(f"💰 Purchased {item.name}!")
            else:
                QMessageBox.warning(self, "Not Enough Gold",
                                  f"You need {item.value} gold to buy {item.name}. You have {self.hero.gold} gold.")
        else:
            QMessageBox.warning(self, "Item Not Found", f"Could not find item: {item_name}")

    def sell_items(self):
        """Sell items from inventory using overlay"""
        if not self.hero or not self.hero.inventory:
            self.log_message("You have no items to sell!")
            return

        # Create item selection overlay
        overlay = ItemSelectionOverlay(
            self.hero.inventory,
            title="Sell Item",
            action_text="Sell",
            show_price=True,
            parent=self
        )
        overlay.item_selected.connect(self.on_item_sold)
        overlay.show()

    def on_item_sold(self, item):
        """Handle item being sold"""
        if self.hero:
            sell_value = item.value // 2  # Sell for half price
            self.hero.inventory.remove(item)
            self.hero.gold += sell_value
            self.update_stats_display()
            self.log_message(f"Sold {item.name} for {sell_value} gold!")

    def show_stats(self):
        """Show detailed stats"""
        if not self.hero:
            return

        # Navigate to stats tab
        self.tab_widget.setCurrentIndex(PageIndex.STATS)

        # Update GUI display
        self.update_stats_display()

    def rest(self):
        """Rest to restore health"""
        if self.hero:
            self.hero.health = self.hero.max_health
            self.update_stats_display()
            self.log_message("You rest and restore your health!")

    def quit_game(self):
        """Quit the game"""
        reply = QMessageBox.question(self, "Quit Game",
                                   "Are you sure you want to quit?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def combat_attack(self):
        """Handle combat attack action"""
        self.process_combat_round("attack")

    def combat_run(self):
        """Handle combat run action"""
        self.process_combat_round("run")

    def combat_use_skill(self):
        """Handle using a skill during combat using overlay"""
        if not self.hero or not self.current_enemy:
            return

        if not self.hero.unlocked_skills:
            self.log_message("You have no skills to use!")
            return

        # Create skill selection overlay
        # Note: We need a way to display skills in an overlay. For now, we'll just use the first skill.
        # This should be replaced with a proper skill selection overlay.
        skill_to_use = self.hero.unlocked_skills[0]
        self.on_combat_skill_used(skill_to_use)

    def on_combat_skill_used(self, skill):
        """Handle skill being used in combat"""
        if self.hero and self.hero.mana >= skill.mana_cost:
            self.hero.mana -= skill.mana_cost
            self.process_combat_round(('use_skill', skill))
        else:
            self.log_message(f"Not enough mana to use {skill.name}!")

    def combat_use_item(self):
        """Handle using an item during combat using overlay"""
        if not self.hero or not self.current_enemy:
            return

        # Filter for consumable items only
        consumables = [item for item in self.hero.inventory if item.item_type == 'consumable']

        if not consumables:
            self.log_message("You have no consumable items to use!")
            return

        # Create item selection overlay
        overlay = ItemSelectionOverlay(
            consumables,
            title="Use Item in Combat",
            action_text="Use",
            show_price=False,
            parent=self
        )
        overlay.item_selected.connect(self.on_combat_item_used)
        overlay.show()

    def on_combat_item_used(self, item):
        """Handle item being used in combat"""
        if self.hero:
            # Use the item
            message = self.hero.use_item(item)
            self.hero.inventory.remove(item)

            # Log the action
            if message:
                self.log_message(f"\U0001f9ea {message}")
                # Flash green for healing
                QTimer.singleShot(100, lambda: self.flash_widget(self.combat_page.hero_sprite_label, "rgba(46, 204, 113, 0.3)", 200))

            # Update stats display
            self.update_stats_display()

            # Enemy gets a turn after using item - pass tuple for action
            self.process_combat_round(("use_item", item))

    def view_enemy_stats(self):
        """Show detailed enemy statistics using the monster stats viewer"""
        if not self.current_enemy:
            self.log_message("No enemy to view stats for!")
            return

        # Create a dialog window to show monster stats
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        from ui.views.monster_stats_page import MonsterStatsViewer

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.current_enemy.name} - Monster Stats")
        dialog.setModal(True)  # Block interaction with main window
        dialog.setMinimumSize(800, 600)
        dialog.setMaximumSize(1000, 800)

        # Create the monster stats viewer
        stats_viewer = MonsterStatsViewer(dialog, self.current_enemy)

        # Set up dialog layout
        layout = QVBoxLayout(dialog)
        layout.addWidget(stats_viewer)
        layout.setContentsMargins(0, 0, 0, 0)

        # Connect controller signals
        self.monster_stats_controller.enemy_displayed.connect(
            lambda enemy: stats_viewer.display_enemy_stats(enemy)
        )

        # Show the stats via controller
        self.monster_stats_controller.view_enemy_stats(self.current_enemy)

        # Show dialog
        dialog.exec()

        self.log_message(f"Closed stats viewer for {self.current_enemy.name}")

    def increase_stat(self, stat_name):
        """Increase a character's stat using available stat points"""
        if not self.hero:
            return

        if self.hero.stat_points > 0:
            # Increase the stat
            if stat_name == 'strength':
                self.hero.strength += 1
                self.hero.attack_power = self.hero.calculate_attack_power()
            elif stat_name == 'defense':
                self.hero.defense += 1
            elif stat_name == 'magic':
                self.hero.intelligence += 1
                self.hero.magic_power = self.hero.calculate_magic_power()
            elif stat_name == 'speed':
                self.hero.dexterity += 1
                # Recalculate crit/dodge chances
                self.hero.refresh_derived_stats()

            # Consume stat point
            self.hero.stat_points -= 1

            # Update display
            self.update_stats_display()
            self.log_message(f"🏋️ Increased {stat_name}!")
        else:
            QMessageBox.information(self, "No Stat Points", "You have no available stat points to allocate.")

    def setup_keyboard_shortcuts(self):
        """Set up global keyboard shortcuts for the application"""
        from PySide6.QtGui import QShortcut, QKeySequence

        self.shortcuts = []
        # General shortcuts
        shortcut = QShortcut(QKeySequence("F1"), self)
        shortcut.activated.connect(self.show_help)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence.StandardKey.Quit, self)
        shortcut.activated.connect(self.quit_game)
        self.shortcuts.append(shortcut)

        # Tab navigation shortcuts
        shortcut = QShortcut(QKeySequence("Alt+S"), self)
        shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(PageIndex.STATS))
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("Alt+I"), self)
        shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(PageIndex.INVENTORY))
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("Alt+P"), self)
        shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(PageIndex.SHOP))  # P for shop
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("Alt+C"), self)
        shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(PageIndex.CUSTOMIZATION))  # C for character
        self.shortcuts.append(shortcut)

        # Combat shortcuts (only active in combat)
        shortcut = QShortcut(QKeySequence("A"), self)
        shortcut.activated.connect(lambda: self.combat_attack() if self.current_state == GameState.COMBAT else None)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("S"), self)
        shortcut.activated.connect(lambda: self.combat_use_skill() if self.current_state == GameState.COMBAT else None)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("I"), self)
        shortcut.activated.connect(lambda: self.combat_use_item() if self.current_state == GameState.COMBAT else None)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("R"), self)
        shortcut.activated.connect(lambda: self.combat_run() if self.current_state == GameState.COMBAT and self.combat_page else None)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("V"), self)
        shortcut.activated.connect(lambda: self.view_enemy_stats() if self.current_state == GameState.COMBAT and self.combat_page else None)
        self.shortcuts.append(shortcut)

        # Adventure shortcuts
        shortcut = QShortcut(QKeySequence("E"), self)
        shortcut.activated.connect(lambda: self.explore() if self.current_state == GameState.ADVENTURE and self.hero else None)
        self.shortcuts.append(shortcut)

        shortcut = QShortcut(QKeySequence("T"), self)
        shortcut.activated.connect(lambda: self.rest() if self.current_state == GameState.ADVENTURE and self.hero else None)
        self.shortcuts.append(shortcut)

    def show_help(self):
        """Show help dialog with keyboard shortcuts"""
        help_text = """
        <h2>PyRPG Adventure - Keyboard Shortcuts</h2>

        <h3>General</h3>
        <b>F1</b> - Show this help<br>
        <b>Ctrl+Q</b> - Quit game<br>

        <h3>Navigation</h3>
        <b>Alt+S</b> - Stats tab<br>
        <b>Alt+I</b> - Inventory tab<br>
        <b>Alt+Shop</b> - Shop tab<br>

        <h3>Combat</h3>
        <b>A</b> - Attack<br>
        <b>S</b> - Use Skill<br>
        <b>I</b> - Use Item<br>
        <b>R</b> - Run away<br>

        <h3>Character Creation</h3>
        Enter your hero's name (1-20 characters, letters/numbers/space/-/underscore)

        <h3>Tooltip System</h3>
        Hover over items, buttons, and stats for detailed information.
        """
        QMessageBox.information(self, "PyRPG Help", help_text)
