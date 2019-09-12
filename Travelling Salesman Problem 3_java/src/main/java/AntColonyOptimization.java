import aliceinnets.python.jyplot.JyPlot;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.logging.Level;
import java.util.logging.Logger;


/**
 * Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
 * path specification.
 */
public class AntColonyOptimization {
    public static final int ELITISM = 10;
    private static Level logLevel = Level.ALL;
    private List<Integer> averages;
    private List<Integer> smallest;
    private Logger logger = Logger.getLogger(AntColonyOptimization.class.getName());
    private int antsPerGen;
    private int convergenceRuns;
    private int generations;
    private double Q;
    private double factor;
    private double evaporation;
    private ExecutorService executor;
    private Maze maze;

    /**
     * Constructs a new optimization object using ants.
     *
     * @param maze        the maze .
     * @param antsPerGen  the amount of ants per generation.
     * @param generations the amount of generations.
     * @param Q           normalization factor for the amount of dropped pheromone
     * @param evaporation the evaporation factor.
     */
    public AntColonyOptimization(Maze maze, int antsPerGen, int generations, double Q, double evaporation, int convergenceRuns) {
        this.maze = maze;
        this.antsPerGen = antsPerGen;
        this.generations = generations;
        this.convergenceRuns = convergenceRuns;
        this.averages = new ArrayList<>(generations);
        this.smallest = new ArrayList<>(generations);
        this.factor = 0.00001;
        this.executor = Executors.newFixedThreadPool(antsPerGen);
        this.Q = Q;
        this.evaporation = evaporation;
        this.logger.setLevel(logLevel);
    }

    /**
     * Driver function for Assignment 1
     */
    public static void main(String[] args) throws FileNotFoundException {
        //parameters
        int ants = 100;
        int noGen = 150;
        int convergenceRuns = 150;

        double Q = 1600;
        double evap = 0.5;
        String mazetype = "hard";

        //construct the optimization objects
        Maze maze = Maze.createMaze(String.format("./data/%s maze.txt", mazetype));
        PathSpecification spec = PathSpecification.readCoordinates(String.format("./data/%s coordinates.txt", mazetype));
        AntColonyOptimization aco = new AntColonyOptimization(maze, ants, noGen, Q, evap, convergenceRuns);


        //save starting time
        long startTime = System.currentTimeMillis();

        //run optimization
        Route shortestRoute = aco.findShortestRoute(spec);

        //print time taken
        System.out.println("Time taken: " + ((System.currentTimeMillis() - startTime) / 1000.0) + " seconds");
        JyPlot plt = new JyPlot();
        for (int i = 0; i < aco.smallest.size(); i++) {
            plt.scatter(i, aco.smallest.get(i), 5, "#ff0000");
            plt.scatter(i, aco.averages.get(i), 5, "#00ff00");
        }
        plt.title(String.format("Steps over generations with %d ants at %d", ants, shortestRoute.size()));

        plt.ylabel("Number of steps");
        plt.xlabel("Generation");
//        plt.legend();

        plt.show();
        plt.exec();
        //save solution
        shortestRoute.writeToFile(String.format("./data/%s_solution.txt", mazetype));

        //print route size
        System.out.println("Route size: " + shortestRoute.size());
        aco.close();
    }

    public void close() {
        this.executor.shutdownNow();
    }

    /**
     * Loop that starts the shortest path process
     *
     * @param spec Spefication of the route we wish to optimize
     * @return ACO optimized route
     */
    public Route findShortestRoute(PathSpecification spec) {
        List<Route> routes = new ArrayList<>();
        Route shortestRoute = null;
        int shortRouteCount = 0;
        int averageShortest = 0;
        for (int g = 0; g < this.generations; g++) {
//            logger.log(Level.INFO, "Starting gen " + (g));
            long start = System.currentTimeMillis();

            try {
                List<Callable<Route>> croutes = new ArrayList<>(this.antsPerGen);
                for (int i = 0; i < this.antsPerGen; i++) {
                    croutes.add(() -> new Ant(maze, spec).findRoute());
                }
                List<Future<Route>> froutes = executor.invokeAll(croutes);
                for (Future<Route> fr : froutes) {
                    routes.add(fr.get());
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            long diff = System.currentTimeMillis() - start;
            try {
                routes.sort(Route::compareTo);
            } catch (NullPointerException ignored) {
            }

            if (shortestRoute == null || routes.get(0).shorterThan(shortestRoute)) {
                shortestRoute = routes.get(0);
                shortRouteCount = 0;

            } else if (shortRouteCount++ > this.convergenceRuns) {
                System.out.printf("Converged on %d after %d runs%n", shortestRoute.size(), g);
                break;
            }

            int sum = routes.stream().mapToInt(Route::size).sum();
            int average = sum / this.antsPerGen;
            this.averages.add(average);
            this.smallest.add(routes.get(0).size());
            System.out.printf("Finished gen %d in %d millis with average of %d (best %d)%n", g, diff, sum / this.antsPerGen, shortestRoute.size());
            if (average == shortestRoute.size() && ++averageShortest > this.convergenceRuns) {
                System.out.printf("Converged on %d after %d runs%n", shortestRoute.size(), g);
            } else if (average != shortestRoute.size()) {
                averageShortest = 0;
            }


            this.maze.evaporate(this.evaporation, this.factor);
            weightedPheromones(routes, this.Q);
            this.maze.addPheromoneRoute(shortestRoute, this.Q);
            routes.clear();
        }
        maze.printPheromones(shortestRoute, spec);
        maze.reset();
        return shortestRoute;
    }

    private void weightedPheromones(List<Route> routes, double startq) {
        int i = 1;
        for (Route r : routes.subList(0, ELITISM)) {
            this.maze.addPheromoneRoute(r, (startq * i++) / ELITISM);
        }
    }

}
