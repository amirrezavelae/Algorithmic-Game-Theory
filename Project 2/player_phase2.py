class UGPlayerPhase2_400102222:
    def __init__(self) -> None:
        pass

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        pass

    def proposer_strategy(self, round_number: int) -> int:
        """
        Define the strategy for the proposer.

        Args:
            round_number (int): The current round number (1 to 100).

        Returns:
            int: The amount offered to the responder (0 to 100).
        """
        pass

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        pass

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        pass
