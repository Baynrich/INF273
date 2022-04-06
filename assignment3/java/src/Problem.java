import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.ArrayList;
import java.util.Scanner; // Import the Scanner class to read text files

public class Problem {

    public int n_nodes;
    public int n_vehicles;
    public int n_calls;

    public int[][] cargo;
    public int[][][] travelTime;
    public int[][] firstTravelTime;
    public int[] vesselCapacity;
    public int[][] loadingTime;
    public int[][] unloadingTime;
    public int[][] vesselCargo;
    public int[][][] travelCost;
    public int[][] firstTravelCost;
    public int[][] portCost;

    public Problem(String filename) {
        try {
            File probFile = new File(filename);
            Scanner ps = new Scanner(probFile);
            String n_nodes_str = ps.nextLine();
            n_nodes = Integer.parseInt(n_nodes_str.split(":")[1]);
            String n_vehicles_str = ps.nextLine();
            n_vehicles = Integer.parseInt(n_vehicles_str.split(":")[1]);
            String n_calls_str = ps.nextLine();
            n_calls = Integer.parseInt(n_calls_str.split(":")[1]);
            cargo = new int[n_calls][8];
            travelTime = new int[n_vehicles][n_nodes][n_nodes];
            firstTravelTime = new int[n_vehicles][n_nodes];
            vesselCapacity = new int[n_vehicles];
            loadingTime = new int[n_vehicles][n_calls];
            unloadingTime = new int[n_vehicles][n_calls];
            vesselCargo = new int[n_vehicles][n_calls];
            travelCost = new int[n_vehicles][n_nodes][n_nodes];
            firstTravelCost = new int[n_vehicles][n_nodes];
            portCost = new int[n_vehicles][n_calls];
            parse2d(ps.nextLine(), cargo);
            parse3d(ps.nextLine(), travelTime);
            parse2d(ps.nextLine(), firstTravelTime);
            parse1d(ps.nextLine(), vesselCapacity);
            parse2d(ps.nextLine(), loadingTime);
            parse2d(ps.nextLine(), unloadingTime);
            parse2d(ps.nextLine(), vesselCargo);
            parse3d(ps.nextLine(), travelCost);
            parse2d(ps.nextLine(), firstTravelCost);
            parse2d(ps.nextLine(), portCost);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public boolean checkFeasibility(int[] sol){
        int vehicleidx = 0;
        int vehicleTime = 0;
        int vehicleWeight = 0;
        int vehicle_pos = -1;
        ArrayList<Integer> currentlyCarrying = new ArrayList<>();

        for(int i = 0; i < sol.length; i++){
            if (sol[i] == 0){
                if (vehicleidx == n_vehicles - 1){
                    break;
                }
                vehicleidx += 1;
                vehicleTime = 0;
                vehicleWeight = 0;
                currentlyCarrying.clear();
                continue;
            }

            // Check for incompatible vessel and cargo
            if(vesselCargo[vehicleidx][sol[i] - 1] == 0){
                return false;
            }

            int node_from = cargo[sol[i] - 1][0];
            int node_to = cargo[sol[i] - 1][1];

            if(currentlyCarrying.contains(sol[i])){
                vehicleTime += travelTime[vehicleidx][node_from][node_to];

                // Add time to adjust for early delivery
                if (vehicleTime < cargo[sol[i] - 1][6]){
                    vehicleTime = cargo[sol[i]-1][6];
                }

                // Check if time limit has been exceeded
                if(vehicleTime > cargo[sol[i] - 1][7]){
                    // Time window for delivery exceeded
                    System.out.println("Time window for delivery exceeded");
                    return false;
                }

                // Increment capacity
                currentlyCarrying.remove(currentlyCarrying.indexOf(sol[i]));
                vehicleWeight -= cargo[sol[i]-1][2];
                vehicle_pos = node_to;
            } else {
                if(vehicleTime == 0){
                    vehicleTime += firstTravelTime[vehicleidx][node_from];
                } else {
                    vehicleTime += travelTime[vehicleidx][vehicle_pos][node_from];
                }

                // Add time to adjust for early pickup
                if (vehicleTime < cargo[sol[i]-1][4]){
                    vehicleTime = cargo[sol[i]-1][4];
                }

                // Check if time limit has been exceeded
                if(vehicleTime > cargo[sol[i]-1][5]){
                    // Time window for pickup exceeded
                    return false;
                }

                // Increment capacity
                currentlyCarrying.add(sol[i]);
                vehicleWeight += cargo[sol[i]-1][2];
                vehicle_pos = node_from;
            }
            if (vehicleWeight > vesselCapacity[vehicleidx]){
                return false;
            }
        }
        return true;
    }



    private void parse1d(String data_str, int[] target){
        data_str = data_str.split(":")[1];
        data_str = data_str.replaceAll("\\[", "").replaceAll("]", "").replaceAll(" ", "");
        String[] cargo_array = data_str.split(",");
        for(int i = 0; i < cargo_array.length; i++){
            String item = cargo_array[i];
            target[i] = Integer.parseInt(item.trim());
        }
    }
    private void parse2d(String data_str, int[][] target){
        data_str = data_str.split(":")[1];
        data_str = data_str.replaceAll("\\[", "").replaceAll("]", "").replaceAll("\\{", "").replaceAll(" ", "");
        String[] cargo_array = data_str.split("}");
        for(int i = 0; i < cargo_array.length; i++){
            String line =  cargo_array[i];
            String[] line_arr = line.split(",");
            for(int j = 0; j < line_arr.length; j++) {
                String item = line_arr[j].trim();
                target[i][j] = Integer.parseInt(item);
            }
        }
    }
    private void parse3d(String data_str, int[][][] target){
        data_str = data_str.split(":")[1];
        data_str = data_str.replaceAll("\\[", "").replaceAll("]", "").replaceAll("\\{", "").replaceAll("\\(", "");
        String[] traveltime_array = data_str.split("}");
        for(int i = 0; i < target.length; i++){
            String line =  traveltime_array[i];
            String[] line_arr = line.split("\\)");
            for(int j = 0; j < line_arr.length; j++){
                String[] elems = line_arr[j].split(",");
                for(int k = 0; k < elems.length; k++){
                    target[i][j][k] = Integer.parseInt(elems[k].trim());
                }
            }
        }

    }
}
