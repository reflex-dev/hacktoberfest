from spotipy import SpotifyOAuth
import reflex as rx
from .utilities import src_set_from_images_list

class Artist(rx.Base):
    uri: str
    artist_name: str
    images_srcset: str
    genres: list[str] = []

    def with_genres(self, genres):
        self.genres = genres
        return self

    def __init__(self, artist_dict):
        uri = artist_dict['uri']
        artist_name = artist_dict['name']

        raw_images = artist_dict['images']

        images = [img['url'] for img in raw_images]

        images_srcset = src_set_from_images_list(raw_images)
        
        super().__init__(
            uri=uri,
            artist_name=artist_name,
            images_srcset=images_srcset
        )

class Track(rx.Base):
    uri: str
    track_name: str
    artist_uris_names: list[tuple[str, str]]
    artist_names: list[str]
    album_name: str
    album_art: list[str]
    spotify_url: str
    artist_genres: list[str] = []
    album_art_srcset: str
    added_at: str

    raw_dict: dict = None
        
    def with_artist_genres(self, artist_genres):
        self.artist_genres = artist_genres
        return self
    
    @rx.var
    def artist_uris(self) -> list[str]:
        return [uri for uri, name in self.artist_uris_names]
    
    def __init__(
            self,
            input_dict: dict,
            track_enclosed_in_item: bool = True
        ):
        if track_enclosed_in_item:
            item_dict = input_dict
            track_dict = item_dict['track']
            added_at = item_dict['added_at']\
                if 'added_at' in item_dict\
                else item_dict['played_at']
        else:
            track_dict = input_dict
            added_at = ''


        uri = track_dict['uri']
        track_name = track_dict['name']

        # print(track_name)

        artist_uris_names = [
            (a['uri'], a['name']) 
            for a 
            in track_dict['artists']
        ]
        artist_names = [name for uri, name in artist_uris_names]

        album_name = track_dict['album']['name']

        if 'spotify' in track_dict['external_urls']:
            spotify_url = track_dict['external_urls']['spotify']
        else:
            spotify_url = ''

        raw_album_art = track_dict['album']['images']

        album_art = [img['url'] for img in raw_album_art]

        album_art_srcset = src_set_from_images_list(raw_album_art)
        
        super().__init__(
            uri=uri,
            track_name=track_name,
            artist_uris_names=artist_uris_names,
            artist_names=artist_names,
            album_name=album_name,
            album_art=album_art,
            album_art_srcset=album_art_srcset,
            spotify_url=spotify_url,
            added_at=added_at
        )

class Playlist(rx.Base):
    playlist_name: str
    uri: str
    description: str
    public: bool
    has_genres: bool = False

    def with_genre_flag_true(self):
        self.has_genres = True
        return self

    def __init__(
            self, 
            pl_dict: dict = {
                'name': '',
                'uri': '',
                'description': '',
                'public': True
            }
        ):
        playlist_name = pl_dict['name']
        uri = pl_dict['uri']
        description = pl_dict['description']
        public = bool(pl_dict['public'])

        super().__init__(
            playlist_name=playlist_name,
            uri=uri,
            description=description,
            public=public
        )
    
