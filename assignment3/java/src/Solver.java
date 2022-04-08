import java.util.ArrayList;
import java.util.Arrays;
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
    }

    public void run(int[] initSol, ArrayList<SolCost> sols, String operator, String nbormethod){
        int[] sol = new int[]{};
        if( operator == "localsearch" ){
            sol = localsearch(initSol, nbormethod);
        }
        else {
            sol = anneal(initSol, nbormethod);
        }
        int cost = problem.costFunction(sol);
        sols.add(new SolCost(cost, sol));
    }



    public int[] localsearch(int[] bestSol, String nbormethod){
        float bestCost = problem.costFunction(bestSol);
        ArrayList<int[]> neighborhood;

        for(int i = 0; i < n; i++){
            int[] bestNbor = new int[]{};
            float bestNborCost = Float.POSITIVE_INFINITY;
            if (nbormethod == "oneopt") {
                neighborhood = oneopt_nbors(bestSol);
            }
            else if (nbormethod == "twoopt") {
                neighborhood = twoopt_nbors(bestSol);
            }
            else{
                neighborhood = threeopt_nbors(bestSol);
            }

            for (int[] nbor : neighborhood){
                if(problem.checkFeasibility(nbor)){
                    int nborCost = problem.costFunction(nbor);
                    if(nborCost < bestNborCost){
                        bestNborCost = nborCost;
                        bestNbor = nbor;
                    }
                }
            }
            boolean alternativeFound = !Arrays.equals(bestNbor, new int[]{});
            if(alternativeFound && bestNborCost < bestCost){
                bestCost = bestNborCost;
                bestSol = bestNbor;
            }
            // We've found local optima. Will not get better.
            if(!alternativeFound || bestCost < bestNborCost){
                System.out.println("Exiting early");
                break;
            }
        }
        return bestSol;
    }

    public int[] anneal(int[] bestSol, String nbormethod){
        float bestCost = problem.costFunction(bestSol);
        ArrayList<int[]> neighborhood;
        ArrayList<Float> deltaEs = new ArrayList<>();
        for(int i = 0; i < 100; i++){
            int[] bestNbor = new int[]{};
            float bestNborCost = Float.POSITIVE_INFINITY;
            if (nbormethod == "oneopt") {
                neighborhood = oneopt_nbors(bestSol);
            }
            else if (nbormethod == "twoopt") {
                neighborhood = twoopt_nbors(bestSol);
            }
            else{
                neighborhood = threeopt_nbors(bestSol);
            }

            for (int[] nbor : neighborhood){
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
            }

            if(!Arrays.equals(bestNbor, new int[]{})){
                deltaEs.add(bestCost - bestNborCost);
                if(bestNborCost < bestCost){
                    bestSol = bestNbor;
                    bestCost = bestNborCost;
                }
            }
        }
        System.out.println("exiting initial 100");

        float sum = 0;
        for(float e :deltaEs){
            sum += e;
        }
        double T = (sum / deltaEs.size()) / Math.log(0.8);
        double alpha = Math.pow(0.1 / T, 1/n);
        for(int i = 0; i < n-100; i++){
            if(i % 100 == 0){
                System.out.println("Iteration " + i);
            }
            int[] bestNbor = new int[]{};
            float bestNborCost = Float.POSITIVE_INFINITY;
            if (nbormethod == "oneopt") {
                neighborhood = oneopt_nbors(bestSol);
            }
            else if (nbormethod == "twoopt") {
                neighborhood = twoopt_nbors(bestSol);
            }
            else{
                neighborhood = threeopt_nbors(bestSol);
            }

            for (int[] nbor : neighborhood){
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

    public ArrayList<int[]> oneopt_nbors(int[] initSol){
        ArrayList<int[]> nbors = new ArrayList<>();
        for(int i = 0; i < initSol.length; i++){
            int[] workable = Arrays.copyOf(initSol, initSol.length);
            int item_to_insert = workable[i];
            for(int j = i; j < workable.length - 1; j++){
                workable[j] = workable[j+1];
            }
            for(int j = 0; j < workable.length; j++){
                if(i == j || initSol[i] == initSol[j]){
                    continue;
                }
                int[] insertable = Arrays.copyOf(workable, workable.length);
                int currentVal = insertable[j];
                insertable[j] = item_to_insert;
                for( int k = j+1; k < insertable.length; k++){
                    int to_insert = currentVal;
                    currentVal = insertable[k];
                    insertable[k] = to_insert;
                }

                if(Arrays.equals(insertable, initSol) || !solutionSanity(insertable)){
                    continue;
                }
                for(int[] nbor : nbors){
                    if(Arrays.equals(nbor, insertable)){
                        continue;
                    }
                }
                nbors.add(insertable);
            }
        }
        return nbors;
    }

    public ArrayList<int[]> twoopt_nbors(int[] initSol){
        ArrayList<int[]> nbors = new ArrayList<>();
        for(int i = 0; i < initSol.length; i++){
            for(int j = 0; j < initSol.length; j++){
                if(i == j|| initSol[i] == initSol[j]){
                    continue;
                }
                int[] insertable = Arrays.copyOf(initSol, initSol.length);
                int i_val = insertable[i];
                insertable[i] = insertable[j];
                insertable[j] = i_val;
                if(Arrays.equals(insertable, initSol) || !solutionSanity(insertable)){
                    continue;
                }
                for(int[] nbor : nbors){
                    if(Arrays.equals(nbor, insertable)){
                        continue;
                    }
                }
                nbors.add(insertable);
            }
        }
        return nbors;
    }




    public ArrayList<int[]> threeopt_nbors(int[] initSol){
        ArrayList<int[]> nbors = new ArrayList<>();
        for(int i = 0; i < initSol.length; i++){
            for(int j = 0; j < initSol.length; j++){
                for(int k = 0; k < initSol.length; k++){
                    if(i == j || i == k || j == k || (initSol[i] == initSol[j] && initSol[i] == initSol[j] && initSol[j] == initSol[k])){
                        continue;
                    }
                    int[] insertable = Arrays.copyOf(initSol, initSol.length);
                    int i_val = insertable[i];
                    int j_val = insertable[j];
                    insertable[i] = insertable[k];
                    insertable[j] = i_val;
                    insertable[k] = j_val;
                    if(Arrays.equals(insertable, initSol) || !solutionSanity(insertable)){
                        continue;
                    }
                    for(int[] nbor : nbors){
                        if(Arrays.equals(nbor, insertable)){
                            continue;
                        }
                    }
                    nbors.add(insertable);
                }
            }
        }
        return nbors;
    }


    public boolean solutionSanity(int[] sol){
        ArrayList<Integer> currentCalls = new ArrayList<>();
        for(int call : sol){
            if(call == 0){
                if(currentCalls.size() > 0){
                    return false;
                }
                continue;
            }
            else{
                if(currentCalls.contains(call)){
                    currentCalls.remove(currentCalls.indexOf(call));
                }
                else{
                    currentCalls.add(call);
                }
            }
        }
        return true;
    }
}