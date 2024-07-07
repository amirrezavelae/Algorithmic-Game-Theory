class UGPlayerPhase1_400102222:
    def __init__(self) -> None:
        self.proposer = True
        self.my_log = []
        self.opponent_log = []
        self.my_score = []
        self.bid_even = 1
        self.dick_head_acceptor = 10
        self.dick_head_bidder = 0
        self.pitty_tit_for_tat = False

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        self.my_log = []
        self.opponent_log = []
        self.my_score = []
        self.bid_even = 1
        self.dick_head_acceptor = 10
        self.dick_head_bidder = 0
        self.pitty_tit_for_tat = False

    def proposer_strategy(self, round_number: int) -> int:
        """
        Define the strategy for the proposer.

        Args:
            round_number (int): The current round number (1 to 100).

        Returns:
            int: The amount offered to the responder (0 to 100).
        """
        if round_number > 1 and self.opponent_log:
            # Calculate average accepted offer from observed offers
            accepted_offers = [offer for offer,
                               result in self.opponent_log if result]
            if accepted_offers:
                avg_offer = sum(accepted_offers) / len(accepted_offers)
                # Adjust offer based on average observed and risk tolerance
                bid = int(avg_offer * 0.8 + 50 * 0.2)
            else:
                bid = 50
        else:
            # First round, make a fair offer
            bid = 50
            bid_even = 0
        if round_number > 8 and self.my_score[-1] == 0 and self.my_score[-2] == 0 and self.my_score[-3] == 0:
            self.dick_head_acceptor = self.my_log[-1] + 10
        bid = max(bid, self.dick_head_acceptor)

        if not self.dick_head_bidder and round_number > 10:
            sum_bid = 0
            index = 0
            # 5 min offers in oppenents log
            for i in range(len(self.opponent_log) - 1, max(len(self.opponent_log) - 6, 0), -1):
                sum_bid += self.opponent_log[i][0]
                index += 1
            if sum_bid < 20:
                self.dick_head_bidder = True
        if self.dick_head_bidder:
            bid = 10
        if not round_number % 10:
            self.dick_head_bidder = False

        if round_number > 9 and (round_number//2) % 5 == 0 and not self.pitty_tit_for_tat:
            self.pitty_tit_for_tat = self.is_tit_for_tat_player()
            # print("------------")
            if self.pitty_tit_for_tat:
                bid = 55
        if round_number > 15 and (round_number//2) % 2 == 0 and self.pitty_tit_for_tat:
            # print(round_number)
            if self.is_tit_for_tat_player():
                bid = 100
        self.my_log.append(bid)
        return bid

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        # Personal threshold set at 30%
        personal_threshold = 30
        flexible_threshold = True

        if flexible_threshold:
            if offer < 25:
                threshold = personal_threshold + 10
            elif offer > 45:
                threshold = personal_threshold - 5
            else:
                threshold = personal_threshold
        else:
            threshold = personal_threshold

        self.opponent_log.append((offer, offer >= threshold))
        return offer >= threshold
        # return True

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        self.my_score.append(score)
        # print(f"Is tit for tat{self.pitty_tit_for_tat}")
        # print(f"Is proposer even: {self.bid_even}")
        # print(f"Round {round_number}: {score}")

    def is_tit_for_tat_player(self) -> bool:
        tit_for_tat_counter = 0
        total_comparable_rounds = len(self.my_log) - 1

        for i in range(1, len(self.my_log)):
            # print(self.my_log[i-1])
            # print(self.opponent_log[i-1][0])
            if self.opponent_log[i-1][0] == self.my_log[i-1]:
                tit_for_tat_counter += 1

        if total_comparable_rounds > 0:
            tit_for_tat_percentage = (
                tit_for_tat_counter / total_comparable_rounds) * 100
        else:
            return False  # Cannot determine if no rounds to compare

        # Assuming a threshold of 80% to consider the opponent as "tit for tat" player
        # print(tit_for_tat_percentage)
        return tit_for_tat_percentage >= 98
