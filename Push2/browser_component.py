# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\browser_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from contextlib import contextmanager
from math import ceil
import Live
from ableton.v2.base import BooleanContext, depends, index_if, lazy_attribute, listenable_property, listens, liveobj_changed, liveobj_valid, nop, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, StepEncoderControl, ToggleButtonControl, control_list
from pushbase.browser_util import filter_type_for_hotswap_target, get_selection_for_new_device
from pushbase.consts import MessageBoxText
from pushbase.message_box_component import Messenger
from .browser_item import BrowserItem, ProxyBrowserItem
from .browser_list import BrowserList
from .colors import DISPLAY_BUTTON_SHADE_LEVEL, IndexedColor
NAVIGATION_COLORS = dict(color='Browser.Navigation', disabled_color='Browser.NavigationDisabled')

class LoadNeighbourOverlayComponent(Component):
    __events__ = ('load_next', 'load_previous')
    load_next_button = ButtonControl(repeat=False, **NAVIGATION_COLORS)
    load_previous_button = ButtonControl(repeat=False, **NAVIGATION_COLORS)

    @load_next_button.pressed
    def button(self, button):
        self.notify_load_next()

    @load_previous_button.pressed
    def button(self, button):
        self.notify_load_previous()

    @listenable_property
    def can_load_next(self):
        return self.load_next_button.enabled

    @can_load_next.setter
    def can_load_next(self, can_load_next):
        self.load_next_button.enabled = can_load_next
        self.notify_can_load_next()

    @listenable_property
    def can_load_previous(self):
        return self.load_previous_button.enabled

    @can_load_previous.setter
    def can_load_previous(self, can_load_previous):
        self.load_previous_button.enabled = can_load_previous
        self.notify_can_load_previous()

class WrappedLoadableBrowserItem(BrowserItem):
    def __init__(self, *a, **k):
        super(WrappedLoadableBrowserItem, self).__init__(*a, **k)
        self._browser = Live.Application.get_application().browser

    @property
    def is_selected(self):
        if self._contained_item is None:
            return self._is_selected
        else:  # inserted
            relation = self._browser.relation_to_hotswap_target(self._contained_item)
            return relation == Live.Browser.Relation.equal

class FolderBrowserItem(BrowserItem):
    def __init__(self, wrapped_loadable=None, *a, **k):
        super(FolderBrowserItem, self).__init__(*a, **k)
        self._wrapped_loadable = wrapped_loadable

    @property
    def is_selected(self):
        return self._is_selected if self._contained_item is None else self._contained_item.is_selected

    @lazy_attribute
    def children(self):
        return [self._wrapped_loadable] + list(self.contained_item.children)

class PluginPresetBrowserItem(BrowserItem):
    def __init__(self, preset_name=None, preset_index=None, vst_device=None, *a, **k):
        super(PluginPresetBrowserItem, self).__init__(*a, name=preset_name if preset_name else '<Empty Slot %i>' % (preset_index + 1), is_loadable=True, **k)
        self.preset_index = preset_index
        self._vst_device = vst_device

    @property
    def is_selected(self):
        return self._vst_device.selected_preset_index == self.preset_index

    @property
    def uri(self):
        return 'pluginpreset%i' % self.preset_index

class PluginBrowserItem(BrowserItem):
    def __init__(self, vst_device=None, *a, **k):
        super(PluginBrowserItem, self).__init__(*a, is_loadable=False, is_selected=True, **k)
        self._vst_device = vst_device

    @property
    def children(self):
        return [PluginPresetBrowserItem(preset_name=preset, preset_index=i, vst_device=self._vst_device) for i, preset in enumerate(self._vst_device.presets)]

class CannotFocusListError(Exception):
    pass  # postinserted
