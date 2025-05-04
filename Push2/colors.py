# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from colorsys import hsv_to_rgb, rgb_to_hsv
import MidiRemoteScript
from ableton.v2.base import depends, in_range, listens, liveobj_valid, nop, old_round
from ableton.v2.control_surface.elements.color import DynamicColorBase, DynamicColorFactory
from pushbase.colors import Blink, FallbackColor, Pulse, PushColor, TransparentColor
from .device_util import find_chain_or_track
WHITE_MIDI_VALUE = 122
TRANSLATED_WHITE_INDEX = 7
WHITE_COLOR_INDEX_FROM_LIVE = 13
UNCOLORED_INDEX = WHITE_COLOR_INDEX_FROM_LIVE
HALFLIT_WHITE_MIDI = 14
DISPLAY_BUTTON_SHADE_LEVEL = 1

def make_pulsing_track_color(track, pulse_to_color):
    return Pulse(pulse_to_color, IndexedColor.from_live_index(track.color_index), 48)

def make_blinking_track_color(track, blink_to_color):
    return Blink(blink_to_color, IndexedColor.from_live_index(track.color_index), 24)

def determine_shaded_color_index(color_index, shade_level):
    if shade_level == 0:
        return color_index
    else:  # inserted
        if color_index == WHITE_MIDI_VALUE:
            return color_index + shade_level
        else:  # inserted
            return (color_index - 1) * 2 + 64 + shade_level

class IndexedColor(PushColor):
    needs_rgb_interface = True
    midi_value = None

    def __init__(self, index=None, *a, **k):
        super(IndexedColor, self).__init__(*a, midi_value=index, **k)

    @staticmethod
    def from_push_index(index, shade_level=0):
        return IndexedColor(determine_shaded_color_index(index, shade_level))

    @staticmethod
    def from_live_index(index, shade_level=0):
        return IndexedColor(determine_shaded_color_index(translate_color_index(index), shade_level))

def translate_color_index(index):
    pass
    try:
        return COLOR_INDEX_TO_PUSH_INDEX[index] if index > (-1) else TRANSLATED_WHITE_INDEX
    except:
        return TRANSLATED_WHITE_INDEX

def inverse_translate_color_index(translated_index):
    pass
    return PUSH_INDEX_TO_COLOR_INDEX[translated_index - 1]

class SelectedDrumPadColor(DynamicColorBase):
    pass

    @depends(percussion_instrument_finder=nop)
    def __init__(self, song=None, percussion_instrument_finder=None, *a, **k):
        super(SelectedDrumPadColor, self).__init__(*a, **k)
        self.song = song
        if percussion_instrument_finder is not None:
            self.__on_selected_track_color_index_changed.subject = self.song.view
            self.__on_instrument_changed.subject = percussion_instrument_finder
            self.__on_instrument_changed()

    @listens('instrument')
    def __on_instrument_changed(self):
        drum_group = self.__on_instrument_changed.subject.drum_group
        if liveobj_valid(drum_group):
            self.__on_selected_drum_pad_chains_changed.subject = drum_group.view
            self.__on_selected_drum_pad_chains_changed()

    @listens('selected_drum_pad.chains')
    def __on_selected_drum_pad_chains_changed(self):
        drum_pad = self.__on_selected_drum_pad_chains_changed.subject.selected_drum_pad
        if liveobj_valid(drum_pad) and drum_pad.chains:
            self.__on_color_index_changed.subject = drum_pad.chains[0]
            self.__on_color_index_changed()
            return
        else:  # inserted
            self._update_midi_value(self.song.view.selected_track)

    @listens('color_index')
    def __on_color_index_changed(self):
        chain = self.__on_color_index_changed.subject
        self._update_midi_value(chain)

    @listens('selected_track.color_index')
    def __on_selected_track_color_index_changed(self):
        drum_group = self.__on_selected_drum_pad_chains_changed.subject
        drum_pad = drum_group.selected_drum_pad if liveobj_valid(drum_group) else None
        if not liveobj_valid(drum_pad) or not drum_pad.chains:
            self._update_midi_value(self.song.view.selected_track)

class SelectedDrumPadColorFactory(DynamicColorFactory):
    def instantiate(self, song):
        return SelectedDrumPadColor(song=song, transformation=self._transform)

class SelectedDeviceChainColor(DynamicColorBase):
    @depends(device_provider=nop)
    def __init__(self, device_provider=None, *a, **k):
        super(SelectedDeviceChainColor, self).__init__(*a, **k)
        if device_provider is not None:
            self.__on_device_changed.subject = device_provider
            self.__on_device_changed()

    @listens('device')
    def __on_device_changed(self):
        device = self.__on_device_changed.subject.device
        chain = find_chain_or_track(device)
        self.__on_chain_color_index_changed.subject = chain
        self.__on_chain_color_index_changed()

    @listens('color_index')
    def __on_chain_color_index_changed(self):
        chain = self.__on_chain_color_index_changed.subject
        if liveobj_valid(chain):
            self._update_midi_value(chain)
            return
        else:  # inserted
            return None

class SelectedDeviceChainColorFactory(DynamicColorFactory):
    def instantiate(self, song):
        return SelectedDeviceChainColor(transformation=self._transform)

def make_color_factory_func(factory_class):
    def make_color_factory(shade_level=0):
        return factory_class(transformation=lambda color_index: determine_shaded_color_index(translate_color_index(color_index), shade_level))
    return make_color_factory

