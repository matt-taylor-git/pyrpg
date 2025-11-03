# Dialog & Overlay UI Patterns Analysis

## Executive Summary

The codebase demonstrates **two distinct patterns** for presenting modal content:

1. **QDialog Pattern**: Traditional modal dialogs for narrative moments (victories, quests, story events)
2. **Custom QWidget Overlay Pattern**: Full-screen overlays with custom animations and behavior (menus, inventory)

### Pattern Decision Matrix

| Pattern | Use Case | Modal | Animated | Full-Screen | Example |
|---------|----------|-------|----------|-------------|---------|
| QDialog | Quick wins, rewards, story moments | Yes | No | No | CombatResultDialog, QuestCompletionDialog |
| Overlay | Complex multi-tab UI, persistent state | No* | Yes | Yes | MenuOverlay |

*MenuOverlay uses modal behavior through focus management and mouse event handling

---

## Part 1: QDialog Pattern (Traditional Modals)

### Overview
QDialog-based implementations are used for **narrative moments** that require player acknowledgment before returning to gameplay. They are simple, reliable, and have built-in modal behavior.

### 1.1 CombatResultDialog

**File**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/CombatResultDialog.h/cpp`

#### Header Structure
```cpp
class CombatResultDialog : public QDialog
{
    Q_OBJECT

public:
    explicit CombatResultDialog(bool victory, int expGained, int goldGained,
                                const QString &lootMessage, bool leveledUp,
                                QWidget *parent = nullptr);

private:
    void setupUi(bool victory, int expGained, int goldGained,
                 const QString &lootMessage, bool leveledUp);
};
```

#### Key Implementation Details

**Constructor**:
```cpp
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

**UI Structure** (`setupUi`):
```
┌─────────────────────────────────────┐
│  🎉 VICTORY! 🎉                    │
│  ⭐ LEVEL UP! ⭐  (conditional)    │
│                                     │
│  Rewards:                           │
│  ┌─────────────────────────────┐   │
│  │ 📈 Experience: +150 XP     │   │
│  │ 💰 Gold: +50               │   │
│  │ 🎁 Iron Sword acquired     │   │
│  └─────────────────────────────┘   │
│                                     │
│  [    Continue Button    ]          │
└─────────────────────────────────────┘
```

#### Theme Integration Pattern

```cpp
// Title Label
QLabel *titleLabel = new QLabel(victory ? "🎉 VICTORY! 🎉" : "💀 DEFEAT 💀");
QFont titleFont;
titleFont.setPointSize(24);
titleFont.setBold(true);
titleLabel->setFont(titleFont);
titleLabel->setStyleSheet(QString("color: %1; margin-bottom: 20px;")
    .arg(victory ? Theme::ACCENT.name() : Theme::DESTRUCTIVE.name()));

// Rewards Box with Theme Constants
QLabel *rewardsLabel = new QLabel(rewardsText);
rewardsLabel->setStyleSheet(QString(
    "color: %1; "
    "background-color: %2; "
    "padding: 15px; "
    "border-radius: 8px; "
    "border: 2px solid %3;"
).arg(Theme::FOREGROUND.name())
 .arg(Theme::CARD.name())
 .arg(Theme::BORDER.name()));

// Button with Theme Constants and State Changes
continueButton->setStyleSheet(QString(
    "QPushButton {"
    "    background-color: %1;"
    "    color: %2;"
    "    font-size: 16px;"
    "    font-weight: bold;"
    "    border-radius: 8px;"
    "}"
    "QPushButton:hover { background-color: %3; }"
).arg(victory ? Theme::ACCENT.name() : Theme::PRIMARY.name())
 .arg(Theme::PRIMARY_FOREGROUND.name())
 .arg(victory ? Theme::ACCENT.lighter(110).name() : Theme::PRIMARY.lighter(110).name()));
```

#### Integration with MainWindow

```cpp
// In MainWindow.cpp::handleCombatEnded()
void MainWindow::handleCombatEnded(bool playerWon)
{
    Monster *monster = m_game->getCurrentMonster();
    
    if (playerWon) {
        CombatResultDialog resultDialog(
            true,
            monster ? monster->expReward : 0,
            monster ? monster->goldReward : 0,
            "Iron Sword acquired",  // Loot message
            leveledUp,              // Boolean for level up display
            this                    // Parent widget
        );
        resultDialog.exec();  // BLOCKING - waits for user input
        // Continue game after dialog closes
    } else {
        CombatResultDialog resultDialog(false, 0, 0, "", false, this);
        resultDialog.exec();
    }
}
```

**Critical Pattern**: `resultDialog.exec()` is **blocking**. It suspends game flow until the player clicks the button.

### 1.2 QuestCompletionDialog

**File**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/QuestCompletionDialog.h/cpp`

#### Structure
```cpp
class QuestCompletionDialog : public QDialog
{
    Q_OBJECT

public:
    explicit QuestCompletionDialog(const QString &questTitle, int expGained,
                                   int goldGained, const QList<QString> &itemNames,
                                   QWidget *parent = nullptr);

private:
    void setupUi(const QString &title, int exp, int gold, const QList<QString> &items);
};
```

#### Similar Pattern to CombatResultDialog

```cpp
void QuestCompletionDialog::setupUi(const QString &title, int exp, int gold, 
                                    const QList<QString> &items)
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setSpacing(Theme::SPACING_MD);
    layout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL,
                              Theme::SPACING_XL, Theme::SPACING_XL);

    // Dialog styling
    setStyleSheet(QString(
        "QDialog {"
        "    background-color: %1;"
        "    border: 2px solid %2;"
        "    border-radius: %3px;"
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD));

    // Celebration header
    QLabel *celebrationLabel = new QLabel("🎉 QUEST COMPLETE! 🎉");
    celebrationLabel->setAlignment(Qt::AlignCenter);
    celebrationLabel->setStyleSheet(QString(
        "font-size: %1px; font-weight: %2; color: %3; margin: 10px 0px;"
    ).arg(Theme::FONT_SIZE_XL)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::ACCENT.name()));
    layout->addWidget(celebrationLabel);

    // Rewards display
    // ... (similar structure to CombatResultDialog)
}
```

### 1.3 StoryEventDialog

**File**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/views/StoryEventDialog.h/cpp`

