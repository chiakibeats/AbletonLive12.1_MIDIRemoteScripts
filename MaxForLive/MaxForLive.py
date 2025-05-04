# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MaxForLive\MaxForLive.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import SimpleControlSurface
from ableton.v2.control_surface.input_control_element import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, InputControlElement
STATUS_TO_TYPE = {144: MIDI_NOTE_TYPE, 176: MIDI_CC_TYPE, 224: MIDI_PB_TYPE}

class MaxForLive(SimpleControlSurface):

    def __init__(self, *a, **k):
        super(MaxForLive, self).__init__(*a, **k)
        self._registered_control_names = []
        self._registered_messages = []

    def register_midi_control(self, name, status, number):
        pass