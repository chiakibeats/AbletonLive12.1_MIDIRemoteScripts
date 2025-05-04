# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialDeviceComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.DeviceComponent import DeviceComponent
from .consts import DEVICE_MAP_CHANNEL, FADER_TYPE_STANDARD

class SpecialDeviceComponent(DeviceComponent):

    def set_parameter_controls(self, controls):
        if controls:
            for control in controls:
                control.set_channel(DEVICE_MAP_CHANNEL)
                control.set_light_and_type('Device.On', FADER_TYPE_STANDARD)
        super(SpecialDeviceComponent, self).set_parameter_controls(controls)

    def _update_parameter_controls(self):
        if self._parameter_controls is not None:
            for control in self._parameter_controls:
                control.update()
        else:
            return

    def update(self):
        super(SpecialDeviceComponent, self).update()
        if self.is_enabled():
            self._update_parameter_controls()