#### Advanced QDialog Pattern

```cpp
class StoryEventDialog : public QDialog
{
    Q_OBJECT

public:
    explicit StoryEventDialog(const StoryEvent &event, QWidget *parent = nullptr);

protected:
    void keyPressEvent(QKeyEvent *event) override;

private:
    void setupUi(const StoryEvent &event);
    qint64 m_eventStartTime;  // For timing validation
};
```

#### Advanced Features

**1. Frameless Window with Custom Styling**:
```cpp
StoryEventDialog::StoryEventDialog(const StoryEvent &event, QWidget *parent)
    : QDialog(parent)
{
    setModal(true);
    setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);  // Custom frame
    setMinimumSize(700, 500);
    m_eventStartTime = QDateTime::currentMSecsSinceEpoch();
    setupUi(event);
}
```

**2. Rich Content Display**:
```cpp
// Title
QLabel *titleLabel = new QLabel(event.title, this);
QFont titleFont;
titleFont.setPixelSize(Theme::FONT_SIZE_XXXL);  // Extra large
titleFont.setBold(true);
titleLabel->setFont(titleFont);
titleLabel->setAlignment(Qt::AlignCenter);
titleLabel->setStyleSheet(QString("color: %1; padding: %2px;")
    .arg(Theme::PRIMARY.name())
    .arg(Theme::SPACING_MD));

// Content text with full height
QTextEdit *eventText = new QTextEdit(this);
eventText->setReadOnly(true);
eventText->setPlainText(event.eventText);
eventText->setAlignment(Qt::AlignCenter);
QFont textFont;
textFont.setPixelSize(Theme::FONT_SIZE_LG);
eventText->setFont(textFont);
eventText->setStyleSheet(QString(
    "QTextEdit {"
    "    background-color: transparent;"
    "    color: %1;"
    "    border: none;"
    "    padding: %2px;"
    "}"
).arg(Theme::FOREGROUND.name())
 .arg(Theme::SPACING_MD));
mainLayout->addWidget(eventText, 1);  // Stretch fill
```

**3. User Input Validation (Prevent Accidental Skip)**:
```cpp
void StoryEventDialog::keyPressEvent(QKeyEvent *event)
{
    // Prevent accidental skip within first second
    qint64 elapsed = QDateTime::currentMSecsSinceEpoch() - m_eventStartTime;
    if (elapsed < 1000) {
        return;  // Ignore input for first second
    }

    if (event->key() == Qt::Key_Escape || 
        event->key() == Qt::Key_Return || 
        event->key() == Qt::Key_Space) {
        accept();
        return;
    }

    QDialog::keyPressEvent(event);
}
```

**Integration**:
```cpp
void MainWindow::handleStoryEventTriggered(const StoryEvent &event)
{
    StoryEventDialog dialog(event, this);
    dialog.exec();  // Blocks until dismissed
}
```

### 1.4 QDialog Best Practices Summary

| Feature | Implementation |
|---------|----------------|
| **Modal Behavior** | Built-in via `setModal(true)` |
| **Show/Hide** | `exec()` (blocking) or `open()` (non-blocking) |
| **Theme Integration** | Pass Theme constants to stylesheet |
| **Content** | QVBoxLayout with labels, text widgets |
| **Button Handling** | `connect(button, &QPushButton::clicked, this, &QDialog::accept)` |
| **Customization** | Override `keyPressEvent()`, `setWindowFlags()` |
| **Animation** | Not native to QDialog (need external animations) |

---

## Part 2: Custom Overlay Pattern (Full-Screen UI)

### Overview
The `MenuOverlay` demonstrates how to build a **full-screen overlay widget** with custom animations, tab-based navigation, and sophisticated event handling.

### 2.1 MenuOverlay - Architecture

**File**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/components/MenuOverlay.h/cpp`

#### Class Structure

```cpp
class MenuOverlay : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)  // Animatable property

public:
    explicit MenuOverlay(QWidget *parent = nullptr);

    void showOverlay();
    void hideOverlay();
    void updateContent(Player *player);

    qreal opacity() const { return m_opacity; }
    void setOpacity(qreal opacity);  // For animation

signals:
    void overlayHidden();
    void saveRequested();
    void loadRequested();
    void saveToSlotRequested(int slotNumber);
    void loadFromSlotRequested(int slotNumber);
    void deleteSlotRequested(int slotNumber);
    void quitRequested();

protected:
    void paintEvent(QPaintEvent *event) override;     // Custom semi-transparent BG
    void keyPressEvent(QKeyEvent *event) override;    // ESC to close
    void mousePressEvent(QMouseEvent *event) override; // Click-outside to close

private:
    void setupUi();
    void animateShow();
    void animateHide();

    QWidget *m_contentWidget;           // The actual menu
    QTabWidget *m_tabWidget;            // Inventory, Stats, Shop, Save/Load
    QPushButton *m_closeButton;
    QPushButton *m_saveButton;
    QPushButton *m_loadButton;
    QPropertyAnimation *m_animation;    // Opacity animation

    InventoryPage *m_inventoryPage;
    StatsPage *m_statsPage;
    ShopPage *m_shopPage;
    SaveLoadPage *m_saveLoadPage;

    qreal m_opacity;
    Player *m_currentPlayer;
    QWidget *m_previousFocusWidget;     // For focus restoration
};
```

#### Key Design Pattern: Q_PROPERTY for Animation

```cpp
class MenuOverlay : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)
    //        ^^^^^^^^^  ^^^^^^^^         ^^^        ^^^^^^^^^
    //         type     property name    getter        setter
```

This enables **animated opacity** via `QPropertyAnimation`:

```cpp
m_animation = new QPropertyAnimation(this, "opacity");
m_animation->setDuration(200);  // 200ms fade in/out

