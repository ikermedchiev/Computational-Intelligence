import os
import time
from multiprocessing import Pool
from multiprocessing import cpu_count

# import game
from Ant import Ant
from Maze import Maze
from PathSpecification import PathSpecification


class AntColonyOptimization:
    """
    Class representing the first assignment. Finds shortest path between two points in a maze according to a specific path specification.
    """

    def __init__(self, maze, ants_per_gen, generations, q, evaporation, minconstant):
        """
        Constructs a new optimization object using ants.
         :param: maze the maze .
         :param: antsPerGen the amount of ants per generation.
         :param: generations the amount of generations.
         :param: Q normalization factor for the amount of dropped pheromone
         :param: evaporation the evaporation factor.
        """
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.minconstant = minconstant

    def get_route(self, pathspec):
        # print(f"Ant {i+1} of generation {g+1}")
        ant = Ant(self.maze, pathspec)
        return ant.find_route()

    def get_route_wrapper(self, args):
        return self.get_route(*args)

    def find_shortest_route(self, path_specification):
        """
        Loop that starts the shortest path process
        :param: spec Spefication of the route we wish to optimize
        :return: ACO optimized route
        """
        largelist = []
        p = Pool(cpu_count())

        for g in range(self.generations):
            print(f"Starting gen {g+1}")
            start_time = time.time()

            routelist = p.map(self.get_route_wrapper, zip([path_specification] * self.ants_per_gen))
            diff = time.time() - start_time

            print(f"Finished generation {g+1} in {diff:.2f} seconds with an avg of {sum(route.size() for route in routelist)/len(routelist)}.\nEvaporating previous pheromone")

            self.maze.evaporate(self.evaporation, self.minconstant)
            print(f"Adding pheromone")
            start_time = time.time()
            self.maze.add_pheromone_routes(routelist, self.q)
            diff = time.time() - start_time
            print(f"Finished pheromones in {diff:.2f} seconds")
            largelist.append(routelist)
            # print("\n".join(str(el) for el in self.maze.pheromones))

        shortestroute = largelist[0][0]
        for row in largelist:
            for route in row[1:]:
                # print(str(route))
                if route.shorter_than(shortestroute):
                    shortestroute = route

        self.maze.reset()
        return shortestroute


# Driver function for Assignment 1
if __name__ == "__main__":
    # parameters
    antsingen = 50  # ants per generation
    no_gen = 50  # amount of generations
    q = 1600  # constant to multiply the amount of pheromone
    evap = 0.5  # 1 - evaporation constant
    factor = 0.3
    gamify = False
    mazetype = "medium"
    # convergence criterion:
    # e.g. no imporvement in n steps

    # construct the optimization objects
    print(os.path.abspath(f"./../data/{mazetype} maze.txt"))
    maze = Maze.create_maze(f"./../data/{mazetype} maze.txt")
    spec = PathSpecification.read_coordinates(f"./../data/{mazetype} coordinates.txt")
    aco = AntColonyOptimization(maze, antsingen, no_gen, q, evap, factor)
    print(maze.walls)
    # if gamify:
    #     # startup game
    #     # app = game.App(maze, spec.start)
    #     app.on_init()
    #     app.on_render()
    # else:
    #     app = None
    # app.on_execute()

    # save starting time
    start_time_all = int(round(time.time() * 1000))

    # run optimization
    # shortest_route = aco.find_shortest_route(spec, app)
    shortest_route = aco.find_shortest_route(spec)
    # if gamify:
    #     app.on_cleanup()
    # print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time_all) / 1000.0))

    # save solution
    shortest_route.write_to_file(f"./../data/{mazetype}_solution.txt")

    # print route size
    print("Route size: " + str(shortest_route.size()))
