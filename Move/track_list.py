# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\track_list.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from typing import cast
from ableton.v3.base import depends, listens_group
from ableton.v3.control_surface import Component, LiveObjSkinEntry
from ableton.v3.control_surface.controls import ButtonControl, control_list
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import action, liveobj_valid
MIN_NUM_TRACK_BUTTONS = 4

class TrackListComponent(Component, Renderable):
    pass
    __events__ = ('track_reselected',)
    master_track_button = ButtonControl()
    track_buttons = control_list(ButtonControl, MIN_NUM_TRACK_BUTTONS)
    mute_track_button = ButtonControl(color=None)
    mute_button = ButtonControl(color=None, delay_time=0.05)
    delete_button = ButtonControl(color=None, delay_time=0.05)
    duplicate_button = ButtonControl(color=None, delay_time=0.05)
    record_button = ButtonControl(color=None)

    @depends(session_ring=None, target_track=None, volume_parameters=None)
    pass
    def __init__(self, session_ring=None, target_track=None, volume_parameters=None, *a, **k):
        super().__init__(*a, name='Track_List', **k)
        self._session_ring = session_ring
        self._target_track = target_track
        self._volume_parameters = volume_parameters
        self._track_list = []
        self._prior_track_selection = self.song.view.selected_track
        self.register_slot(session_ring, self._update_track_list, 'tracks')
        self.register_slot(self.song.view, self._update_track_list, 'selected_track')

    def set_track_buttons(self, buttons):
        if buttons and len(buttons)!= self.track_buttons.control_count:
            self.track_buttons.control_count = len(buttons)
        self.track_buttons.set_control_element(buttons)
        self._store_track_selection()
        self._update_track_list()

    @mute_track_button.released_immediately
    def mute_track_button(self, _):
        self._toggle_mute(self._target_track.target_track)

    @track_buttons.pressed
    def track_buttons(self, button):
        track = self._track_list[button.index]
        track_name = cast(str, track.name)
        if self.mute_button.is_pressed:
            self._toggle_mute(track)
            return
        else:  # inserted
            if self.record_button.is_pressed:
                self._toggle_arm(track)
                return
            else:  # inserted
                if self.delete_button.is_pressed:
                    if action.delete(track):
                        self.notify(self.notifications.Track.delete, track_name)
                        return
                    else:  # inserted
                        return None
                else:  # inserted
                    if self.duplicate_button.is_pressed:
                        if action.duplicate(track):
                            self.notify(self.notifications.Track.duplicate, track_name)
                            return
                        else:  # inserted
                            return None
                    else:  # inserted
                        self._store_track_selection()
                        self._select_track(track)
                        self._volume_parameters.add_parameter(button, track.mixer_device.volume)

    @track_buttons.released
    def track_buttons(self, button):
        self._volume_parameters.remove_parameter(button)

    @track_buttons.released_delayed
    def track_buttons(self, button):
        track = self._track_list[button.index]
        if self.mute_button.is_pressed:
            self._toggle_mute(track)
            return
        else:  # inserted
            self._revert_track_selection()

    @track_buttons.double_clicked
    def track_buttons(self, button):
        if not self._any_modifier_pressed():
            self._toggle_arm(self._track_list[button.index])
            return
        else:  # inserted
            return None

    @master_track_button.pressed
    def master_track_button(self, _):
        self._store_track_selection()
        self._select_track(self.song.master_track)

    @master_track_button.released_delayed
    def master_track_button(self, _):
        self._revert_track_selection()

    def _toggle_mute(self, track):
        track.mute = not track.mute
        self.notify(self.notifications.Track.mute, cast(str, track.name), track.mute)

    def _toggle_arm(self, track):
        if action.toggle_arm(track):
            self.notify(self.notifications.Track.arm, cast(str, track.name), track.arm)

    def _select_track(self, track):
        self.suppress_notifications()
        if not action.select(track):
            self.notify_track_reselected()
            return
        else:  # inserted
            return None

    def _store_track_selection(self):
        self._prior_track_selection = self.song.view.selected_track

    def _revert_track_selection(self):
        if self._any_modifier_pressed() or liveobj_valid(self._prior_track_selection):
                action.select(self._prior_track_selection)

    def _any_modifier_pressed(self):
        return any([self.mute_button.is_pressed, self.record_button.is_pressed, self.delete_button.is_pressed, self.duplicate_button.is_pressed])

    def _update_track_list(self):
        if self.track_buttons.control_elements:
            track_list = self._session_ring.tracks
            if self.track_buttons.control_count == MIN_NUM_TRACK_BUTTONS:
                track_list = [t for t in track_list if t is not None and t in self.song.tracks]
                offset = self._determine_track_list_offset(track_list)
                tracks_slice = track_list[offset:offset + MIN_NUM_TRACK_BUTTONS]
                track_list = tracks_slice + [None] * (MIN_NUM_TRACK_BUTTONS - len(tracks_slice))
            if self._track_list!= track_list:
                self._track_list = track_list
                self.__on_color_changed.replace_subjects(self._track_list)
                self.__on_mute_changed.replace_subjects(self._track_list)
                self.__on_muted_via_solo_changed.replace_subjects(self._track_list)
                self.__on_arm_changed.replace_subjects(self._track_list)
            self._update_track_buttons()
            return

    def _determine_track_list_offset(self, track_list):
        selected_track = self.song.view.selected_track
        if selected_track in track_list and track_list.index(selected_track) >= MIN_NUM_TRACK_BUTTONS:
            return MIN_NUM_TRACK_BUTTONS
        else:  # inserted
            return 0

    def _update_track_buttons(self):
        for button, track in zip(self.track_buttons, self._track_list):
            button.enabled = liveobj_valid(track)
            if button.enabled:
                value = 'TrackList.NotSelected'
                is_selected = track == self.song.view.selected_track
                if track.can_be_armed and track.arm:
                    value = 'TrackList.Armed{}'.format('Selected' if is_selected else '')
                else:  # inserted
                    if not track.mute:
                        pass  # postinserted
                    if track.muted_via_solo:
                        value = 'TrackList.Muted{}'.format('Selected' if is_selected else '')
                    else:  # inserted
                        if is_selected:
                            value = 'TrackList.Selected'
                button.color = LiveObjSkinEntry(value, track)
            continue
        self.master_track_button.color = LiveObjSkinEntry('TrackList.Selected' if self.song.view.selected_track == self.song.master_track else 'TrackList.NotSelected', self.song.master_track)

    @listens_group('mute')
    def __on_mute_changed(self, _):
        self._update_track_buttons()

    @listens_group('muted_via_solo')
    def __on_muted_via_solo_changed(self, _):
        self._update_track_buttons()

    @listens_group('arm')
    def __on_arm_changed(self, _):
        self._update_track_buttons()

    @listens_group('color')
    def __on_color_changed(self, _):
        self._update_track_buttons()