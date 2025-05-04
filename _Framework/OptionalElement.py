# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\OptionalElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .ComboElement import ToggleElement
from .SubjectSlot import SlotManager, subject_slot

class ChoosingElement(ToggleElement, SlotManager):
    pass

    def __init__(self, flag=None, *a, **k):
        super(ChoosingElement, self).__init__(*a, **k)
        self._on_flag_changed.subject = flag
        self._on_flag_changed(flag.value)

    @subject_slot('value')
    def _on_flag_changed(self, value):
        self.set_toggled(value)

class OptionalElement(ChoosingElement):
    pass

    def __init__(self, control=None, flag=None, value=None, *a, **k):
        on_control = control if value else None
        off_control = None if value else control
        super(OptionalElement, self).__init__(*a, on_control=on_control, off_control=off_control, flag=flag, **k)