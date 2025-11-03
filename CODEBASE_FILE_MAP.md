# Codebase File Map - Dialog & Overlay Patterns

## Quick File Reference with Absolute Paths

### QDialog Examples

#### 1. CombatResultDialog
**Absolute Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/CombatResultDialog.h`
**Also**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/CombatResultDialog.cpp`

**Purpose**: Victory/Defeat screen after combat

**Key Code Snippet**:
```cpp
// Header
class CombatResultDialog : public QDialog {
    Q_OBJECT
public:
    explicit CombatResultDialog(bool victory, int expGained, int goldGained,
                                const QString &lootMessage, bool leveledUp,
                                QWidget *parent = nullptr);
private:
    void setupUi(bool victory, int expGained, int goldGained,
                 const QString &lootMessage, bool leveledUp);
};

// Constructor
CombatResultDialog::CombatResultDialog(bool victory, int expGained, int goldGained,
                                       const QString &lootMessage, bool leveledUp,
                                       QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle(victory ? "Victory!" : "Defeat");
    setMinimumWidth(400);
    setupUi(victory, expGained, goldGained, lootMessage, leveledUp);
}
```

**Theme Constants Used**:
- `Theme::ACCENT` - Victory title color
- `Theme::DESTRUCTIVE` - Defeat title color
- `Theme::FOREGROUND` - Text color
- `Theme::CARD` - Background
- `Theme::BORDER` - Border color
- `Theme::PRIMARY_FOREGROUND` - Button text

**Integration Point** (MainWindow):
```cpp
void MainWindow::handleCombatEnded(bool playerWon) {
    if (playerWon) {
        CombatResultDialog resultDialog(
            true,
            monster ? monster->expReward : 0,
            monster ? monster->goldReward : 0,
            "Iron Sword acquired",
            leveledUp,
            this
        );
        resultDialog.exec();  // BLOCKING CALL
    }
}
```

---

#### 2. QuestCompletionDialog
**Absolute Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/QuestCompletionDialog.h`
**Also**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/QuestCompletionDialog.cpp`

**Purpose**: Display quest completion rewards

**Key Differences from CombatResultDialog**:
- More flexible reward display (exp, gold, items)
- Celebration emoji header
- List-based reward formatting

**Constructor Signature**:
```cpp
explicit QuestCompletionDialog(const QString &questTitle, int expGained,
                               int goldGained, const QList<QString> &itemNames,
                               QWidget *parent = nullptr);
```

**Sample Usage**:
```cpp
QuestCompletionDialog dialog("Defeat the Dark Lord", 500, 200, 
                             QList<QString>{"Legendary Sword", "Ring of Power"}, 
                             this);
dialog.exec();
```

---

#### 3. StoryEventDialog (Advanced Pattern)
**Absolute Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/views/StoryEventDialog.h`
**Also**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/views/StoryEventDialog.cpp`

**Purpose**: Display narrative story moments with rich content

**Advanced Features Implemented**:
```cpp
class StoryEventDialog : public QDialog {
    Q_OBJECT
public:
    explicit StoryEventDialog(const StoryEvent &event, QWidget *parent = nullptr);
protected:
    void keyPressEvent(QKeyEvent *event) override;
private:
    void setupUi(const StoryEvent &event);
    qint64 m_eventStartTime;  // Timing validation
};

// Constructor shows advanced setup
StoryEventDialog::StoryEventDialog(const StoryEvent &event, QWidget *parent)
    : QDialog(parent)
{
    setModal(true);
    setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);  // Frameless!
    setMinimumSize(700, 500);
    m_eventStartTime = QDateTime::currentMSecsSinceEpoch();
    setupUi(event);
}

// Input validation: Prevent accidental skip
void StoryEventDialog::keyPressEvent(QKeyEvent *event) {
    qint64 elapsed = QDateTime::currentMSecsSinceEpoch() - m_eventStartTime;
    if (elapsed < 1000) return;  // Ignore for 1 second
    
    if (event->key() == Qt::Key_Escape || 
        event->key() == Qt::Key_Return || 
        event->key() == Qt::Key_Space) {
        accept();
        return;
    }
    QDialog::keyPressEvent(event);
}
```

**Integration with MainWindow**:
```cpp
void MainWindow::handleStoryEventTriggered(const StoryEvent &event) {
    StoryEventDialog dialog(event, this);
    dialog.exec();  // Shows modally
}
```

**StoryEvent Model**:
```cpp
// Located in /cpp-qt-rpg/src/models/StoryEvent.h
struct StoryEvent {
    QString title;      // Large title text
    QString eventText;  // Full narrative content
    QString type;       // Event type identifier
};
```

---

### Custom Overlay Pattern

