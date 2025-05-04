# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD226\MPD226.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import cycle
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _MPDMkIIBase.ControlElementUtils import make_button, make_encoder, make_slider
from _MPDMkIIBase.MPDMkIIBase import MPDMkIIBase
PAD_CHANNEL = 1
PAD_IDS = [[81, 83, 84, 86], [74, 76, 77, 79], [67, 69, 71, 72], [60, 62, 64, 65]]

class MPD226(MPDMkIIBase):

    def __init__(self, *a, **k):
        pass

    def _create_controls(self):
        super(MPD226, self)._create_controls()
        self._encoders = ButtonMatrixElement(rows=[[make_encoder(identifier, 0 if index < 4 else 1, 'Encoder_%d' % index) for index, identifier in zip(range(8), cycle(range(22, 26)))]])
        self._sliders = ButtonMatrixElement(rows=[[make_slider(identifier, 0 if index < 4 else 1, 'Slider_%d' % index) for index, identifier in zip(range(8), cycle(range(12, 16)))]])
        self._control_buttons = ButtonMatrixElement(rows=[[make_button(identifier, 0 if index < 4 else 1, 'Control_Button_%d' % index) for index, identifier in zip(range(8), cycle(range(32, 36)))]])
        self._play_button = make_button(118, 0, 'Play_Button')
        self._stop_button = make_button(117, 0, 'Stop_Button')
        self._record_button = make_button(119, 0, 'Record_Button')