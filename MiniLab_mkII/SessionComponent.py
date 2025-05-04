# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_mkII\SessionComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import product
from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotComponentBase
from _Framework.SceneComponent import SceneComponent as SceneComponentBase
from _Arturia.SessionComponent import SessionComponent as SessionComponentBase
EMPTY_VALUE = 0
TRIGGERED_TO_RECORD_VALUE = 1
RECORDING_VALUE = 1
TRIGGERED_TO_PLAY_VALUE = 4
STARTED_VALUE = 4
STOPPED_VALUE = 5

class ClipSlotComponent(ClipSlotComponentBase):
    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._led = None

    def set_led(self, led):
        self._led = led

    def update(self):
        super(ClipSlotComponent, self).update()
        self._update_led()

    def _update_led(self):
        if not self.is_enabled() or self._led!= None:
                value_to_send = self._feedback_value()
                if value_to_send in (None, (-1)):
                    value_to_send = EMPTY_VALUE
                self._led.send_value((value_to_send,))
                return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _feedback_value(self):
        if self._clip_slot!= None and self.has_clip():
            clip = self._clip_slot.clip
            if clip.is_triggered:
                return TRIGGERED_TO_RECORD_VALUE if clip.will_record_on_start else TRIGGERED_TO_PLAY_VALUE
            else:  # inserted
                if clip.is_playing:
                    return RECORDING_VALUE if clip.is_recording else STARTED_VALUE
                else:  # inserted
                    return STOPPED_VALUE
        else:  # inserted
            return None

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent

    def set_clip_slot_leds(self, leds):
        if leds:
            for led, (x, y) in leds.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(led)
            return None
        else:  # inserted
            for x, y in product(range(self._num_tracks), range(self._num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(None)