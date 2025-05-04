# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\focus_follow.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Live.PluginDevice import PluginDevice
from ableton.v3.control_surface import InstrumentFinderComponent, find_instrument_meeting_requirement
from ableton.v3.control_surface.controls import SendValueControl
from ableton.v3.live import liveobj_valid
PLUGIN_NAME_PREFIXES = ('Komplete Kontrol', 'Kontakt')
KONTAKT_PARAMETER_NAME_PREFIX = 'NIKT'

def get_parameter_name_for_instance(instance):
    param_names = instance.get_parameter_names()
    if param_names:
        if instance.name.startswith('Komplete Kontrol'):
            return param_names[0]
        else:
            for index in [2048, 4096]:
                if index < len(param_names) and param_names[index].startswith(KONTAKT_PARAMETER_NAME_PREFIX):
                    return param_names[index]
                else:
                    continue
    return ''

class FocusFollowComponent(InstrumentFinderComponent):
    pass
    focus_follow_control = SendValueControl()

    def _update_instruments(self):
        instance = find_instrument_meeting_requirement(lambda d: isinstance(d, PluginDevice) and d.name.startswith(PLUGIN_NAME_PREFIXES), self._target_track.target_track)
        param_name = ''
        if liveobj_valid(instance):
            param_name = get_parameter_name_for_instance(instance)
        self.focus_follow_control.value = tuple((ord(n) for n in param_name))
        return