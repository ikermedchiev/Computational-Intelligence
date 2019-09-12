import random

from numpy.random import choice

from Direction import Direction
from Maze import Maze
from Route import Route
# from game import App


class Ant:
    """ Class that represents the ants functionality. """
    maze: Maze
    # game: App

    def __init__(self, maze, path_specification):
        """
        Constructor for ant taking a Maze and PathSpecification.
        :param maze: Maze the ant will be running in.
        :param path_specification: The path specification consisting of a start coordinate and an end coordinate.
        """
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        # self.game = game
        self.game = None
        self.current_position = self.start
        self.rand = random

    def decide_dir(self, phs, lastdir):
        p_actions = self.maze.get_possible_actions(self.current_position)
        # print(p_actions)
        if len(p_actions) > 1 and lastdir is not None:
            toremove = Direction.inv_dir(lastdir)
            if toremove in p_actions:
                p_actions.remove(toremove)

        total_pheromone = phs.get_total_pheromone_possible_actions(p_actions)
        percentage = []
        exploration = []
        for i in p_actions:
            if phs.get(i) == 0:
                exploration.append(i)
            else:
                percentage.append(phs.get(i) / total_pheromone)

        if len(exploration) == 0:
            return choice(p_actions, p=percentage)
        return random.choice(exploration)

    def find_route(self):
        """
        Method that performs a single run through the maze by the ant.
        :return The route the ant found through the maze.
        """
        route = Route(self.start)
        poss = [self.current_position]
        lastdir = None
        steps = 0
        maxsteps = 10000
        # print(f"Going from {self.current_position} to {self.end}")
        while self.current_position != self.end:
            # check which ways you can go
            phs = self.maze.get_surrounding_pheromone(self.current_position)
            direction = self.decide_dir(phs, lastdir)
            if direction is None:
                print("NON_VALID_DIRECTION")
                print(f"position: {self.current_position}\nPHS: {phs}")
                # print(phs)
            route.add(direction)
            self.current_position = self.current_position.add_direction(direction)
            if self.game is not None:
                self.game.update(self.current_position)
            # potentially wait till the game updates

            lastdir = direction
            steps += 1
            if steps > maxsteps:
                break
        # print(f"Finished route calculation")
        # route.add(Direction(0))
        return route
