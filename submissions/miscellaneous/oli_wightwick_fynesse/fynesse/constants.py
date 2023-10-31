"""
Constants used throughout UI; in once place for easier modification
"""
NUM_RECCOMENDATIONS_DEFAULT = 10
NUM_SEARCH_RESULTS_DEFAULT = 10

SEARCH_RESULTS_TYPE_OPTIONS = ['tracks', 'artists']
SEARCH_RESULTS_TYPE_TRACKS = 'tracks'
SEARCH_RESULTS_TYPE_ARTISTS = 'artists'


SUB_PANE_WARNING_RED = 'rgb(235,104,91)'
SPOTIFY_API_SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
    'streaming',
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-private',
    'playlist-modify-public',
    'user-read-playback-position',
    'user-top-read',
    'user-read-recently-played',
    'user-library-modify',
    'user-library-read',
]

APP_NAME = 'fynesse'

LIBRARY_PANE_HEADER_TEXT = 'library'
RECOMMENDATIONS_PANE_HEADER_TEXT = 'recommendations'
SEARCH_PANE_HEADER_TEXT = 'search'

RESULTS_SUB_PANE_HEADER_TEXT = 'results'
SEEDS_SUB_PANE_HEADER_TEXT = 'seeds'
TOO_MANY_SEEDS_HEADER_TEXT = '5 seeds max'
PARAMETERS_SUB_PANE_HEADER_TEXT = 'parameters'

LIKED_SONGS_TAB_NAME_TEXT = 'liked songs'
PLAYLIST_TAB_NAME_TEXT = 'playlist'
RECENTLY_PLAYED_TAB_NAME_TEXT = 'recently played'
TOP_TAB_NAME_TEXT = 'top'

GERMINATE_HINT = 'germinate seeds to get recommendations'
SEARCH_HINT = 'type something above'
PLANT_SEEDS_HINT_TEXT = 'plant some seeds'

PLAY_ALL_TRACKS_BUTTON_TEXT = 'play all'
ARTIST_GENRES_BUTTON_TEXT = 'see artist genres'
LOAD_MORE_BUTTON_TEXT = 'load more'
SAVE_PLAYLIST_BUTTON_TEXT = 'save to playlist'
GENERATE_RECOMMENDATIONS_BUTTON_TEXT = 'germinate seeds 🪴'

PLAYLIST_CREATE_DIALOG_HEADER_TEXT = 'new playlist'
CREATE_PLAYLIST_BUTTON_TEXT = 'create playlist'

TARGET_ACOUSTICNESS_SLIDER_TEXT = 'target acousticness'
TARGET_ENERGY_SLIDER_TEXT = 'target energy'
TARGET_LIVENESS_SLIDER_TEXT = 'target liveness'
TARGET_DANCEABILITY_SLIDER_TEXT = 'target danceability'
TARGET_INSTRUMENTALNESS_SLIDER_TEXT = 'target instrumentalness'
NUM_RECOMMENDED_TRACKS_SLIDER_TEXT = 'number of recommended tracks: '

SEARCH_RESULTS_TYPE_RADIO_TEXT = 'results type:'
SEARCH_ARTIST_FIELD_TEXT = 'artist'
SEARCH_TRACK_FIELD_TEXT = 'track'
SEARCH_GENRE_FIELD_TEXT = 'genre'
SEARCH_YEAR_FIELD_TEXT = 'year'
NUM_SEARCH_RESULTS_SLIDER_TEXT = 'number of results: '

SPOTIFY_GREEN = '#1DB954'