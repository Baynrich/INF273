import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {

    public static void main(String args[]) throws IOException {
        int[] initSol = new int[] {0, 2, 2, 0, 3, 3, 0, 6, 6, 1, 1, 4, 4, 5, 5, 7, 7};
        Solver solver = new Solver("./dataCall_7_Vehicle_3.txt");
        System.out.println(Arrays.toString(solver.reassignCall(initSol)));
        Problem problem = solver.getProblem();
        //System.out.println(problem.costFunction(initSol));
        if(false) {
            System.out.println(problem.costFunction(initSol));
            File outfile = new File("./c7v3out.txt");
            outfile.createNewFile();
            FileWriter myWriter = new FileWriter("./c7v3out.txt");
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "oneopt", "localsearch", initSol);
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "twoopt", "localsearch", initSol);
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "threeopt", "localsearch", initSol);
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "oneopt", "anneal", initSol);
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "twoopt", "anneal", initSol);
            doTheThing(myWriter, "./dataCall_7_Vehicle_3.txt", "threeopt", "anneal", initSol);
            myWriter.close();
        }
    }



    public static void doTheThing(FileWriter myWriter, String datafile, String nbormethod, String operator, int[] initSol){
        try{
            int num = 10;

            ArrayList<Thread> threads = new ArrayList<>();
            ArrayList<SolCost> sols = new ArrayList<>();


            long startTime = System.currentTimeMillis();
            for(int i = 0; i < num; i++){
                Solver solver = new Solver(datafile);
                threads.add(solver);
                solver.run(initSol, sols);
            }

            // Wait for threads to finish
            while(true){
                boolean stopRunning = true;
                for(Thread thread : threads){
                    if(thread.isAlive()){
                        stopRunning = false;
                    }
                }
                if(stopRunning){
                    break;
                }
            }
            long time = startTime - System.currentTimeMillis();
            float minCost = Float.POSITIVE_INFINITY;
            float totCost = 0;
            int[] bestSol = new int[0];
            for(int i = 0; i < sols.size(); i++){
                SolCost result = sols.get(i);
                if(result.cost < minCost){
                    minCost = result.cost;
                    bestSol = result.sol;
                }
                totCost += result.cost;
            }

            myWriter.write(operator + " " + nbormethod + String.format("%n"));
            myWriter.write("Top solution: " + Arrays.toString(bestSol) + String.format("%n"));
            myWriter.write("Top solution cost: " + minCost + String.format("%n"));
            myWriter.write("Average solution cost: " + (totCost / 10)+ String.format("%n") + String.format("%n"));
            myWriter.write("Time elapsed: " + (time / 1000) + " seconds"+ String.format("%n") + String.format("%n"));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}
