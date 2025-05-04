# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\TranslationComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class TranslationComponent(ControlSurfaceComponent):
    pass
    pass

    def __init__(self, translated_channel, should_enable=True, should_reset=True, *a, **k):
        self._translated_channel = translated_channel
        self._should_enable = bool(should_enable)
        self._should_reset = should_reset
        super(TranslationComponent, self).__init__(*a, **k)

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._set_control_elements, name[4:])
        else:
            raise AttributeError(name)

    def _set_control_elements(self, name, control_elements):
        if bool(control_elements):
            buttons = control_elements
            for button in buttons:
                if button:
                    if self._should_reset:
                        button.reset()
                    else:
                        button.reset_state()
                    button.set_enabled(self._should_enable)
                    button.set_channel(self._translated_channel)
                pass
                continue
        else:
            return