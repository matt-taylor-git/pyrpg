# Dialog & Overlay Quick Reference

## Pattern Decision Tree

```
Need modal content?
├─ YES: Simple notification (victory, quest, story)?
│   └─ USE QDialog
│       - CombatResultDialog
│       - QuestCompletionDialog
│       - StoryEventDialog
│
└─ NO: Complex full-screen UI (menu, inventory)?
    └─ USE Custom Overlay (QWidget)
        - MenuOverlay (example in codebase)
```

## QDialog Template (Copy-Paste Ready)

```cpp
// MyDialog.h
#ifndef MYDIALOG_H
#define MYDIALOG_H

#include <QDialog>

class QLabel;
class QPushButton;

class MyDialog : public QDialog
{
    Q_OBJECT

public:
    explicit MyDialog(const QString &data, QWidget *parent = nullptr);

private:
    void setupUi(const QString &data);
};

#endif // MYDIALOG_H
```

```cpp
// MyDialog.cpp
#include "MyDialog.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QFont>

MyDialog::MyDialog(const QString &data, QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle("My Dialog");
    setModal(true);
    setMinimumSize(400, 300);
    setupUi(data);
}

void MyDialog::setupUi(const QString &data)
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setSpacing(Theme::SPACING_MD);
    layout->setContentsMargins(Theme::SPACING_XL, Theme::SPACING_XL,
                              Theme::SPACING_XL, Theme::SPACING_XL);

    // Dialog background
    setStyleSheet(QString(
        "QDialog {"
        "    background-color: %1;"
        "    border: 2px solid %2;"
        "    border-radius: %3px;"
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_MD));

    // Title
    QLabel *titleLabel = new QLabel("Title");
    QFont titleFont;
    titleFont.setPixelSize(Theme::FONT_SIZE_XXL);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    titleLabel->setStyleSheet(QString("color: %1;").arg(Theme::PRIMARY.name()));
    layout->addWidget(titleLabel);

    // Content
    QLabel *contentLabel = new QLabel(data);
    contentLabel->setAlignment(Qt::AlignCenter);
    contentLabel->setWordWrap(true);
    contentLabel->setStyleSheet(QString("color: %1; font-size: %2px;")
        .arg(Theme::FOREGROUND.name())
        .arg(Theme::FONT_SIZE_MD));
    layout->addWidget(contentLabel);

    layout->addStretch();

    // Button
    QPushButton *button = new QPushButton("Continue");
    button->setMinimumHeight(40);
    button->setStyleSheet(QString(
        "QPushButton {"
        "    background-color: %1;"
        "    color: %2;"
        "    border: none;"
        "    border-radius: %3px;"
        "    padding: %4px;"
        "    font-weight: %5;"
        "}"
        "QPushButton:hover { background-color: %6; }"
    ).arg(Theme::ACCENT.name())
     .arg(Theme::ACCENT_FOREGROUND.name())
     .arg(Theme::BORDER_RADIUS_SM)
     .arg(Theme::SPACING_MD)
     .arg(Theme::FONT_WEIGHT_BOLD)
     .arg(Theme::ACCENT.lighter(110).name()));

    connect(button, &QPushButton::clicked, this, &QDialog::accept);
    layout->addWidget(button);
}
```

**Usage**:
```cpp
MyDialog dialog("Content here", this);
if (dialog.exec() == QDialog::Accepted) {
    // Handle acceptance
}
```

## Custom Overlay Template (Copy-Paste Ready)

```cpp
// MyOverlay.h
#ifndef MYOVERLAY_H
#define MYOVERLAY_H

#include <QWidget>

class QPropertyAnimation;

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
    
    QWidget *m_contentWidget;
    QPropertyAnimation *m_animation;
    qreal m_opacity;
    QWidget *m_previousFocusWidget;
};

#endif // MYOVERLAY_H
```