class BrowserComponent(Component, Messenger):
    __events__ = ('loaded', 'close')
    NUM_ITEMS_PER_COLUMN = 6
    NUM_VISIBLE_BROWSER_LISTS = 7
    NUM_COLUMNS_IN_EXPANDED_LIST = 3
    EXPAND_LIST_TIME = 1.5
    REVEAL_PREVIEW_LIST_TIME = 0.2
    MIN_TIME = 0.6
    MAX_TIME = 1.4
    MIN_TIME_TEXT_LENGTH = 30
    MAX_TIME_TEXT_LENGTH = 70
    up_button = ButtonControl(repeat=True)
    down_button = ButtonControl(repeat=True)
    right_button = ButtonControl(repeat=True, **NAVIGATION_COLORS)
    left_button = ButtonControl(repeat=True, **NAVIGATION_COLORS)
    back_button = ButtonControl(**NAVIGATION_COLORS)
    open_button = ButtonControl(**NAVIGATION_COLORS)
    load_button = ButtonControl(**NAVIGATION_COLORS)
    close_button = ButtonControl()
    prehear_button = ToggleButtonControl(toggled_color='Browser.Option', untoggled_color='Browser.OptionDisabled')
    scroll_encoders = control_list(StepEncoderControl, num_steps=10, control_count=NUM_VISIBLE_BROWSER_LISTS)
    scroll_focused_encoder = StepEncoderControl(num_steps=10)
    scrolling = listenable_property.managed(False)
    horizontal_navigation = listenable_property.managed(False)
    list_offset = listenable_property.managed(0)
    can_enter = listenable_property.managed(False)
    can_exit = listenable_property.managed(False)
    context_color_index = listenable_property.managed((-1))
    context_text = listenable_property.managed('')

    @depends(commit_model_changes=None, selection=None)
    def __init__(self, preferences=dict(), commit_model_changes=None, selection=None, main_modes_ref=None, *a, **k):
        super(BrowserComponent, self).__init__(*a, **k)
        self._lists = []
        self._browser = Live.Application.get_application().browser
        self._current_hotswap_target = self._browser.hotswap_target
        self._updating_root_items = BooleanContext()
        self._focused_list_index = 0
        self._commit_model_changes = commit_model_changes
        self._preferences = preferences
        self._expanded = False
        self._unexpand_with_scroll_encoder = False
        self._delay_preview_list = BooleanContext()
        self._selection = selection
        self._main_modes_ref = main_modes_ref if main_modes_ref is not None else nop
        self._load_neighbour_overlay = LoadNeighbourOverlayComponent(parent=self, is_enabled=False)
        self._content_filter_type = None
        self._content_hotswap_target = None
        self._preview_list_task = self._tasks.add(task.sequence(task.wait(self.REVEAL_PREVIEW_LIST_TIME), task.run(self._replace_preview_list_by_task))).kill()
        self._update_root_items()
        self._update_navigation_buttons()
        self._update_context()
        self.prehear_button.is_toggled = preferences.setdefault('browser_prehear', True)
        self._on_selected_track_color_index_changed.subject = self.song.view
        self._on_selected_track_name_changed.subject = self.song.view
        self._on_detail_clip_name_changed.subject = self.song.view
        self._on_hotswap_target_changed.subject = self._browser
        self._on_load_next.subject = self._load_neighbour_overlay
        self._on_load_previous.subject = self._load_neighbour_overlay
        self._on_focused_item_changed.subject = self
        self.register_slot(self, self.notify_focused_item, 'focused_list_index')

        def auto_unexpand():
            self.expanded = False
            self._update_list_offset()
        self._unexpand_task = self._tasks.add(task.sequence(task.wait(self.EXPAND_LIST_TIME), task.run(auto_unexpand))).kill()

    @up_button.pressed
    def up_button(self, button):
        pass  # cflow: irreducible

    @up_button.released
    def up_button(self, button):
        self._finish_preview_list_task()
        self._update_scrolling()

    @down_button.pressed
    def down_button(self, button):
        pass  # cflow: irreducible

    @down_button.released
    def down_button(self, button):
        self._finish_preview_list_task()
        self._update_scrolling()

    @right_button.pressed
    def right_button(self, button):
        if self._expanded and self._can_auto_expand() and (self._focused_list_index > 0):
            self.focused_list.select_index_with_offset(self.NUM_ITEMS_PER_COLUMN)
            self._update_scrolling()
            self.horizontal_navigation = True
            return
        else:  # inserted
            if not self._enter_selected_item():
                self._update_auto_expand()
                return
            else:  # inserted
                return None

    @right_button.released
    def right_button(self, button):
        self._update_scrolling()

    @left_button.pressed
    def left_button(self, button):
        if self._expanded and self._focused_list_index > 0 and (self.focused_list.selected_index >= self.NUM_ITEMS_PER_COLUMN):
            self.focused_list.select_index_with_offset(-self.NUM_ITEMS_PER_COLUMN)
            self._update_scrolling()
            self.horizontal_navigation = True
            return
        else:  # inserted
            self._exit_selected_item()

    @left_button.released
    def left_button(self, button):
        self._update_scrolling()

    @open_button.pressed
    def open_button(self, button):
        self._enter_selected_item()

    @back_button.pressed
    def back_button(self, button):
        self._exit_selected_item()

    @scroll_encoders.touched
    def scroll_encoders(self, encoder):
        list_index = self._get_list_index_for_encoder(encoder)
        if list_index is not None:
            try:
                if self._focus_list_with_index(list_index, crop=False):
                    self._unexpand_with_scroll_encoder = True
                    self._prehear_selected_item()
                if self.focused_list.selected_item.is_loadable and encoder.index == self.scroll_encoders.control_count - 1:
                    self._update_list_offset()
                self._on_encoder_touched()
            except CannotFocusListError:
                return None
            else:  # inserted
                return

    @scroll_encoders.released
    def scroll_encoders(self, encoders):
        self._on_encoder_released()

    @scroll_encoders.value
    def scroll_encoders(self, value, encoder):
        list_index = self._get_list_index_for_encoder(encoder)
        if list_index is not None:
            try:
                if self._focus_list_with_index(list_index):
                    self._unexpand_with_scroll_encoder = True
                self._on_encoder_value(value)
            except CannotFocusListError:
                return None

    @scroll_focused_encoder.value
    def scroll_focused_encoder(self, value, encoder):
        self._on_encoder_value(value)

    @scroll_focused_encoder.touched
    def scroll_focused_encoder(self, encoder):
        self._on_encoder_touched()

    @scroll_focused_encoder.released
    def scroll_focused_encoder(self, encoder):
        self._on_encoder_released()

    def _on_encoder_value(self, value):
        pass  # cflow: irreducible

    def _on_encoder_touched(self):
        self._unexpand_task.kill()
        self._update_scrolling()
        self._update_horizontal_navigation()

    def _on_encoder_released(self):
        any_encoder_touched = any(map(lambda e: e.is_touched, self.scroll_encoders)) or self.scroll_focused_encoder.is_touched
        if not any_encoder_touched and self._unexpand_with_scroll_encoder:
            self._unexpand_task.restart()
        self._update_scrolling()

    def _get_list_index_for_encoder(self, encoder):
        if self.expanded:
            return self.list_offset if encoder.index == 0 else self.list_offset + 1
        else:  # inserted
            index = self.list_offset + encoder.index
            if self.focused_list_index + 1 == index and self.should_widen_focused_item:
                index = self.focused_list_index
            if 0 <= index < len(self._lists):
                if index:
                    pass  # postinserted
            else:  # inserted
                return None

    @load_button.pressed
    def load_button(self, button):
        self._load_selected_item()

    @prehear_button.toggled
    def prehear_button(self, toggled, button):
        if toggled:
            self._prehear_selected_item()
        else:  # inserted
            self._browser.stop_preview()
        self._preferences['browser_prehear'] = toggled
        self.notify_prehear_enabled()

    @close_button.pressed
    def close_button(self, button):
        self.notify_close()

    @listenable_property
    def lists(self):
        return self._lists

    @listenable_property
    def focused_list_index(self):
        return self._focused_list_index

    @listenable_property
    def prehear_enabled(self):
        return self.prehear_button.is_toggled

    @property
    def focused_list(self):
        return self._lists[self._focused_list_index]

    @listenable_property
    def focused_item(self):
        return self.focused_list.selected_item

    @listenable_property
    def expanded(self):
        return self._expanded

    @property
    def load_neighbour_overlay(self):
        return self._load_neighbour_overlay

    @listenable_property
    def should_widen_focused_item(self):
        return self.focused_item.is_loadable and (not self.focused_item.is_device)

    @property
    def context_display_type(self):
        return 'custom_button'

    def disconnect(self):
        super(BrowserComponent, self).disconnect()
        self._lists = []
        self._commit_model_changes = None

    @expanded.setter
    def expanded(self, expanded):
        if self._expanded!= expanded:
            self._expanded = expanded
            self._unexpand_with_scroll_encoder = False
            self._update_navigation_buttons()
            if len(self._lists) > self._focused_list_index + 1:
                self._lists[self._focused_list_index + 1].limit = self.num_preview_items
            self.notify_expanded()
            return

    @listens('selected_track.color_index')
    def _on_selected_track_color_index_changed(self):
        if self.is_enabled():
            self._update_context()
            self._update_navigation_buttons()

    @listens('selected_track.name')
    def _on_selected_track_name_changed(self):
        if self.is_enabled():
            self._update_context()

    @listens('detail_clip.name')
    def _on_detail_clip_name_changed(self):
        if self.is_enabled():
            self._update_context()

    @listens('hotswap_target')
    def _on_hotswap_target_changed(self):
        if self.is_enabled():
            if not self._switched_to_empty_pad():
                self._update_root_items()
                self._update_context()
                self._update_list_offset()
                self._update_load_neighbour_overlay_visibility()
            else:  # inserted
                self._load_neighbour_overlay.set_enabled(False)
        self._current_hotswap_target = self._browser.hotswap_target

    @listens('focused_item')
    def _on_focused_item_changed(self):
        self.notify_should_widen_focused_item()

    @property
    def browse_for_audio_clip(self):
        main_modes = self._main_modes_ref()
        if main_modes is None:
            return False
        else:  # inserted
            has_midi_support = self.song.view.selected_track.has_midi_input
            return not has_midi_support and 'clip' in main_modes.active_modes

    def _switched_to_empty_pad(self):
        hotswap_target = self._browser.hotswap_target
        is_browsing_drumpad = isinstance(hotswap_target, Live.DrumPad.DrumPad)
        was_browsing_pad = isinstance(self._current_hotswap_target, Live.DrumPad.DrumPad)
        return is_browsing_drumpad and was_browsing_pad and (len(hotswap_target.chains) == 0)

    def _focus_list_with_index(self, index, crop=True):
        pass
        if self._focused_list_index!= index:
            if self._finish_preview_list_task() and index >= len(self._lists):
                raise CannotFocusListError()
            else:  # inserted
                self._on_focused_selection_changed.subject = None
                if self._focused_list_index > index and crop:
                    for l in self._lists[self._focused_list_index:]:
                        l.selected_index = (-1)
                self._focused_list_index = index
                self.focused_list.limit = (-1)
                if self.focused_list.selected_index == (-1):
                    self.focused_list.selected_index = 0
                self.notify_focused_list_index()
                self._on_focused_selection_changed.subject = self.focused_list
                if crop:
                    self._crop_browser_lists(self._focused_list_index + 2)
                if self._focused_list_index == len(self._lists) - 1:
                    self._replace_preview_list()
                self._load_neighbour_overlay.set_enabled(False)
                self._update_navigation_buttons()
                return True
        else:  # inserted
            return False

    @listens('selected_index')
    def _on_focused_selection_changed(self):
        if self._delay_preview_list and (not self.focused_item.is_loadable):
            self._preview_list_task.restart()
        else:  # inserted
            self._replace_preview_list()
        self._update_navigation_buttons()
        self._prehear_selected_item()
        self._load_neighbour_overlay.set_enabled(False)
        self.notify_focused_item()

    def _get_actual_item(self, item):
        contained_item = getattr(item, 'contained_item', None)
        return contained_item if contained_item is not None else item

    def _previous_can_be_loaded(self):
        return self.focused_list.selected_index > 0 and self.focused_list.items[self.focused_list.selected_index - 1].is_loadable

    def _next_can_be_loaded(self):
        items = self.focused_list.items
        return self.focused_list.selected_index < len(items) - 1 and items[self.focused_list.selected_index + 1].is_loadable

    @listens('load_next')
    def _on_load_next(self):
        self.focused_list.selected_index += 1
        self._load_selected_item()

    @listens('load_previous')
    def _on_load_previous(self):
        self.focused_list.selected_index -= 1
        self._load_selected_item()

    def _update_load_neighbour_overlay_visibility(self):
        self._load_neighbour_overlay.set_enabled(liveobj_valid(self._browser.hotswap_target) and (self._next_can_be_loaded() or (self._previous_can_be_loaded() and (not self.focused_list.selected_item.is_device))))

    def _load_selected_item(self):
        focused_list = self.focused_list
        self._update_load_neighbour_overlay_visibility()
        self._update_navigation_buttons()
        item = self._get_actual_item(focused_list.selected_item)
        self._load_item(item)
        self.notify_loaded()

    def _show_load_notification(self, item):
        notification_text = self._make_notification_text(item)
        text_length = len(notification_text)
        notification_time = self.MIN_TIME
        if text_length > self.MIN_TIME_TEXT_LENGTH:
            if text_length > self.MAX_TIME_TEXT_LENGTH:
                notification_time = self.MAX_TIME
            else:  # inserted
                notification_time = self.MIN_TIME + (self.MAX_TIME - self.MIN_TIME) * old_div(float(text_length - self.MIN_TIME_TEXT_LENGTH), self.MAX_TIME_TEXT_LENGTH - self.MIN_TIME_TEXT_LENGTH)
        self.show_notification(notification_text, notification_time=notification_time)
        self._commit_model_changes()

    def _make_notification_text(self, browser_item):
        return 'Loading %s' % browser_item.name

    def _load_item(self, item):
        pass  # cflow: irreducible

    @contextmanager
    def _insert_right_of_selected(self):
        DeviceInsertMode = Live.Track.DeviceInsertMode
        device_to_select = get_selection_for_new_device(self._selection)
        if device_to_select:
            self._selection.selected_object = device_to_select
        selected_track_view = self.song.view.selected_track.view
        selected_track_view.device_insert_mode = DeviceInsertMode.selected_right
        yield
        selected_track_view.device_insert_mode = DeviceInsertMode.default

    def _prehear_selected_item(self):
        if not self.prehear_button.is_toggled or not self._updating_root_items:
                self._browser.stop_preview()
                item = self._get_actual_item(self.focused_list.selected_item)
                if item and item.is_loadable and isinstance(item, Live.Browser.BrowserItem):
                            self._browser.preview_item(item)
                            return

    def _stop_prehear(self):
        if not self.prehear_button.is_toggled or not self._updating_root_items:
                self._browser.stop_preview()
                return
        else:  # inserted
            return

    def _update_navigation_buttons(self):
        focused_list = self.focused_list
        self.up_button.enabled = focused_list.selected_index > 0
        self.down_button.enabled = focused_list.selected_index < len(focused_list.items) - 1
        selected_item_loadable = self.focused_list.selected_item.is_loadable
        can_exit = self._focused_list_index > 0
        assume_can_enter = self._preview_list_task.is_running and (not selected_item_loadable)
        can_enter = self._focused_list_index < len(self._lists) - 1 or assume_can_enter
        self.back_button.enabled = can_exit
        self.open_button.enabled = can_enter
        self.load_button.enabled = selected_item_loadable
        self._load_neighbour_overlay.can_load_previous = self._previous_can_be_loaded()
        self._load_neighbour_overlay.can_load_next = self._next_can_be_loaded()
        context_button_color = IndexedColor.from_live_index(self.context_color_index, DISPLAY_BUTTON_SHADE_LEVEL) if self.context_color_index > (-1) else 'Browser.Navigation'
        self.load_button.color = context_button_color
        self.close_button.color = context_button_color
        self._load_neighbour_overlay.load_next_button.color = context_button_color
        self._load_neighbour_overlay.load_previous_button.color = context_button_color
        if not self._expanded:
            self.left_button.enabled = self.back_button.enabled
            self.right_button.enabled = can_enter or self._can_auto_expand()
        else:  # inserted
            num_columns = int(ceil(old_div(float(len(self.focused_list.items)), self.NUM_ITEMS_PER_COLUMN)))
            last_column_start_index = (num_columns - 1) * self.NUM_ITEMS_PER_COLUMN
            self.left_button.enabled = self._focused_list_index > 0
            self.right_button.enabled = can_enter or self.focused_list.selected_index < last_column_start_index
        self.can_enter = can_enter
        self.can_exit = can_exit

    def _update_scrolling(self):
        self.scrolling = self.up_button.is_pressed or self.down_button.is_pressed or self.scroll_focused_encoder.is_touched or any(map(lambda e: e.is_touched, self.scroll_encoders)) or (self.right_button.is_pressed and (self._expanded or (self.left_button.is_pressed and self._expanded)))

    def _update_horizontal_navigation(self):
        self.horizontal_navigation = self.right_button.is_pressed or self.left_button.is_pressed

    def _update_context(self):
        selected_track = self.song.view.selected_track
        clip = self.song.view.detail_clip
        if self.browse_for_audio_clip and clip:
            self.context_text = clip.name
        else:  # inserted
            if liveobj_valid(self._browser.hotswap_target):
                self.context_text = self._browser.hotswap_target.name
            else:  # inserted
                self.context_text = selected_track.name
        selected_track_color_index = selected_track.color_index
        self.context_color_index = selected_track_color_index if selected_track_color_index is not None else (-1)

    def _enter_selected_item(self):
        item_entered = False
        self._finish_preview_list_task()
        new_index = self._focused_list_index + 1
        if 0 <= new_index < len(self._lists):
            self._focus_list_with_index(new_index)
            self._unexpand_task.kill()
            self._update_list_offset()
            self._update_auto_expand()
            self._prehear_selected_item()
            item_entered = True
        return item_entered

    def _exit_selected_item(self):
        item_exited = False
        try:
            self._focus_list_with_index(self._focused_list_index - 1)
            self._update_list_offset()
            self._update_auto_expand()
            self._stop_prehear()
            item_exited = True
        except CannotFocusListError:
            pass
        return item_exited

    def _can_auto_expand(self):
        return len(self.focused_list.items) > self.NUM_ITEMS_PER_COLUMN * 2 and self.focused_list.selected_item.is_loadable and (getattr(self.focused_list.selected_item, 'contained_item', None) == None)

    def _update_auto_expand(self):
        self.expanded = self._can_auto_expand()
        self._update_list_offset()

    def _update_list_offset(self):
        if self.expanded:
            self.list_offset = max(0, self.focused_list_index - 1)
            return
        else:  # inserted
            offset = len(self._lists)
            if self.focused_list.selected_item.is_loadable:
                offset += 1
            self.list_offset = max(0, offset - self.NUM_VISIBLE_BROWSER_LISTS)
            return

    def _replace_preview_list_by_task(self):
        self._replace_preview_list()
        self._update_navigation_buttons()

    def _finish_preview_list_task(self):
        if self._preview_list_task.is_running:
            self._replace_preview_list_by_task()
            return True
        else:  # inserted
            return False

    def _replace_preview_list(self):
        self._preview_list_task.kill()
        self._crop_browser_lists(self._focused_list_index + 1)
        selected_item = self.focused_list.selected_item
        children_iterator = selected_item.iter_children
        if len(children_iterator) > 0:
            enable_wrapping = getattr(selected_item, 'enable_wrapping', True) and self.focused_list.items_wrapped
            self._append_browser_list(children_iterator=children_iterator, limit=self.num_preview_items, enable_wrapping=enable_wrapping)

    def _append_browser_list(self, children_iterator, limit=(-1), enable_wrapping=True):
        l = BrowserList(item_iterator=children_iterator, item_wrapper=self._wrap_item if enable_wrapping else nop, limit=limit)
        l.items_wrapped = enable_wrapping
        self._lists.append(l)
        self.register_disconnectable(l)
        self.notify_lists()

    def _crop_browser_lists(self, length):
        num_items_to_crop = len(self._lists) - length
        for _ in range(num_items_to_crop):
            l = self._lists.pop()
            self.unregister_disconnectable(l)
        if num_items_to_crop > 0:
            self.notify_lists()
            return

    def _make_root_browser_items(self):
        filter_type = self._browser.filter_type
        hotswap_target = self._browser.hotswap_target
        if liveobj_valid(hotswap_target):
            filter_type = filter_type_for_hotswap_target(hotswap_target, default=filter_type)
        return make_root_browser_items(self._browser, filter_type)

    def _content_cache_is_valid(self):
        return self._content_filter_type == self._browser.filter_type and (not liveobj_changed(self._content_hotswap_target, self._browser.hotswap_target))

    def _invalidate_content_cache(self):
        self._content_hotswap_target = None
        self._content_filter_type = None

    def _update_content_cache(self):
        self._content_filter_type = self._browser.filter_type
        self._content_hotswap_target = self._browser.hotswap_target

    def _update_root_items(self):
        pass  # cflow: irreducible

    def _select_hotswap_target(self, list_index=0):
        if list_index < len(self._lists):
            l = self._lists[list_index]
            l.access_all = True
            children = l.items
            i = index_if(lambda i: i.is_selected, children)
            if i < len(children):
                self._focused_list_index = list_index
                l.selected_index = i
                self._replace_preview_list()
                self._select_hotswap_target(list_index + 1)

    @property
    def num_preview_items(self):
        return self.NUM_ITEMS_PER_COLUMN * self.NUM_COLUMNS_IN_EXPANDED_LIST if self._expanded else 6

    def update(self):
        super(BrowserComponent, self).update()
        self._invalidate_content_cache()
        if self.is_enabled():
            self._update_root_items()
            self._update_context()
            self._update_list_offset()
            self._update_load_neighbour_overlay_visibility()
            self._update_navigation_buttons()
            self.expanded = False
            self._update_list_offset()
            return
        else:  # inserted
            self._stop_prehear()
            self.list_offset = 0

    def _wrap_item(self, item):
        if item.is_device:
            return self._wrap_device_item(item)
        else:  # inserted
            if self._is_hotswap_target_plugin(item):
                return self._wrap_hotswapped_plugin_item(item)
            else:  # inserted
                return item

    def _wrap_device_item(self, item):
        pass
        wrapped_loadable = WrappedLoadableBrowserItem(name=item.name, is_loadable=True, contained_item=item)
        return FolderBrowserItem(name=item.name, is_loadable=True, is_device=True, contained_item=item, wrapped_loadable=wrapped_loadable, icon='browser_arrowcontent.svg')

    def _is_hotswap_target_plugin(self, item):
        return isinstance(self._browser.hotswap_target, Live.PluginDevice.PluginDevice) and isinstance(item, Live.Browser.BrowserItem) and (self._browser.relation_to_hotswap_target(item) == Live.Browser.Relation.equal)

    def _wrap_hotswapped_plugin_item(self, item):
        return PluginBrowserItem(name=item.name, vst_device=self._browser.hotswap_target)

