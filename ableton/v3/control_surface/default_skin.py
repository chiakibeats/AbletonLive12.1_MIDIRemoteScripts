# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\default_skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .colors import BasicColors
from .skin import Skin, merge_skins

def create_skin(skin=None, colors=None):
    pass
    skins = [default_skin]
    if skin:
        skins.append(Skin(skin))
    if colors:
        skins.append(Skin(colors))
    return merge_skins(*skins)

class DefaultColors:
    pass

    class DefaultButton:
        pass
        On = BasicColors.ON
        Off = BasicColors.OFF
        Disabled = BasicColors.OFF

    class TargetTrack:
        pass
        LockOn = BasicColors.ON
        LockOff = BasicColors.OFF

    class Transport:
        pass
        PlayOn = BasicColors.ON
        PlayOff = BasicColors.OFF
        StopOn = BasicColors.ON
        StopOff = BasicColors.OFF
        AutomationArmOn = BasicColors.ON
        AutomationArmOff = BasicColors.OFF
        LoopOn = BasicColors.ON
        LoopOff = BasicColors.OFF
        MetronomeOn = BasicColors.ON
        MetronomeOff = BasicColors.OFF
        PunchOn = BasicColors.ON
        PunchOff = BasicColors.OFF
        TapTempoPressed = BasicColors.ON
        TapTempo = BasicColors.OFF
        NudgePressed = BasicColors.ON
        Nudge = BasicColors.OFF
        SeekPressed = BasicColors.ON
        Seek = BasicColors.OFF
        CanReEnableAutomation = BasicColors.ON
        CanCaptureMidi = BasicColors.ON
        CanJumpToCue = BasicColors.ON
        CannotJumpToCue = BasicColors.OFF
        SetCuePressed = BasicColors.ON
        SetCue = BasicColors.OFF
        RecordQuantizeOn = BasicColors.ON
        RecordQuantizeOff = BasicColors.OFF

    class Recording:
        pass
        ArrangementRecordOn = BasicColors.ON
        ArrangementRecordOff = BasicColors.OFF
        ArrangementOverdubOn = BasicColors.ON
        ArrangementOverdubOff = BasicColors.OFF
        SessionRecordOn = BasicColors.ON
        SessionRecordTransition = BasicColors.ON
        SessionRecordOff = BasicColors.OFF
        SessionOverdubOn = BasicColors.ON
        SessionOverdubOff = BasicColors.OFF
        NewPressed = BasicColors.ON
        New = BasicColors.OFF

    class UndoRedo:
        pass
        UndoPressed = BasicColors.ON
        Undo = BasicColors.OFF
        RedoPressed = BasicColors.ON
        Redo = BasicColors.OFF

    class ViewControl:
        pass
        TrackPressed = BasicColors.ON
        Track = BasicColors.ON
        ScenePressed = BasicColors.ON
        Scene = BasicColors.ON

    class ViewToggle:
        pass
        SessionOn = BasicColors.ON
        SessionOff = BasicColors.OFF
        DetailOn = BasicColors.ON
        DetailOff = BasicColors.OFF
        ClipOn = BasicColors.ON
        ClipOff = BasicColors.OFF
        BrowserOn = BasicColors.ON
        BrowserOff = BasicColors.OFF

    class Zoom:
        pass
        VerticalPressed = BasicColors.ON
        Vertical = BasicColors.ON
        HorizontalPressed = BasicColors.ON
        Horizontal = BasicColors.ON

    class Mixer:
        pass
        ArmOn = BasicColors.ON
        ArmOff = BasicColors.OFF
        MuteOn = BasicColors.ON
        MuteOff = BasicColors.OFF
        SoloOn = BasicColors.ON
        SoloOff = BasicColors.OFF
        Selected = BasicColors.ON
        NotSelected = BasicColors.OFF
        CrossfadeA = BasicColors.ON
        CrossfadeB = BasicColors.ON
        CrossfadeOff = BasicColors.OFF
        CycleSendIndexPressed = BasicColors.ON
        CycleSendIndex = BasicColors.OFF
        IncrementSendIndexPressed = BasicColors.OFF
        IncrementSendIndex = BasicColors.ON
        NoTrack = BasicColors.OFF

    class Session:
        pass
        Slot = BasicColors.OFF
        SlotRecordButton = BasicColors.OFF
        NoSlot = BasicColors.OFF
        ClipStopped = BasicColors.OFF
        ClipTriggeredPlay = BasicColors.ON
        ClipTriggeredRecord = BasicColors.ON
        ClipPlaying = BasicColors.ON
        ClipRecording = BasicColors.ON
        Scene = BasicColors.OFF
        SceneTriggered = BasicColors.ON
        NoScene = BasicColors.OFF
        StopClipTriggered = BasicColors.ON
        StopClip = BasicColors.OFF
        StopClipDisabled = BasicColors.OFF
        StopAllClipsPressed = BasicColors.ON
        StopAllClips = BasicColors.OFF
        NavigationPressed = BasicColors.ON
        Navigation = BasicColors.ON

    class Zooming:
        pass
        Selected = BasicColors.OFF
        Stopped = BasicColors.ON
        Playing = BasicColors.ON
        Empty = BasicColors.OFF

    class ClipActions:
        pass
        Delete = BasicColors.OFF
        DeletePressed = BasicColors.ON
        Double = BasicColors.OFF
        DoublePressed = BasicColors.ON
        Duplicate = BasicColors.OFF
        DuplicatePressed = BasicColors.ON
        Quantize = BasicColors.OFF
        QuantizedPressed = BasicColors.ON

    class Device:
        pass
        On = BasicColors.ON
        Off = BasicColors.OFF
        FoldOn = BasicColors.ON
        FoldOff = BasicColors.OFF
        LockOn = BasicColors.ON
        LockOff = BasicColors.OFF
        NavigationPressed = BasicColors.ON
        Navigation = BasicColors.ON

        class Bank:
            Selected = BasicColors.ON
            NotSelected = BasicColors.OFF
            NavigationPressed = BasicColors.ON
            Navigation = BasicColors.ON

    class Accent:
        pass
        On = BasicColors.ON
        Off = BasicColors.OFF

    class DrumGroup:
        pass
        PadEmpty = BasicColors.OFF
        PadFilled = BasicColors.OFF
        PadSelected = BasicColors.ON
        PadMuted = BasicColors.ON
        PadMutedSelected = BasicColors.ON
        PadSoloed = BasicColors.ON
        PadSoloedSelected = BasicColors.ON
        PadAction = BasicColors.ON
        ScrollPressed = BasicColors.ON
        Scroll = BasicColors.ON

    class SlicedSimpler:
        pass
        NoSlice = BasicColors.OFF
        SliceNotSelected = BasicColors.OFF
        SliceSelected = BasicColors.ON
        NextSlice = BasicColors.ON
        PadAction = BasicColors.ON
        ScrollPressed = BasicColors.ON
        Scroll = BasicColors.ON

    class NoteEditor:
        pass
        NoClip = BasicColors.OFF
        StepDisabled = BasicColors.OFF
        StepEmpty = BasicColors.OFF
        StepFilled = BasicColors.ON
        StepMuted = BasicColors.OFF

        class Resolution:
            Selected = BasicColors.ON
            NotSelected = BasicColors.OFF

    class LoopSelector:
        pass
        InsideLoopSelected = BasicColors.ON
        InsideLoop = BasicColors.OFF
        OutsideLoopSelected = BasicColors.ON
        OutsideLoop = BasicColors.OFF
        Playhead = BasicColors.OFF
        PlayheadRecord = BasicColors.OFF
        NavigationPressed = BasicColors.ON
        Navigation = BasicColors.ON

    class Clipboard:
        pass
        Empty = BasicColors.OFF
        Filled = BasicColors.ON
        CopyPressed = BasicColors.ON

    class Translation:
        pass

        class Channel:
            Selected = BasicColors.ON
            NotSelected = BasicColors.OFF
default_skin = Skin(DefaultColors)