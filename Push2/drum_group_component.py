# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\drum_group_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import EventObject, flatten, listenable_property, listens, listens_group, liveobj_valid, old_hasattr
from ableton.v2.control_surface import find_instrument_devices
from ableton.v2.control_surface.control import ButtonControl
from pushbase.drum_group_component import DrumGroupComponent as DrumGroupComponentBase
from pushbase.drum_group_component import DrumPadCopyHandler as DrumPadCopyHandlerBase
from pushbase.song_utils import find_parent_track
from .colors import IndexedColor
from .decoration import find_decorated_object
from .device_decoration import SimplerDecoratedPropertiesCopier

def find_simplers(chain):
    return list(filter(lambda i: old_hasattr(i, 'playback_mode'), find_instrument_devices(chain)))

def find_all_simplers_on_pad(drum_pad):
    simplers = []
    for chain in drum_pad.chains:
        simplers.append(find_simplers(chain))
    return list(flatten(simplers))

class DrumPadCopyHandler(DrumPadCopyHandlerBase):

    def __init__(self, decorator_factory=None, song=None, *a, **k):
        super(DrumPadCopyHandler, self).__init__(*a, **k)
        self._song = song
        self._decorator_factory = decorator_factory

    def _finish_copying(self, drum_group_device, destination_pad):
        notification_reference = super(DrumPadCopyHandler, self)._finish_copying(drum_group_device, destination_pad)
        if self._source_pad.note != destination_pad.note and len(destination_pad.chains) > 0:
            source_simplers = find_all_simplers_on_pad(self._source_pad)
            destination_simplers = find_all_simplers_on_pad(destination_pad)
            for source, destination in zip(source_simplers, destination_simplers):
                decorated = find_decorated_object(source, self._decorator_factory)
                if decorated:
                    self._copy_simpler_properties(decorated, destination)
                continue
        return notification_reference

    def _copy_simpler_properties(self, source_simpler, destination_simpler):
        copier = SimplerDecoratedPropertiesCopier(source_simpler, self._decorator_factory)
        copier.apply_properties(destination_simpler, song=self._song)

class DrumPadColorAdapter(object):
    pass

    def __init__(self, drum_pad=None, *a, **k):
        super(DrumPadColorAdapter, self).__init__(*a, **k)
        self._drum_pad = drum_pad

    @property
    def name(self):
        return self._drum_pad.name

    @property
    def color_index(self):
        if self._drum_pad.chains:
            return self._drum_pad.chains[0].color_index
        else:
            return None

    @color_index.setter
    def color_index(self, color_index):
        for chain in self._drum_pad.chains:
            chain.color_index = color_index

    @property
    def is_auto_colored(self):
        if self._drum_pad.chains:
            return self._drum_pad.chains[0].is_auto_colored
        else:
            return None

    @is_auto_colored.setter
    def is_auto_colored(self, is_auto_colored):
        for chain in self._drum_pad.chains:
            chain.is_auto_colored = is_auto_colored

class DrumPadColorNotifier(EventObject):
    _drum_group = None

    @property
    def has_drum_group(self):
        return liveobj_valid(self._drum_group)

    def set_drum_group(self, drum_group):
        self._drum_group = drum_group
        self._update_drum_group_listeners()
        self.notify_note_colors()

    @listens_group('chains')
    def __on_drum_pad_chains_changed(self, pad):
        self._update_drum_group_listeners()
        self.notify_note_colors()

    @listens_group('color_index')
    def __on_chain_color_index_changed(self, pad):
        self.notify_note_colors()

    @listenable_property
    def note_colors(self):

        def get_track_color_index():
            parent_track = find_parent_track(self._drum_group)
            return parent_track.color_index if liveobj_valid(parent_track) else -1
        colors = [-1] * 128
        if self.has_drum_group:
            track_color_index = None
            for pad in self._drum_group.drum_pads:
                if pad.chains and liveobj_valid(pad.chains[0]):
                    colors[pad.note] = pad.chains[0].color_index
                    continue
                else:
                    if track_color_index is None:
                        track_color_index = get_track_color_index()
                    colors[pad.note] = track_color_index
                    continue
        return colors

    def _update_drum_group_listeners(self):
        chains = []
        pads = []
        if self.has_drum_group:
            chains = [pad.chains[0] for pad in self._drum_group.drum_pads if pad.chains and liveobj_valid(pad.chains[0])]
            pads = self._drum_group.drum_pads
        self.__on_chain_color_index_changed.replace_subjects(chains)
        self.__on_drum_pad_chains_changed.replace_subjects(pads)

