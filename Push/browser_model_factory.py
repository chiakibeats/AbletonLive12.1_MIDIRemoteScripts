# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\browser_model_factory.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .browser_model import EmptyBrowserModel, QueryingBrowserModel, filter_type_for_browser
from .browser_query import ColorTagsBrowserQuery, PathBrowserQuery, PlacesBrowserQuery, SourceBrowserQuery, TagBrowserQuery
FilterType = Live.Browser.FilterType
PLACES_LABEL = 'Places'

def make_plugins_query():
    return TagBrowserQuery(include=['Plug-Ins'], root_name='plugins', subfolder='Plug-Ins')

def make_midi_effect_browser_model(browser):
    midi_effects = TagBrowserQuery(include=['MIDI Effects'], root_name='midi_effects')
    max = TagBrowserQuery(include=[['Max for Live', 'Max MIDI Effect']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, midi_effects, max, plugins, places])

def make_audio_effect_browser_model(browser):
    audio_effects = TagBrowserQuery(include=['Audio Effects'], root_name='audio_effects')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Audio Effect']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, audio_effects, max, plugins, places])

def make_instruments_browser_model(browser):
    instrument_rack = PathBrowserQuery(path=['Instruments', 'Instrument Rack'], root_name='instruments')
    drums = SourceBrowserQuery(include=['Drums'], exclude=['Drum Hits'], subfolder='Drum Rack', root_name='drums')
    instruments = TagBrowserQuery(include=['Instruments'], exclude=['Drum Rack', 'Instrument Rack'], root_name='instruments')
    drum_hits = TagBrowserQuery(include=[['Drums', 'Drum Hits']], subfolder='Drum Hits', root_name='drums')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Instrument']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, instrument_rack, drums, instruments, max, drum_hits, plugins, places])

def make_drum_pad_browser_model(browser):
    drums = TagBrowserQuery(include=[['Drums', 'Drum Hits']], root_name='drums')
    samples = SourceBrowserQuery(include=['Samples'], subfolder='Samples', root_name='samples')
    instruments = TagBrowserQuery(include=['Instruments'], root_name='instruments')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Instrument']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags, drums, samples, instruments, max, plugins, places])

def make_fallback_browser_model(browser):
    return EmptyBrowserModel(browser=browser)

def make_browser_model(browser, filter_type=None):
    pass
    factories = {FilterType.instrument_hotswap: make_instruments_browser_model, FilterType.drum_pad_hotswap: make_drum_pad_browser_model, FilterType.audio_effect_hotswap: make_audio_effect_browser_model, FilterType.midi_effect_hotswap: make_midi_effect_browser_model}
    if filter_type == None:
        filter_type = filter_type_for_browser(browser)
    return factories.get(filter_type, make_fallback_browser_model)(browser)