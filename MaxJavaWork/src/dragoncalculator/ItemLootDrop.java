package dragoncalculator;

public class ItemLootDrop extends WeightCalculator {

    //This constructor is currently not doing anything, but I need to rethink how the entire project is structured
    //once I know what wants to call what and pass what where.
    ItemLootDrop(ItemLootDrop itemWanted) {
        super();
        double inheritedWeight = getPlayersWeight();

        //TODO Need to map with key of the item and value with quality - however it also needs to be considered the drop chance
        //  of the item as this is at 30% or based on the summoning eyes placed.
    }

    private void lootDropEquation() {


    }

    private void dragonLootDrop() {

    }
}
