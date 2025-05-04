# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\sliced_simpler_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import NamedTuple, listenable_property, listens, liveobj_valid, task
from ableton.v2.control_surface.components import PlayableComponent, Slideable, SlideComponent
from ableton.v2.control_surface.control import ButtonControl
from .consts import DISTANT_FUTURE, MessageBoxText
from .instrument_component import SelectedNotesProvider
from .matrix_maps import PAD_FEEDBACK_CHANNEL
from .message_box_component import Messenger
from .slideable_touch_strip_component import SlideableTouchStripComponent
BASE_SLICING_NOTE = 36
MAX_NUMBER_SLICES = 64

class NullQuantizer(object):
    def quantize_pitch(self, _pitch, _source=None):
        return

class SlicedSimplerComponent(PlayableComponent, SlideableTouchStripComponent, SlideComponent, Slideable, Messenger):
    delete_button = ButtonControl()
    quantize_button = ButtonControl()
    position_count = 16
    page_length = 4
    page_offset = 0

    def __init__(self, quantizer=None, *a, **k):
        self._position = 0
        super(SlicedSimplerComponent, self).__init__(*a, touch_slideable=self, dragging_enabled=True, **k)
        self._simpler = None
        self._quantizer = quantizer or NullQuantizer()
        self.selected_notes_provider = self.register_disconnectable(SelectedNotesProvider())

    def _get_position(self):
        return self._position

    def _set_position(self, index):
        self._position = index
        self.notify_position()
        self._update_led_feedback()
        self._update_note_translations()
        self.notify_selected_target_note()
    position = property(_get_position, _set_position)

    @property
    def min_pitch(self):
        return BASE_SLICING_NOTE + self.position * self.page_length

    @property
    def max_pitch(self):
        return BASE_SLICING_NOTE + self._coordinate_to_slice_index((0, self.width - 1))

    def set_simpler(self, simpler):
        self._simpler = simpler
        self.__on_selected_slice_changed.subject = simpler
        self.__on_file_changed.subject = simpler
        self.__on_slices_changed.subject = simpler.sample if liveobj_valid(simpler) else None
        self.__on_pad_slicing_changed.subject = simpler
        self.__on_slicing_style_changed.subject = simpler.sample if liveobj_valid(simpler) else None
        self.__on_track_color_changed.subject = self.song.view.selected_track if simpler else None
        self._update_led_feedback()
        self.update()
        self.notify_selected_target_note()

    def set_matrix(self, matrix):
        super(SlicedSimplerComponent, self).set_matrix(matrix)
        self.notify_selected_target_note()

    def update(self):
        super(SlicedSimplerComponent, self).update()
        if self.is_enabled():
            self.notify_position()

    @listens('color_index')
    def __on_track_color_changed(self):
        self._update_led_feedback()

    @listens('slices')
    def __on_slices_changed(self):
        self._update_led_feedback()

    @listens('view.selected_slice')
    def __on_selected_slice_changed(self):
        self._update_led_feedback()
        self.selected_notes_provider.selected_notes = self._get_selected_note()
        self.notify_selected_target_note()

    @listens('pad_slicing')
    def __on_pad_slicing_changed(self):
        self._update_led_feedback()

    @listens('slicing_style')
    def __on_slicing_style_changed(self):
        def set_pad_slicing():
            self._simpler.pad_slicing = self._simpler.sample.slicing_style == Live.Sample.SlicingStyle.manual
        self._tasks.add(task.sequence(task.delay(1), task.run(set_pad_slicing)))

    def _slices(self):
        return self._simpler.sample.slices if liveobj_valid(self._simpler) and liveobj_valid(self._simpler.sample) else []

    def _get_selected_note(self):
        slices = list(self._slices())
        selected_slice = self._selected_slice()
        index = slices.index(selected_slice) if selected_slice in slices else 0
        return [BASE_SLICING_NOTE + index]

    @listenable_property
    def selected_target_note(self):
        slices = list(self._slices())
        selected_slice = self._selected_slice()
        return NamedTuple(note=BASE_SLICING_NOTE + slices.index(selected_slice), channel=PAD_FEEDBACK_CHANNEL) if selected_slice in slices else NamedTuple(note=(-1), channel=(-1))

    def _selected_slice(self):
        return self._simpler.view.selected_slice if liveobj_valid(self._simpler) and liveobj_valid(self._simpler.sample) else (-1)

    @listens('sample')
    def __on_file_changed(self):
        return self._simpler.sample if liveobj_valid(self._simpler) else None
        else:  # inserted
            self.__on_slices_changed.subject = None
        self._update_led_feedback()
        self.notify_selected_target_note()

    def _coordinate_to_slice_index(self, coordinate):
        y, x = coordinate
        y = self.height - y - 1
        y += self._position
        y += self.height if x >= 4 else 0
        return x % 4 + y * 4

    def _update_button_color(self, button):
        index = self._coordinate_to_slice_index(button.coordinate)
        slices = self._slices()
        length_of_slices = len(slices)
        if index < length_of_slices:
            button.color = 'SlicedSimpler.SliceSelected' if slices[index] == self._selected_slice() else 'SlicedSimpler.SliceUnselected'
            return
        else:  # inserted
            if self._should_show_next_slice(index, length_of_slices):
                button.color = self._next_slice_color()
            else:  # inserted
                button.color = 'SlicedSimpler.NoSlice'

    def _note_translation_for_button(self, button):
        identifier = BASE_SLICING_NOTE + self._coordinate_to_slice_index(button.coordinate)
        return (identifier, PAD_FEEDBACK_CHANNEL)

    def _next_slice_color(self):
        return 'SlicedSimpler.NextSlice'

    def _should_show_next_slice(self, index, length_of_slices):
        return index == length_of_slices and liveobj_valid(self._simpler) and self._simpler.pad_slicing and liveobj_valid(self._simpler.sample) and (self._simpler.sample.slicing_style == Live.Sample.SlicingStyle.manual)

    @delete_button.value
    def delete_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    def _try_delete_notes_for_slice(self, index):
        clip = self.song.view.detail_clip
        pitch = BASE_SLICING_NOTE + index
        has_notes = liveobj_valid(clip) and (not clip.is_audio_clip) and (len(clip.get_notes_extended(from_time=0, from_pitch=pitch, time_span=DISTANT_FUTURE, pitch_span=1)) > 0)
        if has_notes:
            clip.remove_notes_extended(from_time=0, from_pitch=pitch, time_span=DISTANT_FUTURE, pitch_span=1)
            slice_label = 'Slice %d' % (index + 1)
            self.show_notification(MessageBoxText.DELETE_NOTES % slice_label)
        return has_notes

    def _try_delete_slice_at_index(self, index):
        slices = self._slices()
        if len(slices) > index:
            self._simpler.sample.remove_slice(slices[index])
            self.show_notification(MessageBoxText.DELETE_SLICE % str(index + 1))

    def set_select_button(self, button):
        self.select_button.set_control_element(button)

    def _try_select_slice_at_index(self, index):
        slices = self._slices()
        if len(slices) > index:
            self._simpler.view.selected_slice = slices[index]

    @quantize_button.value
    def quantize_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    def _try_quantize_notes_for_slice(self, index):
        self._quantizer.quantize_pitch(BASE_SLICING_NOTE + index, 'slice')

    def _on_matrix_pressed(self, button):
        if liveobj_valid(self._simpler) and liveobj_valid(self._simpler.sample):
            slice_index = self._coordinate_to_slice_index(button.coordinate)
            if self.delete_button.is_pressed:
                if not self._try_delete_notes_for_slice(slice_index):
                    self._try_delete_slice_at_index(slice_index)
                pass
            else:  # inserted
                if self.quantize_button.is_pressed:
                    self._try_quantize_notes_for_slice(slice_index)
                else:  # inserted
                    if self.select_button.is_pressed:
                        self._try_select_slice_at_index(slice_index)
        super(SlicedSimplerComponent, self)._on_matrix_pressed(button)