# TASK PRP: Quest Onboarding Tutorial

## Task: "Help new players understand and get started on their first quest after character creation"

## Context Section

```yaml
context:
  docs:
    - url: cpp-qt-rpg/src/game/QuestManager.cpp
      focus: QuestManager::loadQuests() auto-accepts first quest, checkQuestUnlocks() unlocks based on level
    - url: cpp-qt-rpg/src/models/StoryEvent.h
      focus: StoryEvent struct, triggerType, eventText for explaining quest system
    - url: cpp-qt-rpg/src/game/StoryManager.h
      focus: eventTriggered signal, onQuestStarted() handler, automatic story event triggering
    - url: cpp-qt-rpg/src/MainWindow.cpp
      focus: handleStoryEventTriggered() displays events via StoryEventDialog

  patterns:
    - file: cpp-qt-rpg/src/game/factories/StoryEventFactory.cpp
      copy: Pattern for creating story events with triggerType="quest_start"
    - file: cpp-qt-rpg/src/game/QuestManager.cpp:18-54
      copy: Automatic quest acceptance pattern for new players
    - file: cpp-qt-rpg/src/MainWindow.cpp:664-671
      copy: Quest acceptance flow with UI refresh

  gotchas:
    - issue: "StoryEventDialog is modal (exec()), blocks UI thread"
      fix: "Dialog displays after quest acceptance, guides player to next steps"
    - issue: "Quest system already auto-accepts first quest for new players"
      fix: "Trigger story event immediately after auto-acceptance to explain what happened"
    - issue: "No CharacterCustomizationPage in current flow (uses NewGameView)"
      fix: "Trigger tutorial after handleCharacterCreation() in MainWindow"
    - issue: "Story events auto-trigger on quest start via StoryManager connection"
      fix: "Create 'quest_system_intro' event with triggerType='quest_start' and triggerId='main_quest_01'"
```

## Task Structure

```
ACTION cpp-qt-rpg/src/game/factories/StoryEventFactory.cpp:
  - OPERATION: Add new "quest_system_intro" story event with detailed explanation of quest system
  - VALIDATE: Compiles successfully, event registered in getAllEvents()
  - IF_FAIL: Check eventId matches triggerId, ensure proper QMap entry
  - ROLLBACK: Remove added event code

ACTION cpp-qt-rpg/src/models/StoryEvent.h:
  - OPERATION: Ensure StoryEvent struct has necessary fields (already complete)
  - VALIDATE: StoryEvent has all required fields (eventId, triggerType, eventText, etc.)
  - IF_FAIL: Compare against existing StoryEvent struct definition
  - ROLLBACK: No changes needed (file already correct)

ACTION cpp-qt-rpg/src/game/StoryManager.cpp:
  - OPERATION: Verify onQuestStarted() triggers events with matching triggerId
  - VALIDATE: StoryManager::onQuestStarted() correctly finds and triggers matching events
  - IF_FAIL: Check QuestManager::questAccepted signal connection, ensure triggerId matches
  - ROLLBACK: No changes needed (existing pattern works)

ACTION cpp-qt-rpg/src/MainWindow.cpp:
  - OPERATION: Verify handleStoryEventTriggered() displays StoryEventDialog with auto-close option
  - VALIDATE: StoryEventDialog pops up after quest acceptance, blocks until dismissed
  - IF_FAIL: Check StoryEventDialog import, ensure dialog.exec() is called
  - ROLLBACK: Restore original handleStoryEventTriggered() if modified

ACTION cpp-qt-rpg/src/views/StoryEventDialog.h:
  - OPERATION: Add "Don't show again" checkbox to StoryEventDialog for tutorial dismissal
  - VALIDATE: Checkbox saves preference via QSettings, hides future tutorial events
  - IF_FAIL: Add QCheckBox member variable, connect to QSettings in constructor
  - ROLLBACK: Remove checkbox code, keep basic dialog

ACTION cpp-qt-rpg/src/game/QuestManager.cpp:
  - OPERATION: Optionally modify first quest description for better onboarding clarity
  - VALIDATE: Quest "A Dark Omen" has clear, actionable description
  - IF_FAIL: Update quest->longDescription in QuestFactory instead
  - ROLLBACK: Restore original quest description

ACTION cpp-qt-rpg/ (project root):
  - OPERATION: Run comprehensive test suite to verify onboarding flow
  - VALIDATE: All tests pass, manual test shows tutorial after character creation
  - IF_FAIL: Check Qt Test output, fix failing tests individually
  - ROLLBACK: Revert to last known good state via git
```

## Task Sequencing

### 1. Setup Tasks (Foundation)
- ✅ Analyze codebase structure and patterns
- ✅ Review existing quest system and story event integration
- ✅ Identify character creation flow and game initialization

### 2. Core Changes (Implementation)
1. **Create Tutorial Story Event** - Add quest_system_intro event to StoryEventFactory
2. **Enhance StoryEventDialog** - Add dismiss option for better UX
3. **Verify Integration Points** - Ensure story event triggers after quest acceptance
4. **Polish Quest Description** - Make first quest more onboarding-focused

