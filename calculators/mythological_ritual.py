def noSuccessProbability(prob: float, trials: int) -> float:
    """
    Calculate the probability of having no success in k trials
    for a geometric distribution with success probability p.

    :param prob: Probability of success on a single trial
    :param trials: Number of trials
    :return: Probability of having no success in k trials
    """
    if prob <= 0 or prob > 1:
        raise ValueError("Probability p must be in the range (0, 1].")
    if trials < 1:
        raise ValueError("Number of trials k must be at least 1.")

    # Probability of no success in k trials: (1 - prob)^trials
    noSuccessProb: float = (1 - prob) ** trials
    return noSuccessProb


def cumProbabilityGroupScenario(spawnChance: list, probSinglePlayer: float, lootshareProb: float, trials: list) \
        -> float:
    """
    Calculate the cumulative probability of getting at least one success in a group scenario,
    :param spawnChance: A list of spawn chances for each player  (the first element corresponds to single player).
    :param probSinglePlayer: The probability of success for a single player on their own spawn.
    :param lootshareProb: The probability of a player looting the item when another player spawns it.
    :param trials: The number of trials performed by each player (the first element corresponds to single player).
    :return: The cumulative probability of getting at least one success.
    """
    ownProbability: float = 1 - (1 - spawnChance[0] * probSinglePlayer) ** trials[0]

    lootshareProbability: float = 1
    for i in range(1, len(spawnChance)):
        lootshareProbability *= (1 - lootshareProb * spawnChance[i]) ** trials[i]
    lootshareProbability = 1 - lootshareProbability

    totalProbability: float = 1 - ((1 - ownProbability) * (1 - lootshareProbability))
    return totalProbability
