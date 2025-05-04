# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.midi import SYSEX_END, SYSEX_START
SYSEX_HEADER = (SYSEX_START, 0, 32, 114)
NUMERIC_DISPLAY_COMMAND = (0,)
LIVE_INTEGRATION_MODE_ID = (SYSEX_START, 0, 0, 116, 1, 0, 77, 67, 1, 0, 7, 1, 0)