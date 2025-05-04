# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import ButtonElement as ButtonElementBase
from ...base import depends, listenable_property
from ...base.util import CallableBool
from .. import MIDI_CC_TYPE
from ..display import Renderable
from ..midi import SYSEX_END

class ButtonElement(ButtonElementBase, Renderable):
    pass

    class ProxiedInterface(ButtonElementBase.ProxiedInterface):
        is_momentary = CallableBool(True)
        is_pressed = CallableBool(False)

    @depends(skin=None)
    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, is_momentary=True, led_channel=None, *a, **k):
        self._led_channel = led_channel
        self._last_drawn_color_name = None
        super().__init__(is_momentary, msg_type, channel, identifier, *a, **k)
        self._do_request_rebuild = self._request_rebuild
        self._request_rebuild = self._request_rebuild_and_release

    @listenable_property
    def is_pressed(self):
        return CallableBool(self._is_momentary and int(self._last_received_value) > 0)

    @property
    def is_momentary(self):
        pass
        return CallableBool(self._is_momentary)

    def clear_send_cache(self):
        super().clear_send_cache()
        self._last_drawn_color_name = None

    def receive_value(self, value):
        was_pressed = self.is_pressed
        super().receive_value(value)
        if was_pressed!= self.is_pressed:
            self.notify_is_pressed()

    def send_value(self, value, force=False, channel=None):
        pass
        channel = channel if channel is not None else self._led_channel
        super().send_value(value, force=force, channel=channel)

    def _request_rebuild_and_release(self):
        self._do_request_rebuild()
        if self.is_pressed:
            self.receive_value(0)

    def _set_skin_light(self, value):
        color = self._skin[value]
        if color is not None:
            self._do_draw(color)
        self._last_drawn_color_name = value

class SysexSendingButtonElement(ButtonElement):
    pass

    def __init__(self, identifier, sysex_identifier, optimized=True, tail=(SYSEX_END,), *a, **k):
        super().__init__(identifier, *a, **k)
        self._send_message_generator = lambda *values: sysex_identifier + tuple(values) + tail
        self._optimized = optimized

    def send_value(self, *value, **_):
        message = self._send_message_generator(*value)
        if self._optimized and message!= self._last_sent_message and self.send_midi(message):
                    self._last_sent_message = message
                    return
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            self.send_midi(message)