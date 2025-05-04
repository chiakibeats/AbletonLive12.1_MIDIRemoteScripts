# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ..base import BooleanContext, depends, is_iterable, lazy_attribute, task
from .control import ControlManager

class Component(ControlManager):
    pass
    __events__ = ('enabled',)
    name = ''
    canonical_parent = None
    is_private = False
    _has_task_group = False
    _layer = None

    @depends(register_component=None, song=None)
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='', parent=None, register_component=None, song=None, layer=None, is_enabled=True, *a, **k):
        pass  # cflow: irreducible

    def disconnect(self):
        if self._has_task_group:
            self._tasks.kill()
            self._tasks.clear()
        super(Component, self).disconnect()

    @property
    def parent(self):
        return self._parent

    @property
    def is_root(self):
        return self._parent is None

    def add_children(self, *a):
        components = list(map(self._add_child, a))
        return components[0] if len(components) == 1 else components

    def set_enabled(self, enable):
        self._explicit_is_enabled = bool(enable)
        self._update_is_enabled()
        for component in self._child_components:
            component._set_enabled_recursive(self.is_enabled())

    def is_enabled(self, explicit=False):
        pass
        return self._is_enabled if not explicit else self._explicit_is_enabled

    def on_enabled_changed(self):
        self.update()

    def control_notifications_enabled(self):
        return self.is_enabled()

    @property
    def application(self):
        return Live.Application.get_application()

    @property
    def song(self):
        return self._song

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, new_layer):
        if self._layer!= new_layer:
            self._release_all_layers()
            self._layer = new_layer
            if self.is_enabled():
                self._grab_all_layers()

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