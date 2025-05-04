# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\clip_actions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from Live.Song import RecordingQuantization
from ableton.v3.base import EventObject, depends, listenable_property
from ableton.v3.control_surface.components import ClipActionsComponent as ClipActionsComponentBase
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import action
from .step_sequence import GRID_RESOLUTIONS
QUANTIZATION_MAP = {resolution.step_length: (quantization, resolution.name) for resolution, quantization in zip(GRID_RESOLUTIONS, (RecordingQuantization.rec_q_eight_triplet, RecordingQuantization.rec_q_sixtenth, RecordingQuantization.rec_q_sixtenth_triplet, RecordingQuantization.rec_q_thirtysecond, '1/32t'))}

class QuantizationStrength(EventObject):
    pass
    value = listenable_property.managed(0.4)

    def __init__(self, preferences=None, *a, **k):
        super().__init__(*a, **k)
        self._preferences = preferences if preferences is not None else {}
        self.value = self._preferences.setdefault('quantization_strength', self.value)

    @property
    def index(self):
        pass
        return round(self.value / 0.1) - 1

    @index.setter
    def index(self, index):
        self.value = (index + 1) * 0.1
        self._preferences['quantization_strength'] = self.value

class ClipActionsComponent(ClipActionsComponentBase):
    pass
    delete_button = ButtonControl(color=None)
    duplicate_button = ButtonControl(color=None)

    @depends(sequencer_clip=None, quantization_strength=None, grid_resolution=None)
    pass
    pass
    pass
    def __init__(self, sequencer_clip=None, quantization_strength=None, grid_resolution=None, *a, **k):
        self._sequencer_clip = sequencer_clip
        super().__init__(*a, **k)
        self._quantization_strength = quantization_strength
        self._quantization_settings = lambda: (QUANTIZATION_MAP[grid_resolution.step_length][0], quantization_strength.value)
        self.register_slot(sequencer_clip, self._update_double_button, 'length')

    @property
    def quantization_strength(self):
        pass
        return self._quantization_strength

    @delete_button.released_immediately
    def delete_button(self, _):
        clip = self._target_track.target_clip
        if action.delete(clip):
            self.notify(self.notifications.Clip.delete, 'Clip')
            return
        else:  # inserted
            self.notify(self.notifications.Clip.error_delete_empty_slot)

    @duplicate_button.released_immediately
    def duplicate_button(self, _):
        if not self.any_clipboard_has_content:
            clip = self._target_track.target_clip
            if action.duplicate_clip_special(clip):
                self.notify(self.notifications.Clip.duplicate, 'Clip')

    def _quantize_clip(self, clip):
        resolution, strength = self._quantization_settings()
        if isinstance(resolution, str):
            self.notify(self.notifications.Clip.error_quantize_invalid_resolution, resolution)
            return
        else:  # inserted
            clip.quantize(resolution, strength)
            self.notify(self.notifications.Clip.quantize, 'Clip', int(strength * 100))

    def _update_delete_button(self):
        return

    def _update_duplicate_button(self):
        return