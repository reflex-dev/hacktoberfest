import reflex as rx
import openai
import random
import time
import os
from typing import List

openai.api_key = ""
MODEL_VERSION = "gpt-4"

class RoundState(rx.State):

    complete: bool = False
    current_round_correct_answers: int = 0
    current_team: int = -1
    half_truths: dict[str, bool] = {}
    half_truths_bg: dict[str, str] = []
    half_truths_clicked: List[bool] = []
    num_correct_statements_identified: int = 0
    num_teams: int = 2
    num_truths: int = 3
    processing: bool = False
    prompt: str = ""
    round_number: int = 0
    round_start_score: int = 0
    score_mode: str = "fixed"
    scores: List[int] = [0] * num_teams
    text: str = "Select a category to play 50/50 on."
    win_condition: int = 100

    def _generate_facts(self, subject):

        """Generates {num_truths} true and false statements."""

        true_messages = [
            {"role": "system", "content": "You are an assistant that generates a single true fact about subjects you are prompted about. However, you do not explicitly specify that these statements are true."},
            {"role": "user", "content": f"Please generate a single true fact about {subject}."},
        ]
        false_messages = [
            {"role": "system", "content": "You are an assistant that generates a single false statement about subjects you are prompted about. However, you do not explicitly specify that these statements are false."},
            {"role": "user", "content": f"Please generate a single false but believable statement about {subject} that even a person super experienced in the subject might think is true."},
        ]
        for _ in range(self.num_truths):
            true_response = openai.ChatCompletion.create(
                model=MODEL_VERSION,
                messages=true_messages
            )
            self.half_truths[
                true_response['choices'][0]['message']['content']
            ] = True

            # append true response
            true_messages.append({"role": "assistant", "content": true_response['choices'][0]['message']['content']})
            # append next prompt
            true_messages.append({"role": "user", "content": f"Please generate a single true fact about {subject} that is substantially different from the previous facts you generated."})
            
            fake_response = openai.ChatCompletion.create(
                model=MODEL_VERSION,
                messages=false_messages
            )
            self.half_truths[ 
                fake_response['choices'][0]['message']['content']
            ] = False
            # append fake response
            false_messages.append({"role": "assistant", "content": fake_response['choices'][0]['message']['content']})
            # append next prompt
            false_messages.append({"role": "user", "content": f"Please generate a single false but believable statement about {subject} that is substantially different from the previous false statements you generated."})

    def generate_round(self, subject):

        """Generates a round of Half-Truth"""

        if self.prompt == "":
            return rx.window_alert("Prompt Empty")

        # initialize round metrics to start values
        self._update_current_team()
        if self.current_team == 0:
            self.round_number += 1
        self.round_start_score = self.scores[self.current_team]
        self.current_round_correct_answers = 0
        self.half_truths = {}
        self.half_truths_clicked = [False] * self.num_truths * 2

        self.processing, self.complete = True, False
        yield

        # generate the true and false statements
        self._generate_facts(subject)

        # shuffle the dict (converted to list) so that truths and lies are not in predictable order
        self._shuffle_statements()

        # setup game
        self.half_truths_bg = {k: "white" for k in self.half_truths.keys()}
        self.processing, self.complete = False, True

    def reset_game(self):

        # retain settings
        old_num_teams = self.num_teams
        old_score_mode = self.score_mode
        old_num_truths = self.num_truths
        old_score_mode = self.score_mode
        old_win_condition = self.win_condition

        self.reset()

        # retain settings
        self.num_teams = old_num_teams
        self.score_mode = old_score_mode
        self.num_truths = old_num_truths
        self.win_condition = old_win_condition

    def _reveal_all_statements(self):

        """Reveal all of the true and false statements once an incorrect button is pressed."""

        for statement in self.half_truths.keys():
            self.half_truths_bg[statement] = "green" if self.half_truths[statement] else "red"

    def reveal_statement_class(self, statement, index):

        """Reveal if a statement is true or not when clicked."""
        print(self.half_truths)
        if not self.half_truths_clicked[index]:

            if self.half_truths[statement]:
                self.current_round_correct_answers += 1
                self.half_truths_bg[statement] = "green"
                time.sleep(0.3)
                if self.current_round_correct_answers == self.num_truths:
                    self.half_truths_clicked = [True] * self.num_truths * 2
                    self._reveal_all_statements()
            else:
                time.sleep(0.3)
                self._reveal_all_statements()
                self.half_truths_clicked = [True] * self.num_truths * 2
                
            self.half_truths_clicked[index] = True
            self._update_scores(self.half_truths[statement])
        

    def _shuffle_statements(self):

        """Shuffle the generated statements to avoid truth order patterns."""

        half_truths_list = list(list(x) for x in self.half_truths.items())
        random.shuffle(half_truths_list)
        for i, statement in enumerate(half_truths_list, start=1):
            statement[0] = f"{i}.  {statement[0]}"
        self.half_truths = dict(half_truths_list)

    def _update_current_team(self):

        """Update the current team number."""

        self.current_team = self.current_team + 1 if self.current_team + 1 < self.num_teams else 0
    
    def _update_scores(self, statement_is_true):

        """Update the score."""

        match self.score_mode:
            
            case "progressive":

                self.scores[self.current_team] = self.scores[self.current_team] + 10 * self.current_round_correct_answers if statement_is_true else self.round_start_score

            case "fixed":

                self.scores[self.current_team] = self.scores[self.current_team] + 10 if statement_is_true else self.round_start_score

            case _:

                raise NotImplementedError("This score mode doesn't exist.")
            
