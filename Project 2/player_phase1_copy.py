class UGPlayerPhase1_4001022222:
    def __init__(self) -> None:
        self.proposer = True
        self.my_log = []
        self.opponent_log = []
        pass

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        self.my_log = []
        self.opponent_log = []
        pass

    def proposer_strategy(self, round_number: int) -> int:
        """
        Define the strategy for the proposer.

        Args:
            round_number (int): The current round number (1 to 100).

        Returns:
            int: The amount offered to the responder (0 to 100).
        """
        return 50

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        print(f"Round {round_number}: {offer}")
        return offer >= 50

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        print(f"Round {round_number}: {score}")
