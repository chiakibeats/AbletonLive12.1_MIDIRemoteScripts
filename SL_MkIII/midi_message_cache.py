# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\midi_message_cache.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .sysex import NUM_SET_PROPERTY_HEADER_BYTES

class MidiMessageCache:

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._messages = []

    def __call__(self, message):
        self._messages = list(filter(lambda m: m[:NUM_SET_PROPERTY_HEADER_BYTES] != message[:NUM_SET_PROPERTY_HEADER_BYTES], self._messages))
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages

    def clear(self):
        self._messages = []