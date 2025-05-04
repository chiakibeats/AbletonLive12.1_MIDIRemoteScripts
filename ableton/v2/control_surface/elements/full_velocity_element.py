# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\full_velocity_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .proxy_element import ProxyElement

class NullFullVelocity(object):
    enabled = False

class FullVelocityElement(ProxyElement):

    def __init__(self, full_velocity=None, *a, **k):
        super(FullVelocityElement, self).__init__(proxied_object=full_velocity, proxied_interface=NullFullVelocity())