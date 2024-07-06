import sys
import threading
from player_phase2 import UGPlayerPhase2_400102222 as player_class1
from player_phase2_copy import UGPlayerPhase2_400102222 as player_class2
import random


class UltimatumGameTester:
    def __init__(self, player1_class, player2_class, noisy, timeout=0.1):
        self.player1_class = player1_class
        self.player2_class = player2_class
        self.noisy = noisy
        self.total_rounds = 100
        self.amount = 100
        self.timeout = timeout  # timeout in seconds

    def run_with_timeout(self, func, *args):
        """Run a function with a timeout."""
        result = [None]

        def target():
            try:
                result[0] = func(*args)
            except Exception as e:
                result[0] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(self.timeout)
        if thread.is_alive():
            return TimeoutError("Function call timed out")
        # print(result[0])
        return result[0]

    def play_round(self, round_number, proposer, responder):
        """Play a single round of the game with timeout checks."""
        offer = self.run_with_timeout(proposer.proposer_strategy, round_number)
        # print(offer)
        if isinstance(offer, TimeoutError) or offer is None or offer < 0 or offer > 100:
            print("Error in proposer strategy, using default offer.")
            offer = 100  # Default offer if proposer strategy times out
        offer = int(offer)

        if self.noisy:
            offer += random.gauss(0, 5)
        # print(offer)

        acceptance = self.run_with_timeout(
            responder.responder_strategy, round_number, offer)
        if isinstance(acceptance, TimeoutError) or acceptance is None or acceptance not in [True, False]:
            print("Error in responder strategy, using default acceptance.")
            acceptance = True  # Default response if responder strategy times out

        if self.noisy and random.random() < 0.2:
            acceptance = not acceptance

        if acceptance:
            proposer.result(round_number, self.amount - offer)
            responder.result(round_number, offer)
        else:
            proposer.result(round_number, 0)
            responder.result(round_number, 0)

        return (offer, acceptance)

    def play_game(self):
        """Play the full game consisting of multiple rounds."""
        player1 = self.player1_class()
        player2 = self.player2_class()
        self.run_with_timeout(player1.reset)
        self.run_with_timeout(player2.reset)
        results = []
        for round_number in range(1, self.total_rounds + 1):
            if round_number % 2 == 1:
                proposer, responder = player1, player2
            else:
                proposer, responder = player2, player1
            offer, acceptance = self.play_round(
                round_number, proposer, responder)
            results.append((round_number, offer, acceptance))
        return results, player1, player2

    def calculate_scores(self, results):
        """Calculate the scores for both players based on the game results."""
        player1_score = 0
        player2_score = 0
        for round_number, offer, acceptance in results:
            if acceptance:
                if round_number % 2 == 1:
                    player1_score += self.amount - offer
                    player2_score += offer
                else:
                    player1_score += offer
                    player2_score += self.amount - offer
        return player1_score, player2_score

    def run(self):
        """Run the test and print the results."""
        results, player1, player2 = self.play_game()
        player1_score, player2_score = self.calculate_scores(results)
        # print("Player 1 log:" + str(player1.my_log))
        # print("Player 1 score: " + str(player1_score))
        # print("Player 2 score: " + str(player2_score))
        return player1_score, player2_score


if __name__ == "__main__":
    noisy = True
    # Change the player classes here to test different players
    sum_1 = 0
    sum_2 = 0
    rounds_toplay = 500
    tester = UltimatumGameTester(player_class1, player_class2, noisy=noisy)
    tester.run()
    for i in range(rounds_toplay):
        player1_score, player2_score = tester.run()
        sum_1 += player1_score
        sum_2 += player2_score
    print("Player 1 average score: " + str(sum_1 / rounds_toplay))
    print("Player 2 average score: " + str(sum_2 / rounds_toplay))