### 3. Integration (System Connection)
- Verify StoryManager connection to QuestManager (already exists)
- Confirm MainWindow event handler (already exists)
- Test story event triggering on quest_start (automatic via connection)

### 4. Validation (Testing)
- Compile project successfully
- Run full test suite (ctest from build directory)
- Manual test: Character creation → Tutorial event → Quest log visibility
- Verify tutorial doesn't re-trigger on save/load

### 5. Cleanup (Polish)
- Document tutorial dismissal behavior
- Review onboarding text clarity
- Test edge cases (skip tutorial, reload game, etc.)

## Validation Strategy

### Unit Tests
- **test_story_events.cpp**: Verify quest_system_intro event exists and has correct trigger
- **test_quest_system.cpp**: Verify quest auto-acceptance for new players
- **test_story_quest_integration.cpp**: New test for story event triggering on quest start

### Integration Tests
- **test_navigation_flow.cpp**: Verify tutorial displays after character creation
- **test_mainwindow.cpp**: Verify event handler displays dialog correctly

### Manual Testing Checklist
- [ ] Create new character → Tutorial dialog appears
- [ ] Tutorial explains: What quests are, how to view them, how they work
- [ ] "Accept" or close tutorial → Game continues normally
- [ ] Quest log shows "A Dark Omen" as active quest
- [ ] Tutorial explains how to track quest progress
- [ ] Checkbox "Don't show again" persists across game sessions

### Performance Checks
- StoryEventDialog uses QPlainTextEdit (efficient for long text)
- QSettings writes minimal data (one bool value)
- No performance impact on quest tracking system

## User Interaction Points

### 1. Task Review (Pre-Implementation)
**Confirm**:
- Tutorial content should be informative but concise (2-3 paragraphs)
- Dialog should have clear dismissal option ("Got it!" button)
- Tutorial only shows once per new game (not on load)
- Alternative: Add "Help" menu item to re-read tutorial later

**Decide**:
- Should tutorial be skippable entirely or mandatory?
- Should we add a "Help" menu option to replay tutorial?
- Tutorial tone: Gameplay-focused or story/narrative-focused?

### 2. Risk Assessment (During Implementation)
**High Risk**: StoryEventDialog blocking flow
- **Impact**: Player can't proceed if dialog doesn't display
- **Mitigation**: Check StoryEventDialog creation and exec() call
- **Rollback**: Comment out story event in StoryEventFactory

**Medium Risk**: Quest auto-acceptance not working
- **Impact**: Tutorial shows but no quest to explain
- **Mitigation**: Verify QuestManager::loadQuests() logic
- **Rollback**: Manually call acceptQuest() after loadQuests()

**Low Risk**: Tutorial appears on save game load
- **Impact**: Annoying for returning players
- **Mitigation**: Only trigger for new games (player->quests.isEmpty())
- **Rollback**: Add game state flag "hasSeenTutorial"

### 3. Success Criteria (Post-Implementation)
- ✅ New player sees tutorial explaining quest system after character creation
- ✅ Tutorial clearly explains: what quests are, how to view/accept/complete them
- ✅ First quest "A Dark Omen" is active and visible in quest log
- ✅ Player can dismiss tutorial and continue playing
- ✅ All existing tests continue to pass
- ✅ No performance degradation in quest tracking

## Critical Elements

### Debug Patterns
```cpp
// In StoryManager.cpp for debugging
void StoryManager::onQuestStarted(const QString &questId) {
    qDebug() << "Quest started:" << questId;

    // Find matching story event
    for (StoryEvent* event : m_allEvents) {
        if (event->triggerType == "quest_start" && event->triggerId == questId) {
            qDebug() << "Triggering story event:" << event->eventId;
            emit eventTriggered(*event);
        }
    }
}
```

### Performance Checks
- StoryEventDialog creation: <10ms
- QSettings read/write: <1ms
- Story event lookup: O(n) where n=small number of events
- Quest tracking: No performance impact (already exists)

### Security Concerns
- Story text is static (hardcoded), no user input
- QSettings uses application-specific location (safe)
- No network calls or external resources

### Assumptions
- QuestManager already auto-accepts first quest for new players
- StoryManager already connects to QuestManager signals
- MainWindow already displays story events via StoryEventDialog
- StoryEventDialog is modal and blocks UI thread appropriately

## Output

Save as: `TASK_PRP/PRPs/quest_onboarding_tutorial.md`

## Quality Checklist

- [x] All changes identified (StoryEventFactory, StoryEventDialog, QuestFactory)
- [x] Dependencies mapped (QuestManager → StoryManager → MainWindow → StoryEventDialog)
- [x] Each task has validation (compile, test, manual verification)
- [x] Rollback steps included (git revert, comment out code)
- [x] Debug strategies provided (qDebug logging, manual test checklist)
- [x] Performance impact noted (minimal - leverages existing systems)
- [x] Security checked (static content, local settings only)
- [x] No missing edge cases (save/load, skip tutorial, replay help)

## Notes
- **Architecture**: Leverages existing story event and quest system integration
- **Complexity**: Low-Medium (primarily adding content, minimal code changes)
- **Testing**: Existing test suite covers core systems, manual test for UX
- **Time Estimate**: 2-3 hours (mostly content creation, minimal coding)
