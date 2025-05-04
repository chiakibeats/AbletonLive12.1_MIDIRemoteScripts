# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\disconnectable.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .util import find_if

class Disconnectable(object):
    pass

    def disconnect(self):
        return

class CompoundDisconnectable(Disconnectable):
    pass

    def __init__(self, *a, **k):
        super(CompoundDisconnectable, self).__init__(*a, **k)
        self._registered_disconnectables = []

    def register_disconnectables(self, disconnectables):
        for disconnectable in disconnectables:
            self.register_disconnectable(disconnectable)
        return disconnectables

    def register_disconnectable(self, slot):
        if slot not in self._registered_disconnectables:
            self._registered_disconnectables.append(slot)
        return slot

    def unregister_disconnectable(self, slot):
        if slot in self._registered_disconnectables:
            self._registered_disconnectables.remove(slot)

    def disconnect_disconnectable(self, slot):
        if slot in self._registered_disconnectables:
            self._registered_disconnectables.remove(slot)
            slot.disconnect()

    def find_disconnectable(self, predicate):
        return find_if(predicate, self._registered_disconnectables)

    def has_disconnectable(self, slot):
        return slot in self._registered_disconnectables

    def disconnect(self):
        for slot in self._registered_disconnectables:
            slot.disconnect()
        self._registered_disconnectables = []
        super(CompoundDisconnectable, self).disconnect()

class disconnectable(object):
    pass

    def __init__(self, managed=None, *a, **k):
        super(disconnectable, self).__init__(*a, **k)
        self._managed = managed

    def __enter__(self):
        managed = self._managed
        return managed

    def __exit__(self, *a, **k):
        if self._managed is not None:
            self._managed.disconnect()