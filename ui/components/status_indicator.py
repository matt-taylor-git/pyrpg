# -*- coding: utf-8 -*-
"""
Status effect visual indicators for combat
"""

from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QEasingCurve, Signal
from PySide6.QtGui import QFont


class StatusIndicator(QFrame):
    """Visual indicator for status effects like buffs/debuffs"""

    def __init__(self, effect_type, effect_name, duration=None, parent=None):
        super().__init__(parent)
        self.effect_type = effect_type
        self.effect_name = effect_name
        self.duration = duration
        self.remaining_time = duration

        self.init_ui()

        # Set up timer for duration countdown if applicable
        if duration and duration > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_duration)
            self.timer.start(1000)  # Update every second

    def update_duration(self):
        """Update the remaining duration and handle expiration"""
        if self.remaining_time is not None:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.expire_effect()
            else:
                self.update_display()

    def update_display(self):
        """Update the visual display of the status indicator"""
        # This can be overridden by subclasses for custom display updates
        pass

    def expire_effect(self):
        """Handle effect expiration"""
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.hide()
        # Emit signal or handle cleanup as needed

    def get_effect_colors(self):
        """Get colors based on effect type"""
        color_map = {
            'buff': {'bg': '#d4edda', 'border': '#27ae60'},
            'debuff': {'bg': '#f8d7da', 'border': '#e74c3c'},
            'heal': {'bg': '#d1ecf1', 'border': '#3498db'},
            'damage': {'bg': '#fff3cd', 'border': '#f39c12'},
            'default': {'bg': '#f8f9fa', 'border': '#6c757d'}
        }
        return color_map.get(self.effect_type, color_map['default'])

    def get_effect_icon(self):
        """Get icon/emoji based on effect type"""
        icon_map = {
            'buff': '💪',
            'debuff': '☠️',
            'heal': '❤️',
            'damage': '💥',
            'poison': '☠️',
            'strength': '💪',
            'defense': '🛡️',
            'speed': '⚡',
            'regeneration': '💚',
            'burn': '🔥',
            'freeze': '🧊',
            'stun': '💫',
            'default': '✨'
        }
        return icon_map.get(self.effect_type, icon_map['default'])

    def init_ui(self):
        """Initialize the status indicator UI"""
        self.setFixedSize(60, 60)
        self.setFrameShape(QFrame.Shape.Box)

        # Get colors based on effect type
        colors = self.get_effect_colors()

        self.setStyleSheet(f"""
            StatusIndicator {{
                background-color: {colors['bg']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # Icon/emoji
        icon_label = QLabel(self.get_effect_icon())
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_label)

        # Name (abbreviated if needed)
