from spotipy import Spotify

def flatten_list_of_lists(list_of_lists: list[list]):
    return [
        item for sublist
        in list_of_lists 
        for item in sublist
    ]

def flat_genre_list_for_artist_uris(a_uris: list[str], genre_lookup: dict[str, str]):
    flat_genre_list = flatten_list_of_lists( 
        [genre_lookup[a] for a in a_uris]
    )
    return list(set(flat_genre_list))

def src_set_from_images_list(images_list: list[dict[str, str]]) -> str:
    return ', '.join([
            f"{img['url']} {img['width']}w"
            for img in images_list
        ])
