import sys
import traceback

from Direction import Direction
from SurroundingPheromone import SurroundingPheromone


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.


class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.pheromones = []
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.initialize_pheromones()

    def initialize_pheromones(self):
        """Initialize pheromones to a start value. """
        for i in range(self.width):
            self.pheromones.append([])
            for _ in range(self.length):
                self.pheromones[i].append(0)

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    def get_possible_actions(self, position):
        options = []
        for i in [Direction.north, Direction.east, Direction.south, Direction.west]:
            possible_location = position.add_direction(i)
            if self.in_bounds(possible_location) \
                    and self.walls[possible_location.get_x()][possible_location.get_y()] == 1:
                options.append(i)
        return options

    # @staticmethod
    # def add_dir(x,y, dir):
    #     return
    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        if len(route.route) == 0:
            return
        positions = []
        ph_to_add = (1 / route.size()) * q
        position = route.get_start()
        directions = route.get_route()
        self.pheromones[position.get_x()][position.get_y()] += ph_to_add
        for direction in directions:
            position = position.add_direction(direction)
            # if position not in positions:
            self.pheromones[position.get_x()][position.get_y()] += ph_to_add
                # positions.append(position)
        return

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho, factor):
        max = 0
        for i in range(self.width):
            for j in range(self.length):
                self.pheromones[i][j] *= rho
                if self.pheromones[i][j] > max:
                    max = self.pheromones[i][j]
        minconstant = factor * max
        for i in range(self.width):
            for j in range(self.length):
                if self.pheromones[i][j] <= minconstant:
                    self.pheromones[i][j] = 0
        # Add statement for minimum amout of pheromone
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    def get_surrounding_pheromone(self, position):
        """
        Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
        :type position: Coordinate.Coordinate
        :param position: The position to check the neighbours of.
        :return: the pheromones of the neighbouring positions.
        """
        east = self.get_pheromone(position.add_direction(Direction.east))
        north = self.get_pheromone(position.add_direction(Direction.north))
        west = self.get_pheromone(position.add_direction(Direction.west))
        south = self.get_pheromone(position.add_direction(Direction.south))
        return SurroundingPheromone(north, east, south, west)

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        if not self.in_bounds(pos):
            return 0
        return self.pheromones[pos.get_x()][pos.get_y()]

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y + 1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
