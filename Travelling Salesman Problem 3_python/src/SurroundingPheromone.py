from Direction import Direction
import numpy

class SurroundingPheromone:
    """ Class containing the pheromone information around a certain point in the maze """

    def __init__(self, north, east, south, west):
        """
        Creates a surrounding pheromone object.
        :param north: the amount of pheromone in the north.
        :param east: the amount of pheromone in the east.
        :param south: the amount of pheromone in the south.
        :param west: the amount of pheromone in the west.
        """

        #self.all = numpy.array(north, east, south, west)
        # self.get_total_surrounding_pheromone = numpy.sum(self.all)
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.total_surrounding_pheromone = east + north + south + west

    def get_total_surrounding_pheromone(self):
        """
         Get the total amount of surrounding pheromone.
         :return: total surrounding pheromone
        """

        return self.total_surrounding_pheromone

    def get_total_pheromone_possible_actions(self, actions):
        phs = 0
        for action in actions:
            phs += self.get(action)
        return phs

    def __str__(self) -> str:
        return f"N: {self.north}, E: {self.east}, S: {self.south}, W: {self.west}"

    def get(self, dir):
        """
        Get a specific pheromone level
        :param dir: Direction of pheromone
        :return: Pheromone of dir
        :rtype: number
        """
        if dir == Direction.north:
            return self.north
        elif dir == Direction.east:
            return self.east
        elif dir == Direction.west:
            return self.west
        elif dir == Direction.south:
            return self.south
        else:
            return None