// When animation finishes:
connect(m_animation, &QPropertyAnimation::finished, this, [this]() {
    if (m_animation->endValue().toReal() == 0.0) {
        hide();  // Only hide when fading OUT
        if (m_previousFocusWidget) {
            m_previousFocusWidget->setFocus();
        }
        emit overlayHidden();
    }
});
```

### 2.2 Visual Structure

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Menu                                           ✕ │ │
│  ├──────────────────────────────────────────────────┤ │
│  │ [Inventory] [Stats] [Shop] [Save/Load]          │ │
│  │ ┌──────────────────────────────────────────────┐ │ │
│  │ │                                              │ │ │
│  │ │  Tab content here                            │ │ │
│  │ │                                              │ │ │
│  │ └──────────────────────────────────────────────┘ │ │
│  │                                                  │ │
│  │ [💾 Save Game] [📂 Load Game] [🚪 Quit Game]  │ │
│  │                                                  │ │
│  │ Press ESC to close                              │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Semi-transparent black background (opacity: 0.7)    │
└────────────────────────────────────────────────────────┘
```

### 2.3 Constructor & Widget Setup

```cpp
MenuOverlay::MenuOverlay(QWidget *parent)
    : QWidget(parent)
    , m_opacity(0.0)
    , m_currentPlayer(nullptr)
    , m_previousFocusWidget(nullptr)
{
    // Enable custom rendering and transparency
    setAttribute(Qt::WA_TransparentForMouseEvents, false);  // Capture mouse events
    setAttribute(Qt::WA_NoSystemBackground);               // No system bg
    setAttribute(Qt::WA_TranslucentBackground);            // Transparent support
    setFocusPolicy(Qt::StrongFocus);                       // Accept focus

    setupUi();

    // Create animation object
    m_animation = new QPropertyAnimation(this, "opacity");
    m_animation->setDuration(200);

    // Handle animation completion
    connect(m_animation, &QPropertyAnimation::finished, this, [this]() {
        if (m_animation->endValue().toReal() == 0.0) {
            hide();
            if (m_previousFocusWidget) {
                m_previousFocusWidget->setFocus();
                m_previousFocusWidget = nullptr;
            }
            emit overlayHidden();
        }
    });

    hide();  // Start invisible
}
```

### 2.4 Show/Hide with Animation

```cpp
void MenuOverlay::showOverlay()
{
    // Stop any in-progress animation to prevent race conditions
    m_animation->stop();

    // Store the currently focused widget so we can restore it later
    m_previousFocusWidget = QApplication::focusWidget();

    show();
    raise();      // Bring to front
    setFocus();   // Take keyboard focus

    // Animate opacity from 0 to 1
    m_animation->setStartValue(0.0);
    m_animation->setEndValue(1.0);
    m_animation->start();
}

void MenuOverlay::hideOverlay()
{
    // Check if we're already hiding - prevent redundant animations
    if (m_animation->state() == QAbstractAnimation::Running &&
        m_animation->endValue().toReal() == 0.0) {
        return;  // Already hiding
    }

    // Animate opacity from current to 0
    m_animation->setStartValue(m_opacity);
    m_animation->setEndValue(0.0);
    m_animation->start();
}
```

### 2.5 Semi-Transparent Background Rendering

```cpp
void MenuOverlay::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // Draw semi-transparent black background
    // This creates the "dimming" effect behind the menu
    QColor overlayColor = QColor(0, 0, 0);
    overlayColor.setAlphaF(0.7 * m_opacity);  // Opacity controlled by animation
    painter.fillRect(rect(), overlayColor);

    // Content widget is drawn by Qt's normal rendering after this
}
```

### 2.6 Keyboard & Mouse Handling

```cpp
void MenuOverlay::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::keyPressEvent(event);
    }
}

void MenuOverlay::mousePressEvent(QMouseEvent *event)
{
    // Close overlay if clicking outside the content widget
    if (!m_contentWidget->geometry().contains(event->pos())) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::mousePressEvent(event);
    }
}
```

### 2.7 Content Widget Setup

```cpp
void MenuOverlay::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(50, 50, 50, 50);

    // Content widget (the actual menu dialog)
    m_contentWidget = new QWidget();
    m_contentWidget->setObjectName("menuOverlayContent");
    m_contentWidget->setStyleSheet(QString(
        "QWidget#menuOverlayContent { "
        "background-color: %1; "
        "border: %2px solid %3; "
        "border-radius: %4px; "
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER_WIDTH_MEDIUM)
     .arg(Theme::ACCENT.name())
     .arg(Theme::BORDER_RADIUS_XL));

    QVBoxLayout *contentLayout = new QVBoxLayout(m_contentWidget);
    contentLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, 
                                     Theme::SPACING_LG, Theme::SPACING_LG);

    // Header with title and close button
    QHBoxLayout *headerLayout = new QHBoxLayout();
    
    QLabel *titleLabel = new QLabel("Menu");
    QFont titleFont;
    titleFont.setPointSize(Theme::FONT_SIZE_XL);
    titleFont.setWeight(static_cast<QFont::Weight>(Theme::FONT_WEIGHT_SEMIBOLD));
    titleLabel->setFont(titleFont);
    titleLabel->setStyleSheet(QString("color: %1;").arg(Theme::ACCENT.name()));

    m_closeButton = new QPushButton("✕");
    m_closeButton->setObjectName("closeButton");
    m_closeButton->setFixedSize(32, 32);
    m_closeButton->setStyleSheet(QString(
        "QPushButton#closeButton { "
        "background-color: %1; "
        "color: %2; "
        "border: 1px solid %3; "
        "border-radius: 16px; "
        "font-size: 16px; "
        "font-weight: bold; "
        "} "
        "QPushButton#closeButton:hover { "
        "background-color: %4; "
        "}"
    ).arg(Theme::MUTED.name())
     .arg(Theme::FOREGROUND.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::DESTRUCTIVE.name()));
    
    connect(m_closeButton, &QPushButton::clicked, this, &MenuOverlay::hideOverlay);

    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(m_closeButton);
    contentLayout->addLayout(headerLayout);

    // Tab widget
    m_tabWidget = new QTabWidget();
    m_tabWidget->setMinimumSize(600, 400);
    // ... tab styling ...

    // Create pages
    m_inventoryPage = new InventoryPage();
    m_statsPage = new StatsPage();
    m_shopPage = new ShopPage();
    m_saveLoadPage = new SaveLoadPage();

    // Connect back signals
    connect(m_inventoryPage, &InventoryPage::backRequested, this, &MenuOverlay::hideOverlay);
    connect(m_statsPage, &StatsPage::backRequested, this, &MenuOverlay::hideOverlay);
    connect(m_shopPage, &ShopPage::leaveRequested, this, &MenuOverlay::hideOverlay);
    connect(m_saveLoadPage, &SaveLoadPage::backRequested, this, &MenuOverlay::hideOverlay);

    // Add tabs
    m_tabWidget->addTab(m_inventoryPage, "🎒 Inventory");
    m_tabWidget->addTab(m_statsPage, "📊 Stats");
    m_tabWidget->addTab(m_shopPage, "🏪 Shop");
    m_tabWidget->addTab(m_saveLoadPage, "💾 Save/Load");

    contentLayout->addWidget(m_tabWidget);

    // Add action buttons at bottom
    // ...

    mainLayout->addWidget(m_contentWidget);
}
```

