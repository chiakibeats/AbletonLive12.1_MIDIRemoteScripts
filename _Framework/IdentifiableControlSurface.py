# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\IdentifiableControlSurface.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from . import Task
from .ControlSurface import ControlSurface
SYSEX_IDENTITY_REQUEST = (240, 126, 0, 6, 1, 247)

class IdentifiableControlSurface(ControlSurface):
    pass
    identity_request_delay = 0.5
    identity_request = SYSEX_IDENTITY_REQUEST

    def __init__(self, product_id_bytes=None, *a, **k):
        super(IdentifiableControlSurface, self).__init__(*a, **k)
        self._product_id_bytes = product_id_bytes
        self._identity_response_pending = False
        self._request_task = self._tasks.add(Task.sequence(Task.wait(self.identity_request_delay), Task.run(self._send_identity_request)))
        self._request_task.kill()

    def on_identified(self):
        raise NotImplementedError

    def port_settings_changed(self):
        self._request_task.restart()

    def handle_sysex(self, midi_bytes):
        if self._is_identity_response(midi_bytes):
            product_id_bytes = self._extract_product_id_bytes(midi_bytes)
            if product_id_bytes == self._product_id_bytes:
                self._request_task.kill()
                if self._identity_response_pending:
                    self.on_identified()
                    self._identity_response_pending = False
            else:
                self.log_message('MIDI device responded with wrong product id (%s != %s).' % (str(self._product_id_bytes), str(product_id_bytes)))
        else:
            super(IdentifiableControlSurface, self).handle_sysex(midi_bytes)

    def _is_identity_response(self, midi_bytes):
        return midi_bytes[3:5] == (6, 2)

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[5:5 + len(self._product_id_bytes)]

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi(self.identity_request)