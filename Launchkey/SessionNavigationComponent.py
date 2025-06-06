# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey\SessionNavigationComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework import Task
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ScrollComponent import ScrollComponent
from _Framework.ViewControlComponent import BasicSceneScroller, TrackScroller

def is_recording_clip(tracks, check_arrangement):
    found_recording_clip = False
    for track in tracks:
        if track.can_be_armed and track.arm:
            if check_arrangement:
                found_recording_clip = True
                break
            else:
                playing_slot_index = track.playing_slot_index
                if playing_slot_index in range(len(track.clip_slots)):
                    slot = track.clip_slots[playing_slot_index]
                    if slot.has_clip and slot.clip.is_recording:
                        found_recording_clip = True
                        break
        continue
    return found_recording_clip

class ArmingTrackScrollComponent(ScrollComponent):
    pass

    def __init__(self, *a, **k):
        super(ArmingTrackScrollComponent, self).__init__(*a, **k)
        self._arming_task = self._tasks.add(Task.sequence(Task.delay(1), self._arm_task))
        self._arming_task.kill()

    def scroll_up(self):
        super(ArmingTrackScrollComponent, self).scroll_up()
        self._start_arming_task()

    def scroll_down(self):
        super(ArmingTrackScrollComponent, self).scroll_down()
        self._start_arming_task()

    def _start_arming_task(self):
        if self._arming_task.is_killed:
            self._arming_task.restart()
            return
        else:
            return None

    @property
    def is_scrolling(self):
        return not self._scroll_task_up.is_killed or not self._scroll_task_down.is_killed

    def _track_to_arm(self):
        track = self.song().view.selected_track
        can_arm_track = track != None and track.has_midi_input and track.can_be_armed and (not track.arm)
        return track if can_arm_track else None

    def _try_arm(self):
        track_to_arm = self._track_to_arm()
        if track_to_arm != None:
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            if not is_recording_clip(tracks, check_arrangement):
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed and track != track_to_arm:
                            track.arm = False
                        continue
                track_to_arm.arm = True
                track_to_arm.view.select_instrument()
                return
        else:
            return

    def _arm_task(self, delta):
        result_state = Task.KILLED
        if self.is_enabled():
            if self.is_scrolling:
                result_state = Task.RUNNING
            else:
                self._try_arm()
        return result_state

class SessionNavigationComponent(CompoundComponent):
    pass

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        self._scroll_tracks, self._scroll_scenes = self.register_components(ArmingTrackScrollComponent(TrackScroller()), ScrollComponent(BasicSceneScroller()))
        song = self.song()
        view = song.view
        self.register_slot(song, self._scroll_tracks.update, 'visible_tracks')
        self.register_slot(song, self._scroll_tracks.update, 'return_tracks')
        self.register_slot(song, self._scroll_scenes.update, 'scenes')
        self.register_slot(view, self._scroll_tracks.update, 'selected_track')
        self.register_slot(view, self._scroll_scenes.update, 'selected_scene')

    def set_next_track_button(self, button):
        self._scroll_tracks.set_scroll_down_button(button)

    def set_prev_track_button(self, button):
        self._scroll_tracks.set_scroll_up_button(button)

    def set_next_scene_button(self, button):
        self._scroll_scenes.set_scroll_down_button(button)

    def set_prev_scene_button(self, button):
        self._scroll_scenes.set_scroll_up_button(button)