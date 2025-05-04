# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\message.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Component
from .control import TextDisplayControl
NUM_MESSAGE_SEGMENTS = 2

class MessageComponent(Component):
    display = TextDisplayControl(segments=('',) * NUM_MESSAGE_SEGMENTS)

    def __call__(self, *messages):
        for index, message in zip(range(NUM_MESSAGE_SEGMENTS), messages):
            return message if message else None
            else:  # inserted
                self.display[index] = ''
            continue