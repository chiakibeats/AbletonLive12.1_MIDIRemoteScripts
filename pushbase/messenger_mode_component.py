# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\messenger_mode_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import BooleanContext
from ableton.v2.control_surface.mode import ModesComponent
from .message_box_component import Messenger

class MessengerModesComponent(ModesComponent, Messenger):
    notify_when_enabled = False

    def __init__(self, muted=False, *a, **k):
        super(MessengerModesComponent, self).__init__(*a, **k)
        self._mode_message_map = {}
        self._default_and_alternative_mode_map = {}
        self._is_being_enabled = BooleanContext()
        self._muted = muted
    pass
    pass
    pass

    def add_mode(self, name, mode_or_component, message=None, default_mode=None, alternative_mode=None, **k):
        super(MessengerModesComponent, self).add_mode(name, mode_or_component, **k)
        self._mode_message_map[name] = message
        self._default_and_alternative_mode_map[name] = (default_mode, alternative_mode)

    def get_mode_message(self):
        message = self._mode_message_map.get(self.selected_mode, '')
        return message

    def get_default_mode_and_alternative_mode(self):
        default_mode, alternative_mode = self._default_and_alternative_mode_map.get(self.selected_mode, '')
        return (default_mode, alternative_mode)

    def on_enabled_changed(self):
        pass

    def _do_enter_mode(self, name):
        super(MessengerModesComponent, self)._do_enter_mode(name)
        if self._is_being_enabled and self.notify_when_enabled:
            if not self._muted:
                message = self._mode_message_map.get(name, None)
                if message:
                    self.show_notification(message)
                    return
            else:
                return None
        else:
            return

    @property
    def muted(self):
        return self._muted

    @muted.setter
    def muted(self, muted):
        self._muted = muted