class Rgb(object):
    AMBER = IndexedColor(3)
    AMBER_SHADE = IndexedColor(69)
    AMBER_SHADE_TWO = IndexedColor(70)
    YELLOW = IndexedColor(6)
    YELLOW_SHADE = IndexedColor(75)
    YELLOW_SHADE_TWO = IndexedColor(76)
    YELLOW_HIGHLIGHT = IndexedColor(40)
    PURPLE = IndexedColor(49)
    OCEAN = IndexedColor(33)
    DEEP_OCEAN = IndexedColor(95)
    SKY = IndexedColor(46)
    GREEN = IndexedColor(126)
    GREEN_SHADE = IndexedColor(32)
    RED = IndexedColor(127)
    RED_SHADE = IndexedColor(27)
    RED_SHADE_TWO = IndexedColor(66)
    BLUE = IndexedColor(125)
    LIGHT_GREY = IndexedColor(123)
    DARK_GREY = IndexedColor(124)
    BLACK = IndexedColor(0)
    WHITE = IndexedColor(WHITE_MIDI_VALUE)

class Basic(object):
    HALF = FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)
    FULL_BLINK_SLOW = Blink(FallbackColor(Rgb.WHITE, 127), FallbackColor(Rgb.BLACK, 0), 24)
    FULL_PULSE_SLOW = Pulse(FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI), FallbackColor(Rgb.WHITE, 127), 48)
    FAST_PULSE = Pulse(FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI), FallbackColor(Rgb.WHITE, 127), 24)
    TRANSPARENT = TransparentColor()

class ScreenColor(object):
    pass

    def __init__(self, red, green, blue):
        super(ScreenColor, self).__init__()
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def from_hsv(*hsv):
        pass
        return ScreenColor(*hsv_to_rgb(*hsv)).denormalise()

    def as_hsv(self):
        pass
        return rgb_to_hsv(*self.normalise().as_tuple())

    def as_tuple(self):
        pass
        return (self.red, self.green, self.blue)

    def as_remote_script_color(self, alpha=255):
        pass
        return MidiRemoteScript.RgbaColor(self.red, self.green, self.blue, alpha)

    def map_channels(self, map_function):
        pass
        return ScreenColor(map_function(self.red), map_function(self.green), map_function(self.blue))

    def shade(self, amount):
        pass
        scale = 1.0 - amount
        return self.map_channels(lambda component: int(old_round(component * scale)))

    def normalise(self):
        pass
        return self.map_channels(lambda component: old_div(float(component), 255.0))

    def denormalise(self):
        pass
        return self.map_channels(lambda component: int(old_round(255 * component)))

    def adjust_saturation(self, amount):
        pass
        h, s, v = self.as_hsv()
        s *= 1.0 + amount
        return ScreenColor.from_hsv(h, s, v)
COLOR_INDEX_TO_PUSH_INDEX = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 7, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 5, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 22, 25, 17, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 21, 2, 4, 6, 8, 10, 12, 14, 20, 19, 18, 22, 23, 26, 6)
PUSH_INDEX_TO_SCREEN_COLOR = (ScreenColor(255, 255, 255), ScreenColor(237, 89, 56), ScreenColor(209, 23, 10), ScreenColor(255, 100, 0), ScreenColor(255, 50, 0), ScreenColor(128, 71, 19), ScreenColor(88, 35, 7), ScreenColor(0, 218, 60), ScreenColor(0, 187, 173), ScreenColor(0, 106, 202), ScreenColor(171, 80, 255), ScreenColor(225, 87, 227), ScreenColor(255, 30, 50), ScreenColor(255, 74, 150), ScreenColor(255, PUSH_INDEX_TO_SCREEN_COLOR, 137), ScreenColor(255, 187, 173), ScreenColor(255, 164, <mask_62>), ScreenColor(255, 202, <mask_64>), ScreenColor(255, 179, <mask_66>), ScreenColor(255, <mask_67>, <mask_68>), ScreenColor(255, <mask_69>, 221), ScreenColor
COLOR_INDEX_TO_SCREEN_COLOR = tuple([PUSH_INDEX_TO_SCREEN_COLOR[push_index] for push_index in COLOR_INDEX_TO_PUSH_INDEX])
COLOR_INDEX_TO_SCREEN_COLOR_SHADES = [tuple([color.shade(0.2) for color in COLOR_INDEX_TO_SCREEN_COLOR]), tuple([color.shade(0.5) for color in COLOR_INDEX_TO_SCREEN_COLOR]), tuple([color.shade(0.7).adjust_saturation((-0.2)) for color in COLOR_INDEX_TO_SCREEN_COLOR]), tuple([color.adjust_saturation((-0.7)) for color in COLOR_INDEX_TO_SCREEN_COLOR])]
PUSH_INDEX_TO_COLOR_INDEX = (0, 14, 1, 15, 2, 16, 3, 17, 4, 18, 5, 19, 6, 20, 7, 21, 8, 22, 9, 23, 10, 24, 11, 25, 12, 26)
for 7995160 in ((0, 0, 0), (1, 16728114, 2), (2, 8389632, 4), (3, 13188096, 6), (4, 11280128, 8), (5, 9195544, 10), (6, 4790276, 12), (7, 16440379, 14), (8, 16762134, 16), (9, 11992846, 18), (10, 7995160, 20), (11, 3457558, 22), (5212676, 24, 13), (24, 6487893, 26), (2719059, 28, 15), (2530930, 30, 3255807), (32, 17, 3564540), (34, 1717503, 36), (19, 1838310, 38), (1391001, 40, 21), (3749887, 42, 5710591), (44, 23, 9907199), (46, 8724856, 48),