class TrackBrowserItem(BrowserItem):
    filter_type = Live.Browser.FilterType.hotswap_off

    def create_track(self, song):
        raise NotImplementedError

class MidiTrackBrowserItem(TrackBrowserItem):
    filter_type = Live.Browser.FilterType.midi_track_devices

    def __init__(self, *a, **k):
        super(MidiTrackBrowserItem, self).__init__(*a, name='MIDI track', **k)

    def create_track(self, song):
        song.create_midi_track()

class AudioTrackBrowserItem(TrackBrowserItem):
    filter_type = Live.Browser.FilterType.audio_effect_hotswap

    def __init__(self, *a, **k):
        super(AudioTrackBrowserItem, self).__init__(*a, name='Audio track', **k)

    def create_track(self, song):
        song.create_audio_track()

class ReturnTrackBrowserItem(TrackBrowserItem):
    filter_type = Live.Browser.FilterType.audio_effect_hotswap

    def __init__(self, *a, **k):
        super(ReturnTrackBrowserItem, self).__init__(*a, name='Return track', **k)

    def create_track(self, song):
        song.create_return_track()

class DefaultTrackBrowserItem(BrowserItem):
    pass

    def __init__(self, *a, **k):
        super(DefaultTrackBrowserItem, self).__init__(*a, name='Default track', is_loadable=True, **k)