```cpp
// MyOverlay.cpp
#include "MyOverlay.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QPropertyAnimation>
#include <QPainter>
#include <QKeyEvent>
#include <QMouseEvent>
#include <QApplication>
#include <QLabel>

MyOverlay::MyOverlay(QWidget *parent)
    : QWidget(parent)
    , m_opacity(0.0)
    , m_previousFocusWidget(nullptr)
{
    // Enable transparency and custom rendering
    setAttribute(Qt::WA_TransparentForMouseEvents, false);
    setAttribute(Qt::WA_NoSystemBackground);
    setAttribute(Qt::WA_TranslucentBackground);
    setFocusPolicy(Qt::StrongFocus);

    setupUi();

    // Create animation
    m_animation = new QPropertyAnimation(this, "opacity");
    m_animation->setDuration(200);

    connect(m_animation, &QPropertyAnimation::finished, this, [this]() {
        if (m_animation->endValue().toReal() == 0.0) {
            hide();
            if (m_previousFocusWidget) {
                m_previousFocusWidget->setFocus();
            }
            emit overlayHidden();
        }
    });

    hide();
}

void MyOverlay::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(50, 50, 50, 50);

    m_contentWidget = new QWidget();
    m_contentWidget->setStyleSheet(QString(
        "QWidget { "
        "background-color: %1; "
        "border: 2px solid %2; "
        "border-radius: %3px; "
        "}"
    ).arg(Theme::CARD.name())
     .arg(Theme::BORDER.name())
     .arg(Theme::BORDER_RADIUS_XL));

    QVBoxLayout *contentLayout = new QVBoxLayout(m_contentWidget);
    contentLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG,
                                     Theme::SPACING_LG, Theme::SPACING_LG);

    QLabel *label = new QLabel("Overlay Content");
    contentLayout->addWidget(label);

    mainLayout->addWidget(m_contentWidget);
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

void MyOverlay::setOpacity(qreal opacity)
{
    m_opacity = opacity;
    update();
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
```

**Usage**:
```cpp
// Create and show
MyOverlay *overlay = new MyOverlay(this);
overlay->showOverlay();

// Handle closing
connect(overlay, &MyOverlay::overlayHidden, [overlay]() {
    overlay->deleteLater();
});
```

## Theme Constants Quick Reference

```cpp
// Colors
Theme::BACKGROUND        // Dark bg (#1a1826)
Theme::FOREGROUND        // Light text (#f1f0f2)
Theme::CARD              // Card/Dialog bg (#221e30)
Theme::PRIMARY           // Crimson success (#dc3545)
Theme::ACCENT            // Purple highlight (#8c52ff)
Theme::SECONDARY         // Secondary bg (#352e4d)
Theme::DESTRUCTIVE       // Red danger (#d23a1a)
Theme::BORDER            // Subtle borders (#3e3754)

// Spacing (pixels)
Theme::SPACING_XS        // 4px
Theme::SPACING_SM        // 8px
Theme::SPACING_MD        // 15px
Theme::SPACING_LG        // 20px
Theme::SPACING_XL        // 30px

// Border Radius
Theme::BORDER_RADIUS_SM  // 4px (buttons)
Theme::BORDER_RADIUS_MD  // 6px (cards)
Theme::BORDER_RADIUS_LG  // 8px (panels)
Theme::BORDER_RADIUS_XL  // 12px (overlays)

// Font Sizes
Theme::FONT_SIZE_SM      // 12px (secondary)
Theme::FONT_SIZE_MD      // 14px (body)
Theme::FONT_SIZE_LG      // 16px (headers)
Theme::FONT_SIZE_XL      // 18px (titles)
Theme::FONT_SIZE_XXL     // 24px (main)
Theme::FONT_SIZE_XXXL    // 36px (hero)

// Font Weights
Theme::FONT_WEIGHT_NORMAL     // 400
Theme::FONT_WEIGHT_MEDIUM     // 500
Theme::FONT_WEIGHT_SEMIBOLD   // 600
Theme::FONT_WEIGHT_BOLD       // 700
```

