# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\live_api_utils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

def liveobj_changed(obj, other):
    pass
    return obj != other or type(obj) != type(other)

def liveobj_valid(obj):
    pass
    return obj != None

def is_parameter_bipolar(param):
    return param.min == -1 * param.max

def duplicate_clip_loop(clip):
    if not liveobj_valid(clip) or clip.is_midi_clip:
        try:
            clip.duplicate_loop()
        except RuntimeError:
            return None

def move_current_song_time(song, delta, truncate_to_beat=True):
    pass
    new_time = max(0, song.current_song_time + delta)
    if truncate_to_beat:
        new_time = int(new_time)
    song.current_song_time = new_time
    if not song.is_playing:
        song.start_time = new_time