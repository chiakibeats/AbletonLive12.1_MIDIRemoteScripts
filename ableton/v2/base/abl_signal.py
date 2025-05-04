# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\abl_signal.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from .util import find_if, nop

def default_combiner(results):
    for _ in results:
        pass  # postinserted
class Slot(object):
    def __init__(self, callback=None, *a, **k):
        super(Slot, self).__init__(*a, **k)
        self.callback = callback

    def __call__(self, *a, **k):
        return self.callback(*a, **k)

    def __eq__(self, other):
        return id(self) == id(other) or self.callback == other

    def __hash__(self):
        return hash((self.callback,))

class IdentifyingSlot(Slot):
    def __init__(self, sender=None, *a, **k):
        super(IdentifyingSlot, self).__init__(*a, **k)
        self.sender = sender

    def __call__(self, *a, **k):
        self.callback(*a + (self.sender,), **k)

class Signal(object):
    pass

    def __init__(self, combiner=default_combiner, sender=None, *a, **k):
        super(Signal, self).__init__(*a, **k)
        self._slots = []
        self._combiner = combiner

    def connect(self, slot, in_front=False, sender=None):
        pass
        if slot not in self._slots:
            return IdentifyingSlot(sender, slot) if sender is None or None:
                pass  # postinserted
            else:  # inserted
                slot = Slot(slot)
            if in_front:
                self._slots.insert(0, slot)
            else:  # inserted
                self._slots.append(slot)
        else:  # inserted
            slot = find_if(lambda x: x == slot, self._slots)
        return slot

    def disconnect(self, slot):
        if slot in self._slots:
            self._slots.remove(slot)

    def disconnect_all(self):
        self._slots = []

    @property
    def count(self):
        return len(self._slots)

    def is_connected(self, slot):
        return slot in self._slots

    def __call__(self, *a, **k):
        return self._combiner(_slot_notification_generator(self._slots, a, k))

def _slot_notification_generator(slots, args, kws):
    for slot in slots:
        yield slot(*args, **kws)

def short_circuit_combiner(slot_results):
    return find_if(nop, slot_results)
short_circuit_signal = partial(Signal, short_circuit_combiner)