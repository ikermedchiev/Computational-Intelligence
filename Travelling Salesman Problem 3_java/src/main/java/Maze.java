import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

/**
 * Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
 * well as the starting and end coordinates.
 */
public class Maze {
    private int width;
    private int length;
    private int[][] walls;
    private double[][] pheromones;
//    private Coordinate start;
//    private Coordinate end;

    /**
     * Constructor of a maze
     *
     * @param walls  int array of tiles accessible (1) and non-accessible (0)
     * @param width  width of Maze (horizontal)
     * @param length length of Maze (vertical)
     */
    public Maze(int[][] walls, int width, int length) {
        this.walls = walls;
        this.length = length;
        this.width = width;
        initializePheromones();
    }

    /**
     * Method that builds a mze from a file
     *
     * @param filePath Path to the file
     * @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
     */
    public static Maze createMaze(String filePath) throws FileNotFoundException {
        Scanner scan = new Scanner(new FileReader(filePath));
        int width = scan.nextInt();
        int length = scan.nextInt();
        int[][] mazeLayout = new int[width][length];
        for (int y = 0; y < length; y++) {
            for (int x = 0; x < width; x++) {
                mazeLayout[x][y] = scan.nextInt();
            }
        }
        scan.close();
        return new Maze(mazeLayout, width, length);
    }

    /**
     * Initialize pheromones to a start value.
     */
    private void initializePheromones() {
        this.pheromones = new double[this.width][this.length];
        for (int i = 0; i < this.width; i++) {
            for (int j = 0; j < this.length; j++) {
                this.pheromones[i][j] = 10;
            }
        }
    }

    /**
     * Reset the maze for a new shortest path problem.
     */
    public void reset() {
        initializePheromones();
    }

    /**
     * Update the pheromones along a certain route according to a certain Q
     *
     * @param r The route of the ants
     * @param Q Normalization factor for amount of dropped pheromone
     */
    public void addPheromoneRoute(Route r, double Q) {
        double phToAdd = (1.0 / r.size()) * Q;
//        System.out.println(phToAdd);
        Coordinate pos = r.getStart();
        this.pheromones[pos.getX()][pos.getY()] += phToAdd;
        HashSet<Coordinate> poss = new HashSet<>(r.size());
        for (Direction d : r.getRoute()) {
            pos = pos.add(d);
            if (poss.add(pos)) {
                this.pheromones[pos.getX()][pos.getY()] += phToAdd;
            }
        }

    }

    /**
     * Update pheromones for a list of routes
     *
     * @param routes A list of routes
     * @param Q      Normalization factor for amount of dropped pheromone
     */
    public void addPheromoneRoutes(List<Route> routes, double Q) {
        for (Route r : routes) {
            addPheromoneRoute(r, Q);
        }
    }

    /**
     * Evaporate pheromone
     *
     * @param rho    evaporation factor
     * @param factor
     */
    public void evaporate(double rho, double factor) {
        double max = 0;
        for (int i = 0; i < this.width; i++) {
            for (int j = 0; j < this.length; j++) {
                this.pheromones[i][j] *= (1.0 - rho);
//                if (this.pheromones[i][j] > max) {
//                    max = this.pheromones[i][j];
//                }
            }
        }
//        double minconstant = max * factor;
//        for (int i = 0; i < this.width; i++) {
//            for (int j = 0; j < this.length; j++) {
//                if (this.pheromones[i][j] < minconstant)
//                    this.pheromones[i][j] = 0;
//            }
//        }
    }

    /**
     * Width getter
     *
     * @return width of the maze
     */
    public int getWidth() {
        return width;
    }

    /**
     * Length getter
     *
     * @return length of the maze
     */
    public int getLength() {
        return length;
    }

    /**
     * Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
     *
     * @param position The position to check the neighbours of.
     * @return the pheromones of the neighbouring positions.
     */
    public SurroundingPheromone getSurroundingPheromone(Coordinate position) {
        double east = this.getPheromone(position.add(Direction.East));
        double north = this.getPheromone(position.add(Direction.North));
        double south = this.getPheromone(position.add(Direction.South));
        double west = this.getPheromone(position.add(Direction.West));
        return new SurroundingPheromone(north, east, south, west);
    }

    public List<Direction> getValidActions(Coordinate pos) {
        List<Direction> pactions = new ArrayList<>(4);
        for (int i = 0; i < 4; i++) {
            Coordinate newPos = pos.add(Direction.intToDir(i));
            if (this.isWalkAble(newPos)) {
                pactions.add(Direction.intToDir(i));
            }
        }
        return pactions;

    }

    private boolean isWalkAble(Coordinate p) {
        if (!this.inBounds(p)) {
            return false;
        }
        return walls[p.getX()][p.getY()] == 1;
    }

    /**
     * Pheromone getter for a specific position. If the position is not in bounds returns 0
     *
     * @param pos Position coordinate
     * @return pheromone at point
     */
    private double getPheromone(Coordinate pos) {
        if (!this.inBounds(pos)) {
            return 0;
        }
        return this.pheromones[pos.getX()][pos.getY()];
    }

    /**
     * Check whether a coordinate lies in the current maze.
     *
     * @param position The position to be checked
     * @return Whether the position is in the current maze
     */
    public boolean inBounds(Coordinate position) {
        return position.xBetween(0, width) && position.yBetween(0, length);
    }

    /**
     * Representation of Maze as defined by the input file format.
     *
     * @return String representation
     */
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(width);
        sb.append(' ');
        sb.append(length);
        sb.append(" \n");
        for (int y = 0; y < length; y++) {
            for (int x = 0; x < width; x++) {
                sb.append(walls[x][y]);
                sb.append(' ');
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    public void printPheromones(Route r, PathSpecification spec) {
        StringBuilder sb = new StringBuilder("Pheromones: \n");
        for (int i = 0; i < this.length; i++) {
            sb.append("|");
            for (int j = 0; j < this.width; j++) {
                sb.append(String.format("%-8.0f ", pheromones[j][i]));
            }
            sb.append("|\n");
        }
        try {
            if (!Files.exists(Paths.get("output"))) {
                Files.createDirectory(Paths.get("output"));
            }
            Files.write(Paths.get(String.format("output/pheromones_%s-%s(%d).txt",
                spec.getStart(), spec.getEnd(), r.size())), sb.toString().getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
//        System.out.println(sb.toString());
    }
}
