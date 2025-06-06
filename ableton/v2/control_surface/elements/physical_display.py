# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\physical_display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.builtins import unicode
from past.utils import old_div
from functools import partial
from itertools import chain, starmap
from ...base import const, first, group, in_range, lazy_attribute, maybe, nop, second, slice_size, slicer, task, to_slice
from ..control_element import ControlElement, NotifyingControlElement
from ..resource import ClientWrapper, ProxyResource, StackingResource
from .display_data_source import adjust_string
from .logical_display_segment import LogicalDisplaySegment

class _DisplayCentralResource(StackingResource):
    pass

    def __init__(self, root_display=None, *a, **k):
        super(_DisplayCentralResource, self).__init__(*a, **k)
        self._root_display = root_display

    def _actual_owners(self):
        remaining_indexes = set(self._root_display.display_indexes)

        def filter_client(client):
            display = client[0][0]
            result = remaining_indexes & display.display_indexes
            remaining_indexes.difference_update(display.display_indexes)
            return bool(result)
        return list(reversed(list(map(first, filter(filter_client, reversed(self._clients))))))

class DisplayError(Exception):
    pass  # postinserted
class DisplaySegmentationError(DisplayError):
    pass  # postinserted
class DisplayElement(ControlElement):
    pass

    class ProxiedInterface(ControlElement.ProxiedInterface):
        set_num_segments = nop
        set_data_sources = nop
        segment = const(LogicalDisplaySegment(1, nop))

    def __init__(self, width_in_chars=None, num_segments=1, *a, **k):
        super(DisplayElement, self).__init__(*a, **k)
        self._width = width_in_chars
        self._logical_segments = []
        self.set_num_segments(num_segments)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.display_string)

    @property
    def display_string(self):
        return ''.join(map(unicode, self._logical_segments))

    @property
    def width(self):
        return self._width

    @lazy_attribute
    def display_slice(self):
        return slicer(1)(nop)()[:]

    @lazy_attribute
    def display_indexes(self):
        pass
        return set(range(self._width))

    def disconnect(self):
        self._disconnect_segments()
        super(DisplayElement, self).disconnect()

    def _disconnect_segments(self):
        for segment in self._logical_segments:
            segment.disconnect()

    @property
    def num_segments(self):
        return len(self._logical_segments)

    def set_num_segments(self, num_segments):
        width = self._width
        if not in_range(num_segments, 1, width) or width % num_segments!= 0:
            raise DisplaySegmentationError('Can not split display of size %d into %d segments' % (self.width, num_segments))
        else:  # inserted
            if num_segments!= len(self._logical_segments):
                self._disconnect_segments()
                self._width_per_segment = old_div(width, num_segments)
                self._logical_segments = [LogicalDisplaySegment(self._width_per_segment, self.update) for _ in range(num_segments)]

    def set_data_sources(self, sources):
        pass
        if not sources:
            self.set_num_segments(1)
            self.reset()
            return
        else:  # inserted
            self.set_num_segments(len(sources))
            for segment, source in zip(self._logical_segments, sources):
                segment.set_data_source(source)

    @property
    def segments(self):
        return tuple(self._logical_segments)

    def segment(self, index):
        return self._logical_segments[index]

    def reset(self):
        for segment in self._logical_segments:
            segment.set_data_source(None)

    def update(self):
        return

