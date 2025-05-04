# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\actions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import liveobj_valid
from pushbase.actions import CaptureAndInsertSceneComponent as CaptureAndInsertSceneComponentBase
from .clip_decoration import ClipDecoratedPropertiesCopier

class CaptureAndInsertSceneComponent(CaptureAndInsertSceneComponentBase):

    def __init__(self, name=None, decorator_factory=None, *a, **k):
        super(CaptureAndInsertSceneComponent, self).__init__(name, *a, **k)
        self._decorator_factory = decorator_factory

    def _copy_decorated_properties(self, source_clip, destination_clip):
        ClipDecoratedPropertiesCopier(source_clip=source_clip, destination_clip=destination_clip, decorator_factory=self._decorator_factory).post_duplication_action()

    def post_trigger_action(self):
        view = self.song.view
        if liveobj_valid(view.detail_clip) and view.detail_clip.is_arrangement_clip:
            previous_detail_clip = view.detail_clip
            super(CaptureAndInsertSceneComponent, self).post_trigger_action()
            self._copy_decorated_properties(previous_detail_clip, view.detail_clip)
            return
        else:

            def get_playing_clip(track):
                slot_ix = track.playing_slot_index
                return track.clip_slots[slot_ix].clip if slot_ix > -1 else None
            played_clips = [get_playing_clip(track) for track in self.song.tracks]
            super(CaptureAndInsertSceneComponent, self).post_trigger_action()
            new_slots = view.selected_scene.clip_slots
            for ix, clip in enumerate(played_clips):
                if liveobj_valid(clip):
                    self._copy_decorated_properties(clip, new_slots[ix].clip)
                pass
                continue
            return None