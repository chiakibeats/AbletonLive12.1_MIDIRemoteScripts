# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\mode.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from ..base import NamedTuple, depends, infinite_context_manager, is_contextmanager, is_iterable, lazy_attribute, listenable_property, listens, old_hasattr, task
from . import defaults
from .component import Component
from .control import ButtonControl, ButtonControlBase, control_color
from .layer import CompoundLayer, Layer
from .resource import StackingResource

def tomode(thing):
    if thing is None:
        return Mode()
    elif isinstance(thing, Mode):
        return thing
    elif old_hasattr(thing, 'set_enabled'):
        return EnablingMode(thing)
    else:
        if isinstance(thing, tuple) and len(thing) == 2:
            if isinstance(thing[0], Component) and isinstance(thing[1], (Layer, CompoundLayer)):
                return LayerMode(*thing)
            elif callable(thing[0]) and callable(thing[1]):
                mode = Mode()
                mode.enter_mode, mode.leave_mode = thing
                return mode
        if is_iterable(thing):
            return CompoundMode(*thing)
        elif is_contextmanager(thing):
            return ContextManagerMode(thing)
        elif callable(thing):
            mode = Mode()
            mode.enter_mode = thing
            return mode
        else:
            return thing

def to_camel_case_name(mode_name, separator=''):
    return separator.join(map(lambda s: s.capitalize(), mode_name.split('_')))

def pop_last_mode(component, mode):
    if len(component.active_modes) > 1:
        component.pop_mode(mode)

class Mode(object):
    pass

    def enter_mode(self):
        return

    def leave_mode(self):
        return

    def __enter__(self):
        self.enter_mode()

    def __exit__(self, *a):
        return self.leave_mode()

class ContextManagerMode(Mode):
    pass

    def __init__(self, context_manager=None, *a, **k):
        super(ContextManagerMode, self).__init__(*a, **k)
        self._context_manager = context_manager

    def enter_mode(self):
        self._context_manager.__enter__()

    def leave_mode(self):
        self._context_manager.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        return self._context_manager.__exit__(exc_type, exc_value, traceback)

def generator_mode(function):
    makecontext = infinite_context_manager(function)
    return lambda *a, **k: ContextManagerMode(makecontext(*a, **k))

class EnablingMode(Mode):
    pass

    def __init__(self, enableable=None, *a, **k):
        super(EnablingMode, self).__init__(*a, **k)
        self._enableable = enableable

    def enter_mode(self):
        self._enableable.set_enabled(True)

    def leave_mode(self):
        self._enableable.set_enabled(False)

class LazyEnablingMode(Mode):
    pass

    def __init__(self, factory=None, *a, **k):
        super(LazyEnablingMode, self).__init__(*a, **k)
        self._factory = factory

    @lazy_attribute
    def enableable(self):
        return self._factory()

    def enter_mode(self):
        self.enableable.set_enabled(True)

    def leave_mode(self):
        self.enableable.set_enabled(False)

class LayerModeBase(Mode):

    def __init__(self, component=None, layer=None, *a, **k):
        super(LayerModeBase, self).__init__(*a, **k)
        self._component = component
        self._layer = layer

    def _get_component(self):
        return self._component() if callable(self._component) else self._component

class LayerMode(LayerModeBase):
    pass

    def enter_mode(self):
        self._get_component().layer = self._layer

    def leave_mode(self):
        self._get_component().layer = None

class AddLayerMode(LayerModeBase):
    pass

    def enter_mode(self):
        self._layer.grab(self._get_component())

    def leave_mode(self):
        self._layer.release(self._get_component())

class CompoundMode(Mode):
    pass

    def __init__(self, *modes, **k):
        super(CompoundMode, self).__init__(**k)
        self._modes = list(map(tomode, modes))

    def enter_mode(self):
        for mode in self._modes:
            mode.enter_mode()

    def leave_mode(self):
        for mode in reversed(self._modes):
            mode.leave_mode()

class SetAttributeMode(Mode):
    pass

    def __init__(self, obj=None, attribute=None, value=None, *a, **k):
        super(SetAttributeMode, self).__init__(*a, **k)
        self._obj = obj
        self._attribute = attribute
        self._old_value = None
        self._value = value

    def _get_object(self):
        return self._obj() if callable(self._obj) else self._obj

    def enter_mode(self):
        self._old_value = getattr(self._get_object(), self._attribute, None)
        setattr(self._get_object(), self._attribute, self._value)

    def leave_mode(self):
        if getattr(self._get_object(), self._attribute) == self._value:
            setattr(self._get_object(), self._attribute, self._old_value)