class NewTrackBrowserComponent(BrowserComponent):
    def __init__(self, *a, **k):
        self._content = []
        self._track_type_items = [MidiTrackBrowserItem(children=self._content), AudioTrackBrowserItem(children=self._content), ReturnTrackBrowserItem(children=self._content)]
        super(NewTrackBrowserComponent, self).__init__(*a, **k)
        if self.is_enabled():
            self._update_filter_type()

    def _make_root_browser_items(self):
        self._update_root_content()
        return self._track_type_items

    def disconnect(self):
        super(NewTrackBrowserComponent, self).disconnect()
        self._content = []

    @property
    def browse_for_audio_clip(self):
        return False

    @property
    def context_display_type(self):
        return 'cancel_button'

    def _update_root_content(self):
        real_root_items = super(NewTrackBrowserComponent, self)._make_root_browser_items()
        self._content[:] = [DefaultTrackBrowserItem()] + real_root_items

    def _update_root_items(self):
        self._set_filter_type(self._track_type_items[0].filter_type)
        super(NewTrackBrowserComponent, self)._update_root_items()
        self._on_root_list_selection_changed.subject = self._lists[0]

    def _update_filter_type(self):
        self._set_filter_type(self._selected_track_item().filter_type)

    def _set_filter_type(self, filter_type):
        if self._browser.filter_type!= filter_type:
            self._browser.filter_type = filter_type
            self._update_root_content()
            return

    def _update_context(self):
        return

    def _load_item(self, item):
        pass  # cflow: irreducible

    def _make_notification_text(self, browser_item):
        if isinstance(browser_item, DefaultTrackBrowserItem):
            return 'Default track created'
        else:  # inserted
            new_track_position = self._selected_track_index() + 1
            return '%s loaded in track %i' % (browser_item.name, new_track_position)

    def _selected_track_index(self):
        song = self.song
        selected_track = self._selection.selected_track
        return list(song.tracks).index(selected_track) if selected_track in song.tracks else (-1)

    def _selected_track_item(self):
        return self._lists[0].selected_item

    @listens('selected_index')
    def _on_root_list_selection_changed(self):
        self._update_filter_type()
        self._replace_preview_list()

