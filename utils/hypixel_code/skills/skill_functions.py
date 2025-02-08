from math import floor
from utils.hypixel_code.constants.skills_constants import HEART_OF_THE_MOUNTAIN, CATACOMBS_LEVELS


def calculatePowderSpent(currentLevel: int, levelCost: int) -> int:
    """
    Function to calculate the amount of powder spent on a HOTM perk based on the current level and the exponential
    upgrade cost.
    :param currentLevel: The current level of the user on that specific perk
    :param levelCost: The exponential cost of that perk, gathered from the HEART_OF_THE_MOUNTAIN dictionary
    :return: The amount of powder the user has spent on the current perk
    """
    total: int = 0
    while currentLevel > 1:
        total += floor((currentLevel + 1) ** levelCost)
        currentLevel -= 1
    return total


def buildHOTMTree() -> list:
    """
    Function to build a tree of the HEART_OF_THE_MOUNTAIN dictionary (9 x 11) to make it easier to visualize. The tree
    will be built by level, where each level 1 starts at the 10th row and its centered in the middle of the tree
    :return: A list to be printed as a tree
    """
    treeDimension: int = 11
    tree: list = ['*' * treeDimension]
    icon: dict = {
        'core of the mountain': '?',
        'ability': 'A',
        'un-upgradable perk': 'U',
        'glacite': 'C',
        'gemstone': 'G',
        'mithril': 'M'
    }
    for key in HEART_OF_THE_MOUNTAIN.keys():
        tempStr: str = ''
        for value in HEART_OF_THE_MOUNTAIN[key].values():
            if ['ability', 'un-upgradable perk', 'core of the mountain'].__contains__(value['type']):
                char: str = icon[value['type']]
            else:
                char: str = icon[value['powder type']]
            tempStr += char

        if len(tempStr) == 3:
            tempStr = tempStr[0] + '*' + tempStr[1] + '*' + tempStr[2]

        tree.append(tempStr.center(treeDimension, '*'))
    tree.append('*' * treeDimension)

    return tree[::-1]


def printHOTMTree(tree: list) -> str:
    """
    Function to print the tree of the HEART_OF_THE_MOUNTAIN dictionary
    :param tree: The tree to be printed
    :return: A string representation of the tree
    """
    return '\n'.join([''.join([str(cell) for cell in row]) for row in tree])


def calculateDungeonLevel(dungeonXp: float) -> float:
    """
    Function to calculate the catacombs level based on the amount of experience the player has
    :param dungeonXp: The amount of experience the player has
    :return: The catacombs level
    """
    # Fetch the catacombs level from the dictionary
    currentLevel: float = 0
    for key, value in CATACOMBS_LEVELS.items():
        if dungeonXp >= value:
            currentLevel = key

    # Having the current level, we'll calculate the percentage to the next level (xp for next level - current xp) / (xp for next level - xp for current level)
    nextLevel: float = CATACOMBS_LEVELS[currentLevel + 1]
    currentLevelXp: float = CATACOMBS_LEVELS[currentLevel]
    percentage: float = (dungeonXp - currentLevelXp) / (nextLevel - currentLevelXp)

    return currentLevel + percentage
