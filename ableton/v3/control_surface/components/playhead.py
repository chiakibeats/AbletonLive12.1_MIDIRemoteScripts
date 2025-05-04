# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\playhead.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import depends, is_iterable, listens
from ...live import liveobj_valid
from .. import Component
from . import DEFAULT_STEP_TRANSLATION_CHANNEL

class PlayheadComponent(Component):
    pass

    @depends(playhead=None, sequencer_clip=None, grid_resolution=None)
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='Playhead', playhead=None, sequencer_clip=None, grid_resolution=None, paginator=None, notes=None, triplet_notes=None, channels=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._notes = notes or tuple(range(8))
        self._triplet_notes = triplet_notes or tuple(range(6))
        self._channels = channels or [DEFAULT_STEP_TRANSLATION_CHANNEL]
        self._playhead = playhead
        self._sequencer_clip = sequencer_clip
        self._grid_resolution = grid_resolution
        self._paginator = paginator
        self.register_slot(self._grid_resolution, self.update, 'index')
        self.register_slot(self._paginator, self.update, 'page')
        self.register_slot(self.song, self.update, 'is_playing')
        self.__on_sequencer_clip_playing_status_changed.subject = sequencer_clip
        self.update()

    def update(self):
        super().update()
        playhead_clip = None
        sequencer_clip = self._sequencer_clip.clip
        if self.is_enabled() and liveobj_valid(sequencer_clip) and self.song.is_playing and (sequencer_clip.is_arrangement_clip or sequencer_clip.is_playing):
            playhead_clip = sequencer_clip
        self._playhead.clip = playhead_clip
        self._playhead.set_feedback_channels(self._channels)
        if playhead_clip:
            self._update_playhead_notes()
            self._playhead.start_time = self._paginator.page_time
            self._playhead.step_length = self._grid_resolution.step_length
            return

    def _update_playhead_notes(self):
        self._playhead.notes = list(self._triplet_notes if self._grid_resolution.is_triplet else self._notes)

    @listens('clip.playing_status')
    def __on_sequencer_clip_playing_status_changed(self):
        self.update()