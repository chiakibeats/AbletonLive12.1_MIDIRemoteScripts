# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Layer.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from itertools import repeat
from .ControlElement import ControlElementClient
from .Disconnectable import Disconnectable
from .Resource import CompoundResource, ExclusiveResource
from .Util import nop

class LayerError(Exception):
    pass

class UnhandledControlError(LayerError):
    pass

class SimpleLayerOwner(Disconnectable):
    pass

    def __init__(self, layer=None):
        self._layer = layer
        self._layer.grab(self)

    def disconnect(self):
        self._layer.release(self)

class LayerClient(ControlElementClient):
    pass

    def __init__(self, layer=None, layer_client=None, *a, **k):
        super(LayerClient, self).__init__(*a, **k)
        self.layer_client = layer_client
        self.layer = layer

    def set_control_element(self, control_element, grabbed):
        layer = self.layer
        owner = self.layer_client
        names = layer._control_to_names[control_element]
        if not grabbed:
            control_element = None
        for name in names:
            try:
                handler = getattr(owner, 'set_' + name)
            except AttributeError:
                try:
                    control = getattr(owner, name)
                    handler = control.set_control_element
                except AttributeError:
                    if name[0] != '_':
                        raise UnhandledControlError('Component %s has no handler for control_element %s' % (str(owner), name))
                    handler = nop
            handler(control_element or None)
            layer._name_to_controls[name] = control_element
            continue

class LayerBase(object):
    pass

class CompoundLayer(LayerBase, CompoundResource):
    pass

    def _get_priority(self):
        return self.first.priority

    def _set_priority(self, priority):
        self.first.priority = priority
        self.second.priority = priority
    priority = property(_get_priority, _set_priority)

    def __getattr__(self, key):
        try:
            return getattr(self.first, key)
        except AttributeError:
            return getattr(self.second, key)

class Layer(LayerBase, ExclusiveResource):
    pass

    def __init__(self, priority=None, **controls):
        super(Layer, self).__init__()
        self._priority = priority
        self._name_to_controls = dict(zip(iter(controls.keys()), repeat(None)))
        self._control_to_names = dict()
        self._control_clients = dict()
        for name, control in controls.items():
            self._control_to_names.setdefault(control, []).append(name)

    def __add__(self, other):
        return CompoundLayer(self, other)

    def _get_priority(self):
        return self._priority

    def _set_priority(self, priority):
        if priority != self._priority:
            if self.owner:
                raise RuntimeError("Cannot change priority of a layer while it's owned")
            else:
                self._priority = priority
    priority = property(_get_priority, _set_priority)

    def __getattr__(self, name):
        pass
        try:
            return self._name_to_controls[name]
        except KeyError:
            raise AttributeError

    def grab(self, client, *a, **k):
        if client == self.owner:
            self.on_received(client, *a, **k)
            return True
        else:
            return super(Layer, self).grab(client, *a, **k)

    def on_received(self, client, *a, **k):
        pass
        for control in self._control_to_names.keys():
            k.setdefault('priority', self._priority)
            control.resource.grab(self._get_control_client(client), *a, **k)

    def on_lost(self, client):
        pass
        for control in self._control_to_names.keys():
            control.resource.release(self._get_control_client(client))

    def _get_control_client(self, client):
        try:
            control_client = self._control_clients[client]
        except KeyError:
            control_client = self._control_clients[client] = LayerClient(layer_client=client, layer=self)
        return control_client