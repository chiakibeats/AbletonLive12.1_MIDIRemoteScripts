# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.base import depends
from ableton.v3.control_surface.components import RecordingMethod
from ableton.v3.live import is_track_armed, prepare_new_clip_slot

class FixedLengthRecordingMethod(RecordingMethod):
    pass

    @depends(settings_component=None)
    def __init__(self, settings_component=None, *a, **k):
        super().__init__(*a, **k)
        self._fixed_length = settings_component.fixed_length

    def trigger_recording(self):
        if not self.stop_recording():
            for track in self.song.tracks:
                if is_track_armed(track):
                    slot = prepare_new_clip_slot(track)
                    if self.can_record_into_clip_slot(slot):
                        if self._fixed_length.enabled:
                            slot.fire(record_length=self._fixed_length.record_length)
                            continue
                        else:
                            slot.fire()
                continue