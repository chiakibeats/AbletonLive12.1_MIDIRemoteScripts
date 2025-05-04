# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .colors import PULSE_CHANNEL, Mono, Rgb, make_animated_color, make_color_for_liveobj

class Skin:

    class Transport:
        PlayOff = Mono.DIM
        StopOff = Mono.DIM
        LoopOff = Mono.DIM
        MetronomeOff = Mono.DIM
        CanCaptureMidi = Mono.ON
        SetCuePressed = Mono.ON
        SetCue = Mono.DIM

    class Recording:
        ArrangementRecordOff = Mono.DIM
        SessionRecordTransition = Mono.BLINK
        SessionRecordOff = Mono.DIM

    class ViewControl:
        TrackPressed = Mono.ON
        Track = Mono.DIM

    class UndoRedo:
        UndoPressed = Mono.ON
        Undo = Mono.DIM
        RedoPressed = Mono.ON
        Redo = Mono.DIM

    class Device:
        NavigationPressed = Mono.ON
        Navigation = Mono.DIM

        class Bank:
            NavigationPressed = Mono.ON
            Navigation = Mono.DIM

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        MuteOn = Rgb.ORANGE
        MuteOff = Rgb.ORANGE_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        Selected = Rgb.WHITE
        NotSelected = make_color_for_liveobj
        IncrementSendIndexPressed = Mono.ON
        IncrementSendIndex = Mono.DIM

    class Session:
        SlotRecordButton = Rgb.RED_HALF
        ClipStopped = make_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        SequencerClip = lambda x: make_animated_color(make_color_for_liveobj(x).midi_value, PULSE_CHANNEL)
        SequencerSlot = Rgb.RED_PULSE
        Scene = make_color_for_liveobj
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.OFF
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF
        NavigationPressed = Mono.ON
        Navigation = Mono.DIM

    class DrumGroup:
        Empty = make_color_for_liveobj
        PadEmpty = Rgb.OFF
        PadFilled = make_color_for_liveobj
        PadSelected = Rgb.WHITE
        PadMuted = Rgb.ORANGE_HALF
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        ScrollPressed = Mono.ON
        Scroll = Mono.DIM

    class NoteEditor:
        StepFilled = make_color_for_liveobj

    class LoopSelector:
        NavigationPressed = Mono.ON
        Navigation = Mono.DIM
        DoublePressed = Mono.ON
        Double = Mono.DIM
        QuantizePressed = Mono.ON
        Quantize = Mono.DIM

    class Clipboard:
        Empty = None
        Filled = None
        CopyPressed = None

    class ModifierBackground:
        PadFunctionButtonPressed = Rgb.WHITE
        PadFunctionButton = Rgb.WHITE_HALF

    class LowerPadModes:

        class ClipLaunch:
            On = Rgb.WHITE_HALF

        class Stop:
            On = Rgb.RED

        class Mute:
            On = Rgb.ORANGE

        class Solo:
            On = Rgb.BLUE

    class SequencerModes:

        class Default:
            On = Rgb.WHITE_HALF

        class ClipSelect:
            On = Rgb.WHITE

    class MixerEncoderModes:

        class Level:
            On = Mono.OFF
            Off = Mono.DIM

        class Pan:
            On = Mono.OFF
            Off = Mono.DIM

    class FaderButtonModes:

        class Arm:
            On = Rgb.RED

        class Select:
            On = Rgb.WHITE