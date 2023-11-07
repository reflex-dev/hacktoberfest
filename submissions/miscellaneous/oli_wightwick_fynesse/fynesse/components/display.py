"""
Generic components for displaying information
"""
from fynesse.data import Track
from fynesse.state import Artist, SearchState, State, Track

import reflex as rx


def genre_card(genre: str):
    return rx.box(
        rx.hstack(
            rx.text('#' + genre, as_='small'),
                rx.button(
                    rx.icon(tag="search"),
                    on_click=SearchState.stage_genre_for_search(genre),

                    size='xs',
                    variant='ghost'
                ),
            ),
        border_radius='lg',
        border_width='thin',
        padding_left='6px'
    )


def artist_card(
        artist_uri_name: tuple[str, str],
        add_remove_button: bool
    ) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(artist_uri_name.__getitem__(1)),
            rx.cond(
                add_remove_button,
                rx.button(
                    '🌱',
                    on_click=State.add_artist_to_seeds(artist_uri_name),
                    is_disabled=State.seed_artist_uris.contains(artist_uri_name.__getitem__(0)),
                    size='xs',
                    variant='ghost'
                ),
                rx.button(
                    rx.icon(tag="minus"),
                    on_click=State.remove_artist_from_seeds(artist_uri_name),
                    size='xs',
                    variant='ghost'
                ),
            ),
        ),

        border_radius='lg',
        border_width='thin',
        padding_left='6px'
    )


def track_card(
        track: Track,
        buttons: list[rx.Component],
        artists_interactive: bool,
        show_genres: bool=False,
        genres_interactive: bool=True
    ):
    return rx.box(
            rx.hstack(
                rx.image(
                    src_set=track.album_art_srcset,
                    html_width='100',
                    border_radius='md',
                ),
                rx.vstack(
                    rx.box(
                        rx.text(
                            track.track_name,
                            as_='strong'
                        ),
                        margin_top='0.5'
                    ),
                    rx.cond(
                        artists_interactive,
                        rx.wrap(
                            rx.foreach(
                                track.artist_uris_names,
                                lambda x: rx.wrap_item(artist_card(x, True))
                            )
                        ),
                        rx.text(track.artist_names.join(', '))
                    ),
                    rx.box(
                        rx.text(
                            track.album_name,
                            as_='small'
                        )
                    ),

                    rx.cond(
                        (track.artist_genres.length() > 0) & show_genres,
                        rx.cond(
                            genres_interactive,
                            rx.wrap(
                                rx.foreach(
                                    track.artist_genres,
                                    #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                    lambda x: rx.wrap_item(genre_card(x))
                                ),
                                padding_bottom='1.5'
                            ),
                            rx.text('#' + track.artist_genres.join(', #'), as_='small')
                        ),
                        rx.text('')
                    ),

                    align_items='left',
                ),
                rx.spacer(),
                rx.vstack(*buttons)
        ),
        border_width=2,
        border_radius='lg',
        overflow='hidden',
        padding_right=3,
        width='100%',
    )


def artist_card_lg(
        artist: Artist,
        show_genres: bool=False,
    ):
    artist_uri_name = (artist.uri, artist.artist_name)

    return rx.box(
            rx.hstack(
                rx.image(
                    src_set=artist.images_srcset,
                    html_width='100',
                    border_radius='md'
                ),
                rx.vstack(
                    rx.box(
                        rx.text(
                            artist.artist_name,
                        ),
                        margin_top='0.5'
                    ),
                    rx.cond(
                        (artist.genres.length() > 0) & show_genres,
                        rx.wrap(
                            rx.foreach(
                                artist.genres,
                                #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                lambda x: rx.wrap_item(genre_card(x))
                            ),
                            padding_bottom='1.5'
                        ),
                        rx.text('')
                    ),
                    align_items='left',
                ),
                rx.spacer(),
                rx.button(
                    '🌱',
                    on_click=State.add_artist_to_seeds(artist_uri_name),
                    is_disabled=State.seed_artist_uris.contains(artist_uri_name[0]),
                ),

        ),
        border_width=2,
        border_radius='lg',
        overflow='hidden',
        padding_right=3,
        width='100%',
    )


def pane(
        content: rx.component,
        heading_text: str,
        padding: int = 4
    ) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                heading_text,
                margin_left='19px',
                margin_bottom=-4,
                z_index=2,
            ),
            rx.box(
                content,
                border_width='thick',
                border_radius='3xl',
                padding=padding,
                z_index=1,
            ),
            align_items='left'
        ),
        margin_left=2,
        margin_right=2,
        width=420
    )


def sub_pane(
        content: rx.Component,
        heading: str,
        border_color: str = None
    ) -> rx.Component:
    return rx.box(
            rx.vstack(
                rx.heading(
                    heading,
                    size='md',
                    margin_bottom='-12.5px',
                    margin_left=2,
                    z_index=2
                ),
                rx.box(
                    content,
                    border_width='medium',
                    border_radius='xl',
                    border_color=border_color,
                    padding=15,
                    # width=400,
                    z_index=1
                ),
                align_items='left'
            ),
            width='100%'
        )


def hint_text(text: str):
    return rx.text(
        text,
        opacity=0.3,
        text_align='center',
    )
