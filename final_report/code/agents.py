import random
from enum import IntEnum
from contextlib import suppress


verbs = {(0, 1): "covered by",
         (0, 2): "smashes",
         (1, 0): "covers",
         (1, 2): "cut by",
         (2, 0): "smashed by",
         (2, 1): "cuts"}


def score(a1, a2, verbose=False):
    """
    Return the score for a rock-paper-scissors game.
    If verbose, display a message
    
    >>> score(Action.r, Action.r)
    0
    >>> score(Action.r, Action.r, verbose=True)
    ROCK ties ROCK: No win!
    0
    >>> score(Action.p, Action.r, True)
    PAPER covers ROCK: Player 1 wins!
    1
    >>> score(Action.s, Action.r, True)
    SCISSORS smashed by ROCK: Player 2 wins!
    -1
    >>> score(0, 1)
    -1
    """
    result = 0
    if a1 == a2:
        if verbose:
            print("{} ties {}: No win!".format(a1.name, a2.name))
        return result

    # if parity is the same, lower value wins
    if a1 % 2 == a2 % 2:
        result = 1 if a1 < a2 else -1
    else:     # if parity is different, higher value wins
        result = 1 if a1 > a2 else -1
        
    if verbose:
        winner = 1 if result > 0 else 2
        print("{} {} {}: Player {} wins!".format(a1.name,
                                                 verbs[(a1, a2)],
                                                 a2.name, 
                                                 winner))
    return result
          


class Action(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2
    # aliases
    r = 0
    p = 1
    s = 2
    R = 0
    P = 1
    S = 2
    rock = 0
    paper = 1
    scissors = 2

class RPSAgent():
    """
    Interface for a generic Rock-Paper-Scissors agent.
    """
    
    def __init__(self):
        """
        Whatever setup you might need to do for a match, do here.
        """
        pass
    
    def act(self):
        """
        And however you might want to act, do it here.
        Must return an Action.
        """
        return Action.r
    
    def react(self, response):
        """
        And respond however you would like to the action taken by 
        the other player. Nothing returned.
        """
        pass
    
    def __str__(self):
        """
        Return a nicely formatted name
        """
        return self.__class__.__name__
    
    @classmethod
    def _name(cls):
        """
        Convenience for logging
        """
        return cls.__name__
          
    
class CommandLineAgent(RPSAgent):
    """
    Allows humans to play in the bot tournaments. Prompts user for action 
    selection at each round. Does not cheat.
    """
    def __init__(self, actions="[r]ock, [p]aper, [s]cissors", name=None):
        self.actions = actions
        self.name = name
        self.choice = None
        pass

        
    def act(self):
        choice = None
        while choice is None:
            choice = input("Select action {}: ".format(self.actions))
            try:
                choice = Action[choice]
            except KeyError:
                # one last try
                with suppress(ValueError):
                    choice = Action(int(choice))
                    self.choice = choice
                    return choice
                
                # okay, this is not a choice
                print("{} is not a valid action".format(choice))
                choice = None
        self.choice = choice
        return choice
    
    def react(self, response):
        score(self.choice, response, verbose=True)

    
class StubbornAgent(RPSAgent):
    """
    Choose an action at the start and stick to it.
    """
    def __init__(self, action=None):
        if action is None:
            action = random.choice(list(Action))
        self.action = action
            
    def act(self):
        return self.action

    
class NashAgent(RPSAgent):
    """
    Uniformly randomly choose an action each time, ignoring
    opponent actions.
    """
    def __init__(self):
        self.actions = list(Action)
    
    def act(self):
        return random.choice(self.actions)
        

class MirrorAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the action
    the opponent chose last time
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action

    def react(self, response):
        self.action = response


class ScaredyAgent(RPSAgent):
    """
    Randomly chooses a first action, then keep doing it as long as it wins, otherwise 
    randomly switch to one of the other two.
    """
    def __init__(self):
        self.action = random.choice(list(Action))
    
    def act(self):
        return self.action
    
    def react(self, response):
        result = score(self.action, response)

        # if we won, keep doing the same thing.
        if result > 0:
            return
        # otherwise we need to choose a new action
        options = list(Action)
        
        # if we tied, randomly choose from everything
        if result == 0:
            self.action = random.choice(options)
        else: # choose anything but what you just did
            options.remove(self.action)
            self.action = random.choice(options)
            
        

class CounterAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the next action
    that would have beaten the opponent's last action
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action
    
    def react(self, response):
        action = (response + 1) % len(Action)
        self.action = Action(action)
        
class SelfCounterAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the next action
    that would have beaten your last action
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action
    
    def react(self, response):
        response = (self.action + 1) % len(Action)
        self.action = Action(response)
    
  
##########################################
## STUDENT AGENTS
##########################################

class StatisticAgent(RPSAgent):
    """
    Randomly selects first action, then chooses the next action
    based on the most played action from opponent
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        self.total_each = [0, 0, 0]

    def act(self):
        return self.action

    def react(self, response):
        self.total_each[response] += 1
        max_index = self.total_each.index(max(self.total_each))
        if max_index == Action.ROCK:
            self.action = Action.PAPER
        elif max_index == Action.PAPER:
            self.action = Action.SCISSORS
        else:
            self.action = Action.ROCK

class SimpleCycleAgent(RPSAgent):
    """
    Beats the cycle R, P, S by playing P, S, R all the time
    """

    def __init__(self):
        self.action = Action.PAPER

    def act(self):
        return self.action

    def react(self, response):
        self.action = Action((self.action + 1) % len(Action))

class BiggerCycleAgent(RPSAgent):
    """
    Generates a big random cycle and uses it
    """

    def __init__(self):
        self.cycle_size = random.randint(1000, 10000)
        self.cycle = []
        for _ in range(self.cycle_size):
            self.cycle.append(random.choice(list(Action)))
        self.next = 0

    def act(self):
        return self.cycle[self.next]

    def react(self, response):
        self.next = (self.next + 1) % self.cycle_size

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Done tests")
    