### 2.8 Overlay Integration with MainWindow

```cpp
// In MainWindow.h
class MainWindow : public QMainWindow
{
    // ...
private:
    MenuOverlay *m_menuOverlay;
};

// In MainWindow.cpp constructor
void MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    // ... other initialization ...
{
    // Create overlay on top of stacked widget
    m_menuOverlay = new MenuOverlay(this);
    stackedWidget->addWidget(m_menuOverlay);
    
    // The overlay is "always there" but hidden
    // It's a sibling of the main game views
}

// When player presses menu key
void MainWindow::handleMenuButtonClicked()
{
    m_menuOverlay->updateContent(m_game->player());
    m_menuOverlay->showOverlay();
}

// When player closes menu
// The overlayHidden() signal is connected in MainWindow constructor
```

---

## Part 3: Pattern Comparison & Decision Guide

### 3.1 When to Use QDialog

**Use QDialog when**:
- You need a **simple, focused interaction** (yes/no, confirm, display result)
- You want **blocking behavior** (suspend game, wait for response)
- Content is **single-purpose** (not tab-based or multi-section)
- You don't need **custom animations**
- You want **modal dialog** with built-in window decorations

**Examples in Codebase**:
- `CombatResultDialog` - Victory/Defeat notification
- `QuestCompletionDialog` - Quest reward display
- `StoryEventDialog` - Narrative moments
- `ItemSelectionDialog` - Item picking

**Structure Template**:
```cpp
// MyDialog.h
class MyDialog : public QDialog
{
    Q_OBJECT
public:
    explicit MyDialog(const Data &data, QWidget *parent = nullptr);
private:
    void setupUi(const Data &data);
};

// MyDialog.cpp
MyDialog::MyDialog(const Data &data, QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle("My Dialog");
    setMinimumSize(400, 300);
    setupUi(data);
}

void MyDialog::setupUi(const Data &data)
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    // Add widgets...
    setStyleSheet(QString("QDialog { background-color: %1; }").arg(Theme::CARD.name()));
}

// Usage:
MyDialog dialog(data, this);
if (dialog.exec() == QDialog::Accepted) {
    // Handle result
}
```

### 3.2 When to Use Custom Overlay

**Use Custom Overlay when**:
- You need a **full-screen modal** with complex interaction
- Content has **multiple tabs/sections** (Inventory, Stats, Shop)
- You want **smooth animations** with opacity control
- You need **custom event handling** (click-outside-to-close)
- Content is **persistent/stateful** (inventory changes persist)
- You want **non-standard appearance** (no title bar, custom background)

**Examples in Codebase**:
- `MenuOverlay` - Full game menu system
- `ItemSelectionOverlay` - Could be upgraded to overlay pattern

**Structure Template**:
```cpp
// MyOverlay.h
class MyOverlay : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)

public:
    explicit MyOverlay(QWidget *parent = nullptr);
    void showOverlay();
    void hideOverlay();
    
    qreal opacity() const { return m_opacity; }
    void setOpacity(qreal opacity);

signals:
    void overlayHidden();

protected:
    void paintEvent(QPaintEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;

private:
    void setupUi();
    void animateShow();
    void animateHide();

    QWidget *m_contentWidget;
    QPropertyAnimation *m_animation;
    qreal m_opacity;
    QWidget *m_previousFocusWidget;
};

// MyOverlay.cpp
MyOverlay::MyOverlay(QWidget *parent)
    : QWidget(parent), m_opacity(0.0), m_previousFocusWidget(nullptr)
{
    setAttribute(Qt::WA_TransparentForMouseEvents, false);
    setAttribute(Qt::WA_NoSystemBackground);
    setAttribute(Qt::WA_TranslucentBackground);
    setFocusPolicy(Qt::StrongFocus);

    setupUi();

    m_animation = new QPropertyAnimation(this, "opacity");
    m_animation->setDuration(200);
    connect(m_animation, &QPropertyAnimation::finished, this, [this]() {
        if (m_animation->endValue().toReal() == 0.0) {
            hide();
            if (m_previousFocusWidget) m_previousFocusWidget->setFocus();
            emit overlayHidden();
        }
    });

    hide();
}

void MyOverlay::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    QPainter painter(this);
    QColor bg(0, 0, 0);
    bg.setAlphaF(0.7 * m_opacity);
    painter.fillRect(rect(), bg);
}

void MyOverlay::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::keyPressEvent(event);
    }
}

void MyOverlay::mousePressEvent(QMouseEvent *event)
{
    if (!m_contentWidget->geometry().contains(event->pos())) {
        hideOverlay();
        event->accept();
    } else {
        QWidget::mousePressEvent(event);
    }
}

void MyOverlay::showOverlay()
{
    m_animation->stop();
    m_previousFocusWidget = QApplication::focusWidget();
    show();
    raise();
    setFocus();
    m_animation->setStartValue(0.0);
    m_animation->setEndValue(1.0);
    m_animation->start();
}

void MyOverlay::hideOverlay()
{
    if (m_animation->state() == QAbstractAnimation::Running &&
        m_animation->endValue().toReal() == 0.0) {
        return;
    }
    m_animation->setStartValue(m_opacity);
    m_animation->setEndValue(0.0);
    m_animation->start();
}
```