#### MenuOverlay (Full-Screen Pattern Example)
**Absolute Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/MenuOverlay.h`
**Also**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/MenuOverlay.cpp`

**Purpose**: Full-screen game menu with tabbed interface

**Key Architecture**:
```cpp
class MenuOverlay : public QWidget {  // NOTE: QWidget, not QDialog!
    Q_OBJECT
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)  // Animatable!

public:
    explicit MenuOverlay(QWidget *parent = nullptr);
    void showOverlay();
    void hideOverlay();
    void updateContent(Player *player);
    
    qreal opacity() const { return m_opacity; }
    void setOpacity(qreal opacity);  // Called by animation

signals:
    void overlayHidden();
    void saveRequested();
    void loadRequested();

protected:
    void paintEvent(QPaintEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;

private:
    QWidget *m_contentWidget;
    QTabWidget *m_tabWidget;
    QPropertyAnimation *m_animation;  // Opacity animation
    qreal m_opacity;
    QWidget *m_previousFocusWidget;
};
```

**Constructor Implementation**:
```cpp
MenuOverlay::MenuOverlay(QWidget *parent)
    : QWidget(parent)
    , m_opacity(0.0)
    , m_currentPlayer(nullptr)
    , m_previousFocusWidget(nullptr)
{
    // Enable custom rendering
    setAttribute(Qt::WA_TransparentForMouseEvents, false);
    setAttribute(Qt::WA_NoSystemBackground);
    setAttribute(Qt::WA_TranslucentBackground);
    setFocusPolicy(Qt::StrongFocus);

    setupUi();

    // Create animation
    m_animation = new QPropertyAnimation(this, "opacity");
    m_animation->setDuration(200);

    // Handle animation completion
    connect(m_animation, &QPropertyAnimation::finished, this, [this]() {
        if (m_animation->endValue().toReal() == 0.0) {
            hide();
            if (m_previousFocusWidget) m_previousFocusWidget->setFocus();
            emit overlayHidden();
        }
    });

    hide();
}
```

**Show/Hide Animation**:
```cpp
void MenuOverlay::showOverlay() {
    m_animation->stop();
    m_previousFocusWidget = QApplication::focusWidget();
    show();
    raise();
    setFocus();
    
    m_animation->setStartValue(0.0);
    m_animation->setEndValue(1.0);
    m_animation->start();  // Fade in
}

void MenuOverlay::hideOverlay() {
    if (m_animation->state() == QAbstractAnimation::Running &&
        m_animation->endValue().toReal() == 0.0) {
        return;  // Already hiding
    }
    
    m_animation->setStartValue(m_opacity);
    m_animation->setEndValue(0.0);
    m_animation->start();  // Fade out
}
```

**Semi-Transparent Background**:
```cpp
void MenuOverlay::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Draw darkening overlay with animated opacity
    QColor overlayColor = QColor(0, 0, 0);
    overlayColor.setAlphaF(0.7 * m_opacity);  // 0.7 = 70% opacity at full animation
    painter.fillRect(rect(), overlayColor);
}
```

**Event Handling**:
```cpp
void MenuOverlay::keyPressEvent(QKeyEvent *event) {
    if (event->key() == Qt::Key_Escape) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::keyPressEvent(event);
    }
}

void MenuOverlay::mousePressEvent(QMouseEvent *event) {
    // Close if clicking outside content widget
    if (!m_contentWidget->geometry().contains(event->pos())) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::mousePressEvent(event);
    }
}
```

**MainWindow Integration**:
```cpp
// In MainWindow.h
class MainWindow : public QMainWindow {
    // ...
private:
    MenuOverlay *m_menuOverlay;
};

// In MainWindow constructor
m_menuOverlay = new MenuOverlay(this);

// When menu button pressed
void MainWindow::handleMenuButtonClicked() {
    m_menuOverlay->updateContent(m_game->player());
    m_menuOverlay->showOverlay();  // Animated fade-in
}
```

---

### Theme System

**Absolute Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/theme/Theme.h`

**Header-Only namespace** containing all design system constants:

```cpp
namespace Theme {
    // Color Palette (Semantic naming)
    const QColor BACKGROUND = QColor("#1a1826");      // Dark purple
    const QColor FOREGROUND = QColor("#f1f0f2");      // Light text
    const QColor CARD = QColor("#221e30");            // Card backgrounds
    const QColor PRIMARY = QColor("#dc3545");         // Crimson (success/important)
    const QColor PRIMARY_FOREGROUND = QColor("#f9f8fa");
    const QColor SECONDARY = QColor("#352e4d");       // Secondary background
    const QColor ACCENT = QColor("#8c52ff");          // Purple highlight (attention)
    const QColor ACCENT_FOREGROUND = QColor("#f1f0f2");
    const QColor DESTRUCTIVE = QColor("#d23a1a");     // Red (danger/defeat)
    const QColor BORDER = QColor("#3e3754");          // Subtle dividers
    const QColor MUTED = QColor("#2d283d");           // Muted interactive
    const QColor INPUT = QColor("#3e3754");           // Input field backgrounds
    
