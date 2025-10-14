
from PySide6.QtWidgets import QProgressBar, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPixmap

class AnimatedProgressBar(QProgressBar):
    """Progress bar with smooth animation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = None

    def setValue(self, value):
        """Override setValue to add smooth animation"""
        if self._animation:
            self._animation.stop()

        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(500)  # 500ms animation
        self._animation.setStartValue(self.value())
        self._animation.setEndValue(value)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.start()

class ShadowedProgressBar(AnimatedProgressBar):
    """A progress bar that draws text with a shadow for better contrast."""
    def paintEvent(self, event):
        # First, draw the progress bar as usual but without the text
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        text = self.text()
        text_rect = self.rect()

        # Draw the shadow/outline
        painter.setPen(QColor('#1e2228'))
        painter.drawText(text_rect.translated(1, 1), Qt.AlignCenter, text)

        # Draw the main text
        painter.setPen(QColor('#ffffff'))
        painter.drawText(text_rect, Qt.AlignCenter, text)

class ScalablePixmapLabel(QLabel):
    """A QLabel that scales its pixmap while maintaining aspect ratio."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_pixmap = None
        self.setMinimumSize(150, 150) # Set a minimum size for the sprite
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setOriginalPixmap(self, pixmap):
        """Set the original, full-resolution pixmap."""
        self._original_pixmap = pixmap
        self.update_pixmap(self.size())

    def resizeEvent(self, event):
        """Handle the widget being resized by rescaling the pixmap."""
        if self._original_pixmap:
            self.update_pixmap(event.size())
        super().resizeEvent(event)

    def update_pixmap(self, size):
        """Scale the original pixmap to fit the new size and set it."""
        if not self._original_pixmap:
            return
        scaled_pixmap = self._original_pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
