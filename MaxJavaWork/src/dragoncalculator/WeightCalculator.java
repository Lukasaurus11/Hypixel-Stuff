package dragoncalculator;

//Temp unused imports

import dragoncalculator.enums.DragonPlacements;

/**
 * A class to handle the calculations of weighting for the likelihood of getting a dragon pet or certain drop.
 * Author @Max
 * */
public class WeightCalculator {

    //Variables used to store data that is referenced in different contexts
    private double playersWeight;
    private double playersDamage;

    /**
     * Method that sets the players weight after the calculations with the vales inputted.
     */
    public double getPlayersWeight(){
       return playersWeight;
    }

    /**
     * A method that returns the value of the players quality which determines what can be dropped.
     *
     * @param inEyesPlaced - A value which is passed in for the users eyes placed.
     * @param inFirstsDamage - A value of the first placed damage dealt.
     * @param inYourDamage - A value of your damage dealt to the dragon.
     * @param inPlacement - A value which defines what placement you got for the dragon.
     * */
    public void setWeight(DragonPlacements inPlacement, int inEyesPlaced, double inYourDamage, double inFirstsDamage){
        this.playersDamage = inYourDamage;
        this.playersWeight = placementQuality(inPlacement) + eyesPlaced(inEyesPlaced) + placementDamage(inFirstsDamage, inYourDamage);
    }

    /**
     * A method that returns the placement quality of the player which is calculated by the placement that the player
     * on the dragon
     *
     * @param inPlacement - Value passed in of the players placement for the dragon.
     * */
    private int placementQuality(DragonPlacements inPlacement) {

        //I'm aware that this is dogshit and awful but it works so shutup.
        if (playersDamage < 1) {
            return switch (inPlacement) {
                case FIRST -> 200;
                case SECOND -> 176;
                case THIRD -> 150;
                case FOURTH -> 125;
                case FIFTH -> 110;
                case SIXTH, SEVENTH, EIGTH -> 100;
                case NINTH, TENTH -> 90;
                case ELEVENTH, TWELTH -> 80;
                case THIRTEENTH, FOURTEENTH, FIFTHTEENTH, SIXTEENTH, SEVENTEETH, EIGHTEENTH, NINETEENTH, TWENTYETH, TWENTYFIRST, TWENTYSECOND, TWENTYTHIRD, TWENTYFOURTH, TWENTYFIFTH ->
                        70;
            };
        }
        return 10;
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
     * @param yourDamage - A double value of your damage on the leaderboard.
     * */
    private double placementDamage(double firstPlace, double yourDamage){
        return (100 * (firstPlace / yourDamage));
    }

}
