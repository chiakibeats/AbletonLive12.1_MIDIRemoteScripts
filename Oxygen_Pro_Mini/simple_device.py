# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro_Mini\simple_device.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from novation.simple_device import SimpleDeviceParameterComponent as SimpleDeviceParameterComponentBase
NUM_CONTROLS = 4

class SimpleDeviceParameterComponent(SimpleDeviceParameterComponentBase):

    def __init__(self, *a, **k):
        super(SimpleDeviceParameterComponent, self).__init__(*a, **k)
        self._parameter_offset = 0

    def toggle_parameter_offset(self):
        self._parameter_offset = NUM_CONTROLS - self._parameter_offset
        self.update()

    @SimpleDeviceParameterComponentBase.selected_bank.getter
    def selected_bank(self):
        bank = self._banks[0] or []
        if self._parameter_offset and len(bank) > self._parameter_offset:
            offset_bank = bank[self._parameter_offset:]
            if any(offset_bank):
                return offset_bank
        return bank