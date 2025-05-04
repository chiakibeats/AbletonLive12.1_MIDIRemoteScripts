# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\NotifyingControlElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .ControlElement import ControlElement
from .SubjectSlot import Subject, SubjectEvent

class NotifyingControlElement(Subject, ControlElement):
    pass
    __subject_events__ = (SubjectEvent(name='value', doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)