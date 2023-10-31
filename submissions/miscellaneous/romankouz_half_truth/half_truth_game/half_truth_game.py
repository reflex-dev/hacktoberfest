"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

from half_truth_game.round import RoundState
from half_truth_game.rules import RulesState
from half_truth_game.settings import SettingsState

import reflex as rx

filename = f"{config.app_name}/{config.app_name}.py"

def display_statement(statement, index):
    return rx.vstack(
        rx.button(
            statement[0],
            on_click=lambda statement=statement, index=index: RoundState.reveal_statement_class(statement[0], index),
            bg=RoundState.half_truths_bg[statement[0]],
            border_radius="lg",
            variant=rx.cond(
                (RoundState.half_truths_bg[index] == "red") | (RoundState.half_truths_bg[index] == "green"), 
                "unstyled", 
                "solid"
            ),
            # is_disabled=RoundState.half_truths_clicked[index],
            style={"_hover": {"bg": rx.cond(RoundState.half_truths_clicked[index], RoundState.half_truths_bg[index], "#ebedf0")}},
        ),
        rx.spacer(),
        align_items="start"
    )

@rx.page(route="/", on_load=RoundState.reset_game)
def index():
    return rx.center(
        navbar(),
        rx.vstack(
            rx.vstack(
                rx.cond(
                    RoundState.scores[RoundState.current_team] >= RoundState.win_condition, 
                    rx.heading(f"Team {RoundState.current_team + 1} wins!"), 
                    rx.cond(RoundState.round_number != 0, 
                        rx.heading(f"Round Number: {RoundState.round_number}"), 
                        rx.heading("Welcome to 50/50!")
                    )
                ),
                rx.form(
                    rx.input(
                        placeholder="Select a subject to play 50/50 on.",
                        on_change=RoundState.set_prompt
                    ),
                    rx.button(
                        rx.cond(RoundState.round_number != 0, "End Turn", "Generate Round!"),
                        is_loading=RoundState.processing,
                        width="100%",
                        type_="submit",
                        is_disabled=(RoundState.scores[RoundState.current_team] >= RoundState.win_condition)
                    ),
                    on_submit=lambda _: RoundState.generate_round(RoundState.prompt),
                ),
                rx.vstack(
                    rx.cond(
                        RoundState.complete,
                        rx.box(
                            rx.foreach(
                                RoundState.half_truths,
                                lambda statement, index: display_statement(statement, index)
                            )
                        )
                    ),
                    align_items="start"
                ),
                padding="2em",
                shadow="lg",
                border_radius="lg",
            ),
            scores(),
            rx.button(
                "Generate New Game",
                on_click=RoundState.reset_game(),
            )
        ),
        width="100%",
        height="100vh",
        # style={"backgroundImage": "/red-green-gradient.jpeg", "backgroundRepeat": "no-repeat", "backgroundSize": "cover"}
    )

def navbar():
    return rx.box(
        rx.hstack(
            rx.image(src="/5050_small.png"),
            rx.heading("The AI Fact Turing test."),
            rx.spacer(),
            rx.menu(
                rx.link(
                    "Home",
                    href="/",
                    color="rgb(107,99,246)",
                    button=True,
                    padding=3,
                ),
                rx.link(
                    "Rules",
                    href="/rules",
                    color="rgb(107,99,246)",
                    button=True,
                    padding=3,
                ),
                rx.link(
                    "Settings",
                    href="/settings",
                    color="rgb(107,99,246)",
                    button=True,
                    padding=3,
                ),
            ),
        ),
        padding_right="1.5%",
        position="fixed",
        width="100%",
        top="0px",
        z_index="5",
    )

def scores():
    return rx.box(
        rx.hstack(
            rx.foreach(
                RoundState.scores,
                lambda score, index: rx.button(
                    f"Team {index + 1}: {score}",
                    size="lg",
                    variant=rx.cond(index == RoundState.current_team, "solid", "ghost")
                )
            )
        ),
    )


def display_rule(rule, index) -> rx.Component:
    return rx.button(
        f"{index + 1}) {rule}",
        variant="unstyled",
        size="sm"
    )

def rules() -> rx.Component:
    return rx.center(
        navbar(),
        rx.flex(
            rx.vstack(
                rx.foreach(
                    RulesState.rules,
                    lambda rule, index: display_rule(rule, index),
                ),
                align_items="start",
            ),
        ),
        width="100%",
        height="100vh",
    )

def settings() -> rx.Component:
    return rx.center(
        navbar(),
        rx.vstack(
            rx.heading("Scoring Method", size="sm"),
            rx.button_group(
                rx.tooltip(
                    rx.button(
                        "Fixed",
                        on_click=lambda: SettingsState.set_score_mode("fixed"),
                        color_scheme=rx.cond(SettingsState.score_mode == "fixed", "linkedin", "gray"),
                    ),
                    label="Fixed points for each correct answer: e.g. (+10, +10, +10, ...)"
                ),
                rx.tooltip(
                    rx.button(
                        "Progressive",
                        on_click=lambda: SettingsState.set_score_mode("progressive"),
                        color_scheme=rx.cond(SettingsState.score_mode == "progressive", "linkedin", "gray"),
                    ),
                    label="Progressive points for each correct answer: e.g (+10, +20, +30, ...)"
                ),
                is_attached=True,
            ),
            rx.spacer(),
            rx.spacer(),
            rx.divider(border_color="black"),
            rx.spacer(),
            rx.spacer(),
            rx.hstack(
                rx.heading(f"Number of True Statements: {SettingsState.num_truths}", size="sm"),
                rx.tooltip(
                    rx.icon(tag="info"),
                    label="The total number of statements will be twice this value."
                ),
            ),
            rx.slider(on_change=SettingsState.set_value, min_=1, max_=5, default_value=3, focus_thumb_on_change=False),
            rx.spacer(),
            rx.spacer(),
            rx.divider(border_color="black"),
            rx.spacer(),
            rx.spacer(),
            
            rx.hstack(
                rx.heading(f"Victory Achieved: {SettingsState.win_condition} points", size="sm"),
                rx.tooltip(
                    rx.icon(tag="info"),
                    label="The total number of points needed to claim victory."                    
                ),
            ),
            rx.button_group(
                rx.tooltip(
                    rx.button(
                        "Blitz",
                        on_click=lambda: SettingsState.set_win_condition("blitz"),
                        color_scheme=rx.cond(SettingsState.win_condition == 50, "linkedin", "gray"),
                    ),
                    label="50 points"
                ),
                rx.tooltip(
                    rx.button(
                        "Standard",
                        on_click=lambda: SettingsState.set_win_condition("standard"),
                        color_scheme=rx.cond(SettingsState.win_condition == 100, "linkedin", "gray"),
                    ),
                    label="100 points"
                ),
                rx.tooltip(
                    rx.button(
                        "Extended",
                        on_click=lambda: SettingsState.set_win_condition("extended"),
                        color_scheme=rx.cond(SettingsState.win_condition == 250, "linkedin", "gray"),
                    ),
                    label="250 points"
                ),
                rx.tooltip(
                    rx.button(
                        "Marathon",
                        on_click=lambda: SettingsState.set_win_condition("marathon"),
                        color_scheme=rx.cond(SettingsState.win_condition == 500, "linkedin", "gray"),
                    ),
                    label="500 points"
                ),
                is_attached=True,
            ),
        ),
        width="100%",
        height="100vh",
    )

app = rx.App()
app.add_page(index)
app.add_page(rules)
app.add_page(settings)
app.compile()
