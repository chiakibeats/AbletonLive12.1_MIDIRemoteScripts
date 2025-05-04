# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\pad_sensitivity.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from collections import namedtuple
playing_profile = 0
pass
default_profile = 1
pass
loop_selector_profile = 2
pass
MONO_AFTERTOUCH_ENABLED = 1
MONO_AFTERTOUCH_DISABLED = 0
PadSettings = namedtuple('PadSettings', ['sensitivity', 'aftertouch_enabled'])
pass

def index_to_pad_coordinate(index):
    pass
    x, y = divmod(index, 8)
    return (8 - x, y + 1)

def pad_parameter_sender(global_control, pad_control, aftertouch_control):
    pass

    def do_send(pad_settings, pad=None):
        if pad is None:
            global_control.send_value(0, 0, pad_settings.sensitivity)
            aftertouch_control.send_value(0, 0, pad_settings.aftertouch_enabled)
            return
        else:
            scene, track = index_to_pad_coordinate(pad)
            pad_control.send_value(scene, track, pad_settings.sensitivity)
            aftertouch_control.send_value(scene, track, pad_settings.aftertouch_enabled)
    return do_send