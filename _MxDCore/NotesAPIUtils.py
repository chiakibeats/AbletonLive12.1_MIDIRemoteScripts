# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\NotesAPIUtils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

MIDI_NOTE_ATTRS = ('note_id', 'pitch', 'start_time', 'duration', 'velocity', 'mute', 'probability', 'velocity_deviation', 'release_velocity')
REQUIRED_MIDI_NOTE_ATTRS = ('pitch', 'start_time', 'duration')
VALID_DUPLICATE_NOTES_BY_ID_PARAMETERS = ('note_ids', 'destination_time', 'transposition_amount')

def midi_note_to_dict(note, properties_to_return=None):

    def get_note_attr(attr_name):
        prop = getattr(note, attr_name)
        return int(prop) if attr_name == 'mute' else prop
    note_dict = {}
    for attr in MIDI_NOTE_ATTRS:
        if properties_to_return is None or attr in properties_to_return:
            note_dict[attr] = get_note_attr(attr)
        continue
    return note_dict

def midi_notes_to_notes_dict(notes):
    return {'notes': [midi_note_to_dict(note) for note in notes]}

def verify_note_specification_requirements(note_specification):
    missing_keys = set(REQUIRED_MIDI_NOTE_ATTRS) - set(note_specification.keys())
    if len(missing_keys) > 0:
        raise RuntimeError('Missing required keys: ', ', '.join(missing_keys))