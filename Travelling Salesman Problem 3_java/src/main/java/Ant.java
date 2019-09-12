import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;

/**
 * Class that represents the ants functionality.
 */
public class Ant {
    private static final int MAXSTEPS = Integer.MAX_VALUE;
    private static Random rand;
    private Maze maze;
    private Coordinate start;
    private Coordinate end;
    private Coordinate currentPosition;
    private List<Coordinate> positionsPassed;
    private HashSet<Coordinate> allPositions;

    /**
     * Constructor for ant taking a Maze and PathSpecification.
     *
     * @param maze Maze the ant will be running in.
     * @param spec The path specification consisting of a start coordinate and an end coordinate.
     */
    public Ant(Maze maze, PathSpecification spec) {
        this.positionsPassed = new ArrayList<>();
        this.maze = maze;
        this.start = spec.getStart();
        this.end = spec.getEnd();
        this.currentPosition = start;
        this.allPositions = new HashSet<>();
        if (rand == null) {
            rand = new Random();
        }
    }

    private Direction choice(List<Direction> choices, List<Double> percentages) {
        double ran = rand.nextDouble();
        for (int i = 0; i < choices.size(); i++) {
            double chance = percentages.get(i);
            if (ran <= chance) {
                return choices.get(i);
            }
            ran -= chance;
        }
        System.out.printf("We got an exception at pos %s (going from %s to %s)%n", this.currentPosition, this.start, this.end);
        System.out.println("percentages = " + percentages.toString());
        System.out.println("choices = " + choices);
        throw new IllegalStateException();
//        return null;
    }

    /**
     * Method that performs a single run through the maze by the ant.
     *
     * @return The route the ant found through the maze.
     */
    public Route findRoute() {
        Route route = new Route(start);
        Direction lastdir = null;
        int steps = 0;
//        System.out.printf("Going from %s to %s%n", this.currentPosition, this.end);
        while (!this.currentPosition.equals(this.end)) {
            SurroundingPheromone phs = this.maze.getSurroundingPheromone(this.currentPosition);
            Direction dir = this.decideDirection(phs, lastdir);
            route.add(dir);
            this.currentPosition = this.currentPosition.add(dir);
            this.allPositions.add(currentPosition);
            lastdir = dir;
            this.positionsPassed.add(this.currentPosition);
            int index = this.positionsPassed.indexOf(this.currentPosition);

            if (index != this.positionsPassed.size() - 1) { // error here with removing
                int oldSize = this.positionsPassed.size();
                this.positionsPassed = new ArrayList<>(this.positionsPassed.subList(0, index + 1));
                int toRemove = oldSize - this.positionsPassed.size();
                route.removeLastN(toRemove);
            }
            if (steps++ > MAXSTEPS) {
                System.out.println("STOPPED BECAUSE EXCEEDED MAXSTEPS");
                return null;
            }

        }
        return route;
    }

    private Direction decideDirection(SurroundingPheromone phs, Direction lastdir) {
        // get our valid actions
        List<Direction> pactions = this.maze.getValidActions(this.currentPosition);
        // if we have a lastAction
        boolean removed = false;
        if (lastdir != null) {
            removed = pactions.remove(Direction.inverse(lastdir));
        }
        if (pactions.isEmpty() && removed) {
            return Direction.inverse(lastdir);
        }
        if (pactions.size() == 1) {
            return pactions.get(0);
        }

        List<Direction> explore = new ArrayList<>();
        List<Double> explorePercent = new ArrayList<>();
        List<Double> percentages = new ArrayList<>();
        double explorePhs = 0.0, normalPhs = 0.0;

        for (Direction d : pactions) {
            double pheromone = phs.get(d);
            if (!allPositions.contains(this.currentPosition.add(d))) {
                explore.add(d);
                explorePercent.add(pheromone);
                explorePhs += pheromone;
            } else {
                percentages.add(pheromone);
                normalPhs += pheromone;
            }
        }
        if (!explore.isEmpty()) {
            if (explorePhs == 0) {
                System.out.println("SDAWJDWAD");
            }
            for (int i = 0; i < explorePercent.size(); i++) {
                double newExp = explorePercent.get(i) / explorePhs;
                explorePercent.set(i, newExp);
            }
            return choice(explore, explorePercent);
        }


        for (int i = 0; i < percentages.size(); i++) {
            double newP = percentages.get(i) / normalPhs;
            percentages.set(i, newP);
        }
        return choice(pactions, percentages);
    }
}

