# -*- coding: utf-8 -*-
"""
Custom, reusable UI widgets for the PyRPG application, styled to match the
modern look and feel of the React reference UI.
"""
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QProgressBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from .theme import Theme

class Card(QFrame):
    """A customizable card widget, serving as a base container for UI sections."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            Card {{
                background-color: {Theme.CARD.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 8px;
            }}
            Card:hover {{
                background-color: {Theme.MUTED.name()};
            }}
        """)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        self.main_layout.setSpacing(Theme.SPACING_MD)

    def setLayout(self, layout):
        # This is a convenience method to allow setting the layout directly on the card
        # while preserving the main_layout that holds the styling.
        content_widget = QWidget()
        content_widget.setLayout(layout)
        self.main_layout.addWidget(content_widget)

class StyledButton(QPushButton):
    """A button with variants using QSS object names for consistent styling."""
    def __init__(self, text, variant="default", size="default", parent=None):
        super().__init__(text, parent)
        self.setVariant(variant)  # Use proper method name
        self.setSize(size)        # Use proper method name
        self.setAccessibleName(text)  # For screen readers

        # Set proper focus policy for keyboard navigation
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setVariant(self, variant):
        """Sets the button's visual style using QSS object name targeting."""
        # Map friendly names to QSS object names
        variant_map = {
            "primary": "primary",
            "destructive": "destructive",
            "secondary": "secondary"
        }
        qss_name = variant_map.get(variant, "default")
        self.setObjectName(qss_name)

    def setSize(self, size):
        """Sets the button's size with theme constants."""
        size_configs = {
            "sm": {
                "width": Theme.SIZE_FACTOR_SM * Theme.PREFERRED_BUTTON_WIDTH,
                "height": Theme.SIZE_FACTOR_SM * Theme.PREFERRED_BUTTON_HEIGHT,
                "font_size": Theme.FONT_SIZE_SM,
                "padding": f"{Theme.SPACING_XS}px {Theme.SPACING_SM}px"
            },
            "lg": {
                "width": Theme.SIZE_FACTOR_LG * Theme.PREFERRED_BUTTON_WIDTH,
                "height": Theme.SIZE_FACTOR_LG * Theme.PREFERRED_BUTTON_HEIGHT,
                "font_size": Theme.FONT_SIZE_LG,
                "padding": f"{Theme.SPACING_MD}px {Theme.SPACING_LG}px"
            },
            "default": {
                "width": Theme.PREFERRED_BUTTON_WIDTH,
                "height": Theme.PREFERRED_BUTTON_HEIGHT,
                "font_size": Theme.FONT_SIZE_MD,
                "padding": f"{Theme.SPACING_SM}px {Theme.SPACING_MD}px"
            }
        }

        config = size_configs.get(size, size_configs["default"])

        self.setMinimumSize(int(config["width"]), int(config["height"]))
        self.setStyleSheet(f"""
            QPushButton {{
                padding: {config["padding"]};
                font-size: {config["font_size"]}px;
                min-width: {config["width"]}px;
                min-height: {config["height"]}px;
            }}
        """)

    def enterEvent(self, event):
        """Handle mouse entering button for enhanced hover effects"""
        super().enterEvent(event)
        # Could add tooltip delays or other visual feedback here

    def leaveEvent(self, event):
        """Handle mouse leaving button"""
        super().leaveEvent(event)
        # Reset any hover effects here


