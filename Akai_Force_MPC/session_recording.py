# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\session_recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.control import ToggleButtonControl

class SessionRecordingComponent(SessionRecordingComponentBase):
    mpc_automation_toggle = ToggleButtonControl(toggled_color='Automation.On', untoggled_color='Automation.Off')

    def _on_session_automation_record_changed(self):
        super(SessionRecordingComponent, self)._on_session_automation_record_changed()
        self.mpc_automation_toggle.is_toggled = self.song.session_automation_record

    @mpc_automation_toggle.toggled
    def mpc_automation_toggle(self, is_toggled, _):
        self.song.session_automation_record = is_toggled