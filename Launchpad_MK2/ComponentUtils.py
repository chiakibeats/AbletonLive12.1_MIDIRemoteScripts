# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\ComponentUtils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

def skin_scroll_component(component):
    for button in [component.scroll_up_button, component.scroll_down_button]:
        button.color = 'Scrolling.Enabled'
        button.pressed_color = 'Scrolling.Pressed'
        button.disabled_color = 'Scrolling.Disabled'