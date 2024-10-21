from math import floor

"""
Cant be asked to do the other skill information right now
"""

HEART_OF_THE_MOUNTAIN: dict = {
    1: {
        'mining speed': {
            'total cost': 1758267,
            'level exponential': 3,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        }
    },
    2: {
        'mining speed boost': {
            'type': 'ability',
            'powder type': 'mithril'
        },
        'precision mining': {
            'type': 'un-upgradable perk',
            'powder type': 'mithril'
        },
        'mining fortune': {
            'total cost': 2114821,
            'level exponential': 3.05,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        },
        'titanium insanium': {
            'total cost': 2544096,
            'level exponential': 3.1,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        },
        'pickobulus': {
            'type': 'ability',
            'powder type': 'mithril'
        }
    },
    3: {
        'luck of the cave': {
            'total cost': 1502539,
            'level exponential': 3.07,
            'max level': 45,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        },
        'efficient miner': {
            'total cost': 4644659,
            'level exponential': 2.6,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        },
        'quick forge': {
            'total cost': 93838,
            'level exponential': 3.2,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'mithril'
        }
    },
    4: {
        'sky mall': {
            'type': 'un-upgradable perk',
            'powder type': 'gemstone'
        },
        'old-school': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'professional': {
            'total cost': 3792862,
            'level exponential': 2.3,
            'max level': 140,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'mole': {
            'total cost': 6646936,
            'level exponential': 2.17883,  # bruh
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'gem lover': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'seasoned mineman': {
            'total cost': 1267045,
            'level exponential': 2.3,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'front loaded': {
            'type': 'un-upgradable perk',
            'powder type': 'gemstone'
        }
    },
    5: {
        'daily grind': {
            'type': 'un-upgradable perk',
            'powder type': 'gemstone'
        },
        'core of the mountain': {
            'max level': 10,
            'type': 'core of the mountain',
        },
        'daily powder': {
            'type': 'un-upgradable perk',
            'powder type': 'gemstone'
        }
    },
    6: {
        'anomalous desire': {
            'type': 'ability',
            'powder type': 'gemstone'
        },
        'blockhead': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'subterranean fisher': {
            'total cost': 945621,
            'level exponential': 3.07,
            'max level': 40,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'keep it cool': {
            'total cost': 2277033,
            'level exponential': 3.07,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'lonesome miner': {
            'total cost': 1502539,
            'level exponential': 3.07,
            'max level': 45,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'great explorer': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'maniac miner': {
            'type': 'ability',
            'powder type': 'gemstone'
        }
    },
    7: {
        'speedy mineman': {
            'total cost': 3683370,
            'level exponential': 3.2,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'powder buff': {
            'total cost': 3683370,
            'level exponential': 3.2,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        },
        'fortunate mineman': {
            'total cost': 3683370,
            'level exponential': 3.2,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'gemstone'
        }
    },
    8: {
        'miner\'s blessing': {
            'type': 'unupgradable perk',
            'powder type': 'glacite'
        },
        'no stone unturned': {
            'total cost': 2114821,
            'level exponential': 3.05,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'strong arm': {
            'total cost': 1267045,
            'level exponential': 2.3,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'steady hand': {
            'total cost': 4644659,
            'level exponential': 2.6,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'warm hearted': {
            'total cost': 2544096,
            'level exponential': 3.1,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'surveyor': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'mineshaft mayhem': {
            'type': 'un-upgradable perk',
            'powder type': 'glacite'
        }
    },
    9: {
        'metal head': {
            'total cost': 917130,
            'level exponential': 4,
            'max level': 20,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'rags to riches': {
            'total cost': 2114821,
            'level exponential': 3.05,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'eager adventurer': {
            'total cost': 1267045,
            'level exponential': 2.3,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        }
    },
    10: {
        'gemstone infusion': {
            'type': 'ability',
            'powder type': 'glacite'
        },
        'crystalline': {
            'total cost': 5335845,
            'level exponential': 3.3,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'gifts from the departed': {
            'total cost': 2423618,
            'level exponential': 2.45,
            'max level': 100,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'mining master': {
            'total cost': 4705857,
            'level exponential': 5,
            'max level': 10,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'dead man\'s chest': {
            'total cost': 3683370,
            'level exponential': 3.2,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'vanguard seeker': {
            'total cost': 2544096,
            'level exponential': 3.1,
            'max level': 50,
            'type': 'upgradable perk',
            'powder type': 'glacite'
        },
        'sheer force': {
            'type': 'ability',
            'powder type': 'glacite'
        }
    }
}


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


print(printHOTMTree(buildHOTMTree()))
