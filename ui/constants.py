
class GameState:
    """Manages the current state of the game"""
    MENU = "menu"
    ADVENTURE = "adventure"
    COMBAT = "combat"
    SHOP = "shop"
    STATS = "stats"

class PageIndex:
    """Page indices for QTabWidget tabs"""
    ADVENTURE = 0
    COMBAT = 1
    STATS = 2
    INVENTORY = 3
    SHOP = 4
