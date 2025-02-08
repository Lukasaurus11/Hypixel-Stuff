from random import random
from utils.hypixel_code.constants.minion_constants import INFERNO_MINION_SPEED, INFERNO_MINION_TABLE


def calculateInfernoMinionSpeed(level: int, nMinion: int, minionExpanders: int, flycatchers: int, beaconBuff: float,
                                fuelType: int, mithrilInfused: bool, postCard: bool, freewill: bool) -> float:
    """
    Calculate the speed of an inferno minion with the given parameters

    :param level: The level of the minion
    :param nMinion: How many minions are placed
    :param minionExpanders: How many minion expanders are placed
    :param flycatchers: How many flycatchers are placed
    :param beaconBuff: The buff given by the beacon
    :param fuelType: The buff to account given the fuel type
    :param mithrilInfused: Is the minion has been mithril infused
    :param postCard: If the minion has the postcard buff
    :param freewill: If the minion has the freewill buff
    :return: The speed of the minion
    """
    fuelSpeedMultiplier: dict = {
        0: 10,
        1: 15,
        2: 20
    }

    # fetch the speed of the minion
    speed: float = INFERNO_MINION_SPEED[level]

    # Buff x minion (18% per minion, capped at 180%)
    speedBuff: float = 0.18 * nMinion if nMinion <= 10 else 1.8

    # Buff x minion expander (5% per expander)
    speedBuff += 0.05 * minionExpanders

    # Buff x flycatcher (20% per flycatcher)
    speedBuff += 0.2 * flycatchers

    # Buff x specified beacon parameter
    speedBuff += beaconBuff

    # Buff x mithril infused
    speedBuff += 0.1 if mithrilInfused else 0

    # Buff x postcard
    speedBuff += 0.05 if postCard else 0

    # Buff x freewill
    speedBuff += 0.1 if freewill else 0

    fuelMultiplier: int = fuelSpeedMultiplier[fuelType]

    totalSpeedMultiplier: float = (1 + speedBuff) * (1 + fuelMultiplier)

    newSpeed: float = speed / totalSpeedMultiplier

    return round(newSpeed, 1)


def simulateInfernoMinion(**params) -> dict:
    """
    Simulate an inferno_minion minion with the given parameters

    example:
        - simulateInfernoMinion(level=10, nMinion=10, minionExpanders=0, flycatchers=11, beaconBuff=0.11, fuelType=2,
                                mithrilInfused=True, eyesDrop=True, postCard=True, freewill=True)

    :param params:
        - level (int): The level of the minion
        - nMinion (int): How many minions are placed (caps at 10)
        - minionExpanders (int): How many minion expanders are placed
        - flycatchers (int): How many flycatchers are placed
        - beaconBuff (float): The buff given by the beacon
        - fuelType (int): The buff to account given the fuel type
        - mithrilInfused (bool): Is the minion has been mithril infused
        - eyesDrop (bool): If the minion has the eyesdrop buff
        - postCard (bool): If the minion has the postcard buff
        - freewill (bool): If the minion has the freewill buff

    :return: The average drops per 24h of having a single minion down
    """
    level: int = params['level']
    nMinion: int = params['nMinion']
    minionExpanders: int = params['minionExpanders']
    flycatchers: int = params['flycatchers']

    if minionExpanders + flycatchers > 2:
        print('Too many minion expanders or flycatchers')
        return {}

    beaconBuff: float = params['beaconBuff']
    fuelType: int = params['fuelType']
    mithrilInfused: bool = params['mithrilInfused']
    postCard: bool = params['postCard']
    freewill: bool = params['freewill']

    minionSpeed: float = calculateInfernoMinionSpeed(level, nMinion, minionExpanders, flycatchers, beaconBuff,
                                                     fuelType, mithrilInfused, postCard, freewill)

    actionsPerDay = ((60 * 60 * 24) / minionSpeed) // 2

    dropTable = INFERNO_MINION_TABLE['Eyesdrops'] if params['eyesDrop'] else INFERNO_MINION_TABLE['Base']
    drops: dict = {key: 0 for key in dropTable.keys()}
    for _ in range(int(actionsPerDay)):

        for drop, dropChance in dropTable.items():
            if random() < dropChance and fuelType == 2:
                if drop == 'Inferno Apex' and level >= 10:
                    drops[drop] += 2

                else:
                    drops[drop] += 1

    drops['Crude Gabagool'] = actionsPerDay
    return drops