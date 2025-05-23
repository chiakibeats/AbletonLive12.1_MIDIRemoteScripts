# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\ConfigurableButtonElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import OFF_VALUE, ON_VALUE, ButtonElement
from _Framework.Skin import SkinColorMissingError

class ConfigurableButtonElement(ButtonElement):
    pass
    default_states = {True: 'DefaultButton.On', False: 'DefaultButton.Disabled'}
    send_depends_on_forwarding = False
    pass
    pass

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=None, default_states=None, *a, **k):
        super(ConfigurableButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin=skin, **k)
        if default_states is not None:
            self.default_states = default_states
        self.states = dict(self.default_states)

    @property
    def _on_value(self):
        return self.states[True]

    @property
    def _off_value(self):
        return self.states[False]

    @property
    def on_value(self):
        return self._try_fetch_skin_value(self._on_value)

    @property
    def off_value(self):
        return self._try_fetch_skin_value(self._off_value)

    def _try_fetch_skin_value(self, value):
        try:
            return self._skin[value]
        except SkinColorMissingError:
            return value

    def reset(self):
        self.set_light('DefaultButton.Disabled')
        self.reset_state()

    def reset_state(self):
        self.states = dict(self.default_states)
        super(ConfigurableButtonElement, self).reset_state()
        self.set_enabled(True)

    def set_on_off_values(self, on_value, off_value):
        self.states[True] = on_value
        self.states[False] = off_value

    def set_enabled(self, enabled):
        self.suppress_script_forwarding = not enabled

    def is_enabled(self):
        return not self.suppress_script_forwarding

    def set_light(self, value):
        super(ConfigurableButtonElement, self).set_light(self.states.get(value, value))

    def send_value(self, value, **k):
        if value is ON_VALUE:
            self._do_send_on_value()
            return
        elif value is OFF_VALUE:
            self._do_send_off_value()
            return
        else:
            super(ConfigurableButtonElement, self).send_value(value, **k)

    def _do_send_on_value(self):
        self._skin[self._on_value].draw(self)

    def _do_send_off_value(self):
        self._skin[self._off_value].draw(self)

    def script_wants_forwarding(self):
        return not self.suppress_script_forwarding