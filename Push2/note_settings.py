# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\note_settings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from ableton.v2.base import listenable_property, listens
from ableton.v2.control_surface.control import StepEncoderControl
from ableton.v2.control_surface.elements.color import SelectedClipColor
from pushbase.note_settings_component import NoteSettingBase, NoteSettingsComponentBase, step_offset_percentage
from .colors import SelectedDrumPadColor

class NoteSetting(NoteSettingBase):

    def set_min_max(self, min_max_value):
        super(NoteSetting, self).set_min_max(min_max_value)
        self.notify_min()
        self.notify_max()

    @listenable_property
    def min(self):
        return self._get_min_max_value(0)

    @listenable_property
    def max(self):
        return self._get_min_max_value(1)

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    def transform_value(self, value):
        raise NotImplementedError

    def _get_min_max_value(self, index):
        value = self._min_max_value
        if value is not None:
            value = self.transform_value(self._min_max_value[index])
        return value

class NoteNudgeSetting(NoteSetting):
    attribute_index = 1

    def transform_value(self, value):
        return step_offset_percentage(self.step_length, value)

class NoteLengthCoarseSetting(NoteSetting):
    attribute_index = 2
    encoder = StepEncoderControl()

    def transform_value(self, value):
        return int(old_div(value, self.step_length))

    @encoder.value
    def encoder(self, value, _):
        self._on_encoder_value_changed(value)

class NoteLengthFineSetting(NoteSetting):
    attribute_index = 2

    def transform_value(self, value):
        return step_offset_percentage(self.step_length, value)

class NoteVelocitySetting(NoteSetting):
    attribute_index = 3

    def encoder_value_to_attribute(self, value):
        return value * 128

    def transform_value(self, value):
        return round(value)

class NoteVelocityDeviationSetting(NoteSetting):
    attribute_index = 4

    def encoder_value_to_attribute(self, value):
        return value * 128

    def transform_value(self, value):
        return round(value)

class NoteProbabilitySetting(NoteSetting):
    attribute_index = 5

    def encoder_value_to_attribute(self, value):
        return value * 128

    def transform_value(self, value):
        return round(value * 100)

class NoteSettingsComponent(NoteSettingsComponentBase):

    def __init__(self, *a, **k):
        super(NoteSettingsComponent, self).__init__(*a, **k)
        self._selected_drum_pad_color = self.register_disconnectable(SelectedDrumPadColor(song=self.song))
        self._selected_clip_color = self.register_disconnectable(SelectedClipColor(song_view=self.song.view))
        self._color = self._selected_clip_color
        self.__on_midi_value_changed.subject = self._color

    def _create_settings(self, grid_resolution):
        args = dict(grid_resolution=grid_resolution)
        self._nudge = NoteNudgeSetting(**args)
        self._coarse = NoteLengthCoarseSetting(**args)
        self._fine = NoteLengthFineSetting(**args)
        self._velocity = NoteVelocitySetting(**args)
        self._velocity_deviation = NoteVelocityDeviationSetting(**args)
        self._probability = NoteProbabilitySetting(**args)
        self._add_setting(self._nudge)
        self._add_setting(self._coarse)
        self._add_setting(self._fine)
        self._add_setting(self._velocity)
        if self.show_velocity_ranges_and_probabilities:
            self._add_setting(self._velocity_deviation)
            self._add_setting(self._probability)

    def set_color_mode(self, color_mode):
        self._color = self.get_color_for_mode(color_mode)
        self.__on_midi_value_changed.subject = self._color
        self.notify_color_index()

    def get_color_for_mode(self, color_mode):
        if color_mode == 'drum_pad':
            return self._selected_drum_pad_color
        elif color_mode == 'clip':
            return self._selected_clip_color
        else:
            return None

    @property
    def nudge(self):
        return self._nudge

    @property
    def coarse(self):
        return self._coarse

    @property
    def fine(self):
        return self._fine

    @property
    def velocity(self):
        return self._velocity

    @property
    def velocity_deviation(self):
        return self._velocity_deviation

    @property
    def probability(self):
        return self._probability

    @listenable_property
    def color_index(self):
        color_index = self._color.midi_value
        return color_index if color_index is not None else -1

    @listens('midi_value')
    def __on_midi_value_changed(self, *a):
        self.notify_color_index()