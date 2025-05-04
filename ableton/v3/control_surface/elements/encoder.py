# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\encoder.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import EncoderElement as EncoderElementBase
from ableton.v2.control_surface.elements.encoder import _map_modes
from ...base import lazy_attribute, listenable_property, listens, task
from ...live import display_name, liveobj_valid, parameter_value_to_midi_value
from .. import MIDI_CC_TYPE
from ..controls import is_internal_parameter
from ..display import Renderable
from ..parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, FINE_GRAIN_SENSITIVITY_FACTOR

class MappingSensitivity:
    pass

    def __init__(self, standard, parent):
        fine_grain = standard * FINE_GRAIN_SENSITIVITY_FACTOR
        self._standard = standard
        self._fine_grain = fine_grain
        self._use_fine_grain = False
        self._parent = parent
        self._parent.set_sensitivities = self._set_sensitivities
        self._default_encoder_sensitivity = parent.encoder_sensitivity
        self.reset = lambda: self._set_sensitivities(standard, fine_grain)
        self._update_sensitivity()

    def should_use_fine_grain(self, use_fine_grain):
        pass
        self._use_fine_grain = use_fine_grain
        self._update_sensitivity()

    def _set_sensitivities(self, standard, fine_grain):
        self._standard = standard
        self._fine_grain = fine_grain
        self._update_sensitivity()

    def _update_sensitivity(self):
        sensitivity = self._fine_grain if self._use_fine_grain else self._standard
        setattr(self._parent, 'mapping_sensitivity', sensitivity)
        if self._parent.is_mapped_to_parameter():
            self._parent.encoder_sensitivity = sensitivity
        else:  # inserted
            self._parent.encoder_sensitivity = self._default_encoder_sensitivity

class EncoderElement(EncoderElementBase, Renderable):
    pass
    mapped_object = listenable_property.managed(None)

    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, map_mode=_map_modes.absolute, mapping_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, sensitivity_modifier=None, needs_takeover=True, is_feedback_enabled=False, feedback_delay=0, *a, **k):
        super().__init__(msg_type, channel, identifier, map_mode, *a, is_feedback_enabled=is_feedback_enabled, **k)
        self._needs_internal_parameter_feedback_delay = feedback_delay >= 0
        self._block_internal_parameter_feedback = False
        self._sensitivity = MappingSensitivity(mapping_sensitivity, self)
        self._sensitivity_modifier = sensitivity_modifier
        self.__on_sensitivity_modifier_value.subject = sensitivity_modifier
        self.set_needs_takeover(needs_takeover)
        self.set_feedback_delay(feedback_delay)
        self._feedback_values = self._mapping_feedback_values()
        self._update_listeners_task = self._tasks.add(task.run(self._update_parameter_listeners))
        self._update_listeners_task.kill()

    def disconnect(self):
        self.mapped_object = None
        super().disconnect()

    @listenable_property
    def parameter(self):
        pass
        return self._parameter_to_map_to if liveobj_valid(self._parameter_to_map_to) and (not self.is_mapped_manually()) else None
        else:  # inserted
            return None

    @listenable_property
    def parameter_name(self):
        pass
        return display_name(self.mapped_object) if self.is_mapped_to_parameter() else ''

    @listenable_property
    def parameter_value(self):
        pass
        return str(self.mapped_object) if self.mapped_object else ''

    def message_map_mode(self):
        pass
        return self._map_mode

    def reset_state(self):
        pass
        self._sensitivity.reset()
        super().reset_state()

    def is_mapped_to_parameter(self):
        pass
        return liveobj_valid(self.mapped_object) and (not self.is_mapped_manually())

    def is_mapped_manually(self):
        pass
        return not self._is_mapped and (not self._is_being_forwarded)

    def install_connections(self, *a, **k):
        super().install_connections(*a, **k)
        if self.is_mapped_manually():
            self.mapped_object = None
        else:  # inserted
            if self.mapped_object is None:
                self.reset()
        self._clear_parameter_listeners()
        self._update_listeners_task.restart()

    def connect_to(self, parameter):
        self.mapped_object = parameter
        if not is_internal_parameter(parameter):
            super().connect_to(parameter)
        self._clear_parameter_listeners()
        self._update_listeners_task.restart()

    def release_parameter(self):
        super().release_parameter()
        self.mapped_object = None
        self._update_listeners_task.restart()

    def receive_value(self, value):
        super().receive_value(value)
        if self._needs_internal_parameter_feedback_delay:
            self._block_internal_parameter_feedback = True
            self._unblock_internal_parameter_feedback_task.restart()

    def _parameter_value_changed(self):
        if not is_internal_parameter(self.mapped_object) or not self._block_internal_parameter_feedback:
                midi_value = parameter_value_to_midi_value(self.mapped_object, max_value=self._max_value)
                if len(self._feedback_values) > midi_value:
                    midi_value = self._feedback_values[midi_value]
                    if isinstance(midi_value, tuple):
                        midi_value = midi_value[0] + (midi_value[1] << 7)
                self.send_value(midi_value)
                return

    def _clear_parameter_listeners(self):
        self.__on_parameter_name_changed.subject = None
        self.__on_parameter_value_changed.subject = None

    def _update_parameter_listeners(self):
        self.__on_parameter_name_changed.subject = self.mapped_object
        self.__on_parameter_value_changed.subject = self.mapped_object
        self.__on_parameter_name_changed()
        self.__on_parameter_value_changed()
        self.notify_parameter()

    def _unblock_internal_parameter_feedback(self):
        self._block_internal_parameter_feedback = False
        self._parameter_value_changed()

    @lazy_attribute
    def _unblock_internal_parameter_feedback_task(self):
        unblocking_task = self._tasks.add(task.sequence(task.wait(self._mapping_feedback_delay / 10), task.run(self._unblock_internal_parameter_feedback)))
        unblocking_task.kill()
        return unblocking_task

    @listens('name')
    def __on_parameter_name_changed(self):
        self.notify_parameter_name()

    @listens('value')
    def __on_parameter_value_changed(self):
        self.notify_parameter_value()
        self._parameter_value_changed()

    @listens('value')
    def __on_sensitivity_modifier_value(self, _):
        self._set_sensitivity(self._sensitivity_modifier.is_pressed)

    def _set_sensitivity(self, use_fine_grain):
        self._sensitivity.should_use_fine_grain(use_fine_grain)