## Common Styling Patterns

### Title Label
```cpp
QLabel *title = new QLabel("Title");
QFont font;
font.setPixelSize(Theme::FONT_SIZE_XXL);
font.setWeight(static_cast<QFont::Weight>(Theme::FONT_WEIGHT_BOLD));
title->setFont(font);
title->setStyleSheet(QString("color: %1;").arg(Theme::PRIMARY.name()));
```

### Content Box
```cpp
QLabel *box = new QLabel(content);
box->setStyleSheet(QString(
    "background-color: %1; "
    "color: %2; "
    "padding: %3px; "
    "border-radius: %4px; "
    "border: 1px solid %5;"
).arg(Theme::CARD.name())
 .arg(Theme::FOREGROUND.name())
 .arg(Theme::SPACING_MD)
 .arg(Theme::BORDER_RADIUS_SM)
 .arg(Theme::BORDER.name()));
```

### Button (Primary)
```cpp
QPushButton *btn = new QPushButton("Click");
btn->setMinimumHeight(40);
btn->setStyleSheet(QString(
    "QPushButton {"
    "    background-color: %1;"
    "    color: %2;"
    "    border: none;"
    "    border-radius: %3px;"
    "    padding: %4px;"
    "    font-weight: %5;"
    "}"
    "QPushButton:hover { background-color: %6; }"
    "QPushButton:pressed { background-color: %7; }"
).arg(Theme::ACCENT.name())
 .arg(Theme::ACCENT_FOREGROUND.name())
 .arg(Theme::BORDER_RADIUS_SM)
 .arg(Theme::SPACING_MD)
 .arg(Theme::FONT_WEIGHT_BOLD)
 .arg(Theme::ACCENT.lighter(110).name())
 .arg(Theme::PRIMARY.name()));
```

## Animation Pattern (Q_PROPERTY)

```cpp
// Header
class MyWidget : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)

public:
    qreal opacity() const { return m_opacity; }
    void setOpacity(qreal op) { m_opacity = op; update(); }

private:
    qreal m_opacity;
};

// Usage
QPropertyAnimation *anim = new QPropertyAnimation(widget, "opacity");
anim->setStartValue(0.0);
anim->setEndValue(1.0);
anim->setDuration(300);
anim->setEasingCurve(QEasingCurve::InOutQuad);
anim->start();
```

## Key Methods

### QDialog
- `exec()` - Show modally (blocking)
- `open()` - Show non-blocking
- `accept()` - Return QDialog::Accepted
- `reject()` - Return QDialog::Rejected
- `setModal(true)` - Make modal
- `setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint)` - Custom frame

### Custom Overlay (QWidget)
- `show()` - Make visible
- `hide()` - Make invisible
- `raise()` - Bring to front
- `setFocus()` - Take focus
- `setAttribute(Qt::WA_TranslucentBackground)` - Enable transparency
- `setOpacity(value)` - Set opacity (via Q_PROPERTY)

## Integration Checklist

- [ ] Include Theme.h
- [ ] Use Theme constants (no hardcoded colors)
- [ ] Set minimum size appropriately
- [ ] Style dialog background
- [ ] Create logical content sections
- [ ] Style buttons with hover/pressed states
- [ ] Connect signals properly
- [ ] Test keyboard interaction (ESC, Enter)
- [ ] Test with different window sizes
- [ ] Check focus behavior

## Files to Reference

- CombatResultDialog: `/cpp-qt-rpg/src/components/CombatResultDialog.h/cpp`
- QuestCompletionDialog: `/cpp-qt-rpg/src/components/QuestCompletionDialog.h/cpp`
- StoryEventDialog: `/cpp-qt-rpg/src/views/StoryEventDialog.h/cpp`
- MenuOverlay: `/cpp-qt-rpg/src/components/MenuOverlay.h/cpp`
- Theme: `/cpp-qt-rpg/src/theme/Theme.h`
