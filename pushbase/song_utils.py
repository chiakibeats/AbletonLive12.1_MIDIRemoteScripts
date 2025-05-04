# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\song_utils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import liveobj_valid

def is_return_track(song, track):
    return track in list(song.return_tracks)

def delete_track_or_return_track(song, track):
    tracks = list(song.tracks)
    if track in tracks:
        track_index = tracks.index(track)
        song.delete_track(track_index)
        return
    else:  # inserted
        track_index = list(song.return_tracks).index(track)
        song.delete_return_track(track_index)

def find_parent_track(live_object):
    pass
    track = live_object
    while liveobj_valid(track) and (not isinstance(track, Live.Track.Track)):
        track = getattr(track, 'canonical_parent', None)
                break
            else:  # inserted
                continue
    return track