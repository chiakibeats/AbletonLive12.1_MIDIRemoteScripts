# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\drum_group.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listens
from ableton.v3.control_surface import LiveObjSkinEntry
from ableton.v3.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from ableton.v3.live import liveobj_valid

class DrumGroupComponent(DrumGroupComponentBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.__on_target_track_color_changed.subject = self._target_track

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        return self._color_for_pad(pad) if pad else None
        else:  # inserted
            button.color = LiveObjSkinEntry('DrumGroup.Empty', self._target_track.target_track)

    @listens('target_track.color')
    def __on_target_track_color_changed(self):
        if not liveobj_valid(self._drum_group_device):
            self._update_led_feedback()
            return
        else:  # inserted
            return None