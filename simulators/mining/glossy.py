from utils.hypixel_code.constants.gemstone_constants import THRESHOLDS
from random import random

"""
Changelog:
    - 20-02-2025 - Added a function to plot the results of the simulation
"""

def fetchTickRate(gemstone: str, miningSpeed: int) -> int:
    """
    Fetch the tick rate for a specific gemstone type and mining speed.

    :param gemstone: The breaking power of the gemstone being broken
    :param miningSpeed: The mining speed of the player
    :return: The tick rate for that specific gemstone type and mining speed
    """
    if gemstone not in THRESHOLDS.keys():
        raise ValueError("Gemstone type must be in the range [6, 10].")

    for tickRate, threshold in sorted(THRESHOLDS[gemstone]['thresholds'].items()):
        if miningSpeed >= threshold:
            return tickRate

    return 22


def calculateGlossyChance(gemstoneType: str, refinedMind: int) -> float:
    """
    Calculate the chance of getting a glossy gemstone from mining a gemstone block.

    :param gemstoneType: The breaking power of the gemstone being broken
    :param refinedMind: The level of refined mind
    :return: The chance of getting a glossy gemstone for that specific gemstone type
    """
    if gemstoneType not in THRESHOLDS.keys():
        raise ValueError("Invalid gemstone type.")
    if refinedMind < 0 or refinedMind > 5:
        raise ValueError("Refined mind level must be in the range [1, 5].")

    return (THRESHOLDS[gemstoneType]['breakingPower'] / 2000) * (1 + ((refinedMind * 2) / 100))


def simulateMining(**params) -> dict:
    """
    Simulates mining for 1 hour and tracks glossy gemstone acquisition over time.

    :param params: The parameters for the simulation
        - gemstone: The type of gemstone being mined (e.g. RUBY)
        - refinedMind: The level of refined mind (1-5)
        - miningSpeed: The mining speed of the player

    :return: Dictionary with second-by-second cumulative glossy gemstones obtained
    """
    timeToSimulate: int = 3600
    tickRate: int = fetchTickRate(params['gemstone'], params['miningSpeed'])
    glossyChance: float = calculateGlossyChance(params['gemstone'], params['refinedMind'])

    secondsPerAction: float = (tickRate / 20)
    nextMiningTime: float = 0
    glossyCount: int = 0
    glossyTimeline: dict = {}

    for second in range(timeToSimulate + 1):
        if second >= nextMiningTime:
            nextMiningTime += secondsPerAction

            if random() < glossyChance:
                glossyCount += 1

        glossyTimeline[second] = glossyCount

    return glossyTimeline


def plotSimulationResults(results: dict, colors: list) -> None:
    """
    Plots the results of a simulation

    :param results: The results of the simulation
    :param colors: The colors to use for the plot
    """
    # Import from within the function as this function is not meant to always be called
    from matplotlib.pyplot import plot, xlabel, ylabel, legend, show


    for i, (key, value) in enumerate(results.items()):
        finalCount: int = list(value.values())[-1]
        plot(list(value.keys()), list(value.values()), color=colors[i], label=f"{key} ({finalCount})")

    xlabel('Time (s)')
    ylabel('Glossy Gemstones')
    legend(fontsize='small')
    show()
