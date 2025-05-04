# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\identification.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import logging
from abc import ABC, abstractmethod
from ..base import depends, listenable_property, nop, task
from . import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, Component, InputControlElement, midi
from .controls import InputControl
from .display import Renderable
from .elements import SysexElement
logger = logging.getLogger(__name__)
NON_REALTIME_HEADER = (midi.SYSEX_START, midi.SYSEX_NON_REALTIME)
STANDARD_RESPONSE_BYTES = (midi.SYSEX_GENERAL_INFO, midi.SYSEX_IDENTITY_RESPONSE_ID)
PRODUCT_ID_BYTES_START_INDEX = 3

def status_byte_to_msg_type(status_byte):
    pass
    status_byte = 240 & status_byte
    msg_type = MIDI_CC_TYPE
    if status_byte == midi.NOTE_ON_STATUS:
        msg_type = MIDI_NOTE_TYPE
    elif status_byte == midi.PB_STATUS:
        msg_type = MIDI_PB_TYPE
    return msg_type

def create_responder(identity_response_id_bytes, custom_identity_response):
    pass
    if identity_response_id_bytes is not None:
        return StandardResponder(identity_response_id_bytes)
    elif custom_identity_response[0] == midi.SYSEX_START:
        return CustomSysexResponder(custom_identity_response)
    else:
        return PlainMidiResponder(custom_identity_response)

class Responder(ABC):
    pass

    def __init__(self, response_bytes, *a, **k):
        super().__init__(*a, **k)
        self._response_bytes = tuple(response_bytes)

    @abstractmethod
    def create_response_element(self):
        return

    @abstractmethod
    def is_valid_response(self, response_bytes):
        return

class CustomSysexResponder(Responder):
    pass

    def create_response_element(self):
        return SysexElement(sysex_identifier=self._response_bytes)

    def is_valid_response(self, _):
        return True

class PlainMidiResponder(Responder):
    pass

    def __init__(self, response_bytes, *a, **k):
        super().__init__(response_bytes, *a, **k)
        self._expected_response_value_bytes = midi.extract_value(response_bytes) if len(response_bytes) == 3 else None

    def create_response_element(self):
        first_byte = self._response_bytes[0]
        element = InputControlElement(msg_type=status_byte_to_msg_type(first_byte), channel=15 & first_byte, identifier=self._response_bytes[1])
        element.reset = nop
        return element

    def is_valid_response(self, response_bytes):
        return self._expected_response_value_bytes is None or self._expected_response_value_bytes == response_bytes

class StandardResponder(Responder):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._variable_byte_index = self._response_bytes.index(-1) if -1 in self._response_bytes else None
        if self._variable_byte_index is not None:
            self._response_bytes = list(self._response_bytes)

    def create_response_element(self):
        return SysexElement(sysex_identifier=NON_REALTIME_HEADER)

    def is_valid_response(self, response_bytes):
        if response_bytes[1:PRODUCT_ID_BYTES_START_INDEX] == STANDARD_RESPONSE_BYTES:
            product_id_bytes = self._extract_product_id_bytes(response_bytes)
            expected_bytes = tuple(self._response_bytes)
            if product_id_bytes != expected_bytes:
                raise IdentityResponseError(expected_bytes=expected_bytes, actual_bytes=product_id_bytes)
            else:
                return True
        else:
            return False

    def _extract_product_id_bytes(self, midi_bytes):
        id_bytes = midi_bytes[PRODUCT_ID_BYTES_START_INDEX:PRODUCT_ID_BYTES_START_INDEX + len(self._response_bytes)]
        if self._variable_byte_index is not None:
            self._response_bytes[self._variable_byte_index] = id_bytes[self._variable_byte_index]
        return id_bytes

class IdentityResponseError(Exception):
    pass

    def __init__(self, expected_bytes=None, actual_bytes=None):
        super().__init__('Hardware controller responded with wrong identity bytes: ({} != {}).'.format(expected_bytes, actual_bytes))

class IdentificationComponent(Component, Renderable):
    pass
    identity_response_control = InputControl()
    is_identified = listenable_property.managed(False)
    received_response_bytes = listenable_property.managed(None)

    @depends(send_midi=None)
    def __init__(self, name='Identification', identity_request=midi.SYSEX_IDENTITY_REQUEST_MESSAGE, identity_request_delay=0.0, identity_response_id_bytes=None, custom_identity_response=None, send_midi=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._send_midi = send_midi
        self._identity_request = identity_request
        self._has_notified = False
        self._responder = create_responder(identity_response_id_bytes, custom_identity_response)
        response_element = self._responder.create_response_element()
        response_element.name = 'identity_control'
        response_element.is_private = True
        self.identity_response_control.set_control_element(response_element)
        self._request_task = self._tasks.add(task.sequence(task.run(self._send_identity_request), task.wait(identity_request_delay), task.run(self._send_identity_request), task.wait(identity_request_delay + 0.5), task.run(lambda: setattr(self, '_has_notified', False))))
        self._request_task.kill()

    @identity_response_control.value
    def identity_response_control(self, response_bytes, _):
        try:
            if self._responder.is_valid_response(response_bytes):
                self._request_task.kill()
                self.identity_response_control.enabled = False
                self.received_response_bytes = response_bytes
                self.is_identified = True
                if not self._has_notified:
                    self.notify(self.notifications.identify)
                    self._has_notified = True
                    return
        except IdentityResponseError as e:
            logger.error(e)

    def request_identity(self):
        pass
        self._request_task.restart()
        self.received_response_bytes = None
        self.is_identified = False

    def _send_identity_request(self):
        self.identity_response_control.enabled = True
        self._send_midi(self._identity_request)