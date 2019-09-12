import random


class MyEGreedy:

    def __init__(self):
        print("Made EGreedy")

    def get_random_action(self, agent, maze):
        """selects an action at random in State s"""
        possibleactions = maze.get_valid_actions(agent)
        choice = random.choice(possibleactions)
        return choice

    def get_max_action_value(self, agent, maze, q_learning):
        possibleactions = maze.get_valid_actions(agent)
        actionvalues = q_learning.get_action_values(agent.get_state(maze), possibleactions)
        bestvalue = max(actionvalues)
        return bestvalue

    def get_best_action(self, agent, maze, q_learning):
        """select the best possible action currently known in State s."""
        possibleactions = maze.get_valid_actions(agent)
        actionvalues = q_learning.get_action_values(agent.get_state(maze), possibleactions)
        bestvalue = max(actionvalues)
        if bestvalue == 0:
            return self.get_random_action(agent, maze)
        c = actionvalues.count(bestvalue)
        myc = random.randint(0, c - 1)
        curcount = 0
        for i, val in enumerate(actionvalues):
            if val == bestvalue:
                if curcount == myc:
                    return possibleactions[i]
                curcount += 1
        # should not be executed
        print("EEEEEEEEE")
        ind = actionvalues.index(bestvalue)   
        return possibleactions[ind]             
        
    def get_egreedy_action(self, agent, maze, q_learning, epsilon):
        """ elect between random or best action selection based on epsilon."""
        chance = random.uniform(0,1)
        if chance <= epsilon:
            return self.get_random_action(agent, maze)
        else:
            return self.get_best_action(agent, maze, q_learning)
