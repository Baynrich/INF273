import java.util.Arrays;

public class Main {

    public static void main(String args[]){
        try{
            Problem problem = new Problem("./dataCall_7_Vehicle_3.txt");
            int[] sol = new int[] {0, 3, 3, 0, 5, 5, 7, 7, 0, 6, 6, 1, 1, 4, 4, 2, 2};
            System.out.println(problem.checkFeasibility(sol));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}
