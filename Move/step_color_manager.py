# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\step_color_manager.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v3.base import EventObject, depends, listens, task
from ableton.v3.control_surface import ACTIVE_PARAMETER_TIMEOUT
from ableton.v3.live import liveobj_valid

class StepColorManager(EventObject):
    pass

    @depends(song=None, parent_task_group=None, update_method=None)
    def __init__(self, song=None, parent_task_group=None, update_method=None, *a, **k):
        super().__init__(*a, **k)
        self.song = song
        self.clip = None
        self._colors = {}
        self._update_method = update_method
        self._last_beat = None
        self.register_slot(self.song, self._update_method, 'is_playing')
        self._tasks = parent_task_group
        self._revert_colors_task = self._tasks.add(task.sequence(task.wait(ACTIVE_PARAMETER_TIMEOUT), task.run(partial(self.show_colors, {}))))
        self._revert_colors_task.kill()

    def set_clip(self, clip):
        pass
        self.clip = clip if liveobj_valid(clip) else None
        self.__on_song_time_changed.subject = None if self.clip else self.song
        if self.clip and self.song.is_playing:
            self._update_method()
        else:
            return

    def show_colors(self, colors_for_steps):
        pass
        self._revert_colors_task.kill()
        self._colors = colors_for_steps
        self._update_method()

    def revert_colors(self, immediate=False):
        pass
        if immediate:
            self.show_colors({})

    def get_color_for_step(self, index, visible_steps):
        pass
        if self.clip is None and self.song.is_playing and (index in visible_steps) and (index // 4 == self._last_beat):
            return 'NoteEditor.Playhead'
        elif self.clip:
            return self._colors.get(index, None)
        else:
            return None

    @listens('current_song_time')
    def __on_song_time_changed(self):
        beat = self.song.get_current_beats_song_time().beats - 1
        if beat != self._last_beat:
            self._last_beat = beat
            self._update_method()