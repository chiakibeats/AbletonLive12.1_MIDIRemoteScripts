# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\menu_modes.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listenable_property, listens
from ableton.v3.control_surface.controls import ButtonControl, StepEncoderControl
from ableton.v3.control_surface.mode import ModesComponent
from .menu import create_scale_menu, create_settings_menu, create_workflow_menu
from .menu_cursor import MenuCursor

class MenuModesComponent(ModesComponent):
    pass
    wheel = StepEncoderControl(num_steps=64)
    wheel_push_button = ButtonControl(color=None)
    back_button = ButtonControl(color='DefaultButton.Back', pressed_color='DefaultButton.Pressed')
    menu_content = listenable_property.managed(None)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._menus = {'settings_menu': create_settings_menu(self), 'scale_menu': create_scale_menu(self), 'workflow_menu': create_workflow_menu(self)}
        self._menu_cursor = self.register_disconnectable(MenuCursor())
        self.wheel.connect_property(self._menu_cursor, 'position')
        self.__on_menu_cursor_content_changed.subject = self._menu_cursor

    def go_back(self, **k):
        pass
        if self._menu_cursor.can_go_back():
            self._menu_cursor.go_back(**k)
            return
        else:
            self.selected_mode = self._mode_list[0]

    @back_button.pressed
    def back_button(self, _):
        self.go_back()

    @wheel_push_button.pressed
    def wheel_push_button(self, _):
        if self._menu_cursor.menu is None:
            self.selected_mode = self._mode_list[0]
        else:
            self._menu_cursor.click()

    def notify_selected_mode(self, mode):
        super().notify_selected_mode(mode)
        self._menu_cursor.menu = self._menus.get(mode, None)
        self.wheel.enabled = self._menu_cursor.menu is not None
        if mode != self._mode_list[0]:
            self.suppress_notifications()

    def _update_mode_controls(self, selected_mode):
        super()._update_mode_controls(selected_mode)
        self.back_button.enabled = selected_mode != self._mode_list[0]

    def update_menu(self, menu):
        if self._menu_cursor.menu == menu:
            self.__on_menu_cursor_content_changed()

    @listens('content')
    def __on_menu_cursor_content_changed(self):
        self.menu_content = self._menu_cursor.get_content() if self._menu_cursor.menu else None