def wrap_item(item, icon, **k):
    return ProxyBrowserItem(proxied_object=item, icon=icon, **k)

def wrap_items(items, icon, enable_wrapping=True):
    for i, place in enumerate(items):
        items[i] = wrap_item(place, icon, enable_wrapping=enable_wrapping)
    return items

class UserFilesBrowserItem(BrowserItem):
    def __init__(self, browser, *a, **k):
        super(UserFilesBrowserItem, self).__init__(*a, **k)
        self._browser = browser

    @property
    def is_selected(self):
        return any(map(lambda c: c.is_selected, self.children))

    @lazy_attribute
    def children(self):
        res = [wrap_item(self._browser.user_library, 'browser_userlibrary.svg')] + wrap_items(list(self._browser.user_folders), 'browser_folder.svg')
        self._browser = None
        return res

class CollectionsBrowserItem(BrowserItem):
    def __init__(self, browser, *a, **k):
        super(CollectionsBrowserItem, self).__init__(*a, **k)
        self._browser = browser

    @property
    def is_selected(self):
        return any(map(lambda c: c.is_selected, self.children))

    @lazy_attribute
    def children(self):
        color_labels = wrap_items(list(self._browser.colors), 'browser_collection_icon.svg', enable_wrapping=False)
        self._browser = None
        return color_labels

