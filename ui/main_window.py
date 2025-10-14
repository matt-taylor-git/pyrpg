# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTextEdit,
                               QGridLayout, QGroupBox, QInputDialog, QMessageBox,
                               QProgressBar, QListWidget, QListWidgetItem, QGraphicsDropShadowEffect,
                               QStackedWidget, QScrollArea, QFrame, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPropertyAnimation, QEasingCurve, QPoint, Property
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap
import random
import time
from game.models import Hero, Enemy
from game.game import random_encounter, get_shop_items, apply_item_effects, handle_player_turn, handle_enemy_turn
from ui_components import ItemCard, ItemSelectionOverlay, CharacterCreationOverlay
from .constants import GameState, PageIndex
from .custom_widgets import AnimatedProgressBar, ShadowedProgressBar, ScalablePixmapLabel
from .views.adventure_page import AdventurePage
from .views.stats_page import StatsPage
from .views.inventory_page import InventoryPage
from .views.shop_page import ShopPage
from .views.combat_page import CombatPage

class RPGGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hero = None
        self.current_state = GameState.MENU
        self.current_enemy = None
        self.game_log = []
        self.animations = []  # Store active animations
        self.init_ui()

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
        # Scale font size of the log display based on window height
        font_size = max(8, min(18, int(self.height() / 50)))
        font = self.log_display.font()
        font.setPointSize(font_size)
        self.log_display.setFont(font)


    def init_ui(self):
        """Initialize the enhanced user interface with modern design"""
        self.setWindowTitle("PyRPG Adventure")
        self.resize(1200, 750)
        self.setMinimumSize(800, 600)

        # Modern dark theme inspired by professional applications
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282c34;
                color: #abb2bf;
                font-family: 'Inter', 'SF Pro Display', 'Segoe UI', sans-serif;
            }

            /* Professional Button Styling */
            QPushButton {
                color: #abb2bf;
                background-color: #282c34;
                border: 1px solid #3e4452;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3e4452;
            }
            QPushButton:pressed {
                background-color: #4b5263;
            }

            /* Primary Action Buttons */
            QPushButton#explore_btn,
            QPushButton#shop_btn,
            QPushButton#stats_btn,
            QPushButton#rest_btn {
                background-color: #282c34;
                border: 1px solid #61afef;
                color: #61afef;
                padding: 10px 24px;
                font-weight: 500;
            }
            QPushButton#explore_btn:hover,
            QPushButton#shop_btn:hover,
            QPushButton#stats_btn:hover,
            QPushButton#rest_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }

            QPushButton#quit_btn {
                background-color: #282c34;
                border: 1px solid #e06c75;
                color: #e06c75;
            }
            QPushButton#quit_btn:hover {
                background-color: #3e4452;
            }

            /* Combat Buttons */
            QPushButton#attack_btn {
                background-color: #282c34;
                color: #e06c75;
                font-size: 15px;
                font-weight: 600;
                padding: 12px 28px;
                border: 1px solid #e06c75;
                border-radius: 4px;
            }
            QPushButton#attack_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }

            QPushButton#run_btn {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4452;
            }
            QPushButton#run_btn:hover {
                background-color: #3e4452;
            }

            /* Professional GroupBox */
            QGroupBox {
                color: #98c379;
                border: 1px solid #3e4452;
                border-radius: 5px;
                margin-top: 1ex;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #98c379;
            }

            /* Text Display */
            QTextEdit {
                background-color: #21252b;
                color: #abb2bf;
                border: 1px solid #3e4452;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Inter', 'SF Pro Display', 'Segoe UI', sans-serif;
                selection-background-color: #3e4452;
            }

            /* Progress Bars */
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                text-align: center;
                font-weight: 600;
                font-size: 11px;
                background-color: #21252b;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #61afef;
            }

            /* Label Styling */
            QLabel {
                color: #abb2bf;
                font-size: 13px;
            }

            /* Sidebar Navigation */
            QListWidget {
                background-color: #21252b;
                color: #abb2bf;
                border: none;
                border-right: 1px solid #3e4452;
                font-size: 15px;
                padding: 10px 0;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-left: 3px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #282c34;
            }
            QListWidget::item:selected {
                background-color: #282c34;
                color: #61afef;
                border-left-color: #61afef;
            }

            /* Combat Info Card */
            QLabel#combat_info {
                background-color: #21252b;
                border: 1px solid #3e4452;
                border-radius: 5px;
                padding: 15px;
                font-size: 13px;
                color: #abb2bf;
            }

            /* Stats Labels */
            QLabel#health_label,
            QLabel#mana_label {
                color: #abb2bf;
                font-weight: 600;
                font-size: 13px;
            }
            QLabel#attack_label {
                color: #e06c75;
                font-weight: 600;
                font-size: 12px;
            }
            QLabel#defense_label {
                color: #61afef;
                font-weight: 600;
                font-size: 12px;
            }
            QLabel#gold_label {
                color: #e5c07b;
                font-weight: 600;
                font-size: 12px;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Game log (top section) - Enhanced with better styling
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        welcome_msg = """
        <div style='text-align: center; padding: 10px; font-size: 14px;'>
            <span style='color: #61afef; font-weight: bold; font-size: 16px;'>\u2694\ufe0f Welcome to PyRPG Adventure! \u2694\ufe0f</span><br>
            <span style='color: #abb2bf; font-size: 11px;'>Embark on an epic quest filled with danger and glory!</span>
        </div>
        """
        self.log_display.setHtml(welcome_msg)
        self.main_layout.addWidget(self.log_display, 1) # Add with stretch factor

        # Main content area: Sidebar + Stacked Widget
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar navigation
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setFocusPolicy(Qt.NoFocus)
        content_layout.addWidget(self.sidebar)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget, 1)  # Stretch factor 1

        self.main_layout.addLayout(content_layout, 4)  # Add with stretch factor

        # Create and add pages
        self.adventure_page = AdventurePage()
        self.stats_page = StatsPage()
        self.inventory_page = InventoryPage()
        self.shop_page = ShopPage()
        self.combat_page = CombatPage()

        self.stacked_widget.addWidget(self.adventure_page)
        self.stacked_widget.addWidget(self.stats_page)
        self.stacked_widget.addWidget(self.inventory_page)
        self.stacked_widget.addWidget(self.shop_page)
        self.stacked_widget.addWidget(self.combat_page)

        # Setup sidebar items
        self.sidebar.addItem("🏠 Adventure")
        self.sidebar.addItem("📊 Stats")
        self.sidebar.addItem("🎒 Inventory")
        self.sidebar.addItem("🏪 Shop")

        # Connect sidebar to page switching
        self.sidebar.currentRowChanged.connect(self.on_sidebar_changed)

        # Connect adventure page buttons
        self.adventure_page.explore_btn.clicked.connect(self.explore)
        self.adventure_page.rest_btn.clicked.connect(self.rest)
        self.adventure_page.quit_btn.clicked.connect(self.quit_game)

        # Connect combat page buttons
        self.combat_page.attack_btn.clicked.connect(self.combat_attack)
        self.combat_page.use_skill_btn.clicked.connect(self.combat_use_skill)
        self.combat_page.use_item_btn.clicked.connect(self.combat_use_item)
        self.combat_page.run_btn.clicked.connect(self.combat_run)

        # Connect shop page buttons and item cards
        for card in self.shop_page.item_cards:
            card.action_clicked.connect(self.on_shop_item_clicked)
        self.shop_page.sell_btn.clicked.connect(self.sell_items)
        self.shop_page.leave_btn.clicked.connect(self.leave_shop)

        # Start with adventure page selected
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)

        self.show_menu()

    def on_sidebar_changed(self, index):
        """Handle sidebar selection changes"""
        # Only allow navigation if hero exists (except for adventure page which shows menu)
        if not self.hero and index != PageIndex.ADVENTURE:
            self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
            return

        # Update the stacked widget
        self.stacked_widget.setCurrentIndex(index)

        # Update stats display when switching pages
        if self.hero:
            self.update_stats_display()

    def log_message(self, message):
        """Add a message to the game log with color coding"""
        self.game_log.append(message)
        # Keep only last 20 messages
        if len(self.game_log) > 20:
            self.game_log = self.game_log[-20:]

        # Build HTML with color-coded messages (newest at bottom)
        log_html = "<div style='padding: 5px; line-height: 1.6;'>"
        for msg in self.game_log[-10:]:  # Show last 10 messages in correct order
            # Color code based on message content
            color = "#e8e8e8"  # default

            if "damage" in msg.lower() or "defeated" in msg.lower() or "\U0001f4a5" in msg or "\u2694\ufe0f" in msg:
                color = "#e06c75"  # red for damage/combat
            elif "gold" in msg.lower() or "\U0001f4b0" in msg:
                color = "#e5c07b"  # gold/yellow color
            elif "experience" in msg.lower() or "level" in msg.lower() or "\u2b50\ufe0f" in msg or "\U0001f389" in msg:
                color = "#c678dd"  # purple for XP/level
            elif "heal" in msg.lower() or "restored" in msg.lower() or "rest" in msg.lower():
                color = "#98c379"  # green for healing
            elif "found" in msg.lower() or "\U0001f4e6" in msg:
                color = "#61afef"  # blue for items
            elif "welcome" in msg.lower() or "===" in msg:
                color = "#61afef"  # blue for welcome messages
            elif "failed" in msg.lower() or "\u274c" in msg or "\U0001f480" in msg:
                color = "#e06c75"  # red for failures
            elif "escape" in msg.lower() or "\U0001f3c3" in msg:
                color = "#abb2bf"  # gray for escape

            log_html += f"<div style='color: {color}; margin: 2px 0;'>{msg}</div>"
        log_html += "</div>"

        self.log_display.setHtml(log_html)
        # Scroll to bottom to show newest messages
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def handle_event(self, event):
        """Processes a game event and logs a message."""
        event_type = event.get('type')
        params = event
        
        message = ""
        if event_type == 'critical_hit':
            message = "\U0001f4a5 Critical hit!"
        elif event_type == 'player_damage':
            message = f"\u2694\ufe0f You deal {params['damage']} damage to {params['target']}!"
            self.shake_widget(self.combat_page.enemy_sprite_label)
        elif event_type == 'player_miss':
            message = f"\U0001f6e1\ufe0f {params['target']} dodges your attack!"
        elif event_type == 'enemy_defeated':
            message = f"\U0001f389 You defeated the {params['enemy_name']}!"
        elif event_type == 'gain_experience':
            message = f"\u2b50\ufe0f Gained {params['amount']} experience!"
        elif event_type == 'gain_gold':
            message = f"\U0001f4b0 Gained {params['amount']} gold!"
        elif event_type == 'level_up':
            message = params['message']
        elif event_type == 'item_drop':
            message = f"\U0001f4e6 Found {params['item_name']} ({params['rarity']})!"
        elif event_type == 'escape_success':
            message = "\U0001f3c3 You successfully escaped!"
        elif event_type == 'escape_fail':
            message = "\u274c Failed to escape!"
        elif event_type == 'enemy_miss':
            message = f"\U0001f6e1\ufe0f {params['enemy_name']} attacks, but you dodge!"
        elif event_type == 'enemy_damage':
            message = f"\U0001f4a5 {params['enemy_name']} deals {params['damage']} damage to you!"
            self.shake_widget(self.combat_page.hero_sprite_label)
        elif event_type == 'player_defeated':
            message = "\U0001f480 You have been defeated..."
        elif event_type == 'status_effect_damage':
            message = f"\u2620\ufe0f You take {params['damage']} damage from status effects!"
        elif event_type == 'use_skill':
            message = f"\u2728 You used {params['skill_name']}!"

        if message:
            self.log_message(message)

    def show_menu(self):
        """Show the main menu"""
        self.current_state = GameState.MENU
        self.log_message("=== Welcome to PyRPG Adventure! ===")
        self.log_message("Click 'New Game' to start your adventure!")

        # Ensure we're on adventure page
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)

        # Hide existing game buttons
        self.adventure_page.explore_btn.hide()
        self.adventure_page.rest_btn.hide()

        # Show new game button with professional styling
        self.new_game_btn = QPushButton("🎮 New Game")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                border: 2px solid #61afef;
                color: #61afef;
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

    def new_game(self):
        """Start a new game using character creation overlay"""
        # Create character creation overlay
        overlay = CharacterCreationOverlay(self)
        overlay.character_created.connect(self.on_character_created)
        overlay.show()

    def on_character_created(self, hero_name):
        """Handle character creation completion"""
        self.hero = Hero(hero_name)
        self.current_state = GameState.ADVENTURE

        # Remove new game button and show game buttons
        if hasattr(self, 'new_game_btn') and self.new_game_btn:
            self.adventure_page.button_layout.removeWidget(self.new_game_btn)
            self.new_game_btn.deleteLater()
            self.new_game_btn = None

        self.adventure_page.explore_btn.show()
        self.adventure_page.rest_btn.show()

        self.update_stats_display()
        self.log_message(f"Welcome, {hero_name}!")
        self.log_message("Your adventure begins now!")

    def update_stats_display(self):
        """Update the stats display with current hero stats"""
        if not self.hero:
            return

        # Update adventure page stats
        self.adventure_page.name_label.setText(f"Name: {self.hero.name}")
        self.adventure_page.level_label.setText(f"Level: {self.hero.level}")
        self.adventure_page.attack_label.setText(f"\u2694\ufe0f Attack: {self.hero.attack_power}")
        self.adventure_page.defense_label.setText(f"\U0001f6e1\ufe0f Defense: {self.hero.defense}")
        self.adventure_page.gold_label.setText(f"\U0001f4b0 Gold: {self.hero.gold}")

        # Update progress bars
        health_percent = int((self.hero.health / self.hero.max_health) * 100)
        self.adventure_page.health_bar.setValue(health_percent)
        self.adventure_page.health_bar.setFormat(f"{self.hero.health}/{self.hero.max_health} HP")

        exp_percent = int((self.hero.experience / self.hero.experience_to_level) * 100)
        self.adventure_page.exp_bar.setValue(exp_percent)
        self.adventure_page.exp_bar.setFormat(f"{self.hero.experience}/{self.hero.experience_to_level} XP")

        # Update equipment labels
        self.adventure_page.weapon_label.setText(f"\U0001f5e1\ufe0f Weapon: {self.hero.equipment['weapon'].name if self.hero.equipment['weapon'] else 'None'}")
        self.adventure_page.armor_label.setText(f"\U0001f6e1\ufe0f Armor: {self.hero.equipment['armor'].name if self.hero.equipment['armor'] else 'None'}")
        self.adventure_page.accessory_label.setText(f"\U0001f48d Accessory: {self.hero.equipment['accessory'].name if self.hero.equipment['accessory'] else 'None'}")

        # Show inventory
        if self.hero.inventory:
            inv_items = [item.name for item in self.hero.inventory[:3]]
            inventory_text = f"\U0001f392 Inventory: {', '.join(inv_items)}"
            if len(self.hero.inventory) > 3:
                inventory_text += f" (+{len(self.hero.inventory) - 3} more)"
        else:
            inventory_text = "\U0001f392 Inventory: Empty"

        self.adventure_page.inventory_label.setText(inventory_text)

        # Update detailed stats page
        stats_html = self.format_stats_html()
        self.stats_page.detailed_stats_label.setText(stats_html)

        # Update gold labels on other pages
        self.shop_page.shop_gold_label.setText(f"\U0001f4b0 Gold: {self.hero.gold}")
        self.inventory_page.inventory_gold_label.setText(f"\U0001f4b0 Gold: {self.hero.gold}")

        # Update inventory grid
        self.update_inventory_grid()

        # Color code progress bars based on health percentage
        if health_percent > 60:
            self.adventure_page.health_bar.setStyleSheet("""
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
        elif health_percent > 25:
            self.adventure_page.health_bar.setStyleSheet("""
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
                    background-color: #e5c07b;
                    width: 10px;
                    margin: 0.5px;
                }
            """)
        else:
            self.adventure_page.health_bar.setStyleSheet("""
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
                    background-color: #e06c75;
                    width: 10px;
                    margin: 0.5px;
                }
            """)

    def format_stats_html(self):
        """Format hero stats as HTML for detailed stats page"""
        if not self.hero:
            return "No character created yet"

        return f"""
