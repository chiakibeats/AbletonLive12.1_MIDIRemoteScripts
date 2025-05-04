# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\auto_arm.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends, listens
from ableton.v3.control_surface.components import AutoArmComponent as AutoArmComponentBase

class AutoArmComponent(AutoArmComponentBase):
    pass

    @depends(session_ring=None)
    def __init__(self, session_ring=None, *a, **k):
        super().__init__(*a, **k)
        self._last_track_offset = -1
        self.__on_offset_changed.subject = session_ring

    @listens('offset')
    def __on_offset_changed(self, track_offset, _):
        if track_offset != self._last_track_offset:
            self._set_auto_arm_state(False)
        self._last_track_offset = track_offset