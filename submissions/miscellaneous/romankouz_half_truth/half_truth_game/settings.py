import reflex as rx

from half_truth_game.round import RoundState

class SettingsState(RoundState):

    game_modes: dict[str, int] = {
        "blitz": 50,
        "standard": 100,
        "extended": 250,
        "marathon": 500,
    }

    def set_value(self, value):
        if self.round_number == 0:
            self.num_truths = value

    def set_score_mode(self, selected_mode):
        if self.round_number == 0:
            self.score_mode = selected_mode

    def set_win_condition(self, game_mode):
        if self.round_number == 0:
            self.win_condition = self.game_modes[game_mode]