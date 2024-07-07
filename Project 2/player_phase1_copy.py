import numpy as np


class UGPlayerPhase1_4001022221:
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
            offer = self.last_offer_received
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
        # print(f"Round {round_number}: {offer}")
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
        # print(f"Round {round_number}: {offer}")
        return offer >= 50

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        # print(f"Round {round_number}: {score}")


class UGPlayerPhase1_4001022223:
    punish = 20
    generous = 40

    def init(self) -> None:
        pass

    def reset(self) -> None:
        """ Reset any state variables if necessary. Called before starting a new game. """
        self.propose_first = None
        self.rounds_length = 0
        self.proposals = np.zeros(50)
        self.responds = np.zeros(50)
        self.opponent_proposals = np.zeros(50)
        self.opponent_responds = np.zeros(50)
        self.results = np.zeros(100)
        self.lambda_v = np.ones(4)/4  # min, max, mean, mean proposal opponent
        self.score = 0
        self.last_state_propose = False
        self.incentive = self.generous
        return

    def proposer_strategy(self, round_number: int) -> int:
        """
        Define the strategy for the proposer.

        Args:
            round_number (int): The current round number (1 to 100).

        Returns:
            int: The amount offered to the responder (0 to 100).
        """
        self.last_state_propose = True
        if self.propose_first == None:
            self.propose_first = 1

        index = round_number//2-(1-self.propose_first)
        if round_number == 1:
            propose = self.generous
        elif index == 0:
            propose = self.generous/2+self.opponent_proposals[index]/2
        else:
            try:
                arr = np.where(self.opponent_responds[:index] == 1)[0]
                min_val = np.min(self.proposals[arr])
                mean_val = np.mean(self.proposals[arr])
            except:
                min_val = 50
                mean_val = 50
            try:
                arr = np.where(self.opponent_responds[:index] == 0)[0]
                max_val = np.max(self.proposals[arr])
            except:
                max_val = 50
            mean_proposals = np.mean(
                self.opponent_proposals[:index])  # later debug
            if (min_val > max_val):  # Not rational! punish
                propose = max_val
            else:
                propose = np.average(np.array(
                    [min_val, max_val, mean_val, mean_proposals]), weights=self.lambda_v)*0.9+0.1*self.incentive
        final_propose = min(50, max(self.punish, int(propose)))
        self.proposals[index] = final_propose
        return final_propose

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        self.last_state_propose = False
        if self.propose_first == None:
            self.propose_first = 0

        index = round_number//2-self.propose_first
        self.opponent_proposals[index] = offer
        if offer == 0:
            self.responds[index] = 0
            return False
        elif offer >= 50:
            self.responds[index] = 1
            return True
        elif index == 0:
            if (offer >= 30):
                self.responds[index] = 1
                return True
            self.responds[index] = 0
            return False
        else:
            mean_v = np.mean(self.opponent_proposals[:index])
            std_v = np.std(self.opponent_proposals[:index])
            if offer < mean_v-1.5*std_v:
                self.responds[index] = 0
                return False
            my_mean = np.mean(self.proposals[:index])
            my_std = np.std(self.opponent_proposals[:index])
            if offer < my_mean-1.5*my_std:
                self.responds[index] = 0
                return False
        self.responds[index] = 1
        return True

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """


class UGPlayerPhase1_4001022224:
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
        return 0

    def responder_strategy(self, round_number: int, offer: int) -> bool:
        """
        Define the strategy for the responder.

        Args:
            round_number (int): The current round number (1 to 100).
            offer (int): The amount offered by the proposer (0 to 100).

        Returns:
            bool: True if the offer is accepted, False otherwise.
        """
        # print(f"Round {round_number}: {offer}")
        return offer >= 0

    def result(self, round_number: int, score: int) -> None:
        """
        Receive the result of the round.

        Args:
            round_number (int): The round number (1 to 100).
            score (int): The score for the round.
        """
        # print(f"Round {round_number}: {score}")
