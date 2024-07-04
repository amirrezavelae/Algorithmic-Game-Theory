class UGPlayerPhase1_400102222:
    def __init__(self) -> None:
        self.proposer = True
        self.my_log = []
        self.opponent_log = []

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        self.my_log = []
        self.opponent_log = []

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
        self.my_log.append(bid)
        if self.my_log[-1] == self.my_log[-2] == 50 and
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
        threshold = threshold - 5
        return offer >= threshold
        # return True

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        # print(f"Round {round_number}: {score}")
