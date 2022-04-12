import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.lang.Math;


public class Solver extends Thread {
    private Problem problem;
    private int n = 10000;
    private Random r = new Random();

    public Problem getProblem(){
        return problem;
    }

    public Solver(String file){
        problem = new Problem(file);
        r.setSeed(27);
    }

    public void run(int[] initSol, ArrayList<SolCost> sols){
        int[] sol = anneal(initSol);
        int cost = problem.costFunction(sol);
        sols.add(new SolCost(cost, sol));
    }

    public int[] anneal(int[] bestSol){
        float bestCost = problem.costFunction(bestSol);
        ArrayList<Float> deltaEs = new ArrayList<>();
        for(int i = 0; i < 100; i++){
            int[] bestNbor = new int[]{};
            float bestNborCost = Float.POSITIVE_INFINITY;

            //TODO - Logic for selecting operator
            int[] nbor = reassignCall(bestSol);


            if(problem.checkFeasibility(nbor)){
                int nborCost = problem.costFunction(nbor);
                if(nborCost < bestNborCost){
                    bestNborCost = nborCost;
                    bestNbor = nbor;
                }
                else{
                    if(r.nextFloat() < 0.8){
                        bestNborCost = nborCost;
                        bestNbor = nbor;
                    }

                }
            }
            if(!Arrays.equals(bestNbor, new int[]{})){
                deltaEs.add(bestCost - bestNborCost);
                if(bestNborCost < bestCost){
                    bestSol = bestNbor;
                    bestCost = bestNborCost;
                }
            }
        }

        float sum = 0;
        for(float e :deltaEs){
            sum += e;
        }

        double T = (sum / deltaEs.size()) / Math.log(0.8);
        double alpha = Math.pow(0.1 / T, 1/n);

        for(int i = 0; i < n-100; i++){

            int[] bestNbor = new int[]{};
            float bestNborCost = Float.POSITIVE_INFINITY;
            //TODO - Logic for selecting operator
            int[] nbor = reassignCall(bestSol);

            if(problem.checkFeasibility(nbor)){
                int nborCost = problem.costFunction(nbor);
                if(nborCost < bestNborCost){
                    bestNborCost = nborCost;
                    bestNbor = nbor;
                }
                else{
                    float delta_e = nborCost - bestNborCost;
                    if(r.nextFloat() < Math.exp(-delta_e / T)){
                        bestNborCost = nborCost;
                        bestNbor = nbor;
                    }

                }
            }
            if(!Arrays.equals(bestNbor, new int[]{})){
                if(bestNborCost < bestCost){
                    bestSol = bestNbor;
                    bestCost = bestNborCost;
                }
            }
            T = T * alpha;

        }
        return bestSol;
    }

    /*
     * Moves a random call between vehicles, or retires call.
     */
    public int[] reassignCall(int[] sol){
        ArrayList<int[]> vehicles = new ArrayList<>();
        int v_idx = 0;
        for(int i = 0; i < sol.length; i++){

        }

        int callToReassign = r.nextInt(problem.n_vehicles) + 1;
        System.out.println(callToReassign);
        Tuple callPositions = new Tuple(-1, -1);
        int[] zeroIndexes = new int[problem.n_vehicles + 1];
        int curVehicle = 0;
        int illegal = -1;
        // Find current indexes of call, zeros
        for(int i = 0; i < sol.length; i++){
            if(sol[i] == callToReassign){
                callPositions.assignPosition(i);
                illegal = curVehicle;
            }
            if(sol[i] == 0){
                zeroIndexes[curVehicle] = i;
                curVehicle += 1;
            }
        }
        zeroIndexes[zeroIndexes.length - 1] = sol.length - 1;

        int newVehicle = illegal;
        while(newVehicle == illegal){
            // Select random vehicle, or retire call.
            newVehicle = r.nextInt(curVehicle+1);
        }
        System.out.println(newVehicle);

        if(newVehicle == zeroIndexes.length-1){
            // Retire vehicle
        }
        else{

        }


        /*if(newVehicle == zeroIndexes.length){
            // Retire vehicle
            newSol.add(newSol.size() - 1, callToReassign);
            newSol.add(newSol.size() - 1, callToReassign);
        }
        else{
            int minVal = zeroIndexes[newVehicle];
            int idx = 0;
            while(newSol.get(minVal + idx + 1) != 0){
                System.out.println(newSol.get(minVal+idx+1));
                idx += 1;
            }
            newSol.add(minVal, callToReassign);
            newSol.add(r.nextInt(idx) + minVal, callToReassign);
        }
        return newSol.stream().mapToInt(i -> i).toArray();*/
    }


}

class Tuple{
    public int one;
    public int two;
    public Tuple(int one, int two){
        this.one = one;
        this.two = two;
    }


    public void assignPosition(int i){
        if(one == -1){
            one = i;
        }
        else{
            two = i;
        }
    }
}