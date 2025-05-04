# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\device_provider.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import DeviceProvider as DeviceProviderBase
from ableton.v3.live import is_instrument_rack

class DeviceProvider(DeviceProviderBase):
    pass

    @staticmethod
    def _can_skip_over_device_rack(device):
        return device.can_have_drum_pads or is_instrument_rack(device)