<div style='line-height: 1.6;'>
    <h2 style='color: #61afef; border-bottom: 2px solid #3e4452; padding-bottom: 10px;'>\u2694\ufe0f {self.hero.name}</h2>

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

    <h3 style='color: #61afef; margin-top: 20px;'>\u2694\ufe0f Combat Stats</h3>
    <div style='margin-left: 15px;'>
        <p><b>Attack Power:</b> <span style='color: #e06c75;'>{self.hero.attack_power}</span></p>
        <p><b>Magic Power:</b> <span style='color: #c678dd;'>{self.hero.magic_power:.1f}</span></p>
        <p><b>Defense:</b> <span style='color: #61afef;'>{self.hero.defense}</span></p>
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

    def update_inventory_grid(self):
        """Update the inventory grid with current items"""
        # Clear existing items
        while self.inventory_page.inventory_grid_layout.count():
            item = self.inventory_page.inventory_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.hero or not self.hero.inventory:
            # Show empty state
            self.inventory_page.inventory_empty_label = QLabel("No items in inventory\n\nDefeat enemies and visit the shop to collect items!")
            self.inventory_page.inventory_empty_label.setStyleSheet("""
                font-size: 14px;
                color: #abb2bf;
                padding: 40px;
            """)
            self.inventory_page.inventory_empty_label.setAlignment(Qt.AlignCenter)
            self.inventory_page.inventory_grid_layout.addWidget(self.inventory_page.inventory_empty_label, 0, 0, Qt.AlignCenter)
            return

        # Create item cards
        row = 0
        col = 0
        max_cols = 4

        for item in self.hero.inventory:
            # Determine action based on item type
            if item.item_type == 'consumable':
                action_text = "Use"
            else:
                action_text = "Equip"

            card = ItemCard(item, action_text=action_text, show_price=False)
            card.action_clicked.connect(self.on_inventory_item_clicked)
            self.inventory_page.inventory_grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def on_shop_item_clicked(self, item, action):
        """Handle shop item card clicks"""
        if action.lower() == "buy":
            self.buy_item(item.name, item.value)

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
        self.stacked_widget.setCurrentIndex(PageIndex.COMBAT)

        # Re-enable combat buttons for new fight
        self.set_combat_buttons_enabled(True)

        # Update names
        self.combat_page.hero_combat_name.setText(f"{self.hero.name} (Lv.{self.hero.level})")
        self.combat_page.enemy_combat_name.setText(f"{self.current_enemy.name} (Lv.{self.current_enemy.level})")

        # Update sprites
        hero_sprite = QPixmap("assets/Hero.png")
        
        enemy_sprite_map = {
            'warrior': "assets/Orc.png",
            'mage': "assets/mage.png",
            'rogue': "assets/rogue.png",
            'tank': "assets/golem.png"
        }
        enemy_sprite_path = enemy_sprite_map.get(self.current_enemy.enemy_type, "assets/Orc.png")
        enemy_sprite = QPixmap(enemy_sprite_path)

        self.combat_page.hero_sprite_label.setOriginalPixmap(hero_sprite)
        self.combat_page.enemy_sprite_label.setOriginalPixmap(enemy_sprite)

        # Update health bars
        self.combat_page.hero_combat_health_bar.setRange(0, self.hero.max_health)
        self.combat_page.hero_combat_health_bar.setValue(self.hero.health)
        self.combat_page.hero_combat_health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health}")

        self.combat_page.hero_combat_mana_bar.setRange(0, self.hero.max_mana)
        self.combat_page.hero_combat_mana_bar.setValue(self.hero.mana)
        self.combat_page.hero_combat_mana_bar.setFormat(f"{self.hero.mana} / {self.hero.max_mana}")

        self.combat_page.enemy_combat_health_bar.setRange(0, self.current_enemy.max_health)
        self.combat_page.enemy_combat_health_bar.setValue(self.current_enemy.health)
        self.combat_page.enemy_combat_health_bar.setFormat(f"{self.current_enemy.health} / {self.current_enemy.max_health}")

        self.log_message(f"A wild {self.current_enemy.name} (Lv.{self.current_enemy.level}) appears!")

    def hide_combat_interface(self):
        """Hide combat interface and return to adventure"""
        self.stacked_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
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
        """Update all combat UI elements."""
        self.combat_page.hero_combat_health_bar.setValue(self.hero.health)
        self.combat_page.hero_combat_health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health}")
        self.combat_page.hero_combat_mana_bar.setValue(self.hero.mana)
        self.combat_page.hero_combat_mana_bar.setFormat(f"{self.hero.mana} / {self.hero.max_mana}")
        self.combat_page.enemy_combat_health_bar.setValue(self.current_enemy.health)
        self.combat_page.enemy_combat_health_bar.setFormat(f"{self.current_enemy.health} / {self.current_enemy.max_health}")
        self.update_stats_display()

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
        self.stacked_widget.setCurrentIndex(PageIndex.SHOP)
        self.sidebar.setCurrentRow(PageIndex.SHOP)

        self.log_message(f"You have {self.hero.gold} gold to spend!")

    def leave_shop(self):
        """Leave the shop"""
        self.current_state = GameState.ADVENTURE
        self.stacked_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
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
                        self.log_message(f"🧪 {message}")
                        self.hero.remove_item(item)  # Remove after using

                self.update_stats_display()
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

        # Navigate to stats page
        self.stacked_widget.setCurrentIndex(PageIndex.STATS)
        self.sidebar.setCurrentRow(PageIndex.STATS)

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

        if reply == QMessageBox.Yes:
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

        # Enemy gets a turn after using item
        self.process_combat_round("use_item")