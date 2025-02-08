def calculateMagicFindBoostedDropChance(baseDropChance: float, magicFind: float) -> float:
    """
    Calculate the boosted drop chance of an item with a base drop chance
    when the player has a certain magic find percentage.

    :param baseDropChance: Base drop chance of the item
    :param magicFind: Magic find percentage of the player
    :return: Boosted drop chance of the item
    """
    if baseDropChance <= 0 or baseDropChance > 1:
        raise ValueError("Base drop chance must be in the range (0, 1].")
    if magicFind < 0:
        raise ValueError("Magic find percentage must be at least 0.")

    magicFindBoost: float = 1 + (magicFind / 100)
    boostedDropChance: float = baseDropChance * magicFindBoost
    return min(boostedDropChance, 1)


def calculateMagicFindBoostedDropChanceWithPetLuck(baseDropChance: float, magicFind: float, petLuck: float) -> float:
    """
    Calculate the boosted drop chance of an item with a base drop chance
    when the player has a certain magic find percentage and pet luck percentage.

    :param baseDropChance: Base drop chance of the item
    :param magicFind: Magic find percentage of the player
    :param petLuck: Pet luck percentage of the player
    :return: Boosted drop chance of the item
    """
    if baseDropChance <= 0 or baseDropChance > 1:
        raise ValueError("Base drop chance must be in the range (0, 1].")
    if magicFind < 0:
        raise ValueError("Magic find percentage must be at least 0.")
    if petLuck < 0:
        raise ValueError("Pet luck percentage must be at least 0.")

    itemBoost: float = 1 + ((magicFind + petLuck) / 100)
    boostedDropChance: float = baseDropChance * itemBoost
    return min(boostedDropChance, 1)
