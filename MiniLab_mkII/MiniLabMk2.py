# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_mkII\MiniLabMk2.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from _Framework import Task
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Layer import Layer
from _Framework.SubjectSlot import subject_slot
from _Framework.SysexValueControl import SysexValueControl
from _Arturia.ArturiaControlSurface import COLOR_PROPERTY, LIVE_MODE_MSG_HEAD, LOAD_MEMORY_COMMAND, MEMORY_SLOT_PROPERTY, OFF_VALUE, SETUP_MSG_PREFIX, SETUP_MSG_SUFFIX, STORE_IN_MEMORY_COMMAND, WORKING_MEMORY_ID, WRITE_COMMAND, split_list
from MiniLab.MiniLab import MiniLab
from .HardwareSettingsComponent import HardwareSettingsComponent
from .SessionComponent import SessionComponent
ANALOG_LAB_MEMORY_SLOT_ID = 1
LIVE_MEMORY_SLOT_ID = 8

class MiniLabMk2(MiniLab):
    session_component_type = SessionComponent
    encoder_msg_channel = 1
    encoder_msg_ids = (22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 52, 53, 54, 55)
    pad_channel = 10

    def __init__(self, *a, **k):
        pass

    def _create_controls(self):
        super(MiniLabMk2, self)._create_controls()
        self._pad_leds = ButtonMatrixElement(rows=[SysexValueControl(message_prefix=SETUP_MSG_PREFIX + (WRITE_COMMAND, WORKING_MEMORY_ID, COLOR_PROPERTY, column + 112 + row * 8), default_value=(0,), name='Pad_LED_%d' % (column,)) for row in range(2)], name='Pad_LED_Matrix')
        self._memory_slot_selection = SysexValueControl(message_prefix=SETUP_MSG_PREFIX + (MEMORY_SLOT_PROPERTY,), name='Memory_Slot_Selection')
        self._hardware_live_mode_switch = SysexValueControl(message_prefix=LIVE_MODE_MSG_HEAD, default_value=(OFF_VALUE,), name='Hardware_Live_Mode_Switch')

    def _create_hardware_settings(self):
        self._hardware_settings = HardwareSettingsComponent(name='Hardware_Settings', is_enabled=False, layer=Layer(memory_slot_selection=self._memory_slot_selection, hardware_live_mode_switch=self._hardware_live_mode_switch))
        self._on_live_mode_changed.subject = self._hardware_settings
        self._hardware_settings.set_enabled(True)

    def _create_session(self):
        super(MiniLabMk2, self)._create_session()
        self._session.set_enabled(False)
        self._session.set_clip_slot_leds(self._pad_leds)

    @subject_slot('live_mode')
    def _on_live_mode_changed(self, is_live_mode_on):
        self._session.set_enabled(is_live_mode_on)

    def _collect_setup_messages(self):
        super(MiniLabMk2, self)._collect_setup_messages()
        self._messages_to_send.append(SETUP_MSG_PREFIX + (STORE_IN_MEMORY_COMMAND, LIVE_MEMORY_SLOT_ID) + SETUP_MSG_SUFFIX)
        self._messages_to_send.append(SETUP_MSG_PREFIX + (LOAD_MEMORY_COMMAND, ANALOG_LAB_MEMORY_SLOT_ID) + SETUP_MSG_SUFFIX)

    def _setup_hardware(self):

        def send_subsequence(subseq):
            for msg in subseq:
                self._send_midi(msg)
        sequence_to_run = [Task.run(partial(send_subsequence, subsequence)) for subsequence in split_list(self._messages_to_send, 20)]
        self._tasks.add(Task.sequence(*sequence_to_run))
        self._messages_to_send = []