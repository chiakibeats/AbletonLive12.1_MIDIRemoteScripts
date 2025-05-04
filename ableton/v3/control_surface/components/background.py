# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\background.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from .. import Component
from ..controls import ButtonControl, InputControl, RadioButtonGroup

class NopControl(InputControl):
    pass

    class State(InputControl.State):

        def _event_listener_required(self):
            return True

class BackgroundComponent(Component):
    pass

    def __init__(self, name='Background', control_type=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._control_type = control_type or NopControl

    def _setup_control_state(self, name, control_state):
        return

    def __getattr__(self, name):
        if name.startswith('set_'):
            return partial(self._set_element_for_control, name[4:])
        else:
            raise AttributeError(name)

    def _set_element_for_control(self, name, element):
        pass
        if element:
            element.reset()
        if name in self.__dict__:
            self.__dict__[name].set_control_element(element)
            return
        else:
            control = self._control_type()
            control_state = control._get_state(self)
            setattr(self, name, control_state)
            self._setup_control_state(name, control_state)
            control_state.set_control_element(element)

class TranslatingBackgroundComponent(BackgroundComponent):
    pass
    channel_selection_buttons = RadioButtonGroup(unchecked_color='Translation.Channel.NotSelected', checked_color='Translation.Channel.Selected')

    def __init__(self, name='Translating_Background', translation_channel=0, *a, **k):
        super().__init__(*a, name=name, **k)
        self._base_translation_channel = translation_channel

    def set_channel_selection_buttons(self, buttons):
        self.channel_selection_buttons.set_control_element(buttons)
        if not buttons or self.channel_selection_buttons.checked_index < 0:
            self.channel_selection_buttons.checked_index = 0

    @channel_selection_buttons.checked
    def channel_selection_buttons(self, button):
        for control_state in self._control_states.values():
            control_state.channel = self._base_translation_channel + button.index

    def _setup_control_state(self, _, control_state):
        control_state.channel = self._base_translation_channel

class ModifierBackgroundComponent(BackgroundComponent):
    pass

    def __init__(self, name='Modifier_Background', *a, **k):
        super().__init__(*a, name=name, control_type=ButtonControl, **k)

    def _setup_control_state(self, name, control_state):
        base_name = self.name.title().replace('_', '')
        control_name = name.title().replace('_', '')
        control_state.color = '{}.{}'.format(base_name, control_name)
        control_state.pressed_color = '{}.{}Pressed'.format(base_name, control_name)