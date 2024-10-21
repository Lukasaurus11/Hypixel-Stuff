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

    magicFindBoost = 1 + (magicFind / 100)
    boostedDropChance = baseDropChance * magicFindBoost
    return boostedDropChance


def cumGeoDistribution(prob, trials):
    """
    Calculate the cumulative probability of getting at least one success in k trials
    for a geometric distribution with success probability p.

    :param prob: Probability of success on a single trial
    :param trials: Number of trials
    :return: Cumulative probability of getting at least one success in k trials
    """
    if prob <= 0 or prob > 1:
        raise ValueError("Probability p must be in the range (0, 1].")
    if trials < 1:
        raise ValueError("Number of trials k must be at least 1.")

    # CDF of geometric distribution: 1 - (1 - prob)^trials
    cumProbability = 1 - (1 - prob) ** trials
    return cumProbability