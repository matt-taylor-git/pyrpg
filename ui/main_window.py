# -*- coding: utf-8 -*-
import sys
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
from .components import AchievementSystem

from .widgets import Card, StyledButton

class NewGameView(QWidget):
    """A view for creating a new character, replacing the old splash screen."""
    character_created = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Central card container
        card = Card()
        card.setMaximumWidth(int(self.size().width() * 0.6))  # Responsive width based on window
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        # Title
        title = QLabel("Realm of Legends")
        title.setObjectName("new-game-title")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #dc3545;")
        card_layout.addWidget(title)

        subtitle = QLabel("Create Your Hero")
        subtitle.setObjectName("new-game-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #9a96a5;")
        card_layout.addWidget(subtitle)

        # Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your hero's name...")
        card_layout.addWidget(self.name_input)

        # Begin Adventure Button
        self.start_btn = StyledButton("Begin Adventure", variant="primary")
        self.start_btn.clicked.connect(self.start_game)
        card_layout.addWidget(self.start_btn)

        main_layout.addWidget(card)

    def start_game(self):
        """Emits the character name and signals the main window to start."""
        char_name = self.name_input.text().strip()

        # Input validation
        if not char_name:
            QMessageBox.warning(self, "Invalid Name", "Please enter a character name.")
            return
        if len(char_name) > 20:
            QMessageBox.warning(self, "Invalid Name", "Character name must be 20 characters or less.")
            return
        if not all(c.isalnum() or c in " _-" for c in char_name):
            QMessageBox.warning(self, "Invalid Name", "Character name can only contain letters, numbers, spaces, hyphens, and underscores.")
            return

        self.character_created.emit(char_name)

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
        """Create a shake animation for a widget"""
        original_pos = widget.pos()

        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setLoopCount(2)

        # Create shake effect by moving left and right
        animation.setKeyValueAt(0, original_pos)
        animation.setKeyValueAt(0.25, original_pos + QPoint(magnitude, 0))
        animation.setKeyValueAt(0.5, original_pos - QPoint(magnitude, 0))
        animation.setKeyValueAt(0.75, original_pos + QPoint(magnitude // 2, 0))
        animation.setKeyValueAt(1, original_pos)

        animation.start()
        self.animations.append(animation)  # Keep reference to prevent garbage collection

    def flash_widget(self, widget, color, duration=300):
        """Create a flash effect on a widget by temporarily changing background"""
        original_style = widget.styleSheet()

        # Flash color
        flash_style = original_style + f"\nbackground-color: {color};"
        widget.setStyleSheet(flash_style)

        # Restore original style after duration
        QTimer.singleShot(duration, lambda: widget.setStyleSheet(original_style))

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

        # Game log (top section) - Enhanced with better styling
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setTextInteractionFlags(Qt.NoTextInteraction)
        self.log_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.log_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.main_layout.addWidget(self.log_display, 1) # Add with stretch factor

        # Initialize with styled welcome messages using the new battle log style
        self.game_log = []
        self.log_message("Welcome to PyRPG Adventure! Type 'help' for commands.")

        # Create tab widget (horizontal tabs at top, like React sample)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #282c34;
            }
            QTabBar::tab {
                background-color: #21252b;
                color: #abb2bf;
                padding: 12px 24px;
                border: none;
                border-bottom: 3px solid transparent;
                font-size: 14px;
                font-weight: 500;
                margin-right: 2px;
            }
            QTabBar::tab:hover {
                background-color: #282c34;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background-color: #282c34;
                color: #dc3545;
                border-bottom-color: #dc3545;
            }
        """)

        # Create and add pages
        self.adventure_page = AdventurePage()
        self.stats_page = StatsPage()
        self.inventory_page = InventoryPage()
        self.shop_page = ShopPage()
        self.combat_page = CombatPage()

        self.tab_widget.addTab(self.adventure_page, "🏠 Adventure")
        self.tab_widget.addTab(self.combat_page, "⚔️ Battle")
        self.tab_widget.addTab(self.stats_page, "📊 Stats")
        self.tab_widget.addTab(self.inventory_page, "🎒 Inventory")
        self.tab_widget.addTab(self.shop_page, "🏪 Shop")

        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        self.main_layout.addWidget(self.tab_widget, 4)  # Add with stretch factor

        # Connect adventure page buttons
        self.adventure_page.explore_btn.clicked.connect(self.explore)
        self.adventure_page.rest_btn.clicked.connect(self.rest)
        self.adventure_page.quit_btn.clicked.connect(self.quit_game)

        # Connect combat page buttons
        self.combat_page.attack_btn.clicked.connect(self.combat_attack)
        self.combat_page.use_skill_btn.clicked.connect(self.combat_use_skill)
        self.combat_page.use_item_btn.clicked.connect(self.combat_use_item)
        self.combat_page.run_btn.clicked.connect(self.combat_run)

        # Connect shop page buttons
        self.shop_page.sell_btn.clicked.connect(self.sell_items)
        self.shop_page.leave_btn.clicked.connect(self.leave_shop)

        # Connect stats page stat buttons
        self.stats_page.strength_plus_btn.clicked.connect(lambda: self.increase_stat('strength'))
        self.stats_page.defense_plus_btn.clicked.connect(lambda: self.increase_stat('defense'))
        self.stats_page.magic_plus_btn.clicked.connect(lambda: self.increase_stat('magic'))
        self.stats_page.speed_plus_btn.clicked.connect(lambda: self.increase_stat('speed'))

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
                    widget = self.inventory_page.inventory_grid_layout.itemAt(i).widget()
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
        """Add a message to the game log with left-border accent style (matching React sample)"""
        # Initialize log display if it doesn't exist
        if not hasattr(self, 'log_display') or self.log_display is None:
            self.game_log = []
            self.log_display = QTextEdit()
            self.log_display.setReadOnly(True)
            self.log_display.setTextInteractionFlags(Qt.NoTextInteraction)
            self.log_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.log_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Add to top of main layout
            self.main_layout.insertWidget(0, self.log_display, 1)

        self.game_log.append(message)
        # Keep only last 20 messages
        if len(self.game_log) > 20:
            self.game_log = self.game_log[-20:]

        # Build HTML with clean left-border style (matching React sample)
        # Use a full HTML document with proper styling
        log_html = """
        <html>
        <head>
            <style>
                body {
                    background-color: #282c34;
                    margin: 0;
                    padding: 0;
                    font-family: 'Inter', 'Segoe UI', sans-serif;
                }
                .log-container {
                    padding: 10px;
                    background-color: #21252b;
                    border-radius: 8px;
                    margin: 5px;
                }
                .log-message {
                    border-left: 3px solid #dc3545;
                    padding-left: 12px;
                    margin: 8px 0;
                    color: #abb2bf;
                    font-size: 13px;
                    line-height: 1.6;
                }
            </style>
        </head>
        <body>
            <div class="log-container">
        """

        for msg in self.game_log[-10:]:  # Show last 10 messages in correct order
            log_html += f'<div class="log-message">{msg}</div>'

        log_html += """
            </div>
        </body>
        </html>
        """

        self.log_display.setHtml(log_html)
        # Scroll to bottom to show newest messages
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


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
        self.new_game_btn.clicked.connect(self.new_game)

        # Add shadow to new game button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.new_game_btn.setGraphicsEffect(shadow)

        # Replace explore button with new game button
        self.adventure_page.button_layout.addWidget(self.new_game_btn, 0, 0, 1, 2)


    def on_shop_item_clicked(self, item, action):
        if action == "buy":
            self.buy_item(item.name, item.value)

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
        """Trigger a random enemy encounter"""
        # Get a random enemy for this encounter
        from game.game import get_random_enemy
        self.current_enemy = get_random_enemy(self.hero.level)

        # Show combat interface
        self.show_combat_interface()

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
            animation.setEasingCurve(QEasingCurve.OutCubic)
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
        if not self.hero:
            return

        self.hero.health = self.hero.max_health
        self.update_stats_display()
        self.log_message("You rest and restore your health!")

    def quit_game(self):
        """Quit the game"""
        reply = QMessageBox.question(self, "Quit Game",
                                   "Are you sure you want to quit?",
                                   QMessageBox.Yes | QMessageBox.No)

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
        if self.hero.mana >= skill.mana_cost:
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
                self.hero.update_secondary_stats()

            # Consume stat point
            self.hero.stat_points -= 1

            # Update display
            self.update_stats_display()
            self.log_message(f"🏋️ Increased {stat_name}!")
        else:
            QMessageBox.information(self, "No Stat Points", "You have no available stat points to allocate.")

    def setup_keyboard_shortcuts(self):
        """Set up global keyboard shortcuts for the application"""
        # For now, keyboard shortcuts are disabled due to import issues
        # This would be implemented once we have proper shortcut import support
        pass

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
