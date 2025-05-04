# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\auto_arm.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.components import AutoArmComponent as AutoArmComponentBase
from ableton.v3.control_surface.components.auto_arm import track_can_be_auto_armed

class AutoArmComponent(AutoArmComponentBase):
    pass

    def restore_auto_arm(self):
        if self.application.number_of_push_apps_running == 0 and self.needs_restore_auto_arm:
                song = self.song
                exclusive_arm = song.exclusive_arm
                for track in song.tracks:
                    if exclusive_arm or track_can_be_auto_armed(track):
                        if track.can_be_armed:
                            track.arm = False
                    pass
                    continue
            else:  # inserted
                return
        else:  # inserted
            return None