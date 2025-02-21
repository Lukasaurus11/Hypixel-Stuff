from numpy import exp as numpy_exp
from numpy.random import choice, rand
from utils.hypixel_code.constants.dragon_constants import DRAGONS
from api import getBazaarInformation
from simulators.helper_functions import calculateMagicFindBoostedDropChance, calculateMagicFindBoostedDropChanceWithPetLuck


def calculateFightProfit(itemName: str, eyesPlaced: int) -> float:
    """
    Function to calculate the profit for a given item given a dragon fight.

    example:
        - calculateFightProfit('Superior Dragon Helmet', 4)

    :param itemName: The name of the item that was dropped
    :param eyesPlaced: How many eyes were place
    :return: The profit for the given item
    """

    armorMapping: dict = {
        'Chestplate': 80,
        'Leggings': 70,
        'Helmet': 50,
        'Boots': 40
    }
    bazaarInformation: dict = getBazaarInformation()

    for key in armorMapping.keys():
        if key in itemName:
            dragonType: str = itemName.split(' ')[0].upper() + "_FRAGMENT"

            return bazaarInformation[dragonType]['buyPrice'] * armorMapping[key] - \
                bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced

    else:
        if 'Ender' in itemName or 'Travel' in itemName or 'Aspect' in itemName:
            if 'Legendary' in itemName:
                return 790000000 - bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced

            elif 'Epic' in itemName:
                return 399000000 - bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced

            elif 'Aspect' in itemName:
                return 1500000 - bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced

            else:
                return 89900 - bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced

        else:
            return bazaarInformation[itemName.upper().replace(" ", "_")]['buyPrice'] - \
                bazaarInformation['SUMMONING_EYE']['buyPrice'] * eyesPlaced


def dragonScoringFunction(**params) -> float:
    """
    Function to score a given dragon fight based on the parameters given.

    Weights:
            500 - "Horn" weight (Making it more likely to drop a horn hurts us so we want to minimize the horns we might get)
            50 - "Claw" weight (Same as above)
            200 - "Dragon" weight (if we were to drop a pet, we want to favor that combination)
            20 - "Profit" weight (the more profit the better)
            5 - "Weight" weight (we want to maximize the remaining weight since it allows for more fragments to drop)

    example:
        - dragonScoringFunction(item_name='Superior Dragon Helmet', eyes_placed=4, legendary_chance=0.1, epic_chance=0.2,
         horn_chance=0.1, claw_chance=0.1, total_weight=100)

    :param params
        - item_name (str): The name of the item that was dropped
        - eyes_placed (int): How many eyes were placed
        - legendary_ender_dragon_chance (float): The chance of getting a legendary ender dragon
        - epic_ender_dragon_chance (float): The chance of getting an epic ender dragon
        - horn_chance (float): The chance of getting a horn
        - claw_chance (float): The chance of getting a claw
        - total_weight_left (int): The total weight left after the fight

    :return: The score for the given dragon fight
    """
    hornPenalty: float = 500 * numpy_exp(params['horn_chance'] * 5)
    clawPenalty: float = 50 * numpy_exp(params['claw_chance'] * 5)
    itemProfit: float = calculateFightProfit(params['item_name'], params['eyes_placed'])

    return (200 * (params['legendary_ender_dragon_chance'] + params['epic_ender_dragon_chance'])) + \
        (20 * itemProfit) - (hornPenalty + clawPenalty) + \
        (5 * params['total_weight_left'])


def simulateDragonFight(**params) -> dict:
    """
    Function to simulate a dragon fight given the magic find and pet luck.

    example:
        - simulateDragonFight(magic_find=100, pet_luck=100, eyes_placed=4)

    :param params
        - magic_find (float): The magic find of the player
        - pet_luck (float): The pet luck of the player
        - eyes_placed (int): The number of eyes placed

    :return: The result dictionary
    """
    magicFind: float = params['magic_find']
    petLuck: float = params['pet_luck']
    eyesPlaced: int = params['eyes_placed']

    def createResultDict() -> dict:
        """
        Function to create a result dictionary for a dragon fight.
        :return: The result dictionary
        """
        return {
            'eyes_placed': eyesPlaced,
            'dragon': dragon['name'],
            'item_name': item['name'],
            'legendary_ender_dragon_chance': calculateMagicFindBoostedDropChanceWithPetLuck(0.0001 * eyesPlaced,
                                                                                            magicFind, petLuck),
            'epic_ender_dragon_chance': calculateMagicFindBoostedDropChanceWithPetLuck(0.0005 * eyesPlaced,
                                                                                       magicFind, petLuck),
            'horn_chance': calculateMagicFindBoostedDropChance(0.3, magicFind) if 'Superior'
                                                                                  in dragon['name'] else 0,
            'claw_chance': calculateMagicFindBoostedDropChance(0.02 * eyesPlaced, magicFind),
            'total_weight_left': 480 - item['weight']
        }

    dragon: dict = choice(DRAGONS, p=[dragon['baseChance'] for dragon in DRAGONS])
    for item in dragon['lootTable']:
        itemChance: float = item['baseChance']
        if item['name'] in ['Dragon Claw', 'Epic Ender Dragon', 'Legendary Ender Dragon', 'Aspect of the Dragons']:
            itemChance *= eyesPlaced

        if 'Ender Dragon' in item['name']:
            boostedChance: float = calculateMagicFindBoostedDropChanceWithPetLuck(itemChance, magicFind, petLuck)
        else:
            boostedChance: float = calculateMagicFindBoostedDropChance(itemChance, magicFind)

        if item == dragon['lootTable'][-1]:
            return createResultDict()

        else:
            if rand() < boostedChance:
                return createResultDict()

    # Realistically, this should never happen
    return {}
