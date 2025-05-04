# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\compound_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from collections import OrderedDict
from ..base import BooleanContext, first, listens_group, second
from .control_element import ControlElementClient, NotifyingControlElement

class NestedElementClient(ControlElementClient):
    def __init__(self, compound=None, client=None, **k):
        super(NestedElementClient, self).__init__(**k)
        self.compound = compound
        self.client = client

    def set_control_element(self, element, grabbed):
        self.compound.set_control_element(element, grabbed)

class CompoundElement(NotifyingControlElement, ControlElementClient):
    pass
    _is_resource_based = False

    def __init__(self, control_elements=None, *a, **k):
        super(CompoundElement, self).__init__(*a, **k)
        resource = self.resource
        original_grab_resource = resource.grab
        original_release_resource = resource.release

        def grab_resource(client, **k):
            self._grab_nested_control_elements(client, **k)
            original_grab_resource(client, **k)

        def release_resource(client):
            original_release_resource(client)
            self._release_nested_control_elements(client)
        self.resource.grab = grab_resource
        self.resource.release = release_resource
        self._nested_control_elements = OrderedDict()
        self._nested_element_clients = dict()
        self._disable_notify_owner_on_button_ownership_change = BooleanContext()
        self._listen_nested_requests = 0
        if control_elements is not None:
            self.register_control_elements(*control_elements)

    def on_nested_control_element_received(self, control):
        pass
        return

    def on_nested_control_element_lost(self, control):
        pass
        return

    def on_nested_control_element_value(self, value, control):
        pass
        self.notify_value(value, control)

    def get_control_element_priority(self, element, priority):
        pass
        return priority

    def register_control_elements(self, *elements):
        return list(map(self.register_control_element, elements))

    def register_control_element(self, element):
        pass  # cflow: irreducible

    def unregister_control_elements(self, *elements):
        return list(map(self.unregister_control_element, elements))

    def unregister_control_element(self, element):
        pass  # cflow: irreducible

    def has_control_element(self, control):
        return control in self._nested_control_elements

    def owns_control_element(self, control):
        return self._nested_control_elements.get(control, False)

    def owned_control_elements(self):
        return list(map(first, filter(second, self._nested_control_elements.items())))

    def nested_control_elements(self):
        return [key for key in self._nested_control_elements]

    def reset(self):
        for element in self.owned_control_elements():
            element.reset()

    def reset_state(self):
        for element in self.owned_control_elements():
            element.reset_state()

    def add_value_listener(self, *a, **k):
        if self.value_listener_count() == 0:
            self.request_listen_nested_control_elements()
        super(CompoundElement, self).add_value_listener(*a, **k)

    def remove_value_listener(self, *a, **k):
        super(CompoundElement, self).remove_value_listener(*a, **k)
        if self.value_listener_count() == 0:
            self.unrequest_listen_nested_control_elements()

    def request_listen_nested_control_elements(self):
        pass
        if self._listen_nested_requests == 0:
            self._connect_nested_control_elements()
        self._listen_nested_requests += 1

    def unrequest_listen_nested_control_elements(self):
        pass
        if self._listen_nested_requests == 1:
            self._disconnect_nested_control_elements()
        self._listen_nested_requests -= 1

    def _connect_nested_control_elements(self):
        self.__on_nested_control_element_value.replace_subjects(list(self._nested_control_elements.keys()))

    def _disconnect_nested_control_elements(self):
        self.__on_nested_control_element_value.replace_subjects([])

    def _on_nested_control_element_received(self, control):
        if control in self._nested_control_elements and (not self._nested_control_elements[control]):
            self._nested_control_elements[control] = True
        self.on_nested_control_element_received(control)

    def _on_nested_control_element_lost(self, control):
        if control in self._nested_control_elements and self._nested_control_elements[control]:
            self._nested_control_elements[control] = False
        self.on_nested_control_element_lost(control)

    @listens_group('value')
    def __on_nested_control_element_value(self, value, sender):
        if self.owns_control_element(sender):
            self.on_nested_control_element_value(value, sender)

    def set_control_element(self, control, grabbed):
        if grabbed:
            self._on_nested_control_element_received(control)
        else:  # inserted
            self._on_nested_control_element_lost(control)
        owner = self._resource.owner
        if not owner or not self._disable_notify_owner_on_button_ownership_change:
                self.notify_ownership_change(owner, True)
                return
        else:  # inserted
            return

    def _grab_nested_control_elements(self, client, priority=None, **k):
        pass  # cflow: irreducible

    def _release_nested_control_elements(self, client):
        pass  # cflow: irreducible

    def _get_nested_client(self, client):
        try:
            nested_client = self._nested_element_clients[client]
        except KeyError:
            nested_client = self._nested_element_clients[client] = NestedElementClient(self, client)
        return nested_client

    def __len__(self):
        return len(self._nested_control_elements)

    def __iter__(self):
        for element, owned in self._nested_control_elements.items():
            return element if owned else None
            else:  # inserted
                yield
            continue

    def __getitem__(self, index_or_slice):
        if isinstance(index_or_slice, slice):
            items = list(self._nested_control_elements.items())[index_or_slice]
            return [element if owned else None for element, owned in items]
        else:  # inserted
            element, owned = list(self._nested_control_elements.items())[index_or_slice]
            return element if owned else None