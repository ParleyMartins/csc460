class BasicAgent:
    def __init__(self, decision_point = 15):
        self.decision_point = decision_point

    def act(self, state):
        if blackjack.BlackJack.calc(state.player_hand) > self.decision_point:
            return 'S'
        else:
            return 'H'