class Badge(QLabel):
    """A small label for displaying status or rarity."""
    def __init__(self, text, variant="default", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_variant(variant)

    def set_variant(self, variant):
        """Sets the badge's color scheme."""
        color_map = {
            "common": (Theme.MUTED, Theme.MUTED_FOREGROUND),
            "rare": (Theme.ACCENT, Theme.ACCENT_FOREGROUND),
            "epic": (Theme.PRIMARY, Theme.PRIMARY_FOREGROUND),
            "legendary": (Theme.PRIMARY, Theme.PRIMARY_FOREGROUND), # Same as epic for now
            "default": (Theme.SECONDARY, Theme.SECONDARY_FOREGROUND)
        }
        bg_color, fg_color = color_map.get(variant, color_map["default"])

        self.setStyleSheet(f"""
            Badge {{
                background-color: {bg_color.name()};
                color: {fg_color.name()};
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)

class StyledProgressBar(QProgressBar):
    """A progress bar with smooth animation and proper validation."""
    def __init__(self, variant="health", parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setTextVisible(True)
        self._cached_animation = None  # Cache animation instance
        self._is_animating = False
        self.set_variant(variant)

    def setValue(self, value):
        """Override to provide smooth animation and validation."""
        # Validate input range
        value = max(0, min(100, value))

        if self._is_animating:
            # Queue the new value if animation is in progress
            self._queued_value = value
            return

        self.animate_to_value(value)

    def animate_to_value(self, value):
        """Smoothly animate to a target value"""
        current_value = self.value()
        if current_value == value:
            return

        self._is_animating = True

        # Calculate animation duration based on value difference (longer changes take longer)
        value_diff = abs(value - current_value)
        duration = max(200, min(800, int(value_diff * 8)))  # Scale duration with difference

        if self._cached_animation:
            self._cached_animation.stop()

        # Cache and reuse animation for performance
        if not self._cached_animation:
            self._cached_animation = QPropertyAnimation(self, b"value")
            self._cached_animation.finished.connect(self._on_animation_finished)

        self._cached_animation.setDuration(duration)
        self._cached_animation.setStartValue(current_value)
        self._cached_animation.setEndValue(value)
        self._cached_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._cached_animation.start()

    def _on_animation_finished(self):
        """Handle animation completion"""
        self._is_animating = False
        # Check if there's a queued animation
        if hasattr(self, '_queued_value'):
            queued = self._queued_value
            delattr(self, '_queued_value')
            self.animate_to_value(queued)

    def setVariant(self, variant):
        """Properly named method for setting variant with QSS object name."""
        self.setObjectName(variant)
        self._apply_variant_styling(variant)

    def _apply_variant_styling(self, variant):
        """Apply styling based on variant."""
        chunk_colors = {
            "health": Theme.PRIMARY.name(),
            "mana": Theme.ACCENT.name(),
            "experience": Theme.MUTED_FOREGROUND.name()
        }

        chunk_color = chunk_colors.get(variant, Theme.PRIMARY.name())

        self.setStyleSheet(f"""
            QProgressBar#{variant} {{
                border: {Theme.BORDER_WIDTH_MEDIUM}px solid {Theme.BORDER.name()};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                text-align: center;
                font-weight: {Theme.FONT_WEIGHT_SEMIBOLD};
                font-size: {Theme.FONT_SIZE_SM}px;
                background-color: {Theme.MUTED.name()};
                color: {Theme.FOREGROUND.name()};
                height: 24px;
                padding: 2px;
            }}
            QProgressBar#{variant}::chunk {{
                background-color: {chunk_color};
                border-radius: {Theme.BORDER_RADIUS_SM}px;
            }}
        """)

    def set_variant(self, variant):
        """Sets the color of the progress bar chunk."""
        chunk_color = Theme.PRIMARY.name()
        if variant == "mana":
            chunk_color = Theme.ACCENT.name()
        elif variant == "experience":
            chunk_color = Theme.MUTED_FOREGROUND.name()

        self.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {Theme.BORDER.name()};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                text-align: center;
                font-weight: {Theme.FONT_WEIGHT_SEMIBOLD};
                font-size: {Theme.FONT_SIZE_SM}px;
                background-color: {Theme.MUTED.name()};
                color: {Theme.FOREGROUND.name()};
                height: 24px;
            }}
            QProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: {Theme.BORDER_RADIUS_SM}px;
            }}
        """)


class AnimationFactory:
    """Centralized factory for creating reusable animations"""

    @staticmethod
    def fade_animation(widget, start_opacity=1.0, end_opacity=0.0, duration=300):
        """Create a fade animation for a widget"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation

    @staticmethod
    def shake_animation(widget, duration=500, magnitude=10):
        """Create a shake animation for a widget"""
        original_pos = widget.pos()
        animation = QPropertyAnimation(widget, b"pos")

        # Create shake keyframes with simple left-right motion
        animation.setDuration(duration)
        animation.setKeyValueAt(0.0, original_pos)
        animation.setKeyValueAt(0.1, original_pos + QPoint(magnitude, 0))
        animation.setKeyValueAt(0.2, original_pos - QPoint(magnitude, 0))
        animation.setKeyValueAt(0.3, original_pos + QPoint(magnitude, 0))
        animation.setKeyValueAt(0.4, original_pos - QPoint(magnitude, 0))
        animation.setKeyValueAt(0.5, original_pos + QPoint(magnitude // 2, 0))
        animation.setKeyValueAt(0.6, original_pos - QPoint(magnitude // 2, 0))
        animation.setKeyValueAt(0.7, original_pos)
        animation.setKeyValueAt(1.0, original_pos)

        return animation

    @staticmethod
    def pulse_animation(widget, min_scale=0.95, max_scale=1.05, duration=800):
        """Create a pulsing scale animation"""
        # This would require more complex property animation setup
        # For now, return a simple opacity pulse
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setStartValue(1.0)
        animation.setEndValue(0.7)
        animation.setDuration(duration // 2)
        animation.setLoopCount(-1)  # Infinite loop
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        return animation

    @staticmethod
    def slide_animation(widget, start_pos, end_pos, duration=400):
        """Create a position slide animation"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation

    @staticmethod
    def color_flash_animation(widget, target_color, duration=300):
        """Create a flash animation by temporarily changing widget color"""
        original_style = widget.styleSheet()

        # Schedule the flash
        QTimer.singleShot(0, lambda: widget.setStyleSheet(f"{original_style}\nbackground-color: {target_color};"))
        QTimer.singleShot(duration, lambda: widget.setStyleSheet(original_style))
