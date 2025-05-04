# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\clip_slot.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import const, depends
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase

class FixedLengthClipSlotComponent(ClipSlotComponentBase):

    @depends(fixed_length_recording=const(None))
    def __init__(self, fixed_length_recording, *a, **k):
        super(FixedLengthClipSlotComponent, self).__init__(*a, **k)
        self._fixed_length_recording = fixed_length_recording

    def _do_launch_clip(self, fire_state):
        slot = self._clip_slot
        if self._fixed_length_recording.should_start_recording_in_slot(slot):
            self._fixed_length_recording.start_recording_in_slot(slot)
            return
        else:
            super(FixedLengthClipSlotComponent, self)._do_launch_clip(fire_state)