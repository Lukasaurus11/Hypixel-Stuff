package dragoncalculator;

import static dragoncalculator.enums.DragonPlacements.*;

public class DragonLootCalc {
    public static void main(String[] args) {

    }

    //TODO This needs to be remodelled as more of a controller that feeds into a main opposed to a main that adds into other classes
    //  Need to work out where I want to send data in to.
    private void dragonWeighting(){
        WeightCalculator weightCalculator = new WeightCalculator();
        weightCalculator.setWeight(FIRST, 4, 360000, 400000);
    }

}
