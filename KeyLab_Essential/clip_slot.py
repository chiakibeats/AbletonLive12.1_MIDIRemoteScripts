# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\clip_slot.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase

class ClipSlotComponent(ClipSlotComponentBase):

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._led = None

    def set_led(self, led):
        self._led = led

    def update(self):
        super(ClipSlotComponent, self).update()
        self._update_led()

    def _update_launch_button_color(self):
        self._update_led()

    def _update_led(self):
        if not self.is_enabled() or self._led != None:
            value_to_send = self._empty_slot_color
            if liveobj_valid(self._clip_slot):
                track = self._clip_slot.canonical_parent
                slot_or_clip = self._clip_slot.clip if self.has_clip() else self._clip_slot
                value_to_send = self._led_feedback_value(track, slot_or_clip)
            self._led.set_light(value_to_send)
            return

    def _led_feedback_value(self, track, slot_or_clip):
        if self.has_clip():
            if slot_or_clip.is_triggered:
                return self._triggered_to_record_color if slot_or_clip.will_record_on_start else self._triggered_to_play_color
            elif slot_or_clip.is_playing:
                return self._recording_color if slot_or_clip.is_recording else self._started_value
            else:
                return self._stopped_value
        else:
            return self._empty_slot_color