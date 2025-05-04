# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from past.utils import old_div
from itertools import repeat
from ableton.v2.control_surface.elements import Color, to_midi_value

class PushColor(Color):
    needs_rgb_interface = False

    def can_draw_on_interface(self, interface):
        return not self.needs_rgb_interface or interface.is_rgb

    def draw(self, interface):
        super(PushColor, self).draw(interface)

class RgbColor(PushColor):
    pass
    needs_rgb_interface = True
    _rgb_value = (0, 0, 0)

    def __init__(self, midi_value=None, rgb_value=None, *a, **k):
        super(RgbColor, self).__init__(*a, midi_value=midi_value, **k)
        if rgb_value is not None:
            self._rgb_value = rgb_value

    def shade(self, shade_level):
        pass
        shade_factor = old_div(1.0, 2.0) * (2 - shade_level)
        return RgbColor(self.midi_value + shade_level, [a * b for a, b in zip(self._rgb_value, repeat(shade_factor))])

    def highlight(self):
        pass
        return RgbColor(self.midi_value - 1, [a * b for a, b in zip(self._rgb_value, repeat(1.5))])

    def __iter__(self):
        return iter(self._rgb_value)

    def __getitem__(self, index_or_slice):
        return self._rgb_value[index_or_slice]

class FallbackColor(PushColor):
    pass

    def __init__(self, default_color=None, fallback_color=None, *a, **k):
        super(FallbackColor, self).__init__(*a, midi_value=to_midi_value(fallback_color), **k)
        self.default_color = default_color

    def draw(self, interface):
        if self.default_color.can_draw_on_interface(interface):
            self.default_color.draw(interface)
            return
        else:  # inserted
            super(FallbackColor, self).draw(interface)

class AnimatedColor(PushColor):
    pass

    @property
    def midi_value(self):
        return self.convert_to_midi_value()

    def __init__(self, color1=RgbColor(), color2=RgbColor(), channel2=7, *a, **k):
        super(AnimatedColor, self).__init__(*a, **k)
        self.color1 = color1
        self.color2 = color2
        self.channel2 = channel2

    def can_draw_on_interface(self, interface):
        return self.color1.can_draw_on_interface(interface) and self.color2.can_draw_on_interface(interface)

    def draw(self, interface):
        interface.send_value(self.color1.midi_value)
        interface.send_value(self.color2.midi_value, channel=self.channel2)

    def convert_to_midi_value(self):
        raise NotImplementedError('Animations cannot be serialized')

class Pulse(AnimatedColor):
    pass

    def __init__(self, color1=RgbColor(), color2=RgbColor(), speed=6, *a, **k):
        channel2 = [4, 6, 12, 24, 48].index(speed) + 6
        super(Pulse, self).__init__(*a, color1=color1, color2=color2, channel2=channel2, **k)

class Blink(AnimatedColor):
    pass

    def __init__(self, color1=0, color2=0, speed=6, *a, **k):
        channel2 = [4, 6, 12, 24, 48].index(speed) + 11
        super(Blink, self).__init__(*a, color1=color1, color2=color2, channel2=channel2, **k)

class TransparentColor(object):
    pass

    def draw(self, interface):
        return

class Rgb(object):
    pass
    BLACK = RgbColor(0)
    DARK_GREY = RgbColor(1)
    GREY = RgbColor(2)
    WHITE = RgbColor(3)
    RED = RgbColor(5)
    AMBER = RgbColor(9)
    YELLOW = RgbColor(13)
    LIME = RgbColor(17)
    GREEN = RgbColor(21)
    SPRING = RgbColor(25)
    TURQUOISE = RgbColor(29)
    CYAN = RgbColor(33)
    SKY = RgbColor(37)
    OCEAN = RgbColor(41)
    BLUE = RgbColor(45)
    ORCHID = RgbColor(49)
    MAGENTA = RgbColor(53)
    PINK = RgbColor(57)

