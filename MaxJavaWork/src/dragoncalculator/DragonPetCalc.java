package dragoncalculator;

//Temp unused imports

/**
 * A class to handle the calculations of weighting for the likelihood of getting a dragon pet or certain drop.
 * Author @Max
 * */
public class DragonPetCalc {

    /**
     * A method that returns the value of the players quality which determines what can be dropped.
     * */
    public double playerQuality(DragonPlacements inPlacement, int inEyesPlaced, double inYourDamage, double inFirstsDamage){

        return placementQuality(inPlacement) + eyesPlaced(inEyesPlaced) + placementDamage(inFirstsDamage, inYourDamage);
    }

    /**
     * A method that returns the placement quality of the player which is calculated by the placement that the player
     * on the dragon
     *
     * @param inPlacement - Value passed in of the players placement for the dragon.
     * */
    //TODO Currently there's nothing that catches if there is 0 damage or below the 25th placement
    private int placementQuality(DragonPlacements inPlacement) {


        //TODO Return to maybe
        /*Map<Enum, Double> placement = new HashMap<>();

        placement.put(FIRST, 200.0);
        placement.put(SECOND, 175.0);
        placement.put(THIRD, 150.0);
        placement.put(FOURTH, 125.0);
        placement.put(FIFTH, 110.0);*/

        //Switch statement which returns the placement weighting.
        return switch (inPlacement) {
            case FIRST -> 200;
            case SECOND -> 176;
            case THIRD -> 150;
            case FOURTH -> 125;
            case FIFTH -> 110;
            case SIXTH, SEVENTEETH, EIGTH -> 100;
            case NINTH, TENTH -> 90;
            case THIRTEENTH, FOURTEENTH, FIFTHTEENTH, SIXTEENTH, SEVENTH, EIGHTEENTH, NINETEENTH, TWENTYETH, TWENTYFIRST, TWENTYSECOND, TWENTYTHIRD, TWENTYFOURTH, TWENTYFIFTH ->
                    70;
            default -> 0;
        };

    }

    /**
     * A method that returns an int value weighting based on the players eyes placed.
     *
     * @param inPlaced - A value that is passed in of the players eyes placed.
     * */
    private int eyesPlaced(int inPlaced){
        return inPlaced * 100;
    }

    /**
     * A method that returns an int vlaue weighting basd on the players damage dealt.
     *
     * @param firstPlace - A double value of first place's damage on the leaderboard.
     * @param yourPlacement - A double value of your damage on the leaderboard.
     * */
    private double placementDamage(double firstPlace, double yourPlacement){

        return (100 * (firstPlace / yourPlacement));
    }

}
