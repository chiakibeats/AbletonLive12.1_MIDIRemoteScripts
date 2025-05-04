# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\internal_parameter.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import EventError, EventObject, Proxy, Slot, clamp, forward_property, listenable_property, liveobj_valid, nop
from ableton.v2.control_surface import EnumWrappingParameter, InternalParameter, InternalParameterBase, RelativeInternalParameter, WrappingParameter, to_percentage_display

class ConstantParameter(InternalParameterBase):
    forward_from_original = forward_property('_original_parameter')

    def __init__(self, original_parameter=None, *a, **k):
        super(InternalParameterBase, self).__init__(*a, **k)
        self._original_parameter = original_parameter
    add_value_listener = forward_from_original('add_value_listener')
    remove_value_listener = forward_from_original('remove_value_listener')
    value_has_listener = forward_from_original('value_has_listener')
    canonical_parent = forward_from_original('canonical_parent')
    min = forward_from_original('min')
    max = forward_from_original('max')
    name = forward_from_original('name')
    original_name = forward_from_original('original_name')
    default_value = forward_from_original('default_value')
    automation_state = forward_from_original('automation_state')
    state = forward_from_original('state')
    _live_ptr = forward_from_original('_live_ptr')

    @property
    def display_value(self):
        return str(self._original_parameter)

    def _get_value(self):
        return self._original_parameter.value

    def _set_value(self, _):
        return
    value = property(_get_value, _set_value)
    linear_value = property(_get_value, _set_value)

    def __str__(self):
        return self.display_value

class ProxyParameter(Proxy):
    pass

    def __getattr__(self, name):
        if not self._skip_wrapper_lookup:
            obj = self.proxied_object
            return getattr(self.proxied_interface, name, getattr(obj, name))
        else:
            raise AttributeError('Does not have attribute %s' % name)

    def __unicode__(self):
        return str(self.proxied_object)

    def __str__(self):
        return str(self.proxied_object)

    def __eq__(self, other):
        if isinstance(other, ProxyParameter):
            return self.proxied_object == other.proxied_object and self.proxied_interface == other.proxied_interface
        else:
            return self.proxied_object == other

    def __ne__(self, other):
        if isinstance(other, ProxyParameter):
            return self.proxied_object != other.proxied_object or self.proxied_interface != other.proxied_interface
        else:
            return self.proxied_object != other

    def __hash__(self):
        return hash((self.proxied_object, self.proxied_interface))