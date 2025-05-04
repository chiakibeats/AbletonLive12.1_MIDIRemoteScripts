# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.control_surface.elements import Color
LIVE_COLOR_TABLE_INDEX_OFFSET = 8
ON_COLOR = Color(127)
OFF_COLOR = Color(0)

class ColorsBase(object):

    class DefaultButton(object):
        On = ON_COLOR
        Off = OFF_COLOR
        Disabled = OFF_COLOR

    class Mixer(object):
        SoloOn = Color(2)
        SoloOff = OFF_COLOR
        MuteOn = Color(1)
        MuteOff = OFF_COLOR
        ArmOff = OFF_COLOR
        CrossfadeAssignA = Color(1)
        CrossfadeAssignB = Color(3)

    class Session(object):
        RecordButton = ON_COLOR
        ClipTriggeredPlay = Color(3)
        ClipTriggeredRecord = Color(6)
        ClipStarted = Color(4)
        ClipRecording = Color(7)
        ClipStopped = Color(2)
        ClipSelected = Color(127)
        Scene = Color(0)
        SceneTriggered = Color(1)
        NoScene = OFF_COLOR
        StopClipTriggered = ON_COLOR
        StopClip = Color(4)
        StopClipDisabled = OFF_COLOR
        ClipEmpty = OFF_COLOR
        ClipEmptyWithStopButton = Color(1)
        SceneOff = OFF_COLOR
        SceneOn = Color(2)
        SceneDefault = Color(21)

    class Action(object):
        Available = OFF_COLOR
        On = Color(1)
        Off = Color(0)
        QuantizeOn = Color(5)
        QuantizeOff = Color(0)

    class Transport(object):
        PlayOn = ON_COLOR
        PlayOff = OFF_COLOR
        StopOn = ON_COLOR
        StopOff = OFF_COLOR
        MetronomeOn = Color(6)
        MetronomeOff = Color(0)
        TapTempo = Color(1)

    class Recording(object):
        On = ON_COLOR
        Off = OFF_COLOR
        Transition = ON_COLOR

    class Automation(object):
        On = Color(2)
        Off = OFF_COLOR

    class Navigation(object):
        Enabled = Color(1)

    class Background(object):
        On = Color(1)

    class Mode(object):
        On = Color(1)
        Off = OFF_COLOR

class ForceColors(ColorsBase):

    class Mixer(ColorsBase.Mixer):
        ArmOn = Color(3)

class MPCColors(ColorsBase):

    class Mixer(ColorsBase.Mixer):
        ArmOn = Color(1)