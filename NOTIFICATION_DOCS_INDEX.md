# PyRPG Qt Notification Patterns - Documentation Index

## Documentation Overview

This directory contains comprehensive analysis and documentation of notification/toast patterns in the PyRPG Qt codebase.

### Files in This Documentation

1. **NOTIFICATION_RESEARCH_SUMMARY.txt** (8.6 KB)
   - Quick overview of all findings
   - Key takeaways and recommendations
   - File location references
   - Signal flow diagram
   - Quick action items
   - **Start here for a quick overview**

2. **NOTIFICATION_PATTERNS.md** (14 KB)
   - Detailed markdown documentation
   - Comprehensive explanation of each pattern
   - Code examples with line numbers
   - Implementation details
   - Visual styling information
   - **Best for thorough understanding**

3. **NOTIFICATION_PATTERNS.yaml** (9.4 KB)
   - YAML-formatted quick reference
   - Structured data for easy parsing
   - Pattern comparisons
   - Implementation checklists
   - **Best for quick lookup and parsing**

---

## Quick Summary

### Existing Notification Patterns

| Pattern | Type | Status | Best For |
|---------|------|--------|----------|
| Quest Completion | Modal Dialog | Intrusive (⭐⭐) | Quest rewards |
| Level Up | Embedded Widget | Expected (⭐⭐) | Combat result feedback |
| Combat Log | Scrollable Widget | Non-intrusive (⭐⭐⭐⭐⭐) | **Lore discovery** |
| Victory Screen | Full-screen Modal | Blocking (⭐⭐) | Game completion |
| Menu Overlay | Animated Overlay | Semi-modal (⭐⭐⭐) | In-game menu |

### Recommended for Lore Discovery

**Use: LogDisplay combat log widget**

**Why:**
- Non-blocking (doesn't interrupt gameplay)
- Already fully integrated with CodexManager
- Theme-consistent with existing system
- Scalable for multiple discoveries
- Immersive (maintains narrative flow)

**Enhancement:**
Add dedicated "lore" color in `LogDisplay.cpp` (lines 17-25)
```cpp
if (messageType == "lore") return QColor("#9d4edd");  // Purple
```

**Effort:** ~5 minutes
**Status:** Ready to deploy as-is

---

## Core Files Referenced

### Lore Discovery System
- `src/game/CodexManager.h` (lines 32-33: signal)
- `src/game/CodexManager.cpp` (lines 39-52: unlock logic)
- `src/MainWindow.cpp` (lines 753-757: handler)

### LogDisplay Component
- `src/components/LogDisplay.h` (full implementation)
- `src/components/LogDisplay.cpp` (color logic at lines 17-25)

### Level-Up Pattern
- `src/components/CombatResultDialog.cpp` (lines 39-51)

### Theme System
- `src/theme/Theme.h` (color constants)

---

## How to Use This Documentation

### For Quick Lookup
1. Start with **NOTIFICATION_RESEARCH_SUMMARY.txt**
2. Check "Key Findings" section
3. Look up specific file references

### For Detailed Implementation
1. Read **NOTIFICATION_PATTERNS.md**
2. Review code examples with line numbers
3. Follow implementation checklist

### For Structured Reference
1. Parse **NOTIFICATION_PATTERNS.yaml**
2. Use for automated parsing/scripts
3. Reference pattern comparison table

---

## Signal Flow: Lore Discovery

```
LoreFactory creates entry
    ↓
CodexManager::checkDiscoveryTriggers()
    ↓
CodexManager::unlockEntry()
    ↓
Emits: CodexManager::loreUnlocked(entryId, title)
    ↓
MainWindow::handleLoreUnlocked()
    ↓
m_combatPage->addLogEntry("New Codex Entry: ...", "lore")
    ↓
LogDisplay creates styled entry with color border
    ↓
CombatPage log shows new entry
    ↓
Auto-scrolls to newest entry
```

---

## Key Recommendations

### Immediate (No Code Changes)
- Deploy lore discoveries using current LogDisplay
- Player sees "New Codex Entry: [Title]" in combat log

### Enhancement (5 minutes)
- Add dedicated lore color to LogDisplay
- Optional: Add emoji prefix (📖)

### Future (Optional)
- Toast notification for major discoveries
- Sound effects for discovery
- Notification badge on main menu
- Track new/unread lore entries

---

## Qt Patterns Analysis

### Used
- ✅ Custom QDialog subclasses
- ✅ Custom QWidget overlays with animation
- ✅ LogDisplay for passive logging

### Not Used
- ❌ QMessageBox (avoided for theme consistency)
- ❌ Application StatusBar (uses QStackedWidget navigation)
- ❌ QSystemTrayIcon (not applicable to game)

---

## Architecture Strengths

1. **Consistent Theming** - All notifications use Theme:: color constants
2. **Mixed Patterns** - Modal for important events, log for passive info
3. **Integrated Signals** - Clean signal/slot architecture
4. **Non-Intrusive Option** - LogDisplay for frequent events
5. **Animation Support** - QPropertyAnimation for smooth transitions

---

## Implementation Checklist

### Phase 1: Add Lore Color
- [ ] Modify LogDisplay.cpp getBorderColor() (lines 17-25)
- [ ] Add: `if (messageType == "lore") return QColor("#9d4edd");`
- [ ] Update comments with message type documentation

### Phase 2: Testing
- [ ] Trigger lore discovery during gameplay
- [ ] Verify color appears correctly
- [ ] Test multiple rapid discoveries
- [ ] Check scroll behavior with many entries

### Phase 3: Optional Enhancements
- [ ] Add emoji prefix (📖)
- [ ] Consider toast notification
- [ ] Add sound effect
- [ ] Track new lore for menu badge

### Phase 4: Documentation
- [ ] Update CLAUDE.md with LogDisplay guide
- [ ] Document lore discovery flow
- [ ] Create usage examples

---

## File Statistics

| Document | Size | Focus |
|----------|------|-------|
| NOTIFICATION_RESEARCH_SUMMARY.txt | 8.6 KB | Quick overview |
| NOTIFICATION_PATTERNS.md | 14 KB | Detailed analysis |
| NOTIFICATION_PATTERNS.yaml | 9.4 KB | Structured reference |
| **Total** | **31.4 KB** | **Complete documentation** |

---

## Related Files in Codebase

```
cpp-qt-rpg/
├── src/
│   ├── components/
│   │   ├── LogDisplay.h/cpp         (Core for lore notifications)
│   │   ├── QuestCompletionDialog.h/cpp
│   │   ├── CombatResultDialog.h/cpp
│   │   └── MenuOverlay.h/cpp
│   ├── game/
│   │   └── CodexManager.h/cpp       (Signal source)
│   ├── views/
│   │   ├── VictoryScreen.h/cpp
│   │   ├── StoryEventDialog.h/cpp
│   │   └── DialogueView.h/cpp
│   ├── theme/
│   │   └── Theme.h                  (Color constants)
│   └── MainWindow.h/cpp             (Signal handler)
└── NOTIFICATION_*.* (This documentation)
```

---

## Conclusion

The PyRPG Qt codebase has excellent notification infrastructure. For lore discovery, the existing LogDisplay combat log pattern is optimal and requires minimal enhancement for visual distinction.

**Status:** Ready to deploy immediately, with optional enhancements available at low effort.

---

*Documentation generated: November 2, 2025*
*Codebase: PyRPG Qt (C++17, Qt6)*
*Analysis method: Comprehensive grep, code review, and signal flow mapping*
