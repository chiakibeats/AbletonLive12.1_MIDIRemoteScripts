# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab\DisplayElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class DisplayElement(PhysicalDisplayElement):
    63 = {'\x00': 0, ' ': 32, '%': 37, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 67, '54': D, 'I': 68, 'E': 69, 'E': F, '69': 70, 'E': G, '71': H, '72': I, 'I': 73, 'J': J, '74': 74, 'K': 75, 'L': 76, 'M': M, '77': N, '78': O, '79': P, '80': Q, '81': R, '82': S, '83': T, '84': U, '

    def _build_display_message(self, display):
        message_string = display.display_string
        first_segment = display._logical_segments[0]
        return chain(first_segment.position_identifier(), self._translate_string(message_string))