class Basic(object):
    pass
    HALF = FallbackColor(Rgb.DARK_GREY, 1)
    HALF_BLINK_SLOW = FallbackColor(Blink(Rgb.DARK_GREY, Rgb.BLACK, 4), 2)
    HALF_BLINK_FAST = FallbackColor(Blink(Rgb.DARK_GREY, Rgb.BLACK, 24), 3)
    FULL = FallbackColor(Rgb.WHITE, 4)
    FULL_BLINK_SLOW = FallbackColor(Blink(Rgb.WHITE, Rgb.BLACK, 4), 5)
    FULL_BLINK_FAST = FallbackColor(Blink(Rgb.WHITE, Rgb.BLACK, 24), 6)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)
    TRANSPARENT = TransparentColor()

class BiLed(object):
    pass
    GREEN = FallbackColor(RgbColor(122), 22)
    GREEN_HALF = FallbackColor(RgbColor(123), 19)
    GREEN_BLINK_SLOW = FallbackColor(Blink(RgbColor(122), Rgb.BLACK, 4), 23)
    GREEN_BLINK_FAST = FallbackColor(Blink(RgbColor(122), Rgb.BLACK, 24), 24)
    RED = FallbackColor(RgbColor(120), 4)
    RED_HALF = FallbackColor(RgbColor(121), 1)
    RED_BLINK_SLOW = FallbackColor(Blink(RgbColor(120), Rgb.BLACK, 4), 5)
    RED_BLINK_FAST = FallbackColor(Blink(RgbColor(120), Rgb.BLACK, 24), 6)
    YELLOW = FallbackColor(RgbColor(124), 16)
    YELLOW_HALF = FallbackColor(RgbColor(125), 13)
    YELLOW_BLINK_SLOW = FallbackColor(Blink(RgbColor(124), Rgb.BLACK, 4), 17)
    YELLOW_BLINK_FAST = FallbackColor(Blink(RgbColor(124), Rgb.BLACK, 24), 18)
    AMBER = FallbackColor(RgbColor(126), 10)
    AMBER_HALF = FallbackColor(RgbColor(127), 7)
    AMBER_BLINK_SLOW = FallbackColor(Blink(RgbColor(126), Rgb.BLACK, 4), 11)
    AMBER_BLINK_FAST = FallbackColor(Blink(RgbColor(126), Rgb.BLACK, 24), 12)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)
LIVE_COLORS_TO_MIDI_VALUES = {10927616: 74, 16149507: 84, 4047616: 76, 6441901: 69, 14402304: 99, 8754719: 19, 16725558: 5, 3947580: 71, 10056267: 15, 8237133: 18, 12026454: 110, 8962746: 102, 5538020: 79, 13684944: 117, 15064289: 119, 119: 119, 119: 14183652, 94: 11442405, 44: 13408551, 100: 1090798, 78: 11096369, 127: 16753961, 96: 1769263, 87: 5480241, 64: 1698303, 90: 16773172, 97: 7491393, 126: 8940772, 80: 14837594, 10: 8912743, 16: 10060650, 105: 13872497, 14: 16753524, 108: 8092539, 70: 70, 2319236: 70, 39: 70, 1716118: 70, 47: 70, 12349846: 70, 59: 70, 11481907:
    pass  # postinserted
assert ((0, 0), (1, 1973790), (2, 8355711), (3, 16777215), (4, 16731212), (5, 16711680), (6, 5832704), (7, 1638400), (8, 16760172), (9, 16733184), (10, 5840128), (11, 2562816), (12, 16777036), (13, 16776960), (14, 5855488), (15, 1644800), (16, 8978252), (17, 5570304), (18, 1923328), (19, 1321728), (20, 5046092), (24, 5046110), (25, 65305), (26, 22797), (27, 6402), (28, 5046152), (5046152, 29), (65365, 30), (22813, 31), (7954, 32), (5046199, 33), (65433, 34),