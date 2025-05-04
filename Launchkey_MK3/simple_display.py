# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\simple_display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v2.base import task
from ableton.v2.control_surface import NotifyingControlElement
from ableton.v3.base import as_ascii, get_default_ascii_translations
NON_ASCII_ENCODING = 17
TRANSLATED_DEGREE_SYMBOL = 48
ascii_translations = get_default_ascii_translations()
ascii_translations['Åã'] = (NON_ASCII_ENCODING, TRANSLATED_DEGREE_SYMBOL)
as_ascii = partial(as_ascii, ascii_translations=ascii_translations)

class SimpleDisplayElement(NotifyingControlElement):
    pass

    def __init__(self, command, tail, *a, **k):
        super(SimpleDisplayElement, self).__init__(*a, **k)
        self._message_command = command
        self._message_header = None
        self._message_tail = tail
        self._message_to_send = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()
        self._initialized = False

    def initialize(self, header):
        self._message_header = header + self._message_command
        self._initialized = True
        self._request_send_message()

    def display_message(self, message):
        pass
        if message:
            self._message_to_send = tuple(as_ascii(message)) + self._message_tail
            self._request_send_message()

    def update(self):
        self._last_sent_message = None
        self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        self.display_message(' ')

    def send_midi(self, message):
        if message != self._last_sent_message:
            NotifyingControlElement.send_midi(self, message)
            self._last_sent_message = message
            return

    def _request_send_message(self):
        if self._initialized:
            self._send_message_task.restart()

    def _send_message(self):
        if self._message_to_send:
            self.send_midi(self._message_header + self._message_to_send)