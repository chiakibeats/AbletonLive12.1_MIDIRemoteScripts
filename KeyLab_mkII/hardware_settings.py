# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\hardware_settings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from KeyLab_Essential import sysex
from KeyLab_Essential.hardware_settings import HardwareSettingsComponent as HardwareSettingsComponentBase

class HardwareSettingsComponent(HardwareSettingsComponentBase):

    def __init__(self, *a, **k):
        super(HardwareSettingsComponent, self).__init__(*a, **k)
        self._vegas_mode_switch = None

    def set_vegas_mode_switch(self, switch):
        self._vegas_mode_switch = switch

    def set_hardware_live_mode_enabled(self, enable):
        super(HardwareSettingsComponent, self).set_hardware_live_mode_enabled(enable)
        if enable and self._vegas_mode_switch:
            self._vegas_mode_switch.send_value(sysex.OFF_VALUE)