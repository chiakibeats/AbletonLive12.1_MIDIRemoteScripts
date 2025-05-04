# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\DisplayController.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import as_ascii
from .consts import *
from .RemoteSLComponent import RemoteSLComponent

class DisplayController(RemoteSLComponent):
    pass

    def __init__(self, remote_sl_parent):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self.__left_strip_names = [str() for x in range(NUM_CONTROLS_PER_ROW)]
        self.__left_strip_parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self.__right_strip_names = [str() for x in range(NUM_CONTROLS_PER_ROW)]
        self.__right_strip_parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self.refresh_state()

    def disconnect(self):
        self.__send_clear_displays()

    def setup_left_display(self, names, parameters):
        pass
        self.__left_strip_names = names
        self.__left_strip_parameters = parameters

    def setup_right_display(self, names, parameters):
        pass
        self.__right_strip_names = names
        self.__right_strip_parameters = parameters

    def update_display(self):
        for row_id in [1, 2, 3, 4]:
            message_string = ''
            if row_id == 1 or row_id == 2:
                if row_id == 1:
                    strip_names = self.__left_strip_names
                else:  # inserted
                    strip_names = self.__right_strip_names
                if len(strip_names) == NUM_CONTROLS_PER_ROW:
                    for s in strip_names:
                        message_string += self.__generate_strip_string(s)
                else:  # inserted
                    message_string += strip_names[0]
            else:  # inserted
                if row_id == 3 or row_id == 4:
                    if row_id == 3:
                        parameters = self.__left_strip_parameters
                    else:  # inserted
                        parameters = self.__right_strip_parameters
                    for p in parameters:
                        if p:
                            message_string += self.__generate_strip_string(str(p))
                            continue
                        else:  # inserted
                            message_string += self.__generate_strip_string('')
                            continue
                    pass
            self.__send_display_string(message_string, row_id, offset=0)
            continue

    def refresh_state(self):
        self.__last_send_row_id_messages = [None, [], [], [], []]

    def __send_clear_displays(self):
        start_clear_sysex = (240, 0, 32, 41, 3, 3, 18, 0)
        left_end_sysex = (ABLETON_PID, 0, 2, 2, 4, 247)
        right_end_sysex = (ABLETON_PID, 0, 2, 2, 5, 247)
        self.send_midi(start_clear_sysex + left_end_sysex)
        self.send_midi(start_clear_sysex + right_end_sysex)

    def __send_display_string(self, message, row_id, offset=0):
        pass
        final_message = ' ' * offset + message
        if len(final_message) < NUM_CHARS_PER_DISPLAY_LINE:
            fill_up = NUM_CHARS_PER_DISPLAY_LINE - len(final_message)
            final_message = final_message + ' ' * fill_up
        else:  # inserted
            if len(final_message) >= NUM_CHARS_PER_DISPLAY_LINE:
                final_message = final_message[0:NUM_CHARS_PER_DISPLAY_LINE]
        final_offset = 0
        sysex_header = (240, 0, 32, 41, 3, 3, 18, 0, ABLETON_PID, 0, 2, 1)
        sysex_pos = (final_offset, row_id)
        sysex_text_command = (4,)
        sysex_text = tuple(as_ascii(final_message))
        sysex_close_up = (247,)
        full_sysex = sysex_header + sysex_pos + sysex_text_command + sysex_text + sysex_close_up
        if self.__last_send_row_id_messages[row_id]!= full_sysex:
            self.__last_send_row_id_messages[row_id] = full_sysex
            self.send_midi(full_sysex)

    def __generate_strip_string(self, display_string):
        pass
        if not display_string:
            return ' ' * NUM_CHARS_PER_DISPLAY_STRIP
        else:  # inserted
            if len(display_string.strip()) > NUM_CHARS_PER_DISPLAY_STRIP - 1 and display_string.endswith('dB') and (display_string.find('.')!= (-1)):
                display_string = display_string[:(-2)]
            if len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1:
                for um in [' ', 'i', 'o', 'u', 'e', 'a']:
                    while len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1 and display_string.rfind(um, 1)!= (-1):
                        um_pos = display_string.rfind(um, 1)
                        display_string = display_string[:um_pos] + display_string[um_pos + 1:]
                                break
                            else:  # inserted
                                continue
                    continue
            else:  # inserted
                display_string = display_string.center(NUM_CHARS_PER_DISPLAY_STRIP - 1)
            return display_string[:NUM_CHARS_PER_DISPLAY_STRIP - 1] + ' '