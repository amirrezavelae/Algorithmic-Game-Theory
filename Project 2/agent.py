from models import Round, Log


class Agent400102222:
    '''
    Player log: A Log object containing all the games played by you.
    Opponent log: A Log object containing all the games played by the opponent.
    Proposer: A boolean indicating whether you are the proposer (True) or the responder (False).
    '''

    def __init__(self, player_log: Log, opponent_log: Log, proposer: bool) -> None:
        self.player_log = player_log
        self.opponent_log = opponent_log
        self.proposer = proposer
        self.my_log = []
        self.opponent_log_list = []
        self.my_score = []
        self.bid_even = 1
        self.dick_head_acceptor = 10
        self.dick_head_bidder = 0
        self.pitty_tit_for_tat = False
        self.round_number = 1
        self.my_id = player_log.player_id

    def proposer_strategy(self) -> int:
        if self.round_number > 1 and self.opponent_log_list:
            accepted_offers = [offer for offer,
                               result in self.opponent_log_list if result]
            if accepted_offers:
                avg_offer = sum(accepted_offers) / len(accepted_offers)
                bid = int(avg_offer * 0.8 + 50 * 0.2)
            else:
                bid = 50
        else:
            bid = 50
            self.bid_even = 0

        if self.round_number > 8 and self.my_score[-1] == 0 and self.my_score[-2] == 0 and self.my_score[-3] == 0:
            self.dick_head_acceptor = self.my_log[-1] + 10
        bid = max(bid, self.dick_head_acceptor)

        if not self.dick_head_bidder and self.round_number > 10:
            sum_bid = 0
            index = 0
            for i in range(len(self.opponent_log_list) - 1, max(len(self.opponent_log_list) - 6, 0), -1):
                sum_bid += self.opponent_log_list[i][0]
                index += 1
            if sum_bid < 20:
                self.dick_head_bidder = True
        if self.dick_head_bidder:
            bid = 10
        if not self.round_number % 10:
            self.dick_head_bidder = False

        if self.round_number > 9 and (self.round_number // 2) % 5 == 0 and not self.pitty_tit_for_tat:
            self.pitty_tit_for_tat = self.is_tit_for_tat_player()
            if self.pitty_tit_for_tat:
                bid = 55
        if self.round_number > 15 and (self.round_number // 2) % 2 == 0 and self.pitty_tit_for_tat:
            if self.is_tit_for_tat_player():
                bid = 100
        self.my_log.append(bid)
        return bid

    def responder_strategy(self, offer: int) -> bool:
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

        accepted = offer >= threshold
        self.opponent_log_list.append((offer, accepted))
        return accepted

    def result(self, result: Round) -> None:
        # print(result)
        if result.accepted:
            self.my_score.append(result.offer)
        else:
            self.my_score.append(0)
        # print(self.my_score)
        # print(self.round_number)
        self.round_number = self.round_number + 1

    def slogan(self) -> str:
        return "The traitor is the greatest sage."

    def is_tit_for_tat_player(self) -> bool:
        tit_for_tat_counter = 0
        total_comparable_rounds = len(self.my_log) - 1

        for i in range(1, len(self.my_log)):
            if self.opponent_log_list[i-1][0] == self.my_log[i-1]:
                tit_for_tat_counter += 1

        if total_comparable_rounds > 0:
            tit_for_tat_percentage = (
                tit_for_tat_counter / total_comparable_rounds) * 100
        else:
            return False  # Cannot determine if no rounds to compare

        return tit_for_tat_percentage >= 98
