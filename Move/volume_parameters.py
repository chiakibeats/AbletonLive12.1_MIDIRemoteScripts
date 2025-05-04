# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\volume_parameters.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import liveobj_changed, liveobj_valid
from .control import ParameterControl
from .elements import ENCODER_SENSITIVITY

class VolumeParametersComponent(Component):
    pass
    volume_encoder = ParameterControl(default_sensitivity=ENCODER_SENSITIVITY)
    volume_encoder_touch_button = ButtonControl(color=None)

    def __init__(self, *a, **k):
        super().__init__(*a, name='Volume_Parameters', **k)
        self._parameters = {}
        self._parameters_pending_removal = []
        self._update_volume_encoder()

    @volume_encoder_touch_button.released
    def volume_encoder_touch_button(self, _):
        self._tasks.add(task.run(self._remove_pending_parameters))

    def add_parameter(self, control, parameter):
        pass
        if control in self._parameters_pending_removal:
            self._parameters_pending_removal.remove(control)
        if liveobj_valid(parameter):
            self._parameters[control] = parameter
            self._update_volume_encoder()
            return

    def remove_parameter(self, control, force=False):
        pass
        if not force and self.volume_encoder_touch_button.is_pressed:
            self._parameters_pending_removal.append(control)
            return
        elif control in self._parameters:
            del self._parameters[control]
            self._update_volume_encoder()
            return
        else:
            return None

    def _remove_pending_parameters(self):
        for control in set(self._parameters_pending_removal):
            if control in self._parameters:
                del self._parameters[control]
            pass
            continue
        self._parameters_pending_removal = []
        self._update_volume_encoder()

    def _update_volume_encoder(self):
        parameter = self.song.master_track.mixer_device.volume
        if self._parameters:
            possible_parameter = list(self._parameters.values())[-1]
            if liveobj_valid(possible_parameter):
                parameter = possible_parameter
        if liveobj_changed(parameter, self.volume_encoder.mapped_parameter):
            self.volume_encoder.mapped_parameter = parameter
            return