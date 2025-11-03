# PRD: Launch Cutscene

**Author:** Gemini
**Date:** 2025-11-01
**Status:** In Review

## 1. Idea

Add a skippable cutscene that plays when the game is launched to build excitement for the player.

## 2. Discovery Process Summary

This document is the result of a discovery process that included technical research and user clarification. The initial idea of an AI-generated cutscene was revised to use a pre-made video file to reduce implementation complexity and focus on the core user experience goal. The target user is a **casual gamer**, and the primary goal is to **build excitement**. Success will be measured by **positive player feedback**.

## 3. Visual Documentation Plan

```yaml
diagrams_needed:
  user_flows:
    - Happy path: Player watches the full cutscene.
    - Alternate path: Player skips the cutscene.
  architecture:
    - System components: How the CutscenePlayer interacts with the MainWindow.
  sequences:
    - Event flow for starting and ending the cutscene.
```

### 3.1. User Flow

*   **Happy Path**:
    1.  User launches the game.
    2.  The cutscene video starts playing automatically in full-screen.
    3.  A "Skip" button is visible.
    4.  The video plays to completion.
    5.  The game's main menu appears.

*   **Alternate Path (Skip)**:
    1.  User launches the game.
    2.  The cutscene video starts playing automatically.
    3.  The user clicks the "Skip" button.
    4.  The video stops immediately.
    5.  The game's main menu appears.

### 3.2. Architecture Diagram

```
+---------------------+
|     MainWindow      |
|---------------------|
| - QStackedWidget    |
| - MainMenu          |
| - CutscenePlayer    |
+---------------------+
        |
        | 1. Creates and shows
        |
+---------------------+
|   CutscenePlayer    |
|---------------------|
| - QMediaPlayer      |
| - QVideoWidget      |
|---------------------|
| + play()            |
| + playbackFinished()|
+---------------------+
```

### 3.3. Sequence Diagram

```
User         MainWindow      CutscenePlayer     MainMenu
 |                |                 |              |
 | launches app   |                 |              |
 |--------------->|                 |              |
 |                | create()        |              |
 |                |---------------->|              |
 |                | play()          |              |
 |                |---------------->|              |
 |                |                 | (video plays)|
 |                |                 |              |
 |                | playbackFinished|              |
 |                |<----------------|              |
 |                | showMainMenu()  |              |
 |                |------------------------------->|
 |                |                 |              |
```

## 4. Research Integration

*   **Market Analysis**: Introductory cutscenes are a standard feature in modern games, even for casual audiences. They are effective at establishing the game's tone and story, which helps to build player engagement from the start. For casual gamers, a visually exciting and concise intro is more effective than a long, complex one.
*   **Technical Options**:
    *   **AI-Generated (Original Idea)**: High complexity, requires significant R&D, potential for long generation times, and may have inconsistent quality.
    *   **Pre-made Video (Chosen Approach)**: Low complexity, predictable quality and performance, easy to integrate with existing frameworks (Qt Multimedia). This is the recommended approach.
*   **Risk Assessment**:
    *   **Video Compatibility**: The chosen video format might not be supported on all systems. **Mitigation**: Use a widely supported format like H.264-encoded MP4.
    *   **Performance**: A high-resolution video could cause performance issues on low-end hardware. **Mitigation**: Test with various hardware and provide an optimized video file.
*   **Success Metrics**:
    *   The feature will be considered successful if it receives positive feedback from user testing.
    *   Analytics could be added later to track how many users skip the cutscene. A low skip rate would indicate high engagement.

## 5. User Story Development

**Epic**: Immersive Game Introduction

> **Story**: First-Time Player Experience
>
> **As a** casual gamer,
> **I want** to see an exciting opening cutscene when I start the game for the first time,
> **So that** I can get hyped up and drawn into the world of the game.
>
> **Acceptance Criteria:**
>
> *   [ ] When the game is launched, a video plays automatically before the main menu appears.
> *   [ ] The video fills the screen.
> *   [ ] There is a clear and intuitive way to skip the cutscene (e.g., a "Skip" button or pressing the 'Esc' key).
> *   [ ] If skipped, the video stops, and the main menu appears instantly.
> *   [ ] If the video finishes, the main menu appears automatically.
>
> **Technical Notes:**
>
> *   The implementation will use the `Qt6::Multimedia` module.
> *   The video file will be loaded from the Qt Resource system (`.qrc`).
> *   A new `CutscenePlayer` widget will be created to encapsulate the video playback logic.

## 6. Implementation Strategy

*   **Phase 1 (MVP)**:
    1.  Integrate the Qt Multimedia module.
    2.  Create the `CutscenePlayer` widget.
    3.  Implement playback of a hardcoded video file from the `assets`.
    4.  Implement the skip functionality.
    5.  Integrate the `CutscenePlayer` into the `MainWindow` to show at launch.

*   **Phase 2 (Enhancements)**:
    *   Add a "Don't show again" checkbox or a setting in the options menu to disable the cutscene on future launches.
    *   Add fade-in and fade-out transitions for a smoother experience.
    *   Investigate adding subtitles to the cutscene for accessibility.
