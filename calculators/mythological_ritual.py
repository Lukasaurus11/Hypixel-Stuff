from scipy.stats import binom
from calculator_helper_functions import *


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


def cumProbabilityGroupScenarioSameSpawnChance(spawnChance: float, probSinglePlayer: float, lootshareProb: float,
                                               trials: int, totalTrials: int) -> float:
    """
    Calculate the cumulative probability of getting at least one success in k trials, accounting for both
    Player 1's own spawns and lootshare opportunities from other players.

    :param spawnChance: Probability of Player 1 spawning the item.
    :param probSinglePlayer: Probability of success for Player 1 on their own spawn.
    :param lootshareProb: Probability of Player 1 looting the item when another player spawns it (without looting).
    :param trials: The number of trials performed by Player 1.
    :param totalTrials: The total amount of trials to consider (including trials by other players).
    :return: The cumulative probability of getting at least one success in k trials.
    """
    ownProbability: float = 1 - (1 - spawnChance * probSinglePlayer) ** trials

    remainingTrials: int = totalTrials - trials
    lootshareProbability: float = 1 - (1 - lootshareProb * spawnChance) ** remainingTrials

    totalProbability: float = 1 - ((1 - ownProbability) * (1 - lootshareProbability))
    return totalProbability


def cumProbabilityGroupScenarioDifferentSpawnChance(spawnChance: float, probSinglePlayer: float, lootshareProb: float,
                                                    otherPlayersSpawnChances: list, trials: int, totalTrials: int) \
        -> float:
    """
    This needs to be redone as its not the latest version (tf happened to it)
    Calculate the cumulative probability of getting at least one success in a group scenario,
    considering different spawn rates for other players and a separate lootshare probability.

    :param spawnChance: Probability of Player 1 spawning the item.
    :param probSinglePlayer: Probability of Player 1 getting the item if it spawns (Player 1's own success rate).
    :param lootshareProb: Probability of Player 1 lootsharing an item when another player spawns it.
    :param otherPlayersSpawnChances: A list of spawn chances for other players.
    :param trials: The number of trials performed by Player 1.
    :param totalTrials: The total number of trials (including Player 1 and others).
    :return: The cumulative probability of getting at least one success.
    """

    ownProbability: float = 1 - (1 - spawnChance * probSinglePlayer) ** trials

    lootshareProbability: float = 1

    remainingTrials: int = totalTrials - trials
    for i, spawnChanceOther in enumerate(otherPlayersSpawnChances):
        if i < remainingTrials % len(otherPlayersSpawnChances):
            trialsOtherPlayer: int = remainingTrials // len(otherPlayersSpawnChances) + 1
        else:
            trialsOtherPlayer = remainingTrials // len(otherPlayersSpawnChances)

        lootshareProbability *= (1 - lootshareProb * spawnChanceOther) ** trialsOtherPlayer

    lootshareProbability = 1 - lootshareProbability

    totalProbability: float = 1 - ((1 - ownProbability) * (1 - lootshareProbability))
    return totalProbability
