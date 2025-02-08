from utils.hypixel_code.constants.diana_constants import DIANA_MOBS, DIANA_TREASURES
from random import random
from numpy.random import choice


def simulateChain(**params) -> dict:
    """
    Simulate a chain of burrows for Diana's Burrows. The simulation will return a dictionary with the results for the
    single chain.

    example:
        - simulateChain(isEnderSlayerNine=True)

    :param params:
        - isEnderSlayerNine (bool): Whether the player has the Ender Slayer 9 perk
    :return: The results of the simulation
    """
    mobs: dict = DIANA_MOBS["Ender Slayer 9" if params["isEnderSlayerNine"] else "Non-Ender Slayer 9"]
    chainResults: dict = {
        "Mobs": {mob: 0 for mob in mobs.keys()},
        "Treasures": {treasure: 0 for treasure in DIANA_TREASURES.keys()}
    }
    for _ in range(2):
        if random() < 0.1:
            treasureDropped = choice(list(DIANA_TREASURES.keys()), p=list(DIANA_TREASURES.values()))
            chainResults["Treasures"][treasureDropped] += 1
        else:
            mobDropped = choice(list(mobs.keys()), p=list(mobs.values()))
            chainResults["Mobs"][mobDropped] += 1

    treasureDropped = choice(list(DIANA_TREASURES.keys()), p=list(DIANA_TREASURES.values()))
    chainResults["Treasures"][treasureDropped] += 1

    return chainResults