### 3.3 Comparison Table

| Feature | QDialog | Overlay |
|---------|---------|---------|
| **Blocking** | Yes (exec()) | No (show()) |
| **Animation** | Manual + library | Q_PROPERTY + QPropertyAnimation |
| **Full Screen** | No | Yes |
| **Tab Support** | Manual | QTabWidget friendly |
| **Window Frame** | Yes (default) | Custom (FramelessWindowHint) |
| **Click-Outside Close** | No (built-in) | Yes (custom event) |
| **Focus Restoration** | No | Yes (stores previous) |
| **Setup Complexity** | Low | High |
| **Code Reusability** | High | Medium |
| **Use Cases** | One-time notifications | Persistent UI |

---

## Part 4: Theme Integration

### 4.1 Theme Constants

**Location**: `/Users/matt.taylor/codeprojects/pyrpg/take2/cpp-qt-rpg/src/theme/Theme.h`

```cpp
namespace Theme {
    // Color Palette
    const QColor BACKGROUND = QColor("#1a1826");      // Dark bg
    const QColor FOREGROUND = QColor("#f1f0f2");      // Light text
    const QColor CARD = QColor("#221e30");            // Card/Dialog bg
    const QColor PRIMARY = QColor("#dc3545");         // Crimson (success)
    const QColor PRIMARY_FOREGROUND = QColor("#f9f8fa");
    const QColor SECONDARY = QColor("#352e4d");       // Secondary bg
    const QColor ACCENT = QColor("#8c52ff");          // Purple accent
    const QColor ACCENT_FOREGROUND = QColor("#f1f0f2");
    const QColor DESTRUCTIVE = QColor("#d23a1a");     // Red (danger)
    const QColor BORDER = QColor("#3e3754");          // Subtle borders

    // Spacing (pixels)
    constexpr int SPACING_XS = 4;      // Extra small
    constexpr int SPACING_SM = 8;      // Small
    constexpr int SPACING_MD = 15;     // Medium
    constexpr int SPACING_LG = 20;     // Large
    constexpr int SPACING_XL = 30;     // Extra large

    // Borders
    constexpr int BORDER_RADIUS_SM = 4;
    constexpr int BORDER_RADIUS_MD = 6;
    constexpr int BORDER_RADIUS_LG = 8;
    constexpr int BORDER_RADIUS_XL = 12;
    constexpr int BORDER_WIDTH_THIN = 1;
    constexpr int BORDER_WIDTH_MEDIUM = 2;
    constexpr int BORDER_WIDTH_THICK = 3;

    // Fonts
    const QString FONT_FAMILY = "Inter, Segoe UI, sans-serif";
    constexpr int FONT_SIZE_SM = 12;    // Secondary
    constexpr int FONT_SIZE_MD = 14;    // Body
    constexpr int FONT_SIZE_LG = 16;    // Headers
    constexpr int FONT_SIZE_XL = 18;    // Titles
    constexpr int FONT_SIZE_XXL = 24;   // Main titles
    constexpr int FONT_SIZE_XXXL = 36;  // Hero titles
    constexpr int FONT_WEIGHT_NORMAL = 400;
    constexpr int FONT_WEIGHT_MEDIUM = 500;
    constexpr int FONT_WEIGHT_SEMIBOLD = 600;
    constexpr int FONT_WEIGHT_BOLD = 700;
}
```

### 4.2 Theme Integration Pattern

**Always use Theme constants** instead of hardcoded values:

```cpp
// GOOD
QLabel *label = new QLabel("Score");
label->setStyleSheet(QString("color: %1; font-size: %2px;")
    .arg(Theme::ACCENT.name())
    .arg(Theme::FONT_SIZE_LG));

// BAD - hardcoded colors/sizes
label->setStyleSheet("color: #8c52ff; font-size: 16px;");
```

### 4.3 Common Dialog Styling Pattern

```cpp
// Dialog background
setStyleSheet(QString(
    "QDialog {"
    "    background-color: %1;"
    "    border: %2px solid %3;"
    "    border-radius: %4px;"
    "}"
).arg(Theme::CARD.name())
 .arg(Theme::BORDER_WIDTH_MEDIUM)
 .arg(Theme::ACCENT.name())
 .arg(Theme::BORDER_RADIUS_MD));

// Title label
QLabel *title = new QLabel("Title Text");
QFont titleFont;
titleFont.setPixelSize(Theme::FONT_SIZE_XXL);
titleFont.setBold(true);
title->setFont(titleFont);
title->setStyleSheet(QString("color: %1;").arg(Theme::PRIMARY.name()));

// Content area
QLabel *content = new QLabel("Content here");
content->setStyleSheet(QString(
    "background-color: %1; "
    "color: %2; "
    "padding: %3px; "
    "border-radius: %4px; "
    "border: 1px solid %5;"
).arg(Theme::BACKGROUND.name())
 .arg(Theme::FOREGROUND.name())
 .arg(Theme::SPACING_MD)
 .arg(Theme::BORDER_RADIUS_SM)
 .arg(Theme::BORDER.name()));

// Button
QPushButton *button = new QPushButton("Action");
button->setMinimumHeight(40);
button->setStyleSheet(QString(
    "QPushButton {"
    "    background-color: %1;"
    "    color: %2;"
    "    border: none;"
    "    border-radius: %3px;"
    "    padding: %4px;"
    "    font-size: %5px;"
    "    font-weight: %6;"
    "}"
    "QPushButton:hover {"
    "    background-color: %7;"
    "}"
).arg(Theme::ACCENT.name())
 .arg(Theme::ACCENT_FOREGROUND.name())
 .arg(Theme::BORDER_RADIUS_SM)
 .arg(Theme::SPACING_MD)
 .arg(Theme::FONT_SIZE_MD)
 .arg(Theme::FONT_WEIGHT_MEDIUM)
 .arg(Theme::ACCENT.lighter(110).name()));
```

---

## Part 5: Animation Patterns

### 5.1 QDialog Animation (No Built-In)

QDialogs don't animate by default. If needed, add custom animations:

