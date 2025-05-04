# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\analog.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name

class AnalogDeviceDecorator(LiveObjectDecorator, EventObject):

    class OscSelect(IntEnum):
        osc1 = 0
        osc2 = 1

    class EnvSelect(IntEnum):
        amp1 = 0
        amp2 = 1
        flt1 = 2
        flt2 = 3

    class OscAmp(IntEnum):
        osc = 0
        amp = 1

    class LFOSelect(IntEnum):
        lfo1 = 0
        lfo2 = 1

    class GlobalSelect(IntEnum):
        voice = 0
        pitch = 1
        unison = 2
        vibrato = 3

    class ModSelect(IntEnum):
        amp = 0
        filter = 1
        osc = 2

    class ModSelect2(IntEnum):
        amp = 0
        env = 1

    class ModSource(IntEnum):
        key = 0
        vel = 1
        env = 2
        lfo = 3
        pb = 4
        press = 5
        slide = 6

    def __init__(self, *a, **k):
        super(AnalogDeviceDecorator, self).__init__(*a, **k)
        self._add_enum_parameter(name='Env Select', values=['Amp 1', 'Amp 2', 'Flt 1', 'Flt 2'], default_value=self.EnvSelect.amp1)
        self._add_enum_parameter(name='Osc Select', values=['Osc 1', 'Osc 2'], default_value=self.OscSelect.osc1)
        self._add_enum_parameter(name='Osc / Amp', values=['Osc', 'Amp'], default_value=self.OscAmp.osc)
        self._add_enum_parameter(name='LFO Select', values=['LFO 1', 'LFO 2'], default_value=self.LFOSelect.lfo1)
        self._add_enum_parameter(name='Select', values=['Voice', 'Pitch', 'Unison', 'Vibrato'], default_value=self.GlobalSelect.voice)
        self._add_enum_parameter(name='Mod Dest', values=['Amp', 'Filter', 'Osc'], default_value=self.ModSelect.amp)
        self._add_enum_parameter(name='Mod Dest Vel', values=['Amp/Flt', 'Env'], default_value=self.ModSelect2.amp)
        self._add_enum_parameter(name='Mod Source', values=['Key', 'Vel', 'Env', 'LFO', 'PB', 'Press', 'Slide'], default_value=self.ModSource.key)
        self._add_switch_option(name='OSC1 Mode', pname='OSC1 Mode', labels=['Sub', 'Sync'])
        self._add_switch_option(name='OSC2 Mode', pname='OSC2 Mode', labels=['Sub', 'Sync'])
        self._add_switch_option(name='AEG1 Exp', pname='AEG1 Exp', labels=['Lin', 'Exp'])
        self._add_switch_option(name='AEG2 Exp', pname='AEG2 Exp', labels=['Lin', 'Exp'])
        self._add_switch_option(name='FEG1 Exp', pname='FEG1 Exp', labels=['Lin', 'Exp'])
        self._add_switch_option(name='FEG2 Exp', pname='FEG2 Exp', labels=['Lin', 'Exp'])
        self._add_switch_option(name='LFO1 Sync', pname='LFO1 Sync', labels=['Hertz', 'Beat'])
        self._add_switch_option(name='LFO2 Sync', pname='LFO2 Sync', labels=['Hertz', 'Beat'])
        self._add_on_off_option(name='Osc 1', pname='OSC1 On/Off')
        self._add_on_off_option(name='Osc 2', pname='OSC2 On/Off')
        self._add_on_off_option(name='Noise', pname='Noise On/Off')
        self._add_on_off_option(name='Amp 1', pname='AMP1 On/Off')
        self._add_on_off_option(name='Amp 2', pname='AMP2 On/Off')
        self._add_on_off_option(name='Filter 1', pname='F1 On/Off')
        self._add_on_off_option(name='Filter 2', pname='F2 On/Off')
        self._add_on_off_option(name='Flt 2 Follow', pname='F2 Slave')
        self._add_on_off_option(name='Amp 1 Legato', pname='AEG1 Legato')
        self._add_on_off_option(name='Amp 2 Legato', pname='AEG2 Legato')
        self._add_on_off_option(name='Flt 1 Legato', pname='FEG1 Legato')
        self._add_on_off_option(name='Flt 2 Legato', pname='FEG2 Legato')
        self._add_on_off_option(name='Amp 1 Free', pname='AEG1 Free')
        self._add_on_off_option(name='Amp 2 Free', pname='AEG2 Free')
        self._add_on_off_option(name='Flt 1 Free', pname='FEG1 Free')
        self._add_on_off_option(name='Flt 2 Free', pname='FEG2 Free')
        self._add_on_off_option(name='LFO 1', pname='LFO1 On/Off')
        self._add_on_off_option(name='LFO 2', pname='LFO2 On/Off')
        self._add_on_off_option(name='LFO 1 Retrig', pname='LFO1 Retrig')
        self._add_on_off_option(name='LFO 2 Retrig', pname='LFO2 Retrig')
        self._add_on_off_option(name='Glide', pname='Glide On/Off')
        self._add_on_off_option(name='Unison', pname='Unison On/Off')
        self._add_on_off_option(name='Vibrato', pname='Vib On/Off')
        self._add_on_off_option(name='Legato', pname='Glide Legato')
        self.register_disconnectables(self.options)