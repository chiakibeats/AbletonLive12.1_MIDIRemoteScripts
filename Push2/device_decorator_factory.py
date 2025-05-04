# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_decorator_factory.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .amp import AmpDeviceDecorator
from .analog import AnalogDeviceDecorator
from .auto_filter import AutoFilterDeviceDecorator
from .beatrepeat import BeatRepeatDeviceDecorator
from .cccontrol import CcControlDeviceDecorator
from .chorus2 import Chorus2DeviceDecorator
from .collision import CollisionDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .corpus import CorpusDeviceDecorator
from .delay import DelayDeviceDecorator
from .device_decoration import DrumBussDeviceDecorator, PedalDeviceDecorator, SamplerDeviceDecorator, UtilityDeviceDecorator
from .drift import DriftDeviceDecorator
from .drumcell import DrumCellDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq3 import EqThreeDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .filterdelay import FilterDelayDeviceDecorator
from .graindelay import GrainDelayDeviceDecorator
from .hybrid_reverb import HybridReverbDeviceDecorator
from .meld import MeldDeviceDecorator
from .operator import OperatorDeviceDecorator
from .phasernew import PhaserNewDeviceDecorator
from .redux2 import Redux2DeviceDecorator
from .resonator import ResonatorDeviceDecorator
from .reverb import ReverbDeviceDecorator
from .roar import RoarDeviceDecorator
from .saturator import SaturatorDeviceDecorator
from .shifter import ShifterDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .tension import TensionDeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .velocity import VelocityDeviceDecorator
from .vinyl import VinylDistortionDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    BeatRepeat = {'Amp': AmpDeviceDecorator, 'AutoFilter': AutoFilterDeviceDecorator, 'BeatRepeat': BeatRepeatDeviceDecorator, 'Chorus2': Chorus2DeviceDecorator, 'Collision': CollisionDeviceDecorator, 'Compressor2': CompressorDeviceDecorator, 'Corpus': CorpusDeviceDecorator, 'Delay': DelayDeviceDecorator, 'Drift': DriftDeviceDecorator, 'DrumBuss': DrumBussDeviceDecorator, 'FilterEQ3': EqThreeDeviceDecorator, 'GrainDelay': GrainDelayDeviceDecorator, 'InstrumentVector': WavetableDeviceDecorator, 'InstrumentMeld': MeldDeviceDecorator, 'Operator': OperatorDeviceDecorator, 'Pedal': PedalDeviceDecorator, 'PhaserNew': PhaserNewDeviceDecorator, 'Redux2': Redux2DeviceDecorator, 'Resonator': ResonatorDeviceDecorator, 'Reverb': ReverbDeviceDecorator, 'Roar': RoarDeviceDecorator, 'RoarDeviceDecorator': SaturatorDeviceDecorator, 'Saturator': Spectral, 'SpectralDeviceDecorator': SpectralDeviceDecorator, 'StereoGain': UtilityDeviceDecorator, 'UtilityDeviceDecorator': StringStudio, 'TensionDeviceDecorator': TensionDeviceDecorator, 'Shifter': ShifterDeviceDecorator, 'TransmuteDeviceDecorator': AnalogDeviceDecorator, 'VelocityDeviceDecorator': VinylDistortionDecorator, 'Transmute': Transmute, 'UltraAnalog'