# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.base import listens, nop
from ableton.v3.control_surface.components import SelectedSlotRecordingMethod, ViewBasedRecordingComponent
from ableton.v3.control_surface.controls import ButtonControl

class ArrangementRecordButtonControl(ButtonControl):
    pass

    class State(ButtonControl.State):
        connect_property = nop

class RecordingComponent(ViewBasedRecordingComponent):
    pass
    session_record_button = ButtonControl()
    arrangement_record_button = ArrangementRecordButtonControl(color='Recording.ArrangementRecordOff', on_color='Recording.ArrangementRecordOn')

    def __init__(self, *a, **k):
        super().__init__(*a, recording_method_type=SelectedSlotRecordingMethod, **k)
        self.__on_record_mode_changed.subject = self.song

    @session_record_button.released_immediately
    def session_record_button(self, _):
        self._recording_method.trigger_recording()

    @arrangement_record_button.released_immediately
    def arrangement_record_button(self, _):
        self.song.record_mode = not self.song.record_mode

    @listens('record_mode')
    def __on_record_mode_changed(self):
        self.arrangement_record_button.is_on = self.song.record_mode