class DelayMode(Mode):
    pass

    @depends(parent_task_group=None)
    def __init__(self, mode=None, delay=None, parent_task_group=None, *a, **k):
        super(DelayMode, self).__init__(*a, **k)
        delay = delay if delay is not None else defaults.MOMENTARY_DELAY
        self._mode = tomode(mode)
        self._mode_entered = False
        self._delay_task = parent_task_group.add(task.sequence(task.wait(delay), task.run(self._enter_mode_delayed)))
        self._delay_task.kill()

    def _enter_mode_delayed(self):
        self._mode_entered = True
        self._mode.enter_mode()

    def enter_mode(self):
        self._delay_task.restart()

    def leave_mode(self):
        if self._mode_entered:
            self._mode.leave_mode()
            self._mode_entered = False
        self._delay_task.kill()

class ModeButtonControl(ButtonControlBase):
    pass

    class State(ButtonControlBase.State):
        mode_selected_color = control_color('DefaultButton.On')
        mode_unselected_color = control_color('DefaultButton.Off')
        mode_group_active_color = control_color('DefaultButton.On')
        pass
        pass
        pass
        pass
        pass

        def __init__(self, modes_component=None, mode_name=None, mode_selected_color=None, mode_unselected_color=None, mode_group_active_color=None, *a, **k):
            self._modes_component = modes_component
            self._mode_name = mode_name
            super(ModeButtonControl.State, self).__init__(*a, **k)
            if mode_selected_color is not None:
                self.mode_selected_color = mode_selected_color
            if mode_unselected_color is not None:
                self.mode_unselected_color = mode_unselected_color
            if mode_group_active_color is not None:
                self.mode_group_active_color = mode_group_active_color
            self.__on_selected_mode_changed.subject = self._modes_component

        @property
        def mode_name(self):
            return self._mode_name

        @listens('selected_mode')
        def __on_selected_mode_changed(self, mode):
            self._send_current_color()

        def _send_button_color(self):
            selected_mode = self._modes_component.selected_mode
            groups = self._modes_component.get_mode_groups(self._mode_name)
            selected_groups = self._modes_component.get_mode_groups(selected_mode)
            if selected_mode == self._mode_name:
                self._control_element.set_light(self.mode_selected_color)
                return
            elif bool(groups & selected_groups):
                self._control_element.set_light(self.mode_group_active_color)
                return
            else:
                self._control_element.set_light(self.mode_unselected_color)

class ModeButtonBehaviour(object):
    pass

    def press_immediate(self, component, mode):
        return

    def release_immediate(self, component, mode):
        return

    def press_delayed(self, component, mode):
        return

    def release_delayed(self, component, mode):
        return

    def update_button(self, component, mode, selected_mode):
        return

class ImmediateBehaviour(ModeButtonBehaviour):
    pass

    def press_immediate(self, component, mode):
        component.push_mode(mode)

class LatchingBehaviour(ImmediateBehaviour):
    pass

    def release_immediate(self, component, mode):
        component.pop_unselected_modes()

    def release_delayed(self, component, mode):
        pop_last_mode(component, mode)

class MomentaryBehaviour(ImmediateBehaviour):
    pass

    def release_immediate(self, component, mode):
        pop_last_mode(component, mode)

    def release_delayed(self, component, mode):
        pop_last_mode(component, mode)

class ReenterBehaviour(LatchingBehaviour):
    pass

    def __init__(self, on_reenter=None, *a, **k):
        super(ReenterBehaviour, self).__init__(*a, **k)
        if on_reenter is not None:
            self.on_reenter = on_reenter

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self.on_reenter()

    def on_reenter(self):
        return

def make_mode_button_control(modes_component, mode_name, behaviour, **k):
    button_control = ModeButtonControl(modes_component=modes_component, mode_name=mode_name, **k)

    @button_control.pressed
    def button_control(modes_component, button):
        behaviour.press_immediate(modes_component, mode_name)

    @button_control.pressed_delayed
    def button_control(modes_component, button):
        behaviour.press_delayed(modes_component, mode_name)

    @button_control.released_immediately
    def button_control(modes_component, button):
        behaviour.release_immediate(modes_component, mode_name)

    @button_control.released_delayed
    def button_control(modes_component, button):
        behaviour.release_delayed(modes_component, mode_name)
    return button_control

class _ModeEntry(NamedTuple):
    pass
    mode = None
    groups = set()
    cycle_mode_button_color = None
    listens = None

class NullModes(object):
    selected_mode = None

