# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\session.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens, product
from ableton.v2.control_surface.components import SceneComponent as SceneComponentBase
from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    def __init__(self, *a, **k):
        super(SceneComponent, self).__init__(*a, **k)
        self._allow_updates = True
        self._update_requests = 0

    def set_allow_update(self, allow_updates):
        allow = bool(allow_updates)
        if self._allow_updates != allow:
            self._allow_updates = allow
            if self._allow_updates and self._update_requests > 0:
                self._update_requests = 0
                self.update()

    def update(self):
        if self._allow_updates:
            super(SceneComponent, self).update()
        else:
            self._update_requests += 1

class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent

    def __init__(self, *a, **k):
        super(SessionComponent, self).__init__(*a, **k)
        self._allow_updates = True
        self._update_requests = 0
        self._on_selected_scene_changed.subject = self.song.view
        self._on_selected_scene_changed()

    def set_allow_update(self, allow_updates):
        allow = bool(allow_updates)
        if self._allow_updates != allow:
            self._allow_updates = allow
            self._selected_scene.set_allow_update(allow_updates)
            for scene in self._scenes:
                scene.set_allow_update(allow_updates)
            if not self._allow_updates or self._update_requests > 0:
                self._update_requests = 0
                self.update()

    def update(self):
        if self._allow_updates:
            super(SessionComponent, self).update()
        else:
            self._update_requests += 1

    def set_clip_slot_leds(self, leds):
        if leds:
            for led, (x, y) in leds.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(led)
            return None
        else:
            for x, y in product(range(self._session_ring.num_tracks), range(self._session_ring.num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(None)

    @listens('selected_scene')
    def _on_selected_scene_changed(self):
        selected_scene_index = list(self.song.scenes).index(self.song.view.selected_scene)
        self._session_ring.set_offsets(self._session_ring.track_offset, selected_scene_index)