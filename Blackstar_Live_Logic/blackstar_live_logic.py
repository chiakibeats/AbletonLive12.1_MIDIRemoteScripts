# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\blackstar_live_logic.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens
from ableton.v2.control_surface import Layer, SimpleControlSurface
from ableton.v2.control_surface.midi import is_sysex
from .elements import Elements
from .looper import LooperComponent

class Blackstar_Live_Logic(SimpleControlSurface):

    def __init__(self, *a, **k):
        pass

    def disconnect(self):
        super(Blackstar_Live_Logic, self).disconnect()
        self._elements.live_integration_mode_switch.send_value(0)

    def port_settings_changed(self):
        self._elements.live_integration_mode_switch.send_value(1)
        self.schedule_message(1, self._looper.set_enabled, True)
        self.schedule_message(2, self.refresh_state)

    def process_midi_bytes(self, midi_bytes, midi_processor):
        pass
        if is_sysex(midi_bytes):
            return
        else:
            return super(Blackstar_Live_Logic, self).process_midi_bytes(midi_bytes, midi_processor)