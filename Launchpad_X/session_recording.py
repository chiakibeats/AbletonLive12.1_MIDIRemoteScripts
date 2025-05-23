# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\session_recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v2.base import task
from ableton.v2.control_surface.control import ButtonControl
BLINK_PERIOD = 0.1

class SessionRecordingMixin(object):
    record_button = ButtonControl(delay_time=0.5)

    def __init__(self, *a, **k):
        super(SessionRecordingMixin, self).__init__(*a, **k)
        blink_on = partial(self._set_record_button_color, 'Recording.CaptureTriggered')
        blink_off = partial(self._set_record_button_color, 'DefaultButton.Off')
        self._blink_task = self._tasks.add(task.sequence(task.run(blink_on), task.wait(BLINK_PERIOD), task.run(blink_off), task.wait(BLINK_PERIOD), task.run(blink_on), task.wait(BLINK_PERIOD), task.run(blink_off)))
        self._blink_task.kill()

    @record_button.released_immediately
    def record_button(self, _):
        self._trigger_recording()

    @record_button.pressed_delayed
    def record_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
                self._blink_task.restart()
        except RuntimeError:
            return None

    @record_button.released
    def record_button(self, _):
        self._update_record_button()

    def _update_record_button(self):
        if not self.record_button.is_pressed:
            self._blink_task.kill()
            super(SessionRecordingMixin, self)._update_record_button()

    def _set_record_button_color(self, color):
        self.record_button.color = color