class DrumGroupComponent(DrumGroupComponentBase):
    __events__ = ('mute_solo_stop_cancel_action_performed',)
    select_color_button = ButtonControl()
    pass
    pass
    pass

    def __init__(self, tracks_provider=None, device_decorator_factory=None, color_chooser=None, *a, **k):
        self._decorator_factory = device_decorator_factory
        super(DrumGroupComponent, self).__init__(*a, **k)
        self.mute_button.color = 'DefaultButton.Transparent'
        self.solo_button.color = 'DefaultButton.Transparent'
        self._tracks_provider = tracks_provider
        self._hotswap_indication_mode = None
        self._color_chooser = color_chooser
        self._drum_pad_color_notifier = self.register_disconnectable(DrumPadColorNotifier())
        self.__on_drum_pad_note_colors_changed.subject = self._drum_pad_color_notifier

    @property
    def drum_group_device(self):
        return self._drum_group_device

    @select_color_button.value
    def select_color_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    @select_color_button.released
    def select_color_button(self, button):
        if self._color_chooser is not None:
            self._color_chooser.object = None

    def select_drum_pad(self, drum_pad):
        if len(drum_pad.chains) > 0 and self.song.view.selected_track.is_showing_chains:
            self._tracks_provider.scroll_into_view(drum_pad.chains[0])

    def _on_matrix_pressed(self, button):
        if self.select_color_button.is_pressed and self._color_chooser is not None:
            pad = self._pad_for_button(button)
            if liveobj_valid(pad) and pad.chains and liveobj_valid(pad.chains[0]):
                self._color_chooser.object = DrumPadColorAdapter(pad)
            else:
                self.show_notification('Cannot color an empty drum pad')
        else:
            super(DrumGroupComponent, self)._on_matrix_pressed(button)
        self.notify_mute_solo_stop_cancel_action_performed()

    def _on_selected_drum_pad_changed(self):
        super(DrumGroupComponent, self)._on_selected_drum_pad_changed()
        chain = self._selected_drum_pad.chains[0] if self._selected_drum_pad and len(self._selected_drum_pad.chains) > 0 else None
        if not self.song.view.selected_track.is_showing_chains or liveobj_valid(chain):
            self._tracks_provider.set_selected_item_without_updating_view(self._selected_drum_pad.chains[0])

    @property
    def hotswap_indication_mode(self):
        return self._hotswap_indication_mode

    @hotswap_indication_mode.setter
    def hotswap_indication_mode(self, mode):
        self._hotswap_indication_mode = mode
        self._update_led_feedback()

    def _color_for_pad(self, pad):
        if self._is_hotswapping(pad):
            color = 'DrumGroup.PadHotswapping'
        else:
            color = super(DrumGroupComponent, self)._color_for_pad(pad)
            color = self._chain_color_for_pad(pad, color)
        return color

    def _chain_color_for_pad(self, pad, color):
        if color == 'DrumGroup.PadFilled':
            color = IndexedColor.from_live_index(pad.chains[0].color_index)
        elif color == 'DrumGroup.PadMuted':
            color = IndexedColor.from_live_index(pad.chains[0].color_index, shade_level=1)
        return color

    def _is_hotswapping(self, pad):
        if self._hotswap_indication_mode == 'current_pad':
            return pad == self._selected_drum_pad
        elif self._hotswap_indication_mode == 'all_pads':
            return True
        else:
            return False

    def _update_drum_pad_listeners(self):
        super(DrumGroupComponent, self)._update_drum_pad_listeners()
        self._drum_pad_color_notifier.set_drum_group(self._drum_group_device)

    @listens('note_colors')
    def __on_drum_pad_note_colors_changed(self):
        self._update_led_feedback()

    def delete_drum_pad_content(self, drum_pad):
        self._tracks_provider.synchronize_selection_with_live_view()
        super(DrumGroupComponent, self).delete_drum_pad_content(drum_pad)

    def _make_copy_handler(self):
        return DrumPadCopyHandler(show_notification=self.show_notification, decorator_factory=self._decorator_factory, song=self.song)