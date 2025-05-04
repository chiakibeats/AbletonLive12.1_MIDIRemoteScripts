# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\SceneComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .ClipSlotComponent import ClipSlotComponent, find_nearest_color
from .CompoundComponent import CompoundComponent
from .SubjectSlot import subject_slot
from .Util import in_range, nop

class SceneComponent(CompoundComponent):
    pass
    clip_slot_component_type = ClipSlotComponent

    def __init__(self, num_slots=0, tracks_to_use_callback=nop, *a, **k):
        super(SceneComponent, self).__init__(*a, **k)
        self._scene = None
        self._clip_slots = []
        self._tracks_to_use_callback = tracks_to_use_callback
        self._color_palette = None
        self._color_table = None
        for _ in range(num_slots):
            new_slot = self._create_clip_slot()
            self._clip_slots.append(new_slot)
            self.register_components(new_slot)
        self._launch_button = None
        self._triggered_value = 127
        self._scene_value = None
        self._no_scene_value = None
        self._track_offset = 0
        self._select_button = None
        self._delete_button = None

    def on_track_list_changed(self):
        self.update()

    def set_scene(self, scene):
        if scene!= self._scene or type(self._scene)!= type(scene):
            self._scene = scene
            self._on_is_triggered_changed.subject = scene
            self._on_scene_color_changed.subject = scene
            self.update()
            return

    def set_launch_button(self, button):
        if button!= self._launch_button:
            self._launch_button = button
            self._launch_value.subject = button
            self.update()

    def set_select_button(self, button):
        self._select_button = button

    def set_delete_button(self, button):
        self._delete_button = button

    def set_track_offset(self, offset):
        if offset!= self._track_offset:
            self._track_offset = offset
            self.update()

    def set_triggered_value(self, value):
        self._triggered_value = value

    def set_scene_value(self, value):
        self._scene_value = value

    def set_no_scene_value(self, value):
        self._no_scene_value = value

    def set_color_palette(self, palette):
        self._scene_value = None
        self._color_palette = palette

    def set_color_table(self, table):
        self._scene_value = None
        self._color_table = table

    def clip_slot(self, index):
        return self._clip_slots[index]

    def update(self):
        super(SceneComponent, self).update()
        if self._allow_updates:
            if self._scene!= None and self.is_enabled():
                clip_index = self._track_offset
                tracks = self.song().tracks
                clip_slots = self._scene.clip_slots
                if self._track_offset > 0:
                    real_offset = 0
                    visible_tracks = 0
                    while visible_tracks < self._track_offset and len(tracks) > real_offset:
                        while True:  # inserted
                            if tracks[real_offset].is_visible:
                                visible_tracks += 1
                            real_offset += 1
                                    break
                                else:  # inserted
                                    continue
                            else:  # inserted
                                break
                    clip_index = real_offset
                for slot in self._clip_slots:
                    while len(tracks) > clip_index and (not tracks[clip_index].is_visible):
                        clip_index += 1
                                break
                            else:  # inserted
                                continue
                    if len(clip_slots) > clip_index:
                        slot.set_clip_slot(clip_slots[clip_index])
                    else:  # inserted
                        slot.set_clip_slot(None)
                    clip_index += 1
                    continue
                pass
            else:  # inserted
                for slot in self._clip_slots:
                    slot.set_clip_slot(None)
            self._update_launch_button()
        else:  # inserted
            self._update_requests += 1

    @subject_slot('value')
    def _launch_value(self, value):
        if self.is_enabled():
            if self._select_button and self._select_button.is_pressed() and value:
                self._do_select_scene(self._scene)
            else:  # inserted
                if self._scene!= None:
                    if self._delete_button and self._delete_button.is_pressed() and value:
                        self._do_delete_scene(self._scene)
                    else:  # inserted
                        self._do_launch_scene(value)

    def _do_select_scene(self, scene_for_overrides):
        if self._scene!= None:
            view = self.song().view
            if view.selected_scene!= self._scene:
                view.selected_scene = self._scene

    def _do_delete_scene(self, scene_for_overrides):
        try:
            if self._scene:
                song = self.song()
                song.delete_scene(list(song.scenes).index(self._scene))
        except RuntimeError:
            return None

    def _do_launch_scene(self, value):
        launched = False
        if self._launch_button.is_momentary():
            self._scene.set_fire_button_state(value!= 0)
            launched = value!= 0
        else:  # inserted
            if value!= 0:
                self._scene.fire()
                launched = True
        if launched and self.song().select_on_launch:
                self.song().view.selected_scene = self._scene

    @subject_slot('is_triggered')
    def _on_is_triggered_changed(self):
        self._update_launch_button()

    @subject_slot('color')
    def _on_scene_color_changed(self):
        self._update_launch_button()

    def _color_value(self, color):
        value = None
        if self._color_palette:
            value = self._color_palette.get(color, None)
        if value is None and self._color_table:
            value = find_nearest_color(self._color_table, color)
        return value

    def _update_launch_button(self):
        if not self.is_enabled() or self._launch_button!= None:
                value_to_send = self._no_scene_value
                if self._scene:
                    if self._scene.is_triggered:
                        value_to_send = self._triggered_value
                    else:  # inserted
                        if self._scene_value is not None:
                            value_to_send = self._scene_value
                        else:  # inserted
                            value_to_send = self._color_value(self._scene.color)
                if value_to_send is None:
                    self._launch_button.turn_off()
                    return
                else:  # inserted
                    if in_range(value_to_send, 0, 128):
                        self._launch_button.send_value(value_to_send)
                        return
                    else:  # inserted
                        self._launch_button.set_light(value_to_send)
                        return
        else:  # inserted
            return

    def _create_clip_slot(self):
        return self.clip_slot_component_type()