class ModesComponent(Component):
    pass
    cycle_mode_button = ButtonControl()
    default_behaviour = LatchingBehaviour()
    pass

    def __init__(self, enable_skinning=False, support_momentary_mode_cycling=True, *a, **k):
        super(ModesComponent, self).__init__(*a, **k)
        self._enable_skinning = enable_skinning
        self._support_momentary_mode_cycling = support_momentary_mode_cycling
        self._last_toggle_value = 0
        self._mode_toggle = None
        self._mode_list = []
        self._mode_map = {}
        self._last_selected_mode = None
        self._mode_stack = StackingResource(self._do_enter_mode, self._do_leave_mode)

    def disconnect(self):
        self._mode_stack.release_all()
        super(ModesComponent, self).disconnect()

    @listenable_property
    def selected_mode(self):
        pass
        return self._mode_stack.owner or self._last_selected_mode

    @selected_mode.setter
    def selected_mode(self, mode):
        if self.is_enabled():
            if self.selected_mode != mode:
                if mode is not None:
                    self.push_mode(mode)
                    self.pop_unselected_modes()
                    return
                else:
                    self._mode_stack.release_all()
                    return
            else:
                return None
        else:
            self._last_selected_mode = mode

    @property
    def selected_groups(self):
        entry = self._mode_map.get(self.selected_mode, None)
        return entry.groups if entry else set()

    @property
    def active_modes(self):
        return self._mode_stack.clients

    def push_mode(self, mode):
        pass
        self._mode_stack.grab(mode)

    def pop_mode(self, mode):
        pass
        self._mode_stack.release(mode)

    def pop_groups(self, groups):
        pass
        if not isinstance(groups, set):
            groups = set(groups)
        for client in self._mode_stack.clients:
            if self.get_mode_groups(client) & groups:
                self._mode_stack.release(client)
            continue

    def pop_unselected_modes(self):
        pass
        self._mode_stack.release_stacked()

    def add_mode(self, name, mode_or_component, cycle_mode_button_color=None, groups=set(), behaviour=None):
        pass
        if not isinstance(groups, set):
            groups = set(groups)
        mode = tomode(mode_or_component)
        behaviour = behaviour if behaviour is not None else self.default_behaviour
        self._mode_list.append(name)
        self._mode_map[name] = _ModeEntry(mode=mode, cycle_mode_button_color=cycle_mode_button_color, behaviour=behaviour, groups=groups)
        self.add_mode_button_control(name, behaviour)

    @property
    def modes(self):
        return self._mode_list

    def get_mode_groups(self, name):
        entry = self._mode_map.get(name, None)
        return entry.groups if entry else set()

    def add_mode_button_control(self, mode_name, behaviour):
        colors = {}
        if self._enable_skinning:
            mode_color_basename = 'Mode.' + to_camel_case_name(mode_name)
            colors = {'mode_selected_color': mode_color_basename + '.On', 'mode_unselected_color': mode_color_basename + '.Off', 'mode_group_active_color': mode_color_basename + '.On'}
        button_control = make_mode_button_control(self, mode_name, behaviour, **colors)
        self.add_control('%s_button' % mode_name, button_control)
        self._update_mode_buttons(self.selected_mode)

    def _get_mode_behaviour(self, name):
        entry = self._mode_map.get(name, None)
        return entry.behaviour if entry is not None else self.default_behaviour

    def get_mode(self, name):
        entry = self._mode_map.get(name, None)
        return entry and entry.mode

    def get_mode_button(self, name):
        return getattr(self, '%s_button' % name)

    def _update_mode_buttons(self, selected):
        if self.is_enabled():
            for name, entry in self._mode_map.items():
                self._get_mode_behaviour(name).update_button(self, name, selected)

    @cycle_mode_button.pressed
    def cycle_mode_button(self, button):
        if len(self._mode_list):
            self.cycle_mode(1)

    @cycle_mode_button.released_delayed
    def cycle_mode_button(self, button):
        if self._support_momentary_mode_cycling and len(self._mode_list) and (self.selected_mode != self._mode_list[0]):
            self.cycle_mode(-1)

    def _update_cycle_mode_button(self, selected):
        entry = self._mode_map.get(selected)
        color = entry.cycle_mode_button_color if entry else None
        if color is not None:
            self.cycle_mode_button.color = color

    def cycle_mode(self, delta=1):
        current_index = self._mode_list.index(self.selected_mode) if self.selected_mode else -delta
        current_index = (current_index + delta) % len(self._mode_list)
        self.selected_mode = self._mode_list[current_index]

    def _do_enter_mode(self, name):
        entry = self._mode_map[name]
        entry.mode.enter_mode()
        self._update_mode_buttons(name)
        self._update_cycle_mode_button(name)
        self.notify_selected_mode(name)

    def _do_leave_mode(self, name):
        self._mode_map[name].mode.leave_mode()
        if self._mode_stack.stack_size == 0:
            self._update_mode_buttons(None)
            self._update_cycle_mode_button(None)
            self.notify_selected_mode(None)
            return

    def on_enabled_changed(self):
        super(ModesComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = self.selected_mode
            self._mode_stack.release_all()
            return
        elif self._last_selected_mode:
            self.push_mode(self._last_selected_mode)
            return
        else:
            return None

class EnablingModesComponent(ModesComponent):
    pass
    pass
    pass
    pass

    def __init__(self, component=None, enabled_color='DefaultButton.On', disabled_color='DefaultButton.Off', *a, **k):
        super(EnablingModesComponent, self).__init__(*a, **k)
        component.set_enabled(False)
        self.add_mode('disabled', None, disabled_color)
        self.add_mode('enabled', component, enabled_color)
        self.selected_mode = 'disabled'