package dragoncalculator;

import java.util.Random;

public class MonteCarlo {

    //Hidden constructor
    MonteCarlo(){

    }

    private double getRandom(){
        Random r = new Random();
        return r.nextDouble(100) + 1;
    }
}
