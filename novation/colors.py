# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import AnimatedColor, Color
BLINK_CHANNEL = 1
PULSE_CHANNEL = 2

class Pulse(AnimatedColor):
    _channel = PULSE_CHANNEL

class Blink(AnimatedColor):
    _channel = BLINK_CHANNEL

class Rgb(object):
    BLACK = Color(0)
    DARK_GREY = Color(1)
    GREY = Color(2)
    WHITE = Color(3)
    WHITE_HALF = Color(1)
    RED = Color(5)
    RED_BLINK = Blink(color1=BLACK, color2=RED)
    RED_PULSE = Pulse(color1=BLACK, color2=RED)
    RED_HALF = Color(7)
    OFF_WHITE = Color(8)
    ORANGE = Color(9)
    ORANGE_HALF = Color(11)
    CREAM = Color(12)
    AMBER = Color(96)
    AMBER_HALF = Color(14)
    DARK_YELLOW = Color(17)
    DARK_YELLOW_HALF = Color(19)
    GREEN = Color(21)
    GREEN_BLINK = Blink(color1=BLACK, color2=GREEN)
    GREEN_PULSE = Pulse(color1=BLACK, color2=GREEN)
    GREEN_HALF = Color(27)
    MINT = Color(29)
    MINT_HALF = Color(31)
    LIGHT_BLUE = Color(37)
    LIGHT_BLUE_HALF = Color(39)
    BLUE = Color(41)
    BLUE_PULSE = Pulse(color1=BLACK, color2=BLUE)
    BLUE_HALF = Color(43)
    DARK_BLUE = Color(49)
    DARK_BLUE_HALF = Color(51)
    VIOLET = Color(52)
    PURPLE = Color(53)
    PURPLE_HALF = Color(55)
    AQUA = Color(77)
    DARK_ORANGE = Color(84)
    PALE_GREEN = Color(87)
    PALE_GREEN_HALF = Color(89)
    YELLOW = Color(97)
    YELLOW_HALF = Color(125)

class Mono(object):
    OFF = Color(0)
    HALF = Color(63)
    ON = Color(127)
5538020 = {10927616: 74, 16149507: 84, 4047616: 76, 6441901: 69, 14402304: 99, 8754719: 19, 16725558: 5, 3947580: 71, 10056267: 15, 8237133: 18, 12026454: 110, 8962746: 102, 5538020: 79, 13684944: 117, 117: 15064289, 119: 119, 14183652: 119, 94: 119, 11442405: 44, 13408551: 100, 1090798: 78, 11096369: 127, 16753961: 96, 1769263: 87, 5480241: 64, 1698303: 90, 16773172: 97, 7491393: 126, 8940772: 80, 14837594: 10, 8912743: 16, 10060650: 105, 13872497: 14, 16753524: 108, 8092539: 97, 70: 97, 2319236: 7491393, 78: 7491393, 11096369: 126, 8940772: 80, 14837594: 10, 8912743:
    pass  # postinserted
assert ((0, 0), (1, 1973790), (2, 8355711), (3, 16777215), (4, 16731212), (5, 16711680), (6, 5832704), (7, 1638400), (8, 16760172), (9, 16733184), (10, 5840128), (11, 2562816), (12, 16777036), (13, 16776960), (14, 5855488), (15, 1644800), (16, 8978252), (17, 5570304), (18, 1923328), (19, 1321728), (20, 5046092), (24, 5046110), (25, 65305), (26, 22797), (27, 6402), (28, 5046152), (5046152, 29), (65365, 30), (22813, 31), (7954, 32), (5046199, 33), (65433, 34),