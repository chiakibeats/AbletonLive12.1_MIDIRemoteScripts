# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\notification_suppression.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl

class NotificationSuppressionComponent(Component):
    pass
    suppress_button = ButtonControl(color='DefaultButton.Back')

    @depends(suppress_notifications=None)
    def __init__(self, suppress_notifications=None, *a, **k):
        super().__init__(*a, **k)
        self._suppress_notifications = suppress_notifications

    @suppress_button.pressed
    def suppress_button(self, _):
        self._suppress_notifications()