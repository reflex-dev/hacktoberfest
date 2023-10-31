import reflex as rx
from typing import List

from half_truth_game.round import RoundState

class RulesState(RoundState):

    rules: List[str] = [
        "Divide all players into 2 teams. It is recommended to nominate a team captain to make selections in this game.",
        "In 50/50, half of the statements generated are true, and the other half are false. Your objective is to identify as many correct statements before choosing false one.",
        "Play begins by prompting a subject for which statements will be generated for the opposing team.",
        "The team guessing tries to guess as many of the statements that are true as possible.",
        "The scoring can either be fixed or progressive and can be set in our settings.",
        "The turn ends either when a guess is incorrect, all correct statements have been identified, or the guessing team chooses to end their turn early.",
        "If a guess is incorrect, all points accumulated during the round are forfeited. If a turn is ended early, all points collected are kept.",
        "Once the turn ends, the roles of the teams switch and you repeat the process starting at Step 3.",
    ]