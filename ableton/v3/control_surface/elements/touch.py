# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\touch.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import listenable_property, listens
from ...live import song
from . import ButtonElement

class TouchElement(ButtonElement):
    pass
    __events__ = ('assignment',)

    def __init__(self, *a, encoder=None, **k):
        super().__init__(*a, **k)
        self.__on_parameter_changed.subject = encoder
        self.__on_parameter_name_changed.subject = encoder
        self.__on_parameter_value_changed.subject = encoder
        self._encoder = encoder

    @listenable_property
    def controlled_parameter(self):
        pass
        return self._encoder.mapped_object

    def receive_value(self, value):
        super().receive_value(value)
        if value:
            song().begin_undo_step()
        else:
            song().end_undo_step()

    @listens('parameter')
    def __on_parameter_changed(self):
        self.notify_assignment()

    @listens('parameter_name')
    def __on_parameter_name_changed(self):
        self.notify_controlled_parameter()

    @listens('parameter_value')
    def __on_parameter_value_changed(self):
        self.notify_controlled_parameter()