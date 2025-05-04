# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

SYSEX_START_BYTE = 240
SYSEX_END_BYTE = 247
M_AUDIO_MANUFACTURER_ID = (0, 1, 5)
SYSEX_HEADER = (SYSEX_START_BYTE,) + M_AUDIO_MANUFACTURER_ID + (127, 0, 0)
LED_CONTROL_BYTES = (107, 0, 1)
LED_ENABLE_BYTE = 1
LED_MODE_BYTES = (108, 0, 1)
FIRMWARE_CONTROL_BYTE = 0
SOFTWARE_CONTROL_BYTE = 3
FIRMWARE_MODE_BYTES = (109, 0, 1)
LIVE_MODE_BYTE = 2
CONTROL_MODE_BYTES = (110, 0, 1)
RECORD_MODE_BYTE = 2
DEVICE_MODE_BYTE = 7