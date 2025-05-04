# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from functools import partial
from .colors import AnimationSpeed, Colors, make_blinking_color, make_color_for_liveobj, make_dimmed_color_for_liveobj, make_pulsing_color, make_pulsing_color_for_liveobj

class Skin:

    class DefaultButton:
        Pressed = Colors.WHITE
        Back = Colors.DARK_GREY
        ShiftButtonLocked = Colors.WHITE_PULSE_HALF

    class ClipActions:
        Double = Colors.DARK_GREY
        DoublePressed = Colors.WHITE
        Quantize = Colors.DARK_GREY
        QuantizePressed = Colors.WHITE

    class NoteRepeat:
        Menu = Colors.WHITE_WITH_ICON_PULSE_HALF
        On = Colors.WHITE_WITH_ICON
        Off = Colors.DARK_GREY

    class Transport:
        PlayOn = Colors.GREEN
        PlayOff = Colors.DARK_GREY
        MetronomeOn = Colors.DARK_GREY_WITH_ICON
        MetronomeOff = Colors.DARK_GREY
        CanCaptureMidi = Colors.DARK_GREY

    class Recording:
        ArrangementRecordOn = Colors.RED
        ArrangementRecordOff = Colors.DARK_GREY
        SessionRecordOn = Colors.RED
        SessionRecordTransition = Colors.RED_BLINK_QUARTER
        SessionRecordOff = Colors.DARK_GREY
        New = Colors.DARK_GREY
        NewPressed = Colors.WHITE

    class UndoRedo:
        Undo = Colors.DARK_GREY
        Redo = Colors.DARK_GREY

    class TrackList:
        Selected = Colors.WHITE
        NotSelected = make_color_for_liveobj
        Muted = make_dimmed_color_for_liveobj
        MutedSelected = Colors.LIGHT_GREY
        Armed = lambda x: make_pulsing_color(Colors.RED, make_color_for_liveobj(x), speed=AnimationSpeed.half)
        ArmedSelected = lambda _: make_pulsing_color(Colors.RED, Colors.WHITE, speed=AnimationSpeed.half)

    class Session:
        SlotRecordButton = Colors.RED_SHADE
        SlotTriggeredPlay = Colors.GREEN_BLINK_QUARTER
        SlotSelected = Colors.LIGHT_GREY
        ClipStopped = make_color_for_liveobj
        ClipTriggeredPlay = lambda _: make_blinking_color(Colors.WHITE, Colors.GREEN)
        ClipTriggeredRecord = Colors.RED_BLINK_QUARTER
        ClipPlaying = lambda x: make_pulsing_color(Colors.WHITE, make_dimmed_color_for_liveobj(x))
        ClipRecording = lambda x: make_pulsing_color(Colors.RED, make_dimmed_color_for_liveobj(x))
        Scene = Colors.GREEN
        SceneTriggered = Colors.GREEN_BLINK_QUARTER
        StopClip = Colors.LIGHT_GREY
        StopClipDisabled = Colors.DARK_GREY
        StopClipTriggered = Colors.RED_BLINK_QUARTER
        StopAllClipsPressed = Colors.WHITE
        StopAllClips = Colors.DARK_GREY
        Navigation = Colors.DARK_GREY

    class Zooming:
        Selected = Colors.WHITE
        Stopped = Colors.LIGHT_GREY
        Playing = make_pulsing_color(Colors.WHITE, Colors.GREEN)

    class Accent:
        On = Colors.DARK_GREY_WITH_ICON
        Off = Colors.DARK_GREY

    class Instrument:
        PadAction = Colors.WHITE
        NoteBase = make_color_for_liveobj
        NoteScale = Colors.LIGHT_GREY
        NoteNotScale = Colors.OFF
        NoteInvalid = Colors.OFF
        NoteInStep = Colors.WHITE
        NoteSelected = Colors.WHITE
        Scroll = Colors.DARK_GREY

    class DrumGroup:
        PadAction = Colors.WHITE
        PadFilled = make_color_for_liveobj
        PadSelected = Colors.WHITE
        PadMuted = Colors.LIGHT_GREY
        PadMutedSelected = Colors.WHITE
        PadSoloed = Colors.BLUE
        PadSoloedSelected = Colors.WHITE
        Scroll = Colors.DARK_GREY

    class SlicedSimpler:
        PadAction = Colors.WHITE
        NoSlice = make_dimmed_color_for_liveobj
        SliceNotSelected = make_color_for_liveobj
        SliceSelected = Colors.WHITE
        NextSlice = make_pulsing_color_for_liveobj
        Scroll = Colors.DARK_GREY

    class NoteEditor:
        NoClip = Colors.DARK_GREY
        StepFilled = Colors.WHITE
        StepMuted = make_dimmed_color_for_liveobj
        StepEmpty = make_dimmed_color_for_liveobj
        StepDisabled = Colors.OFF
        StepAutomated = Colors.RED
        StepTied = make_color_for_liveobj
        StepPartiallyTied = partial(make_dimmed_color_for_liveobj, shade_level=1)
        Playhead = Colors.GREEN

    class LoopSelector:
        InsideLoopSelected = lambda _: make_pulsing_color(Colors.WHITE, Colors.DARK_GREY)
        InsideLoopSelectedPlaying = Colors.WHITE
        InsideLoop = make_pulsing_color_for_liveobj
        InsideLoopPlaying = make_color_for_liveobj
        OutsideLoopSelected = Colors.WHITE
        OutsideLoop = Colors.DARK_GREY
        Playhead = lambda _: make_pulsing_color(Colors.GREEN, Colors.DARK_GREY)
        PlayheadRecord = lambda _: make_pulsing_color(Colors.RED, Colors.DARK_GREY)
        Navigation = Colors.DARK_GREY

    class NoteSettings:
        CursorButton = Colors.DARK_GREY
        CursorButtonPressed = Colors.WHITE

    class Clipboard:
        Empty = Colors.DARK_GREY
        Filled = Colors.WHITE_PULSE_HALF
        CopyPressed = Colors.WHITE

    class ModifierBackground:
        MuteButton = Colors.DARK_GREY
        DeleteButton = Colors.DARK_GREY

    class MenuModes:

        class SettingsMenu:
            On = Colors.WHITE_WITH_ICON_PULSE_HALF
            Off = Colors.DARK_GREY

        class WorkflowMenu:
            On = Colors.WHITE_WITH_ICON_PULSE_HALF
            Off = Colors.DARK_GREY

        class ScaleMenu:
            On = Colors.WHITE_WITH_ICON_PULSE_HALF
            Off = Colors.DARK_GREY

        class TempoMenu:
            On = Colors.WHITE_WITH_ICON_PULSE_HALF
            Off = Colors.DARK_GREY

        class GrooveMenu:
            On = Colors.WHITE_WITH_ICON_PULSE_HALF
            Off = Colors.DARK_GREY

        class LoopMenu:
            On = Colors.WHITE_PULSE_HALF
            Off = Colors.DARK_GREY

    class BackgroundModes:

        class Shift:
            Off = Colors.DARK_GREY

    class MainModes:

        class Note:
            On = Colors.DARK_GREY

        class Session:
            On = Colors.WHITE