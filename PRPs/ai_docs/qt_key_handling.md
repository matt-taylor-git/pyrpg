# Qt Key Event Handling Documentation

## Overview
Qt provides two main mechanisms for handling keyboard input: `QKeyEvent` via `keyPressEvent()` overrides and `QShortcut` objects.

## QKeyEvent and keyPressEvent

### Basic Usage
Override `keyPressEvent(QKeyEvent *event)` in QWidget subclasses:

```cpp
void MyWidget::keyPressEvent(QKeyEvent *event) {
    if (event->key() == Qt::Key_I) {
        // Handle 'I' key press
        handleInventoryShortcut();
        event->accept();  // Mark event as handled
        return;
    }
    // Call parent implementation for unhandled keys
    QWidget::keyPressEvent(event);
}
```

### Key Constants
- `Qt::Key_I` for 'I' key
- `Qt::Key_S` for 'S' key
- `Qt::Key_L` for 'L' key
- `Qt::Key_Escape` for ESC
- `Qt::Key_Return` or `Qt::Key_Enter` for Enter
- Arrow keys: `Qt::Key_Up`, `Qt::Key_Down`, `Qt::Key_Left`, `Qt::Key_Right`

### Event Acceptance
- Key events start with `isAccepted() == true`
- Call `event->accept()` to handle, `event->ignore()` to propagate
- Always call parent implementation for unhandled keys

### Focus Requirements
- Widget must have focus to receive key events
- Set focus policy: `setFocusPolicy(Qt::StrongFocus)`
- Check focus: `hasFocus()`

### Modifiers
```cpp
if (event->modifiers() & Qt::ControlModifier) {
    // Ctrl key held
}
```

## QShortcut Class

### Basic Usage
Create shortcut objects connected to slots:

```cpp
QShortcut *shortcut = new QShortcut(QKeySequence("Ctrl+S"), this);
connect(shortcut, &QShortcut::activated, this, &MyClass::handleSave);
```

### Key Sequences
- String format: `"Ctrl+I"`, `"Alt+F4"`
- Qt::Key constants: `QKeySequence(Qt::Key_I)`
- Multiple keys: `QKeySequence("Ctrl+I, I")`

### Context
- `Qt::WidgetShortcut`: Active when widget has focus
- `Qt::WindowShortcut`: Active when window has focus
- `Qt::ApplicationShortcut`: Always active

## Best Practices

### When to Use QKeyEvent
- Complex key handling logic
- Navigation within widgets (arrow keys, etc.)
- Game controls requiring continuous input
- Custom shortcuts not fitting QShortcut patterns

### When to Use QShortcut
- Standard application shortcuts (Ctrl+S, Ctrl+O)
- Menu accelerators
- Simple action triggering
- When shortcut conflicts need automatic resolution

### Common Patterns in Qt Applications
```cpp
// Global shortcuts in MainWindow
void MainWindow::keyPressEvent(QKeyEvent *event) {
    if (event->key() == Qt::Key_Escape) {
        handleEscape();
        return;
    }
    QMainWindow::keyPressEvent(event);
}

// Widget-specific navigation
void InventoryWidget::keyPressEvent(QKeyEvent *event) {
    switch (event->key()) {
        case Qt::Key_Up:
            selectPreviousItem();
            break;
        case Qt::Key_Down:
            selectNextItem();
            break;
        case Qt::Key_Return:
            activateSelectedItem();
            break;
        default:
            QWidget::keyPressEvent(event);
    }
}
```

### Gotchas
- Focus must be on widget for keyPressEvent
- QShortcut requires proper parent for cleanup
- Key events propagate up widget hierarchy if not handled
- Modifier keys alone don't generate text() content
- Auto-repeat can cause multiple events

### Testing Key Events
Use QTest for unit testing:

```cpp
void TestWidget::testKeyPress() {
    MyWidget widget;
    widget.show();
    widget.setFocus();
    
    QTest::keyClick(&widget, Qt::Key_I);
    // Verify expected behavior
}
```

## References
- Qt 6 QKeyEvent: https://doc.qt.io/qt-6/qkeyevent.html
- Qt 6 QShortcut: https://doc.qt.io/qt-6/qshortcut.html
- Qt Keyboard Focus: https://doc.qt.io/qt-6/qwidget.html#focus-policy
