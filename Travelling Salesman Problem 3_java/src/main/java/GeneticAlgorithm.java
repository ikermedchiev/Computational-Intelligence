import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.Collections;

/**
 * TSP problem solver using genetic algorithms.
 */
public class GeneticAlgorithm {

    private int generations;
    private int popSize;
    private int chromSize;

    /**
     * Constructs a new 'genetic algorithm' object.
     * @param generations the amount of generations.
     * @param popSize the population size.
     */
    public GeneticAlgorithm(int generations, int popSize, int chromSize) {
        this.generations = generations;
        this.popSize = popSize;
        this.chromSize = chromSize;
    }


    /**
     * Knuth-Yates shuffle, reordering a array randomly
     * @param chromosome array to shuffle.
     */
    private void shuffle(int[] chromosome) {
        int n = chromosome.length;
        for (int i = 0; i < n; i++) {
            int r = i + (int) (Math.random() * (n - i));
            int swap = chromosome[r];
            chromosome[r] = chromosome[i];
            chromosome[i] = swap;
        }
    }

    private void shuffle(int[][] chromosomes) {
        int n = chromosomes.length;
        for (int i = 0; i < n; i++) {
            int r = i + (int) (Math.random() * (n - i));
            int[] swap = chromosomes[r];
            chromosomes[r] = chromosomes[i];
            chromosomes[i] = swap;
        }
    }

    private void print(int[] chromosome) {
        for (int i : chromosome) {
            System.out.print(i + ", ");
        }
        System.out.println();
    }

    private void print(int[][] chromosomes) {
        for (int[] chromosome : chromosomes) {
            for (int i : chromosome) {
                System.out.print(i + ", ");
            }
            System.out.println("|");
        }
        System.out.println();
    }

    private int[] initializeChromosome(int length) {
        int[] chromosome = new int[length];
        for (int i = 0; i < length; i++) {
            chromosome[i] = i;
        }
        this.shuffle(chromosome);
        return chromosome;
    }

    private int lengthOfChromosome(int[] chromosome, TSPData pd) {
        int totalLength = pd.getStartDistances()[chromosome[0]];
        for (int i = 0; i < chromosome.length - 1; i++) {
            totalLength += pd.getDistances()[chromosome[i]][chromosome[i+1]];
        }
        totalLength += pd.getEndDistances()[chromosome[chromosome.length-1]];
        return totalLength;
    }

    private int[] mutation(int[] result) {

        Random random = new Random();
        int firstMutationIndex = random.nextInt(result.length - 1);
        int secondMutationIndex = random.nextInt(result.length - 1);

        int tmp = result[firstMutationIndex];
        result[firstMutationIndex] = result[secondMutationIndex];
        result[secondMutationIndex] = tmp;

        return result;

        /*
        ArrayList<Integer> chromosomeTemp = new ArrayList<Integer>();
        for (int i : result) {
            chromosomeTemp.add(i);
        }

        Collections.swap(chromosomeTemp, firstMutationIndex, secondMutationIndex);

        int[] resultMutation = new int[18];
        for (int i = 0; i < chromosomeTemp.size(); i++) {
            result[i] = chromosomeTemp.get(i);
        }
        return resultMutation;*/
    }

    private int[] crossOver(int[] chrom1, int[] chrom2) {
        int crossOverLength;
        Random random = new Random();
        double chance = random.nextDouble();
        if (chance < 0.25) {
            crossOverLength = 1;
        } else if (chance < 0.75) {
            crossOverLength = 2;
        }
        else {
            crossOverLength = 3;
        }

        int randomIndex = random.nextInt(chrom1.length - crossOverLength);

        int[] crossOverProduct = new int[crossOverLength];
        for (int i = 0; i < crossOverLength; i++) {
            crossOverProduct[i] = chrom1[randomIndex + i];
        }

        ArrayList<Integer> chromosome3 = new ArrayList<Integer>();
        for (int i : chrom2) {
            chromosome3.add(i);
        }

        for (int i = 0; i < crossOverLength; i++) {
            chromosome3.remove((Integer) crossOverProduct[i]);
        }
        for (int i = 0; i < crossOverLength; i++) {
            chromosome3.add(randomIndex + i, crossOverProduct[i]);
        }

        return chromosome3.stream().mapToInt(i->i).toArray();
    }

    public int[] reproduce(int[] chrom1, int[] chrom2) {
        int[] chrom3 = chrom1;
        if (Math.random() < 0.8) {
            chrom3 = crossOver(chrom1, chrom2);
        }
        if (Math.random() < 0.01) {
            chrom3 = mutation(chrom3);
        }
        return chrom3;
    }

