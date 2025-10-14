import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import RPGGame

def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PyRPG Adventure")
    app.setApplicationVersion("1.0")

    # Create and show the game window
    game = RPGGame()
    game.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()