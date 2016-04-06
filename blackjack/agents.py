import blackjack


class ThoughtlessAgent:
    def __init__(self, actions=('H', 'S', 'D')):
        self.actions = actions
    
    def act(self, state):
        return self.actions[0]

class BasicAgent:
    def __init__(self, decision_point = 15):
        self.decision_point = decision_point

    def act(self, state):
        if blackjack.BlackJack.calc(state.player_hand) > self.decision_point:
            return 'S'
        else:
            return 'H'
#These clases were meant to be used from the command line on question1
class BasicAgent2(BasicAgent):
    def __init__(self):
        BasicAgent.__init__(self, 13)

class BasicAgent3(BasicAgent):
    def __init__(self):
        BasicAgent.__init__(self, 17)

class SophisticatedReactiveAgent:
    def __init__(self):
        probabilities = {
        11: {'player':[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        12: {'player':[ 0.112151, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        13: {'player':[ 0.113459, 0.121796, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        14: {'player':[ 0.108566, 0.116489, 0.126472, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        15: {'player':[ 0.104683, 0.113339, 0.1226, 0.133229, 0.0, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        16: {'player':[ 0.098878, 0.107766, 0.116696, 0.127078, 0.137868, 0.0, 0.0, 0.0, 0.0 ],
            'dealer': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]},
        17: {'player':[ 0.095005, 0.10293, 0.113352, 0.122757, 0.134463, 0.145419, 0.0, 0.0, 0.0 ],
            'dealer': [0.14529, 0.145208, 0.144938, 0.145957, 0.145811, 0.145079, 0.145296, 0.145812, 0.145341 ]},
        18: {'player':[ 0.087997, 0.096707, 0.106417, 0.116627, 0.12674, 0.138892, 0.150322, 0.0, 0.0 ],
            'dealer': [0.138132, 0.138408, 0.138303, 0.138491, 0.138687, 0.138349, 0.138351, 0.138121, 0.138796 ]},
        19: {'player':[ 0.082508, 0.091814, 0.1014, 0.11165, 0.122521, 0.133452, 0.146136, 0.158993, 0.0 ],
            'dealer': [0.134261, 0.133925, 0.133681, 0.13378, 0.133951, 0.1336, 0.134149, 0.133304, 0.133425 ]},
        20: {'player':[ 0.12726, 0.136027, 0.146199, 0.155699, 0.166065, 0.177608, 0.190502, 0.202323, 0.216712 ],
            'dealer': [0.177847, 0.177267, 0.178381, 0.177834, 0.178087, 0.178177, 0.177683, 0.177177, 0.177654 ]},
        21: {'player':[ 0.069493, 0.078527, 0.087761, 0.098555, 0.108981, 0.120928, 0.133208, 0.145598, 0.159191 ],
            'dealer': [0.121256, 0.12128, 0.120626, 0.120048, 0.120854, 0.121077, 0.120766, 0.120919, 0.120508 ]},
        22: {'player':[ 0.0, 0.034605, 0.079103, 0.134405, 0.203362, 0.283701, 0.379832, 0.493086, 0.624097 ],
            'dealer': [0.283214, 0.283912, 0.284071, 0.28389, 0.28261, 0.283718, 0.283755, 0.284667, 0.284276 ]},
        }
        # This table came from Question 3. Each 'column' represents actions on 
        #    one value from 11 (first column) to 19 (last one), playing 1 million games
        # It's interesting that the dealer's probabilities stay pretty much the same, without
        #    any dependency on the agent's action.
        #(To get the dealer's probabilities, just change line 118 
        #    (I know this should be a parameter, but this is not big enough for that) )

        self.probabilities = {}
        for points in range(11, 20):
            index = points % 11 #Because 11 is the start point on the vectors
            not_bust = 0
            not_bust_dealer = 0
            not_bust = probabilities[points]['player'][index]
            for i in range(points, 22):
                not_bust += probabilities[i]['player'][index] 
                not_bust_dealer += probabilities[i]['dealer'][index] 
            bust = probabilities[22]['player'][index]
            bust_dealer = probabilities[22]['dealer'][index]
            self.probabilities[points] = {'player': {'not_bust': not_bust, 'bust': bust},
            'dealer':{'not_bust': not_bust_dealer, 'bust': bust_dealer}}


    def act(self, state):
        my_points = blackjack.BlackJack.calc(state.player_hand)        
        if my_points < 11:
            return 'H'
        elif my_points >= 18:
            return 'S'

        if ((self.probabilities[my_points]['player']['not_bust'] -
            self.probabilities[my_points]['player']['bust']) > 0.1 and
            self.probabilities[my_points]['player']['not_bust'] >
            self.probabilities[my_points]['dealer']['not_bust']):
            return 'H'
        else:
            return 'S'

class CommandLineAgent:
    interactive = True
    
    def act(self, state):
        """
        Display the game state information and prompt for action choice
        """
        return input("Choose an action [H]it, [S]tand, [D]ouble:").upper()

def print_probabilities(probabilities):
    for value, p in probabilities.items():
        print_value = "| {} |".format(value)
        for probability in p:
            print_value += " {} |".format(probability)
        print(print_value)

def marginal_probability(agent_class=BasicAgent):
    probabilities = {i: [] for i in range(11,23)}
    for i in range(11, 20):
        agent = agent_class(i) #decision point for the basic agent
        num_hands = 1000000
        points_total = {i: 0 for i in range(11,23)}

        for hand in range(num_hands):
            game = blackjack.BlackJack()
            game.start_game()
            while game.state.terminate == 0:
                game.act(agent)
            game.final()
            points = game.calc(game.state.player_hand)
            if(points > 22):
                points = 22
            points_total[points] += 1

        for p, total in points_total.items():
            probabilities[p].append(total/num_hands)
    print_probabilities(probabilities)


def probability_to_exceed_target(hand, target=21):
    probabilities = [0]
    [probabilities.append(1) for i in range(1, 10)]
    probabilities.append(4)
    total_cards = 13

    if(hand_value > target):
        # if your hand already exceeded your target,
        # obviously the next value will also exceed it
        return 1.0

    # It has to be greater than the target, not equals
    min_value = (target - hand_value) + 1

    try:
        probability = 0.0
        for i in range(min_value, 11):
            probability = probability + probabilities[i]
        return probability/total_cards
    except Exception:
        # if the min_value is not found, then you are save
        return 0.0

if __name__ == '__main__':
    import doctest
    doctest.testmod()
