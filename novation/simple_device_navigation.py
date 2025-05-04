# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\simple_device_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(Component):
    pass
    next_button = ButtonControl(color='Device.Navigation', pressed_color='Device.NavigationPressed')
    prev_button = ButtonControl(color='Device.Navigation', pressed_color='Device.NavigationPressed')

    @next_button.pressed
    def next_button(self, _):
        self._scroll_device_chain(NavDirection.right)

    @prev_button.pressed
    def prev_button(self, _):
        self._scroll_device_chain(NavDirection.left)

    def _scroll_device_chain(self, direction):
        view = self.application.view
        if not view.is_view_visible('Detail') or not view.is_view_visible('Detail/DeviceChain'):
            view.show_view('Detail')
            view.show_view('Detail/DeviceChain')
            return
        else:
            view.scroll_view(direction, 'Detail/DeviceChain', False)