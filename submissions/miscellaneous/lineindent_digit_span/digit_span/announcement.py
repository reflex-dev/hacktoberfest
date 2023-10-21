import reflex as rx

css: dict = {
    "width": "100%",
    "height": "45px",
    "bg": "#18181d",
    "padding": [
        "0rem 1rem",
        "0rem 1rem",
        "0rem 0.5rem",
        "0rem 4rem",
        "0rem 10rem",
    ],
    "transition": "all 550ms ease",
}


class Announcement(rx.Hstack):
    def __init__(self) -> rx.Hstack:
        super().__init__(style=css, id="RxAnnouncement")
        self.children = [
            rx.html(
                " <div style='color: #b8b8ba;'>Built with <span><strong style='color: #fff;'>Reflex</strong></span>. For more info visit<span style='vertical-align: middle;'> <a href='https://github.com/reflex-dev/reflex'><img src='/github.png' style='width: 21px; height: 21px; display: inline-block; vertical-align: middle; filter: brightness(0) invert(1);'/></a></span> <a href='https://github.com/reflex-dev/reflex'> <span style='color: #fff;'><strong></strong></span></a></div>"
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="close", color="white", transform="Scale(0.8)"),
                rx.script(
                    """
localStorage.setItem("headerHidden", "true");
var close = document.getElementById("close");

function hide() {
    var RxAnnouncement = document.getElementById("RxAnnouncement");
    
    if (localStorage.getItem("headerHidden") === "true") {
        RxAnnouncement.style.display = "none";
        localStorage.setItem("headerHidden", "false");
    }

}

close.addEventListener("click", hide);
                    """
                ),
                id="close",
                on_click=rx.client_side("hide(args)"),
                color_scheme="None",
            ),
        ]
