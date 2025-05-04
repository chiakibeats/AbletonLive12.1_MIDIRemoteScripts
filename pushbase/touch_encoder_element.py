# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\touch_encoder_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import TouchEncoderElement as TouchEncoderElementBase

class TouchEncoderObserver(object):
    pass

    def on_encoder_touch(self, encoder):
        return

    def on_encoder_parameter(self, encoder):
        return

class TouchEncoderElement(TouchEncoderElementBase):
    pass

    def __init__(self, undo_step_handler=None, delete_handler=None, *a, **k):
        super(TouchEncoderElement, self).__init__(*a, **k)
        self._trigger_undo_step = False
        self._undo_step_open = False
        self._undo_step_handler = undo_step_handler
        self._delete_handler = delete_handler
        self.set_observer(None)

    def set_observer(self, observer):
        if observer is None:
            observer = TouchEncoderObserver()
        self._observer = observer

    def on_nested_control_element_value(self, value, control):
        self._trigger_undo_step = value
        if value:
            param = self.mapped_parameter()
            if self._delete_handler and self._delete_handler.is_deleting and param:
                self._delete_handler.delete_clip_envelope(param)
                return
            else:
                self.begin_gesture()
                self._begin_undo_step()
                self._observer.on_encoder_touch(self)
                self.notify_touch_value(value)
                return
        else:
            self._end_undo_step()
            self._observer.on_encoder_touch(self)
            self.notify_touch_value(value)
            self.end_gesture()

    def connect_to(self, parameter):
        if parameter != self.mapped_parameter():
            self.last_mapped_parameter = parameter
            super(TouchEncoderElement, self).connect_to(parameter)
            self._observer.on_encoder_parameter(self)

    def release_parameter(self):
        if self.mapped_parameter() != None:
            super(TouchEncoderElement, self).release_parameter()
            self._observer.on_encoder_parameter(self)

    def receive_value(self, value):
        self._begin_undo_step()
        super(TouchEncoderElement, self).receive_value(value)

    def disconnect(self):
        super(TouchEncoderElement, self).disconnect()
        self._undo_step_handler = None

    def _begin_undo_step(self):
        if self._undo_step_handler and self._trigger_undo_step:
            self._undo_step_handler.begin_undo_step(client=self)
            self._trigger_undo_step = False
            self._undo_step_open = True

    def _end_undo_step(self):
        if self._undo_step_handler and self._undo_step_open:
            self._undo_step_handler.end_undo_step(client=self)