# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\caching_control_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import depends
from ableton.v2.control_surface import ControlElement
from .sysex import SET_PROPERTY_MSG_HEADER

class CachingControlElement(ControlElement):

    @depends(message_cache=None)
    def __init__(self, message_cache=None, *a, **k):
        super().__init__(*a, **k)
        self._message_cache = message_cache

    def send_midi(self, message, **_):
        self._message_cache(message[len(SET_PROPERTY_MSG_HEADER):-1])

    def reset(self):
        return