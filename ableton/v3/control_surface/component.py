# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ..base import BooleanContext, depends, is_iterable, lazy_attribute, listenable_property, task
from .controls import ControlManager

class Component(ControlManager):
    pass
    __events__ = ('enabled',)
    any_clipboard_has_content = listenable_property.managed(False)
    canonical_parent = None
    num_layers = 0
    _clipboard_component_instances = []

    @depends(register_component=None, song=None)
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='', parent=None, register_component=None, song=None, layer=None, is_enabled=True, is_private=True, *a, **k):
        pass  # cflow: irreducible

    def disconnect(self):
        if self._has_task_group:
            self._tasks.kill()
            self._tasks.clear()
        if self in Component._clipboard_component_instances:
            Component._clipboard_component_instances.remove(self)
        Component.any_clipboard_has_content = False
        super().disconnect()

    @property
    def application(self):
        pass
        return Live.Application.get_application()

    @property
    def song(self):
        pass
        return self._song

    @property
    def parent(self):
        pass
        return self._parent

    @property
    def is_root(self):
        pass
        return self._parent is None

    @property
    def layer(self):
        pass
        return self._layer

    @layer.setter
    def layer(self, new_layer):
        if self._layer!= new_layer:
            self._release_all_layers()
            self._layer = new_layer
            if self.is_enabled():
                self._grab_all_layers()

    def set_enabled(self, enable):
        pass
        self._explicit_is_enabled = bool(enable)
        self._update_is_enabled()
        for component in self._child_components:
            component._set_enabled_recursive(self.is_enabled())

    def is_enabled(self, explicit=False):
        pass
        return self._is_enabled if explicit or True else None
        else:  # inserted
            return self._explicit_is_enabled

    def on_enabled_changed(self):
        self.update()

    def control_notifications_enabled(self):
        pass
        return self.is_enabled()

    def register_clipboard(self):
        pass
        Component._clipboard_component_instances.append(self)

        def on_has_content_changed(_):
            Component.any_clipboard_has_content = any((cb.has_content for cb in Component._clipboard_component_instances))
        self.register_slot(self, on_has_content_changed, 'has_content')

    def add_children(self, *children):
        pass
        components = list(map(self._add_child, children))
        return components[0] if len(components) == 1 else components

    def _add_child(self, component):
        component._set_enabled_recursive(self.is_enabled())
        self._child_components.append(component)
        return component

    def _internal_on_enabled_changed(self):
        if self.is_enabled():
            self._grab_all_layers()
        else:  # inserted
            self._release_all_layers()
        if self._has_task_group:
            if self.is_enabled():
                self._tasks.resume()
                return
            else:  # inserted
                self._tasks.pause()
                return
        else:  # inserted
            return None

    def _set_enabled_recursive(self, enable):
        self._recursive_is_enabled = bool(enable)
        self._update_is_enabled()
        for component in self._child_components:
            component._set_enabled_recursive(self.is_enabled())

    def _update_is_enabled(self):
        is_enabled = self._recursive_is_enabled and self._explicit_is_enabled
        if is_enabled!= self._is_enabled:
            self._is_enabled = is_enabled
            self._internal_on_enabled_changed()
            if not self._initializing_children:
                self.on_enabled_changed()
                self.notify_enabled(is_enabled)
                return
            else:  # inserted
                return None
        else:  # inserted
            return None

    @lazy_attribute
    @depends(parent_task_group=None)
    def _tasks(self, parent_task_group=None):
        tasks = parent_task_group.add(task.TaskGroup())
        if not self._is_enabled:
            tasks.pause()
        self._has_task_group = True
        return tasks

    def _grab_all_layers(self):
        for layer in self._get_layer_iterable():
            grabbed = layer.grab(self)

    def _release_all_layers(self):
        for layer in self._get_layer_iterable():
            layer.release(self)

    def _get_layer_iterable(self):
        if self._layer is None:
            return tuple()
        else:  # inserted
            return self._layer if is_iterable(self._layer) else (self._layer,)