# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\device_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from typing import cast
from ...base import SlotGroup, depends, listens
from ...live import flatten_device_chain, is_device_rack, liveobj_changed, liveobj_valid
from ..display import Renderable
from .item_list import ItemListComponent, ItemProvider

class FlattenedDeviceChain(ItemProvider):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._track = None

        def make_slot_group(event):
            slot_group = SlotGroup(self._update_devices, event)
            return self.register_disconnectable(slot_group)
        self._devices_changed = make_slot_group('devices')
        self._selected_chain_changed = make_slot_group('selected_chain')
        self._selected_pad_changed = make_slot_group('selected_drum_pad')
        self._collapsed_state_changed = make_slot_group('is_collapsed')
        self._macros_mapped_changed = make_slot_group('macros_mapped')
        self._chain_devices_visibility_changed = make_slot_group('is_showing_chain_devices')

    @property
    def track(self):
        pass
        return self._track

    @track.setter
    def track(self, parent):
        if liveobj_changed(parent, self._track):
            self._track = parent
            self._update_devices()
            return
        else:  # inserted
            return None

    def _update_devices(self, *_):
        self.items = flatten_device_chain(self._track)
        self._update_listeners()

    def _update_listeners(self):
        def get_rack_views(racks):
            return [rack.view for rack in racks]
        racks = [rack for rack in self._items if is_device_rack(rack)]
        rack_views = get_rack_views(racks)
        device_parents = chain(map(lambda x: x.selected_chain, rack_views), [self._track])

        def is_empty_pad_drum_rack(rack):
            return rack.can_have_drum_pads and rack.view.selected_drum_pad and (len(rack.view.selected_drum_pad.chains) == 0)
        empty_pad_drum_rack_views = get_rack_views(list(filter(is_empty_pad_drum_rack, racks)))
        self._devices_changed.replace_subjects(device_parents)
        self._selected_chain_changed.replace_subjects(rack_views)
        self._collapsed_state_changed.replace_subjects(rack_views)
        self._chain_devices_visibility_changed.replace_subjects(rack_views)
        self._macros_mapped_changed.replace_subjects(racks)
        self._selected_pad_changed.replace_subjects(empty_pad_drum_rack_views)

class DeviceNavigationComponent(ItemListComponent, Renderable):
    pass

    @depends(device_provider=None)
    pass
    def __init__(self, name='Device_Navigation', device_provider=None, item_provider=None, *a, **k):
        super().__init__(*a, name=name, item_provider=item_provider or FlattenedDeviceChain(), scroll_skin_name='Device.Navigation', **k)
        self._previously_appointed_device = None
        self._device_provider = device_provider
        self.register_slot(self._item_provider, self._update_device_selection, 'selected_item')
        self.__on_selected_track_or_device_changed.subject = self.song.view
        self._update_track_selection()

    def _do_scroll_up(self):
        self._on_devices_scrolled()
        super()._do_scroll_up()

    def _do_scroll_down(self):
        self._on_devices_scrolled()
        super()._do_scroll_down()

    def _on_devices_scrolled(self):
        self._show_device_chain()
        self._tasks.add(self._notify_device_selection)

    def _show_device_chain(self):
        view = self.application.view
        if not view.is_view_visible('Detail/DeviceChain', False):
            view.show_view('Detail/DeviceChain')
            return

    def _notify_device_selection(self, _):
        device = self.song.appointed_device
        if liveobj_changed(device, self._previously_appointed_device):
            self._previously_appointed_device = device
            self.notify(self.notifications.Device.select, cast(str, device.name))

    def _update_device_selection(self):
        device = self._item_provider.selected_item
        if liveobj_valid(device):
            self._device_provider.select_and_appoint_device(device)
            return
        else:  # inserted
            return None

    def _update_track_selection(self):
        track = self.song.view.selected_track
        self._item_provider.track = track
        self._item_provider.selected_item = track.view.selected_device
        self.update()

    @listens('selected_track.view.selected_device')
    def __on_selected_track_or_device_changed(self):
        self._update_track_selection()