    // Spacing System (Consistent layout)
    constexpr int SPACING_XS = 4;      // Extra small gaps
    constexpr int SPACING_SM = 8;      // Small gaps
    constexpr int SPACING_MD = 15;     // Medium (default)
    constexpr int SPACING_LG = 20;     // Large
    constexpr int SPACING_XL = 30;     // Extra large
    
    // Border Radius (Consistency)
    constexpr int BORDER_RADIUS_SM = 4;      // Buttons, inputs
    constexpr int BORDER_RADIUS_MD = 6;      // Cards, dialogs
    constexpr int BORDER_RADIUS_LG = 8;      // Panels
    constexpr int BORDER_RADIUS_XL = 12;     // Overlays, prominent
    
    // Font System
    const QString FONT_FAMILY = "Inter, Segoe UI, sans-serif";
    constexpr int FONT_SIZE_SM = 12;         // Secondary text
    constexpr int FONT_SIZE_MD = 14;         // Body text
    constexpr int FONT_SIZE_LG = 16;         // Headers
    constexpr int FONT_SIZE_XL = 18;         // Titles
    constexpr int FONT_SIZE_XXL = 24;        // Main titles
    constexpr int FONT_SIZE_XXXL = 36;       // Hero titles
    
    // Font Weights
    constexpr int FONT_WEIGHT_NORMAL = 400;
    constexpr int FONT_WEIGHT_MEDIUM = 500;
    constexpr int FONT_WEIGHT_SEMIBOLD = 600;
    constexpr int FONT_WEIGHT_BOLD = 700;
}
```

**Usage Example** (from CombatResultDialog):
```cpp
#include "../theme/Theme.h"

titleLabel->setStyleSheet(QString("color: %1; margin-bottom: 20px;")
    .arg(victory ? Theme::ACCENT.name() : Theme::DESTRUCTIVE.name()));

rewardsLabel->setStyleSheet(QString(
    "color: %1; "
    "background-color: %2; "
    "padding: 15px; "
    "border-radius: 8px; "
    "border: 2px solid %3;"
).arg(Theme::FOREGROUND.name())
 .arg(Theme::CARD.name())
 .arg(Theme::BORDER.name()));
```

---

### Related Files Worth Reviewing

**Animation Support**:
**Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/AnimationManager.h`
- Provides animation utilities for combat screens
- Can be extended for dialog/overlay animations

**Main Application Window**:
**Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/MainWindow.h`
- Central controller coordinating all dialogs/overlays
- Shows integration patterns for all modal content

**Models for Data**:
**Path**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/models/`
- `StoryEvent.h` - Story event data structure
- `Player.h` - Player data for content updates
- `Monster.h` - Monster data for victory screens

---

## File Organization Summary

```
/cpp-qt-rpg/src/
├── MainWindow.h/cpp          <- Integration point for all dialogs/overlays
├── components/               <- Dialog and component widgets
│   ├── CombatResultDialog.h/cpp
│   ├── QuestCompletionDialog.h/cpp
│   ├── MenuOverlay.h/cpp
│   ├── AnimationManager.h/cpp
│   └── ...
├── views/                    <- Page/screen widgets
│   ├── StoryEventDialog.h/cpp
│   ├── InventoryPage.h/cpp
│   ├── StatsPage.h/cpp
│   ├── ShopPage.h/cpp
│   └── ...
├── models/                   <- Data structures
│   ├── StoryEvent.h
│   ├── Player.h/cpp
│   ├── Monster.h/cpp
│   └── ...
├── theme/
│   └── Theme.h              <- All constants (no .cpp!)
├── game/
│   └── Game.h/cpp          <- Game logic coordinator
└── persistence/
    └── SaveManager.h/cpp    <- Save/load functionality
```

---

## Quick Copy-Paste Paths

For file operations from command line:

```bash
# View CombatResultDialog
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/CombatResultDialog.h
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/CombatResultDialog.cpp

# View MenuOverlay
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/MenuOverlay.h
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/MenuOverlay.cpp

# View Theme constants
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/theme/Theme.h

# View StoryEventDialog
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/views/StoryEventDialog.h
cat /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/views/StoryEventDialog.cpp

# View MainWindow integration
grep -n "CombatResultDialog\|MenuOverlay\|StoryEventDialog" \
  /Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/MainWindow.cpp
```

