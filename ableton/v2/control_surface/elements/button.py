# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.builtins import long
import Live
from ...base import BooleanContext, const, has_event, in_range, listens, old_hasattr
from ..input_control_element import MIDI_CC_TYPE, InputControlElement
from ..skin import Skin
from .color import Color

class DummyUndoStepHandler(object):

    def begin_undo_step(self):
        return

    def end_undo_step(self):
        return

class ButtonElementMixin(object):
    pass

    def set_light(self, value):
        return

class ButtonElement(InputControlElement, ButtonElementMixin):
    pass

    class ProxiedInterface(InputControlElement.ProxiedInterface, ButtonElementMixin):
        is_momentary = const(True)
        is_pressed = const(False)

    class Colors:

        class DefaultButton:
            On = Color(127)
            Off = Color(1)
            Disabled = Color(0)
    num_delayed_messages = 2

    def __init__(self, is_momentary, msg_type, channel, identifier, is_rgb=False, skin=Skin(Colors), undo_step_handler=DummyUndoStepHandler(), send_should_depend_on_forwarding=False, *a, **k):
        super(ButtonElement, self).__init__(msg_type, channel, identifier, *a, send_should_depend_on_forwarding=send_should_depend_on_forwarding, **k)
        self.is_rgb = is_rgb
        self._is_momentary = bool(is_momentary)
        self._last_received_value = -1
        self._undo_step_handler = undo_step_handler
        self._skin = skin
        self._drawing_via_skin = BooleanContext()

    def reset(self):
        self.set_light('DefaultButton.Disabled')
        self.use_default_message()
        self.suppress_script_forwarding = False

    def is_momentary(self):
        pass
        return self._is_momentary

    def message_map_mode(self):
        return Live.MidiMap.MapMode.absolute

    def is_pressed(self):
        return self._is_momentary and int(self._last_received_value) > 0

    def set_light(self, value):
        if old_hasattr(value, 'draw'):
            value.draw(self)
            return
        elif type(value) in (int, long) and in_range(value, 0, 128):
            self.send_value(value)
            return
        elif isinstance(value, bool):
            self._set_skin_light('DefaultButton.On' if value else 'DefaultButton.Off')
            return
        else:
            self._set_skin_light(value)

    def _set_skin_light(self, value):
        pass

    def _do_draw(self, color):
        pass

    @listens('midi_value')
    def __on_midi_value_changed(self, *a):
        self._do_draw(self.__on_midi_value_changed.subject)

    def send_value(self, value, force=False, channel=None):
        if not self._drawing_via_skin:
            self._disconnect_color_listener()
        super(ButtonElement, self).send_value(value, force, channel)

    def receive_value(self, value):
        pressed_before = self.is_pressed()
        self._last_received_value = value
        if not pressed_before and self.is_pressed():
            self._undo_step_handler.begin_undo_step()
        super(ButtonElement, self).receive_value(value)
        if not pressed_before or not self.is_pressed():
            self._undo_step_handler.end_undo_step()
            return

    def disconnect(self):
        super(ButtonElement, self).disconnect()
        self._undo_step_handler = None

    def _disconnect_color_listener(self):
        self.__on_midi_value_changed.subject = None