# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\controls\control.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from . import EncoderControl, InputControl, SendValueMixin

class SendValueInputControl(InputControl):
    pass

    class State(SendValueMixin, InputControl.State):
        pass

class SendValueEncoderControl(EncoderControl):
    pass

    class State(SendValueMixin, EncoderControl.State):
        pass