```cpp
class AnimatedDialog : public QDialog
{
    Q_OBJECT
    Q_PROPERTY(qreal scale READ scale WRITE setScale)

public:
    explicit AnimatedDialog(QWidget *parent = nullptr)
        : QDialog(parent), m_scale(0.8)
    {
        // Setup...
        
        // Animate entrance (scale up)
        QPropertyAnimation *anim = new QPropertyAnimation(this, "scale");
        anim->setStartValue(0.8);
        anim->setEndValue(1.0);
        anim->setDuration(300);
        connect(anim, &QPropertyAnimation::finished, [anim]() { delete anim; });
        anim->start();
    }

    qreal scale() const { return m_scale; }
    void setScale(qreal s) { m_scale = s; update(); }

protected:
    void paintEvent(QPaintEvent *e) override
    {
        // Apply scale transform
        QTransform transform;
        transform.translate(width()/2, height()/2);
        transform.scale(m_scale, m_scale);
        transform.translate(-width()/2, -height()/2);
        
        QPainter p(this);
        p.setTransform(transform);
        QDialog::paintEvent(e);
    }

private:
    qreal m_scale;
};
```

### 5.2 Overlay Animation (Best Practice)

The MenuOverlay demonstrates the correct pattern:

```cpp
// Q_PROPERTY makes it animatable
Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)

// Create animation in constructor
m_animation = new QPropertyAnimation(this, "opacity");
m_animation->setDuration(200);

// Use it
void MenuOverlay::showOverlay()
{
    m_animation->setStartValue(0.0);
    m_animation->setEndValue(1.0);
    m_animation->start();
}

void MenuOverlay::hideOverlay()
{
    m_animation->setStartValue(m_opacity);
    m_animation->setEndValue(0.0);
    m_animation->start();
}

// And in paintEvent
void MenuOverlay::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    QColor bg(0, 0, 0);
    bg.setAlphaF(0.7 * m_opacity);  // Opacity controlled by animation
    painter.fillRect(rect(), bg);
}
```

---

## Part 6: Creating a VictoryScreen Pattern

Based on the codebase patterns, here's the recommended approach for a dramatic `VictoryScreen`:

### 6.1 Architecture Decision

**Recommendation**: Use a **hybrid approach**:
- Start with **QDialog** for modal behavior and simplicity
- Add **animations** for dramatic reveal
- Include **rich content** (stats, images, effects)

### 6.2 Header

```cpp
// VictoryScreen.h
#ifndef VICTORYSCREEN_H
#define VICTORYSCREEN_H

#include <QDialog>
#include <QPropertyAnimation>
#include "../models/Player.h"

class QLabel;
class QPushButton;
class QPixmap;

class VictoryScreen : public QDialog
{
    Q_OBJECT
    Q_PROPERTY(qreal scale READ scale WRITE setScale)
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)

public:
    struct VictoryData {
        bool leveledUp;
        int expGained;
        int goldGained;
        int healthRestored;
        QString monsterName;
        QPixmap monsterImage;
        QList<QString> itemsDropped;
    };

    explicit VictoryScreen(const VictoryData &data, QWidget *parent = nullptr);
    ~VictoryScreen();

    qreal scale() const { return m_scale; }
    void setScale(qreal scale);
    qreal opacity() const { return m_opacity; }
    void setOpacity(qreal opacity);

protected:
    void paintEvent(QPaintEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;

private:
    void setupUi(const VictoryData &data);
    void playEntranceAnimation();
    void playRewardAnimation();

    qreal m_scale;
    qreal m_opacity;
    QPropertyAnimation *m_scaleAnimation;
    QPropertyAnimation *m_opacityAnimation;
    QSequentialAnimationGroup *m_sequenceGroup;
    
    QLabel *m_titleLabel;
    QLabel *m_monsterNameLabel;
    QLabel *m_expLabel;
    QLabel *m_goldLabel;
    QLabel *m_itemsLabel;
    QPushButton *m_continueButton;
};

#endif // VICTORYSCREEN_H
```

### 6.3 Implementation

