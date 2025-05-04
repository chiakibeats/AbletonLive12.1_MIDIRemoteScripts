# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\fixed_length_recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

NUM_LENGTHS = 8

def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)

class FixedLengthRecording(object):
    pass

    def __init__(self, song=None, fixed_length_setting=None, *a, **k):
        super(FixedLengthRecording, self).__init__(*a, **k)
        self._song = song
        self._fixed_length_setting = fixed_length_setting

    def should_start_recording_in_slot(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and (not clip_slot.is_recording) and (not clip_slot.has_clip) and (self._fixed_length_setting.enabled or None)

    def start_recording_in_slot(self, clip_slot):
        if self.should_start_recording_in_slot(clip_slot):
            clip_slot.fire(record_length=self._fixed_length_setting.get_selected_length(self._song))
        else:
            clip_slot.fire()