def make_root_browser_items(browser, filter_type):
    collections = CollectionsBrowserItem(browser, name='Collections', icon='browser_collections.svg')
    sounds = wrap_item(browser.sounds, 'browser_sounds.svg')
    drums = wrap_item(browser.drums, 'browser_drums.svg', enable_wrapping=False)
    instruments = wrap_item(browser.instruments, 'browser_instruments.svg')
    audio_effects = wrap_item(browser.audio_effects, 'browser_audioeffect.svg')
    midi_effects = wrap_item(browser.midi_effects, 'browser_midieffect.svg')
    packs = wrap_item(browser.packs, 'browser_packs.svg')
    current_project = wrap_item(browser.current_project, 'browser_currentproject.svg')
    if filter_type == Live.Browser.FilterType.samples:
        categories = [packs, current_project]
    else:  # inserted
        common_items = [wrap_item(browser.max_for_live, 'browser_max.svg'), wrap_item(browser.plugins, 'browser_plugins.svg'), packs, current_project]
        if filter_type == Live.Browser.FilterType.audio_effect_hotswap:
            categories = [audio_effects] + common_items
        else:  # inserted
                categories = [midi_effects] + common_items
            else:  # inserted
                if filter_type == Live.Browser.FilterType.instrument_hotswap:
                    categories = [sounds, drums, instruments] + common_items
                else:  # inserted
                    categories = [sounds, drums, instruments, audio_effects, midi_effects] + common_items
    user_files = UserFilesBrowserItem(browser, name='User Files', icon='browser_userfiles.svg')
    return [collections, user_files] + categories