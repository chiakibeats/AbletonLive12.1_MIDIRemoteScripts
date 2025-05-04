# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\mixer.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface.components import ChannelStripComponent
from ableton.v3.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v3.control_surface.components import SendIndexManager

class TargetStripComponent(ChannelStripComponent):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._send_controls = []
        self._send_index_manager = self.register_disconnectable(SendIndexManager(cycle_size=6))
        self.register_slot(self._send_index_manager, self._update_send_controls, 'send_index')

    def set_send_controls(self, controls):
        self._send_controls = controls or []
        self._update_send_controls()

    def cycle_send_index(self):
        self._send_index_manager.cycle_send_index(range_name='CH Strip')

    def _update_send_controls(self):
        if self._send_index_manager.send_index is None:
            self.send_controls.set_control_element(self._send_controls)
            return
        else:
            self.send_controls.set_control_element([None] * self._send_index_manager.send_index + list(self._send_controls))
            self.update()

class MixerComponent(MixerComponentBase):
    pass

    def __getattr__(self, name):
        if name == 'set_target_track_send_controls':
            return self._target_strip.set_send_controls
        else:
            return super().__getattr__(name)

    def _create_channel_strip(self, is_master=False, is_target=False):
        if is_target:
            return TargetStripComponent(parent=self)
        else:
            return super()._create_channel_strip(is_master=is_master)