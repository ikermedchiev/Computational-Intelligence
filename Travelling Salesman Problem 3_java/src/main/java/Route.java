import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.Serializable;
import java.util.ArrayList;

/**
 * Class representing a route.
 */
public class Route implements Serializable, Comparable {

    private static final long serialVersionUID = 0L;
    private ArrayList<Direction> route;
    private Coordinate start;

    /**
     * Route takes a starting coordinate to initialize
     *
     * @param start starting coordinate
     */
    public Route(Coordinate start) {
        route = new ArrayList<>();
        this.start = start;
    }

    /**
     * After taking a step we add the direction we moved in
     *
     * @param dir Direction we moved in
     */
    public void add(Direction dir) {
        route.add(dir);
    }


    /**
     * Returns the length of the route
     *
     * @return length of the route
     */
    public int size() {
        return route.size();
    }

    /**
     * Getter for the list of directions
     *
     * @return list of directions
     */
    public ArrayList<Direction> getRoute() {
        return route;
    }

    /**
     * Getter for the starting coordinate
     *
     * @return the starting coordinate
     */
    public Coordinate getStart() {
        return start;
    }

    /**
     * Function that checks whether a route is smaller than another route
     *
     * @param other the other route
     * @return whether the route is shorter
     */
    public boolean shorterThan(Route other) {
        if (other == null) return true;
        return this.size() < other.size();
    }

    /**
     * Take a step back in the route and return the last direction
     *
     * @return last direction
     */
    public Direction removeLast() {
        return route.remove(route.size() - 1);
    }

    public void removeLastN(int n) {
//        for (int i = 0; i < n; i++) {
//            this.removeLast();
//        }
        this.route = new ArrayList<>(route.subList(0, route.size() - n));
    }

    /**
     * Build a string representing the route as the format specified in the manual.
     *
     * @return string with the specified format of a route
     */
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Direction dir : route) {
            sb.append(Direction.dirToInt(dir)).append(";\n");
        }
        return sb.toString();
    }


    /**
     * Equals method for route
     *
     * @param other Other route
     * @return boolean whether they are equal
     */
    public boolean equals(Object other) {
        if (!(other instanceof Route)) {
            return false;
        } else {
            Route otherR = (Route) other;
            return this.start.equals(otherR.start)
                    && this.route.equals(otherR.route);
        }
    }

    /**
     * Method that implements the specified format for writing a route to a file.
     *
     * @param filePath path to route file.
     * @throws FileNotFoundException
     */
    public void writeToFile(String filePath) throws FileNotFoundException {
        PrintWriter pw = new PrintWriter(filePath);
        String sb = String.valueOf(route.size()) + ";\n" +
                start + ";\n" +
                this.toString();
        pw.write(sb);
        pw.close();
    }

    /**
     * Compares this object with the specified object for order.  Returns a
     * negative integer, zero, or a positive integer as this object is less
     * than, equal to, or greater than the specified object.
     *
     * <p>The implementor must ensure
     * {@code sgn(x.compareTo(y)) == -sgn(y.compareTo(x))}
     * for all {@code x} and {@code y}.  (This
     * implies that {@code x.compareTo(y)} must throw an exception iff
     * {@code y.compareTo(x)} throws an exception.)
     *
     * <p>The implementor must also ensure that the relation is transitive:
     * {@code (x.compareTo(y) > 0 && y.compareTo(z) > 0)} implies
     * {@code x.compareTo(z) > 0}.
     *
     * <p>Finally, the implementor must ensure that {@code x.compareTo(y)==0}
     * implies that {@code sgn(x.compareTo(z)) == sgn(y.compareTo(z))}, for
     * all {@code z}.
     *
     * <p>It is strongly recommended, but <i>not</i> strictly required that
     * {@code (x.compareTo(y)==0) == (x.equals(y))}.  Generally speaking, any
     * class that implements the {@code Comparable} interface and violates
     * this condition should clearly indicate this fact.  The recommended
     * language is "Note: this class has a natural ordering that is
     * inconsistent with equals."
     *
     * <p>In the foregoing description, the notation
     * {@code sgn(}<i>expression</i>{@code )} designates the mathematical
     * <i>signum</i> function, which is defined to return one of {@code -1},
     * {@code 0}, or {@code 1} according to whether the value of
     * <i>expression</i> is negative, zero, or positive, respectively.
     *
     * @param o the object to be compared.
     * @return a negative integer, zero, or a positive integer as this object
     * is less than, equal to, or greater than the specified object.
     * @throws NullPointerException if the specified object is null
     * @throws ClassCastException   if the specified object's type prevents it
     *                              from being compared to this object.
     */
    @Override
    public int compareTo(Object o) {
        if (!(o instanceof Route)) return 1;
        return Integer.compare(this.size(), ((Route) o).size());
    }
}
