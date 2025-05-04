# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\color.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import EventObject, listenable_property, listens, liveobj_valid, nop, old_hasattr

def to_midi_value(int_or_color):
    if old_hasattr(int_or_color, 'midi_value'):
        return int_or_color.midi_value
    else:
        return int(int_or_color)

class Color(object):
    pass
    midi_value = 0

    def __init__(self, midi_value=None, *a, **k):
        super(Color, self).__init__(*a, **k)
        if midi_value is not None:
            self.midi_value = midi_value

    def draw(self, interface):
        pass
        interface.send_value(self.midi_value)

class DynamicColorFactory(object):

    def __init__(self, transformation=nop, *a, **k):
        super(DynamicColorFactory, self).__init__(*a, **k)
        self._transform = transformation

    def instantiate(self, song):
        raise NotImplementedError

def is_dynamic_color_factory(skin_element):
    return isinstance(skin_element, DynamicColorFactory)

class DynamicColorBase(Color, EventObject):
    midi_value = listenable_property.managed(0)

    def __init__(self, transformation=nop, *a, **k):
        super(DynamicColorBase, self).__init__(*a, **k)
        self._transformation = transformation

    def _update_midi_value(self, colored_object):
        color_index = colored_object.color_index if liveobj_valid(colored_object) else None
        self.midi_value = self._transformation(color_index)

class SelectedTrackColor(DynamicColorBase):

    def __init__(self, song_view=None, *a, **k):
        super(SelectedTrackColor, self).__init__(*a, **k)
        self.__on_color_changed.subject = song_view
        self.__on_color_changed()

    @listens('selected_track.color_index')
    def __on_color_changed(self, *a):
        self._update_midi_value(self.__on_color_changed.subject.selected_track)

class SelectedClipColor(DynamicColorBase):

    def __init__(self, song_view=None, *a, **k):
        super(SelectedClipColor, self).__init__(*a, **k)
        self.__on_color_changed.subject = song_view
        self.__on_color_changed()

    @listens('detail_clip.color_index')
    def __on_color_changed(self, *a):
        view = self.__on_color_changed.subject
        self._update_midi_value(view.detail_clip)

class SelectedTrackColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedTrackColor(song_view=song.view, transformation=self._transform)

class SelectedClipColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedClipColor(song_view=song.view, transformation=self._transform)

class AnimatedColor(Color):
    _channel = None

    def __init__(self, color1=None, color2=None, *a, **k):
        super(AnimatedColor, self).__init__(*a, **k)
        self._color1 = color1
        self._color2 = color2

    def draw(self, interface):
        interface.send_value(self._color1.midi_value)
        interface.send_value(self._color2.midi_value, channel=self._channel)

class SysexRGBColor(Color):

    def __init__(self, midi_value=None, *a, **k):
        super(SysexRGBColor, self).__init__(midi_value, *a, **k)