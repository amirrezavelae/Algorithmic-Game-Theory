from models import Round, Log

'''
This is the class you need to implement for phase 3. It will be used to play the game with the opponent.
Change the class name to match your student number.
'''


class Agent99100000:
    '''
    Player log: A Log object containing all the games played by you.
    Opponent log: A Log object containing all the games played by the opponent.
    Proposer: A boolean indicating whether you are the proposer (True) or the responder (False).
    '''

    def __init__(self, player_log: Log, opponent_log: Log, proposer: bool) -> None:
        # write your code here
        pass

    def proposer_strategy(self) -> int:
        # write your code here
        pass

    def responder_strategy(self, offer: int) -> bool:
        # write your code here
        pass

    def result(self, result: Round) -> None:
        # write your code here
        pass

    def slogan(self) -> str:
        return "The traitor is the greatest sage."
