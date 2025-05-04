# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_Mini_MK4\elements.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Launchkey_MK4.elements import LaunchkeyCommonElements

class Elements(LaunchkeyCommonElements):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_mono_button(102, 'Track_Left_Button')
        self.add_mono_button(103, 'Track_Right_Button')
        self.add_shifted_control(self.record_button)