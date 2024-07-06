class UGPlayerPhase2_400102222:
    def __init__(self) -> None:
        self.proposer = True
        self.my_log = []
        self.opponent_log = []
        self.last_offer_made = 50
        self.last_offer_received = 0
        pass

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        self.my_log = []
        self.opponent_log = []
        self.last_offer_made = 50
        self.last_offer_received = 0
        pass

    def proposer_strategy(self, round_number: int) -> int:
        """
        Define the strategy for the proposer.

        Args:
            round_number (int): The current round number (1 to 100).

        Returns:
            int: The amount to offer (0 to 100).
        """
        if round_number == 1:
            offer = 50  # Start with a generous offer
        else:
            # Mimic the last offer received, with adjustments
            offer = max(0, min(100, self.last_offer_received)) - 4
            if offer < 10:
                offer = 15
            # print(offer)
        self.last_offer_made = offer
        return offer

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        self.last_offer_received = offer
        # Accept if the offer is equal to or better than the last made
        return offer >= self.last_offer_made

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        # This method can be expanded to adjust future strategy based on past results
        pass