```cpp
// VictoryScreen.cpp
#include "VictoryScreen.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QFont>
#include <QPainter>
#include <QPixmap>
#include <QSequentialAnimationGroup>
#include <QParallelAnimationGroup>

VictoryScreen::VictoryScreen(const VictoryData &data, QWidget *parent)
    : QDialog(parent)
    , m_scale(0.0)
    , m_opacity(0.0)
{
    setWindowTitle("Victory!");
    setModal(true);
    setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);
    setMinimumSize(600, 700);
    
    // Dialog background styling
    setStyleSheet(QString(
        "QDialog {"
        "    background-color: %1;"
        "    border: 3px solid %2;"
        "    border-radius: %3px;"
        "}"
    ).arg(Theme::BACKGROUND.name())
     .arg(Theme::ACCENT.name())
     .arg(Theme::BORDER_RADIUS_LG));

    setupUi(data);
    
    // Don't show immediately - wait for animation
    hide();
}

VictoryScreen::~VictoryScreen()
{
    if (m_sequenceGroup) delete m_sequenceGroup;
}

void VictoryScreen::setupUi(const VictoryData &data)
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(Theme::SPACING_LG);
    mainLayout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL,
                                   Theme::SPACING_XL, Theme::SPACING_XL);

    // === TITLE SECTION ===
    m_titleLabel = new QLabel("🎉 VICTORY! 🎉");
    QFont titleFont;
    titleFont.setPixelSize(Theme::FONT_SIZE_XXXL);
    titleFont.setWeight(static_cast<QFont::Weight>(Theme::FONT_WEIGHT_BOLD));
    m_titleLabel->setFont(titleFont);
    m_titleLabel->setAlignment(Qt::AlignCenter);
    m_titleLabel->setStyleSheet(QString(
        "color: %1; "
        "padding: 20px; "
        "background-color: %2; "
        "border-radius: %3px;"
    ).arg(Theme::PRIMARY_FOREGROUND.name())
     .arg(Theme::PRIMARY.name())
     .arg(Theme::BORDER_RADIUS_MD));
    mainLayout->addWidget(m_titleLabel);

    // === DEFEATED ENEMY ===
    QHBoxLayout *enemyLayout = new QHBoxLayout();
    
    // Monster image (if available)
    if (!data.monsterImage.isNull()) {
        QLabel *imageLabel = new QLabel();
        QPixmap scaledImage = data.monsterImage.scaledToWidth(150, Qt::SmoothTransformation);
        imageLabel->setPixmap(scaledImage);
        imageLabel->setAlignment(Qt::AlignCenter);
        imageLabel->setStyleSheet(QString(
            "background-color: %1; "
            "border-radius: %2px; "
            "padding: 10px;"
        ).arg(Theme::CARD.name())
         .arg(Theme::BORDER_RADIUS_SM));
        enemyLayout->addWidget(imageLabel);
    }

    // Enemy info
    m_monsterNameLabel = new QLabel(QString("Defeated: %1").arg(data.monsterName));
    QFont enemyFont;
    enemyFont.setPixelSize(Theme::FONT_SIZE_LG);
    enemyFont.setWeight(static_cast<QFont::Weight>(Theme::FONT_WEIGHT_SEMIBOLD));
    m_monsterNameLabel->setFont(enemyFont);
    m_monsterNameLabel->setStyleSheet(QString("color: %1;").arg(Theme::ACCENT.name()));
    m_monsterNameLabel->setAlignment(Qt::AlignCenter);
    enemyLayout->addWidget(m_monsterNameLabel);

    mainLayout->addLayout(enemyLayout);

    // === REWARDS SECTION ===
    QLabel *rewardsHeaderLabel = new QLabel("REWARDS EARNED");
    rewardsHeaderLabel->setAlignment(Qt::AlignCenter);
    rewardsHeaderLabel->setStyleSheet(QString(
        "color: %1; "
        "font-size: %2px; "
        "font-weight: %3; "
        "padding: 10px;"
    ).arg(Theme::ACCENT.name())
     .arg(Theme::FONT_SIZE_LG)
     .arg(Theme::FONT_WEIGHT_BOLD));
    mainLayout->addWidget(rewardsHeaderLabel);

    // Rewards box
    QWidget *rewardsBox = new QWidget();
    rewardsBox->setStyleSheet(QString(
        "background-color: %1; "
        "border: 2px solid %2; "
        "border-radius: %3px; "
        "padding: %4px;"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD)
     .arg(Theme::SPACING_MD));

    QVBoxLayout *rewardsLayout = new QVBoxLayout(rewardsBox);
    rewardsLayout->setSpacing(Theme::SPACING_SM);

    // Experience reward
    m_expLabel = new QLabel();
    QString expText = QString("📈 Experience: +%1 XP").arg(data.expGained);
    if (data.leveledUp) {
        expText += "\n⭐ LEVEL UP! ⭐";
    }
    m_expLabel->setText(expText);
    m_expLabel->setStyleSheet(QString(
        "color: %1; font-size: %2px; font-weight: %3;"
    ).arg(Theme::ACCENT.name())
     .arg(Theme::FONT_SIZE_MD)
     .arg(Theme::FONT_WEIGHT_MEDIUM));
    rewardsLayout->addWidget(m_expLabel);

    // Gold reward
    m_goldLabel = new QLabel(QString("💰 Gold: +%1").arg(data.goldGained));
    m_goldLabel->setStyleSheet(QString(
        "color: %1; font-size: %2px; font-weight: %3;"
    ).arg(Theme::PRIMARY.name())
     .arg(Theme::FONT_SIZE_MD)
     .arg(Theme::FONT_WEIGHT_MEDIUM));
    rewardsLayout->addWidget(m_goldLabel);

    // Health restored
    if (data.healthRestored > 0) {
        QLabel *healthLabel = new QLabel(QString("❤️ Health Restored: +%1").arg(data.healthRestored));
        healthLabel->setStyleSheet(QString(
            "color: %1; font-size: %2px; font-weight: %3;"
        ).arg(Theme::SECONDARY.name())
         .arg(Theme::FONT_SIZE_MD)
         .arg(Theme::FONT_WEIGHT_MEDIUM));
        rewardsLayout->addWidget(healthLabel);
    }

    // Items dropped
    if (!data.itemsDropped.isEmpty()) {
        m_itemsLabel = new QLabel(QString("🎁 Items: %1").arg(data.itemsDropped.join(", ")));
        m_itemsLabel->setStyleSheet(QString(
            "color: %1; font-size: %2px; font-weight: %3;"
        ).arg(Theme::FOREGROUND.name())
         .arg(Theme::FONT_SIZE_MD)
         .arg(Theme::FONT_WEIGHT_MEDIUM));
        m_itemsLabel->setWordWrap(true);
        rewardsLayout->addWidget(m_itemsLabel);
    }

    mainLayout->addWidget(rewardsBox);
    mainLayout->addStretch();

    // === ACTION BUTTON ===
    m_continueButton = new QPushButton("Continue (Space)");
    m_continueButton->setMinimumHeight(50);
    m_continueButton->setStyleSheet(QString(
        "QPushButton {"
        "    background-color: %1;"
        "    color: %2;"
        "    border: 2px solid %3;"
        "    border-radius: %4px;"
        "    padding: 10px;"
        "    font-size: %5px;"
        "    font-weight: %6;"
        "}"
        "QPushButton:hover {"
        "    background-color: %7;"
        "    border-color: %8;"
        "}"
        "QPushButton:pressed {"
        "    background-color: %9;"
        "}"
    ).arg(Theme::ACCENT.name())
     .arg(Theme::ACCENT_FOREGROUND.name())
     .arg(Theme::PRIMARY.name())
     .arg(Theme::BORDER_RADIUS_MD)
     .arg(Theme::FONT_SIZE_LG)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::ACCENT.lighter(110).name())
     .arg(Theme::ACCENT.lighter(120).name())
     .arg(Theme::PRIMARY.name()));
    
    connect(m_continueButton, &QPushButton::clicked, this, &QDialog::accept);
    mainLayout->addWidget(m_continueButton);
}

void VictoryScreen::setScale(qreal scale)
{
    m_scale = scale;
    update();
}

void VictoryScreen::setOpacity(qreal opacity)
{
    m_opacity = opacity;
    update();
}

void VictoryScreen::paintEvent(QPaintEvent *event)
{
    // Apply scale and opacity transformations
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setOpacity(m_opacity);

    if (m_scale != 1.0) {
        QTransform transform;
        transform.translate(width() / 2.0, height() / 2.0);
        transform.scale(m_scale, m_scale);
        transform.translate(-width() / 2.0, -height() / 2.0);
        painter.setTransform(transform);
    }

    // Draw the dialog normally
    QDialog::paintEvent(event);
}

void VictoryScreen::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Space || event->key() == Qt::Key_Return) {
        accept();
        return;
    }
    QDialog::keyPressEvent(event);
}

// Public method to show with animation
void VictoryScreen::showEvent(QShowEvent *event)
{
    QDialog::showEvent(event);
    playEntranceAnimation();
}

void VictoryScreen::playEntranceAnimation()
{
    // Create sequential animation group
    m_sequenceGroup = new QSequentialAnimationGroup(this);

    // === Entrance animation (scale up with fade) ===
    QParallelAnimationGroup *entranceGroup = new QParallelAnimationGroup();
    
    // Scale animation: 0.0 -> 1.0
    m_scaleAnimation = new QPropertyAnimation(this, "scale");
    m_scaleAnimation->setStartValue(0.0);
    m_scaleAnimation->setEndValue(1.0);
    m_scaleAnimation->setDuration(500);
    m_scaleAnimation->setEasingCurve(QEasingCurve::OutBack);
    entranceGroup->addAnimation(m_scaleAnimation);

    // Opacity animation: 0.0 -> 1.0
    m_opacityAnimation = new QPropertyAnimation(this, "opacity");
    m_opacityAnimation->setStartValue(0.0);
    m_opacityAnimation->setEndValue(1.0);
    m_opacityAnimation->setDuration(500);
    m_opacityAnimation->setEasingCurve(QEasingCurve::InOutQuad);
    entranceGroup->addAnimation(m_opacityAnimation);

    m_sequenceGroup->addAnimation(entranceGroup);

    // === Pause to display rewards ===
    m_sequenceGroup->addPause(1500);  // Wait 1.5 seconds

    // === Button pulse animation (attention getter) ===
    QPropertyAnimation *buttonPulse = new QPropertyAnimation(m_continueButton, "minimumHeight");
    buttonPulse->setStartValue(50);
    buttonPulse->setEndValue(55);
    buttonPulse->setDuration(500);
    buttonPulse->setEasingCurve(QEasingCurve::InOutQuad);
    m_sequenceGroup->addAnimation(buttonPulse);

    m_sequenceGroup->start();
}
```

