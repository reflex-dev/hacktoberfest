brain: dict = {
    "@keyframes brain": {
        "0%": {"transform": "scale(1.1)"},
        "100%": {"transform": "scale(0.8)"},
    },
    "animation": "brain 1s cubic-bezier(0.250, 0.460, 0.450, 0.940) infinite alternate-reverse both",
}

css: dict = {
    "_dark": {
        "bg": "#1f2128",
    },
    "_light": {
        "bg": "#fafafa",
    },
    "font_family": "Roboto",
    "header": {
        "width": "100%",
        "height": "7vh",
        "box_shadow": "0px 4px 8px 0px rgba(0, 0, 0, 0.25)",
        "justify_content": "center",
        "padding": ["0 1rem", "0 1rem", "0 1rem", "0 4rem", "0 10rem"],
        "transition": "all 400ms ease",
        "_dark": {
            "bg": "#141518",
        },
        "_light": {
            "bg": "#ffffff",
        },
    },
    "number": {
        "height": "180px",
        "width": "180px",
        "justify_content": "center",
        "align_items": "center",
        "border_radius": "10px",
        "box_shadow": "0px 15px 30px 0px rgba(0, 0, 0, 0.5)",
        "_dark": {"bg": "#17181d"},
    },
    "content": {
        "width": "100%",
        "height": "inherit",
    },
    "page_link": {
        "_dark": {"color": "white"},
        "_light": {"color": "black"},
        "padding": "0 0.35rem",
    },
    "footer": {
        "width": "100%",
        "height": "50px",
        "padding": ["0 1rem", "0 1rem", "0 1rem", "0 4rem", "0 10rem"],
    },
}