    public int[][] reproduceList(int[][] chromosomes, TSPData pd) {
        double[] inverseLengths = new double[popSize];
        double sumOfInverseLengths = 0;
        for (int i = 0; i < popSize; i++) {
            inverseLengths[i] = 1.0/lengthOfChromosome(chromosomes[i], pd);
            sumOfInverseLengths += inverseLengths[i];
        }

        /*
        // Create reproduction pool
        Random random = new Random();
        int reproductionSize = 3;
        int[][] reproductionChromosomes = new int[reproductionSize][];
        for (int i = 0; i < reproductionSize; i++) {
            double chance = random.nextDouble()*sumOfInverseLengths;
            double addedChance = 0;
            for (int j = 0; j < popSize; j++) {
                addedChance += inverseLengths[j];
                if (addedChance >= chance) {
                    reproductionChromosomes[i] = chromosomes[j];
                    break;
                }
            }
        }

        int[][] newPool = new int[popSize][chromSize];
        for (int i = 0; i < popSize; i++) {
            this.shuffle(reproductionChromosomes);
            int[] chrom1 = reproductionChromosomes[0];
            this.shuffle(reproductionChromosomes);
            int[] chrom2 = reproductionChromosomes[0];

            newPool[i] = reproduce(chrom1, chrom2);
        }*/


        int[][] newPool = new int[popSize][chromSize];
        for (int i = 0; i < popSize; i++) {
            int[] chrom1 = new int[chromSize];
            int[] chrom2 = new int[chromSize];
            double chance1 = Math.random()*sumOfInverseLengths;
            double chance2 = Math.random()*sumOfInverseLengths;
            double addedChance = 0;
            for (int j = 0; j < popSize; j++) {
                addedChance += inverseLengths[j];
                if (addedChance >= chance1) {
                    chrom1 = chromosomes[j];
                    break;
                }
            }
            addedChance = 0;
            for (int j = 0; j < popSize; j++) {
                addedChance += inverseLengths[j];
                if (addedChance >= chance2) {
                    chrom2 = chromosomes[j];
                    break;
                }
            }
            newPool[i] = reproduce(chrom1, chrom2);
        }

        return newPool;
    }

    /**
     * This method should solve the TSP. 
     * @param pd the TSP data.
     * @return the optimized product sequence.
     */
    public int[] solveTSP(TSPData pd) {
        int[][] chromosomes = new int[popSize][chromSize];
        for (int i = 0; i < popSize; i++) {
            chromosomes[i] = initializeChromosome(chromSize);
        }

        for (int i = 0; i < generations; i++) {
            chromosomes = reproduceList(chromosomes, pd);
        }

        int smallestIndex = 0;
        int sizeSmallestIndex = lengthOfChromosome(chromosomes[0], pd);
        for (int i = 0; i < popSize; i++) {
            int newLength = lengthOfChromosome(chromosomes[i], pd);
            if (newLength < sizeSmallestIndex) {
                smallestIndex = i;
                sizeSmallestIndex = newLength;
            }
        }

        return chromosomes[smallestIndex];
    }

    /**
     * Assignment 2.b
     */
    public static void main(String[] args) throws IOException, ClassNotFoundException {
    	//parameters
    	int populationSize = 20;
        int generations = 20;
        int chromSize = 4;

        int[] start = new int[]{1,2,3,4};
        int[] end = new int[]{4,2,3,1};
        int[][] distances = new int[][]{{1,1,3,4},{1,1,1,4},{3,1,1,1},{3,4,1,1}};

        String TSPpath = "./data/tsp products.txt";
        String coordinates = "./data/hard coordinates.txt";
        TSPData tspData = TSPData.readSpecification(coordinates, TSPpath);
        tspData.setDistances(distances);
        tspData.setEndDistances(end);
        tspData.setStartDistances(start);

        /*
        String persistFile = "./tmp/productMatrixDist";
        
        //setup optimization
        TSPData tspData = TSPData.readFromFile(persistFile);
        */
        GeneticAlgorithm ga = new GeneticAlgorithm(generations, populationSize, chromSize);

        //run optimzation and write to file
        int[] solution = ga.solveTSP(tspData);
        for (int i : solution) {
            System.out.print(i + ", ");
        }
        System.out.println("Length: " + ga.lengthOfChromosome(solution, tspData));
        //tspData.writeActionFile(solution, "./data/TSP solution.txt");
    }
}