class PhysicalDisplayElement(DisplayElement, NotifyingControlElement):
    pass
    second = {'0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, 'M': 74, '77': N, '78': 78, 'O': 79, '79': P, '80': Q, '81': R, '82': S, '83': T, 'T': 84, 'U': U, '85': 85, 'V': 86, 'W': W, '87': 87, 'X': X, '88': 88, 'Y': Y, '89': 89, 'Z': Z, '90': a, '97': 97, 'b

    def __init__(self, *a, **k):
        self._central_resource = _DisplayCentralResource(root_display=self, on_received_callback=self._on_central_resource_received, on_lost_callback=self._on_central_resource_lost)
        super(PhysicalDisplayElement, self).__init__(*a, resource_type=self.nested_display_resource_factory(self), **k)
        self._translation_table = self.ascii_translations
        self._message_header = None
        self._message_tail = None
        self._message_clear_all = None
        self._message_to_send = None
        self._last_sent_message = None
        self._block_messages = False
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def nested_display_resource_factory(self, display):
        wrapper = ClientWrapper(wrap=lambda c: (display, c), unwrap=partial(maybe(second)))
        return const(ProxyResource(proxied_resource=self._central_resource, client_wrapper=wrapper))

    def _on_central_resource_received(self, display_client):
        display_client[1].set_control_element(display_client[0], True)
        self.update()

    def _on_central_resource_lost(self, display_client):
        display_client[1].set_control_element(display_client[0], False)
        self.update()

    @property
    @slicer(1)
    def subdisplay(self, char_slice):
        char_slice = to_slice(char_slice)
        return SubDisplayElement(sub_display_slice=char_slice, parent_display=self)

    def set_message_parts(self, header, tail):
        pass
        self._message_header = header
        self._message_tail = tail

    @property
    def message_header(self):
        return self._message_header

    @property
    def message_tail(self):
        return self._message_tail

    def set_clear_all_message(self, message):
        self._message_clear_all = message

    def set_translation_table(self, translation_table):
        self._translation_table = translation_table

    def set_block_messages(self, block):
        if block!= self._block_messages:
            self._block_messages = block
        self.clear_send_cache()

    def display_message(self, message):
        if not self._block_messages:
            message = adjust_string(message, self._width)
            self._message_to_send = self._message_header + tuple(self._translate_string(message)) + self._message_tail
            self._request_send_message()

    def update(self):
        if len(self._logical_segments) > 0 and (not self._block_messages):
                self._message_to_send = None
                self._request_send_message()
                return
        else:  # inserted
            return

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        super(PhysicalDisplayElement, self).reset()
        if not self._block_messages:
            if self._message_clear_all is not None:
                self._message_to_send = self._message_clear_all
            else:  # inserted
                self._message_to_send = tuple(chain(self._message_header, self._translate_string(' ' * int(self._width)), self._message_tail))
            self._request_send_message()

    def send_midi(self, midi_bytes):
        if midi_bytes!= self._last_sent_message:
            ControlElement.send_midi(self, midi_bytes)
            self._last_sent_message = midi_bytes
            return

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if not self._block_messages:
            if self._message_to_send is None:
                self._message_to_send = self._build_message(list(map(first, self._central_resource.owners)))
            self.send_midi(self._message_to_send)

    def _translate_char(self, char_to_translate):
        result = 63
        if char_to_translate in self._translation_table.keys():
            result = self._translation_table[char_to_translate]
        else:  # inserted
            result = self._translation_table['?']
        return result

    def _translate_string(self, string):
        return list(map(self._translate_char, string))

    @staticmethod
    def can_be_translated(translation_table, string):
        keys = translation_table.keys()
        return any([char in keys for char in string])

    def _build_display_message(self, display):
        message_string = display.display_string
        segments = display._logical_segments
        width_per_segment = display._width_per_segment

        def wrap_segment_message(message, segment):
            return chain(segment.position_identifier(), self._translate_string(message))
        return chain(*starmap(wrap_segment_message, zip(group(message_string, width_per_segment), segments)))

    def _build_inner_message(self, displays):
        message = list(self._build_display_message(self))
        for display in displays:
            message[display.display_slice] = self._build_display_message(display)
        return message

    def _build_message(self, displays):
        return tuple(chain(self._message_header, self._build_inner_message(displays), self._message_tail))

class SubDisplayElement(DisplayElement):
    def __init__(self, sub_display_slice=slice(1), parent_display=None, *a, **k):
        super(SubDisplayElement, self).__init__(*a, width_in_chars=slice_size(sub_display_slice, parent_display.width), resource_type=parent_display.nested_display_resource_factory(self), **k)
        self._sub_display_slice = sub_display_slice
        self._parent_display = parent_display

    @lazy_attribute
    def display_slice(self):
        return self._sub_display_slice

    @lazy_attribute
    def display_indexes(self):
        return set(range(*self._sub_display_slice.indices(self._parent_display.width)))

    def _is_visible(self):
        return self in list(map(first, self.resource.proxied_object.owners))

    def update(self):
        if self._is_visible():
            self._parent_display.update()
            return
        else:  # inserted
            return None