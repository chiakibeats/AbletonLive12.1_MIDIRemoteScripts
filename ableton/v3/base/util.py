# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\base\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from . import is_iterable
PITCH_NAMES = ('C', 'Cò/Dó', 'D', 'Dò/Eó', 'E', 'F', 'Fò/Gó', 'G', 'Gò/Aó', 'A', 'Aò/Bó', 'B')
pass

class CallableBool:
    pass

    def __init__(self, value: bool):
        self.value = value

    def __call__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __bool__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return repr(self.value)

def get_default_ascii_translations():
    pass
    ascii_translations = {chr(i): i for i in range(32, 127)}
    ascii_translations['ò'] = 35
    return ascii_translations
DEFAULT_ASCII_TRANSLATIONS = get_default_ascii_translations()

def as_ascii(string, ascii_translations=DEFAULT_ASCII_TRANSLATIONS):
    pass
    result = []
    for char in string:
        translated_char = ascii_translations.get(char, ascii_translations['?'])
        if is_iterable(translated_char):
            result.extend(translated_char)
            continue
        else:
            result.append(translated_char)
            continue
    return result

def hex_to_rgb(hex_value):
    pass
    return ((hex_value & 16711680) >> 16, (hex_value & 65280) >> 8, hex_value & 255)

def pitch_index_to_string(index, pitch_names=PITCH_NAMES):
    pass
    return pitch_names[index % 12] + str(index // 12 - 2)

def round_to_multiple(value, base):
    pass
    return int(value / base) * base