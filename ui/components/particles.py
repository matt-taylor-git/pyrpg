# -*- coding: utf-8 -*-
"""
Particle effects system for visual combat achievements
"""

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, Signal
from PySide6.QtGui import QPixmap
import random
import math


class Particle(QLabel):
    """Individual particle for visual effects"""

    def __init__(self, parent=None, particle_type="star", color="#dc3545"):
        super().__init__(parent)
        self.particle_type = particle_type
        self.color = color
        self._animations = []
        self.init_particle()

    def init_particle(self):
        """Initialize particle appearance"""
        self.setFixedSize(16, 16)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create particle based on type
        if self.particle_type == "star":
            self.setText("⭐")
        elif self.particle_type == "spark":
            self.setText("✨")
        elif self.particle_type == "coin":
            self.setText("💰")
        elif self.particle_type == "heart":
            self.setText("💚")
        else:
            self.setText("•")

        self.setStyleSheet(f"""
            color: {self.color};
            font-size: 12px;
            font-weight: bold;
        """)

    def animate(self, start_pos, end_pos, duration=1000):
        """Animate particle from start to end position"""
        self.move(start_pos)

        # Position animation
        anim = QPropertyAnimation(self, b"pos")
        anim.setStartValue(start_pos)
        anim.setEndValue(end_pos)
        anim.setDuration(int(duration))
        anim.setEasingCurve(QEasingCurve.Type.OutExpo)

        # Add some randomness to end position
        variance = QPoint(random.randint(-10, 10), random.randint(-10, 10))
        anim.setEndValue(end_pos + variance)

        # Fade out animation
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        fade_anim.setDuration(int(duration * 0.7))
        fade_anim.setEasingCurve(QEasingCurve.Type.InQuad)

        fade_anim.finished.connect(self.deleteLater)

        anim.start()
        fade_anim.start()

        # Keep references to prevent garbage collection
        self._animations = [anim, fade_anim]


class ParticleSystem(QWidget):
    """System to manage multiple particles for visual effects"""

    animation_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.particles = []

    def create_burst(self, center_pos, particle_count=12, particle_type="star", color="#dc3545"):
        """Create a particle burst effect at center position"""
        for i in range(particle_count):
            particle = Particle(self, particle_type, color)

            # Calculate position in circle
            angle = (i / particle_count) * 2 * math.pi
            radius = random.randint(30, 80)
            end_x = center_pos.x() + int(math.cos(angle) * radius)
            end_y = center_pos.y() + int(math.sin(angle) * radius)

            start_pos = center_pos - QPoint(8, 8)  # Center the particle
            end_pos = QPoint(end_x, end_y) - QPoint(8, 8)

            duration = random.randint(800, 1200)
            particle.animate(start_pos, end_pos, duration)
            self.particles.append(particle)

        # Clean up after animation completes
        QTimer.singleShot(1500, self.cleanup)

    def cleanup(self):
        """Clean up finished particles"""
        self.particles.clear()
        self.animation_finished.emit()

    def victory_explosion(self, center_pos):
        """Create victory explosion effect"""
        # Gold stars
        self.create_burst(center_pos, 8, "star", "#e5c07b")
        # Victory sparks
        QTimer.singleShot(200, lambda: self.create_burst(center_pos, 6, "spark", "#98c379"))

    def healing_burst(self, center_pos):
        """Create healing burst effect"""
        self.create_burst(center_pos, 10, "heart", "#27ae60")

    def level_up_burst(self, center_pos):
        """Create level up particle burst"""
        self.create_burst(center_pos, 15, "star", "#c678dd")

    def gold_reward_burst(self, center_pos):
        """Create gold reward effect"""
        self.create_burst(center_pos, 8, "coin", "#e5c07b")


class AchievementSystem:
    """Manages achievement notifications and particle effects"""

    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.particle_system = ParticleSystem(parent_widget)
        self.particle_system.animation_finished.connect(self.on_particles_finished)
        self.text_animations = []

    def trigger_achievement(self, achievement_type, position):
        """Trigger a visual achievement effect"""
        if achievement_type == "victory":
            self.particle_system.victory_explosion(position)
            self.show_achievement_text("Victory!", position, "#98c379")
        elif achievement_type == "level_up":
            self.particle_system.level_up_burst(position)
            self.show_achievement_text("Level Up!", position, "#c678dd")
        elif achievement_type == "critical_hit":
            self.particle_system.create_burst(position, 6, "spark", "#e74c3c")
            self.show_achievement_text("Critical!", position, "#e74c3c")
        elif achievement_type == "healing":
            self.particle_system.healing_burst(position)
            self.show_achievement_text("Healed!", position, "#27ae60")

    def show_achievement_text(self, text, position, color):
        """Show floating achievement text"""
        label = QLabel(text, self.parent)
        label.setStyleSheet(f"""
            color: {color};
            font-size: 16px;
            font-weight: bold;
            background: rgba(0, 0, 0, 0);
            border: none;
        """)

        # Position above the effect
        text_pos = position - QPoint(label.fontMetrics().horizontalAdvance(text)//2, 50)
        label.move(text_pos)
        label.show()

        # Animate text floating up and fading
        anim = QPropertyAnimation(label, b"pos")
        anim.setStartValue(text_pos)
        anim.setEndValue(text_pos - QPoint(0, 30))
        anim.setDuration(2000)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        fade_anim = QPropertyAnimation(label, b"windowOpacity")
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        fade_anim.setDuration(2000)

        fade_anim.finished.connect(label.deleteLater)

        anim.start()
        fade_anim.start()

        # Store references to prevent garbage collection
        self.text_animations.append(anim)
        self.text_animations.append(fade_anim)

    def on_particles_finished(self):
        """Handle particle animation completion"""
        # Could trigger additional effects or cleanup here
        pass
