# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\session.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.components import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):
    pass

    def set_copy_button(self, button):
        super().set_copy_button(button)
        for scene in self._scenes:
            scene.duplicate_button.set_control_element(button)