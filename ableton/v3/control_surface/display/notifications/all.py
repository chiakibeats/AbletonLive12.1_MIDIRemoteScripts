# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\notifications\all.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from __future__ import annotations
from typing import NewType
from Live.ClipSlot import ClipSlot
from ....base import pitch_index_to_string
from ....live import display_name, major_version
from .type_decl import Fn, Notification, _DefaultText, _TransformDefaultText
from .util import toggle_text_generator
SceneName = NewType('SceneName', str)
TrackName = NewType('TrackName', str)
ClipName = NewType('ClipName', str)
DeviceName = NewType('DeviceName', str)
DeviceBank = NewType('DeviceBank', str)
PadName = NewType('PadName', str)
ComponentName = NewType('ComponentName', str)
ModeName = NewType('ModeName', str)
Subdivision = NewType('Subdivision', str)
Resolution = NewType('Resolution', str)
Range = NewType('Range', str)
RangeName = NewType('RangeName', str)

class Notifications:
    pass
    identify: Notification = lambda: 'Live {}\nConnected'.format(major_version())
    full_velocity: Notification[Fn[bool]] = toggle_text_generator('Full Velocity\n{}')
    note_repeat: Notification[Fn[bool]] = toggle_text_generator('Note Repeat\n{}')
    controlled_range: Notification[Fn[RangeName, Range]] = '{}\n{}'.format
    generic: Notification[Fn[str]] = '{}'.format

    class Element:
        button_lock: Notification[Fn[str, bool]] = lambda name, state: '{}\n{}'.format(name.replace('_', ' '), 'locked' if state else 'unlocked')

    class Clipboard:
        clear: Notification = 'Clipboard\ncleared'

    class UndoRedo:
        undo: Notification[Fn[str]] = '{}'.format
        error_undo_no_action: Notification = 'No Action To Undo'
        redo: Notification[Fn[str]] = '{}'.format
        error_redo_no_action: Notification = 'No Action To Redo'

    class Transport:
        metronome: Notification[Fn[bool]] = toggle_text_generator('Metronome\n{}')
        midi_capture: Notification[Fn[bool, float]] = lambda tempo_set_by_capture, tempo: 'Captured\n{} BPM'.format(int(tempo)) if tempo_set_by_capture else 'Captured'
        loop: Notification[Fn[bool]] = toggle_text_generator('Loop\n{}')
        tap_tempo: Notification[Fn[float]] = lambda tempo: 'Tap Tempo\n{}'.format(int(tempo))
        record_quantize: Notification[Fn[bool]] = toggle_text_generator('Record Quantize\n{}')

    class Recording:
        new: Notification = 'New Clip Slot\nselected'

    class Automation:
        delete: Notification = 'Automation\ndeleted'

    class Scene:
        select: Notification[Fn[SceneName]] = '{}\nselected'.format
        delete: Notification[Fn[SceneName]] = '{}\ndeleted'.format
        duplicate: Notification[Fn[SceneName]] = '{}\nduplicated'.format

    class Track:
        lock: Notification[Fn[TrackName, bool]] = lambda name, state: '{}\n{}'.format(name, 'locked' if state else 'unlocked')
        select: Notification[Fn[TrackName]] = '{}'.format
        delete: Notification[Fn[TrackName]] = '{}\ndeleted'.format
        duplicate: Notification[Fn[TrackName]] = '{}\nduplicated'.format
        mute: Notification[Fn[TrackName, bool]] = lambda name, state: '{}\n{}'.format(name, 'muted' if state else 'unmuted')
        arm: Notification[Fn[TrackName, bool]] = lambda name, state: '{}\n{}'.format(name, 'armed' if state else 'disarmed')

    class Clip:
        select: Notification[Fn[ClipName]] = '{}\nselected'.format
        delete: Notification[Fn[ClipName]] = '{}\ndeleted'.format
        duplicate: Notification[Fn[ClipName]] = '{}\nduplicated'.format
        error_delete_empty_slot: Notification = 'Clip Slot\nalready empty'
        quantize: Notification[Fn[ClipName, Subdivision]] = '{} {}\nquantized'.format
        error_quantize_invalid_resolution: Notification[Fn[Resolution]] = 'Cannot quantize to {}'.format
        double_loop: Notification = 'Loop\ndoubled'

        class CopyPaste:
            error_copy_from_group_slot: Notification = 'Cannot copy from Group Slot'
            error_copy_from_empty_slot: Notification = 'Cannot copy from empty Slot'
            error_copy_recording_clip: Notification = 'Cannot copy recording Clip'
            copy: Notification[Fn[ClipSlot]] = lambda slot: '{}\ncopied'.format(display_name(slot))
            error_paste_to_group_slot: Notification = 'Cannot paste into Group Slot'
            error_paste_audio_to_midi: Notification = 'Cannot paste an audio Clip into a MIDI Track'
            error_paste_midi_to_audio: Notification = 'Cannot paste a MIDI Clip into an audio Track'
            paste: Notification[Fn[ClipSlot]] = lambda slot: '{}\npasted'.format(display_name(slot))

    class Device:
        lock: Notification[Fn[DeviceName, bool]] = lambda name, state: '{}\n{}'.format(name, 'locked' if state else 'unlocked')
        fold: Notification[Fn[DeviceName, str]] = lambda name, state: '{}\n{}'.format(name, 'unfolded' if state else 'folded')
        on_off: Notification[Fn[DeviceName, str]] = lambda name, state: '{}\n{}'.format(name, state.lower())
        select: Notification[Fn[DeviceName]] = '{}'.format
        bank: Notification[Fn[DeviceBank]] = '{}'.format

    class DrumGroup:

        class Pad:
            select: Notification[Fn[PadName]] = '{}\nselected'.format
            delete: Notification[Fn[PadName]] = '{}\ndeleted'.format
            mute: Notification[Fn[PadName]] = lambda name, state: '{}\n{}'.format(name, 'muted' if state else 'unmuted')
            delete_notes: Notification[Fn[PadName]] = '{}\nnotes deleted'.format

            class CopyPaste:
                error_copy_from_empty_pad: Notification = 'Cannot copy from empty Pad'
                copy: Notification[Fn[PadName]] = '{}\ncopied'.format
                error_paste_to_source_pad: Notification = 'Cannot paste to source Pad'
                paste: Notification[Fn[PadName]] = '{}\npasted'.format

        class Page:
            up: Notification = 'Page up'
            down: Notification = 'Page down'

        class Scroll:
            up: Notification = 'Scroll up'
            down: Notification = 'Scroll down'

    class Simpler:

        class Slice:
            select: Notification[Fn[int]] = 'Slice {}\nselected'.format
            delete: Notification[Fn[int]] = 'Slice {}\ndeleted'.format
            delete_notes: Notification[Fn[int]] = 'Slice {}\nnotes deleted'.format

        class Page:
            up: Notification = 'Page up'
            down: Notification = 'Page down'

        class Scroll:
            up: Notification = 'Scroll up'
            down: Notification = 'Scroll down'

    class Notes:
        delete: Notification = 'Notes\ndeleted'
        error_no_notes_to_delete: Notification = 'No notes\nto delete'
        nudge: Notification[Fn[str]] = 'Notes nudged to\n{}'.format
        transpose: Notification = 'Notes\ntransposed'

        class CopyPaste:
            copy: Notification = 'Notes\ncopied'
            paste: Notification = 'Notes\npasted'

        class Pitch:
            select: Notification[Fn[int]] = lambda index: 'Pitch {}\nselected'.format(pitch_index_to_string(index))
            delete: Notification[Fn[int]] = lambda index: '{}\nnotes deleted'.format(pitch_index_to_string(index))

        class Octave:
            up: Notification = 'Octave up'
            down: Notification = 'Octave down'

        class ScaleDegree:
            up: Notification = 'Scale degree\nup'
            down: Notification = 'Scale degree\ndown'

    class Sequence:
        current_bar: Notification[Fn[int]] = 'Bar {}'.format
        current_bar_with_page: Notification[Fn[int, int]] = 'Bar {} Page {}'.format

    class Modes:
        select: Notification[Fn[ComponentName, ModeName]] = None

    class DefaultText(_DefaultText):
        pass

    class TransformDefaultText(_TransformDefaultText):
        pass