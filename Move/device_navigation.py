# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\device_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.components import DeviceNavigationComponent as DeviceNavigationComponentBase
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import DetailViewController

class DeviceNavigationComponent(DeviceNavigationComponentBase):
    pass
    scroll_encoder_touch = ButtonControl(color=None)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._detail_view_controller = DetailViewController(self.application, show_clip=False)
        self._show_device_chain = lambda: None

    @scroll_encoder_touch.value
    def scroll_encoder_touch(self, value, _):
        if self.can_scroll_down() or self.can_scroll_up():
            if value:
                self._detail_view_controller.show()
                return
            else:
                self._detail_view_controller.restore()