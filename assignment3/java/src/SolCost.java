import java.util.Arrays;

public class SolCost{
    public float cost;
    public int[] sol;
    public SolCost(float cost, int[] sol){
        this.cost = cost;
        this.sol = sol;
    }

    @Override
    public String toString() {
        return "SolCost{" +
                "cost=" + cost +
                ", sol=" + Arrays.toString(sol) +
                '}';
    }
}
