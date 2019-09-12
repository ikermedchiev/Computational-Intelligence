////import org.junit.jupiter.api.Test;
//
//import java.util.Arrays;
//import java.util.Random;
//
//public class PerfTest {
//
//    public static Random random = new Random();
//
////    @Test
//    void testWeightedChoice() {
//        double[] percentages = new double[]{0.1, 0.2, 0.5, 0.2};
//        int[] pactions = new int[]{0, 1, 2, 3};
//
//        // TODO test this
//        int[] counts = new int[4];
//        int tries = 10000000;
//
//        for (int i = 0; i < tries; i++) {
//            int c = choice(pactions, percentages);
//            counts[c]++;
//        }
//
//        System.out.println(Arrays.toString(counts));
//
//        double[] results = new double[4];
//        for (int i = 0; i < counts.length; i++) {
//            results[i] = counts[i] / (double) tries;
//        }
//        System.out.println(Arrays.toString(results));
//
//    }
//
//    int choice(int[] choices, double[] percentages) {
//        double ran = random.nextDouble();
//        for (int i = 0;
//             i < choices.length - 1; i++) {
//            double percentage = percentages[i];
//            if (ran <= percentage) {
//                return choices[i];
//            }
//            ran -= percentage;
//        }
//        return choices[choices.length - 1];
//    }
//}