### 6.4 Integration with MainWindow

```cpp
// In MainWindow.cpp
#include "components/VictoryScreen.h"

void MainWindow::handleCombatEnded(bool playerWon)
{
    Monster *monster = m_game->getCurrentMonster();
    
    if (playerWon) {
        VictoryScreen::VictoryData victoryData;
        victoryData.monsterName = monster->name;
        victoryData.expGained = monster->expReward;
        victoryData.goldGained = monster->goldReward;
        victoryData.leveledUp = m_game->player()->getLevel() > m_previousLevel;
        victoryData.healthRestored = 50;  // Or calculate actual
        victoryData.itemsDropped = QList<QString>{"Iron Sword", "Health Potion"};
        // victoryData.monsterImage = monster->getImage();  // If available

        VictoryScreen *victoryScreen = new VictoryScreen(victoryData, this);
        if (victoryScreen->exec() == QDialog::Accepted) {
            // Player clicked continue
            delete victoryScreen;
            // Return to adventure screen
            stackedWidget->setCurrentWidget(m_adventurePage);
        }
    } else {
        // Show defeat screen (existing pattern)
        CombatResultDialog defeatDialog(false, 0, 0, "", false, this);
        defeatDialog.exec();
    }
}
```

### 6.5 Key Features

| Feature | Implementation |
|---------|----------------|
| **Dramatic Entrance** | Scale (0→1) + Opacity (0→1) animations |
| **Easing** | `OutBack` for scale, `InOutQuad` for opacity |
| **Duration** | 500ms entrance, 1500ms pause, 500ms button pulse |
| **Rich Content** | Monster image, multiple reward types, level-up highlight |
| **Theme Integration** | All colors from Theme:: constants |
| **Keyboard Support** | Space/Enter to continue |
| **Styling** | Nested boxes with border radius, colored backgrounds |

---

## Summary: Implementation Checklist for VictoryScreen

1. **Choose Pattern**: Use QDialog with Q_PROPERTY animations
2. **Header File**: 
   - Inherit from QDialog
   - Add Q_PROPERTY for scale and opacity
   - Create VictoryData struct for parameters
3. **UI Setup**:
   - Use Theme constants exclusively
   - Create nested layouts for sections
   - Make it visually distinct (large fonts, bright colors)
4. **Animations**:
   - Use QPropertyAnimation + QSequentialAnimationGroup
   - Entrance with scale + opacity
   - Pause for reading
   - Optional button pulse for attention
5. **Integration**:
   - Call from MainWindow::handleCombatEnded()
   - Use exec() for blocking modal behavior
   - Handle both victory and defeat flows
6. **Theme Compliance**:
   - Primary colors for main elements
   - Accent colors for highlights
   - Card backgrounds for content areas
   - Use Theme::SPACING_* for all margins/padding

---

## File References

| File | Purpose | Location |
|------|---------|----------|
| CombatResultDialog | Victory/Defeat notification | `/cpp-qt-rpg/src/components/` |
| QuestCompletionDialog | Quest reward display | `/cpp-qt-rpg/src/components/` |
| StoryEventDialog | Narrative moments | `/cpp-qt-rpg/src/views/` |
| MenuOverlay | Full-screen menu system | `/cpp-qt-rpg/src/components/` |
| Theme.h | All color/spacing constants | `/cpp-qt-rpg/src/theme/` |
| MainWindow.cpp | Dialog integration | `/cpp-qt-rpg/src/` |
| AnimationManager | Custom animation handling | `/cpp-qt-rpg/src/components/` |

