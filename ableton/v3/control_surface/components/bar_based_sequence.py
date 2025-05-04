# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\bar_based_sequence.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import math
from typing import NamedTuple
from ...base import listenable_property, listens, memoize, round_to_multiple
from ...live import get_bar_length, liveobj_valid
from .loop_selector import LoopSelectorComponent as LoopSelectorComponentBase
from .note_editor import NoteEditorComponent as NoteEditorComponentBase
from .playhead import PlayheadComponent as PlayheadComponentBase
pass

def get_adjusted_step_count(clip, page_time, page_length, step_length, default_step_count=16):
    pass
    step_count = default_step_count
    if liveobj_valid(clip):
        bar_length = get_bar_length(clip=clip)
        remaining_length = bar_length
        if bar_length > page_length and page_time % bar_length != 0:
            remaining_length = math.ceil(page_time / bar_length) * bar_length - page_time
        step_count = int(remaining_length / step_length)
    return min(step_count, default_step_count)

@memoize
def calculate_page_points(page_length, bar_length):
    pass
    num_pages = math.ceil(bar_length / page_length)
    page_points = [i * page_length for i in range(num_pages)]
    next_page_jumps = [min(page_length, bar_length - point) for point in page_points]
    points = {}
    for i, (point, next_page, prev_page) in enumerate(zip(page_points, next_page_jumps, reversed(next_page_jumps))):
        points[point] = PagePoint(i + 1, -prev_page, next_page)
    return points

def normalize_page_time(page_time, bar_length):
    pass
    normalized = page_time - round_to_multiple(page_time, bar_length)
    return normalized + bar_length if normalized < 0.0 else normalized

def get_relative_page_time(current_page_time, page_length, bar_length, delta):
    pass
    page_point = calculate_page_points(page_length, bar_length)[normalize_page_time(current_page_time, bar_length)]
    current_page_time += page_point.prev_page if delta < 0 else page_point.next_page
    return current_page_time

class PagePoint(NamedTuple):
    pass
    page_num: int
    prev_page: float
    next_page: float

    @property
    def distances(self):
        pass
        return (self.prev_page, self.next_page)

class LoopSelectorComponent(LoopSelectorComponentBase):
    pass

    def _increment_page_time(self, delta):
        self._paginator.page_time = get_relative_page_time(self._paginator.page_time, self._paginator.page_length, self.bar_length, delta)
        self._notify_page_time()

    def _on_page_time_changed_via_matrix(self):
        self._notify_page_time()

    def _notify_page_time(self):
        bar_length = self.bar_length
        page_time = self._paginator.page_time
        if page_time >= 0:
            bar_num = int(page_time / bar_length) + 1
        else:
            bar_num = -abs(math.ceil(abs(page_time) / bar_length))
        page_points = calculate_page_points(self._paginator.page_length, bar_length)
        if len(page_points) > 1:
            self.notify(self.notifications.Sequence.current_bar_with_page, bar_num, page_points[normalize_page_time(page_time, bar_length)].page_num)
        else:
            self.notify(self.notifications.Sequence.current_bar, bar_num)

class NoteEditorComponent(NoteEditorComponentBase):
    pass
    adjusted_step_count = listenable_property.managed(0)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.register_slot(self._sequencer_clip, self._adjust_step_count, 'length')

    def set_clip(self, clip):
        super().set_clip(clip)
        self._adjust_step_count()

    def set_matrix(self, matrix):
        super().set_matrix(matrix)
        self._adjust_step_count()

    def notify_page_length(self):
        super().notify_page_length()
        self._adjust_step_count()

    def page_time_changed(self):
        self._adjust_step_count()

    def _adjust_step_count(self):
        step_count = get_adjusted_step_count(self._clip, self.page_time, self.page_length, self.step_length * self._triplet_factor, self.step_count)
        if not self.matrix.width or step_count != self.adjusted_step_count:
            for index, button in enumerate(self.matrix):
                button.enabled = index < step_count
            self.adjusted_step_count = step_count
            self.__on_clip_notes_changed()

class PlayheadComponent(PlayheadComponentBase):
    pass

    def __init__(self, *a, **k):
        self._note_editor = None
        super().__init__(*a, **k)
        self._unused_triplet_notes = set(self._notes) - set(self._triplet_notes)

    def set_note_editor(self, note_editor):
        self._note_editor = note_editor
        self.__on_step_count_changed.subject = note_editor
        self._update_playhead_notes()

    def _update_playhead_notes(self):
        if self._note_editor:
            step_count = self._note_editor.adjusted_step_count
            notes = self._notes[:step_count]
            if self._grid_resolution.is_triplet:
                notes = set(notes) - self._unused_triplet_notes
            self._playhead.notes = list(notes)

    @listens('adjusted_step_count')
    def __on_step_count_changed(self, *_):
        self._update_playhead_notes()