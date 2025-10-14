
class GameState:
    """Manages the current state of the game"""
    MENU = "menu"
    ADVENTURE = "adventure"
    COMBAT = "combat"
    SHOP = "shop"
    STATS = "stats"

class PageIndex:
    """Page indices for QStackedWidget"""
    ADVENTURE = 0
    STATS = 1
    INVENTORY = 2
    SHOP = 3
    COMBAT = 4
