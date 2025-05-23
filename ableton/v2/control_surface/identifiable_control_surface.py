# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\identifiable_control_surface.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import logging
from ..base import task
from . import midi
from .control_surface import ControlSurface
logger = logging.getLogger(__name__)

class IdentifiableControlSurface(ControlSurface):
    pass
    identity_request_delay = 0.0
    identity_request = midi.SYSEX_IDENTITY_REQUEST_MESSAGE

    def __init__(self, product_id_bytes=None, *a, **k):
        super(IdentifiableControlSurface, self).__init__(*a, **k)
        self._product_id_bytes = product_id_bytes
        self._identity_response_pending = False
        self._request_task = self._tasks.add(task.sequence(task.wait(self.identity_request_delay), task.run(self._send_identity_request)))
        self._request_task.kill()

    def on_identified(self, response_bytes):
        self.refresh_state()

    def port_settings_changed(self):
        self._request_task.restart()

    def process_midi_bytes(self, midi_bytes, midi_processor):
        if midi.is_sysex(midi_bytes) and self._is_identity_response(midi_bytes):
            product_id_bytes = self._extract_product_id_bytes(midi_bytes)
            if product_id_bytes == self._product_id_bytes:
                self._request_task.kill()
                if self._identity_response_pending:
                    self.on_identified(midi_bytes)
                    self._identity_response_pending = False
                    return
                else:
                    return None
            else:
                logger.error('MIDI device responded with wrong product id (%s != %s).', str(self._product_id_bytes), str(product_id_bytes))
                return
        else:
            super(IdentifiableControlSurface, self).process_midi_bytes(midi_bytes, midi_processor)

    def _is_identity_response(self, midi_bytes):
        return midi_bytes[3:5] == (midi.SYSEX_GENERAL_INFO, midi.SYSEX_IDENTITY_RESPONSE_ID)

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[5:5 + len(self._product_id_bytes)]

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi(self.identity_request)