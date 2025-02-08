"""
TODO: Add  example usages for every function and implement missing functions
"""

from collections import defaultdict
from re import sub as re_sub
from nbt.nbt import NBTFile
from utils.data_processing.nbt_processing import decodeBase64NBT, exploreNBTTagsIteratively, processSkullOwner


def decodeItemData(itemData: dict) -> dict:
    """
    Process individual item data, including cleaning escape sequences and handling SkullOwner data.
    :param itemData: The flat dictionary representation of the item data
    :return: The processed item data
    """
    groupedData: dict = groupKeys(itemData)

    try:
        if 'display' in groupedData['tag']:
            display: dict = groupedData['tag']['display']

            if 'Name' in display:
                display['Name'] = cleanEscapeSequences(display['Name'])

            if any(key.startswith('Lore') for key in display):
                display['Lore'] = mergeLoreTags(display)

                for key in list(display.keys()):    # Remove individual lore tags
                    if key.startswith('Lore['):
                        del display[key]

        if 'ExtraAttributes' in groupedData['tag']:
            extraAttributes: dict = groupedData['tag']['ExtraAttributes']

            if 'recipient_name' in extraAttributes:
                extraAttributes['recipient_name'] = cleanEscapeSequences(extraAttributes['recipient_name'])

            if 'name' in extraAttributes:
                extraAttributes['name'] = cleanEscapeSequences(extraAttributes['name'])

        if 'SkullOwner' in groupedData['tag']:
            skullOwnerData: dict = groupedData['tag']['SkullOwner']
            groupedData['tag'].update(processSkullOwner(skullOwnerData))
            del groupedData['tag']['SkullOwner']

    except KeyError:
        pass

    return groupedData


def groupKeys(data: dict) -> dict:
    """
    Group keys with dots into nested dictionaries.
    :param data: The flat dictionary to group
    :return: A nested dictionary representation of the data
    """
    grouped: defaultdict = defaultdict(dict)
    for key, value in data.items():
        if '.' in key:
            prefix: str
            suffix: str
            prefix, suffix = key.split('.', 1)
            grouped[prefix][suffix] = value

        else:
            grouped[key] = value

    for key, value in grouped.items():
        if isinstance(value, dict):
            grouped[key] = groupKeys(value)

    return dict(grouped)


def cleanEscapeSequences(text: str) -> str:
    """
    Removes (\u00a7.|§.) escape sequences from a string.
    :param text: A string that may contain escape sequences
    :return: The string with escape sequences removed
    """
    return re_sub(r'(§.)', '', text)


def mergeLoreTags(display: dict) -> str:
    """
    Merge individual Lore tags into a single string. We use an order to keep the lore tags in the correct order.
    :param display: the display dictionary in which the lore tags are stored
    :return: A single string containing all the lore tags
    """
    loreList: list = [(int(key[5:-1]), display[key]) for key in display.keys() if key.startswith('Lore[')]
    sortedLore: list = [text for _, text in sorted(loreList)]
    return '\n'.join(cleanEscapeSequences(line) for line in sortedLore)


def getInformationFromJSON(jsonData: dict, uuid: str) -> dict:
    """
    Extract different (predefined) information from a JSON dict for easy processing

    :param jsonData: The JSON dictionary to extract information from to then be processed
    :param uuid: The UUID of the player (in case they are in a coop)
    :return: The information from the JSON string
    """
    # /profile/members/{uuid}/inventory/inv_contents/data ( a lot are like this)

    pass



# TODO: (Look more in depth into what exactly this function does, and why it was necessary in the first place)
def processSingleItemNBT(raw: str) -> dict:
    """
    Process the NBT data of an item

    :param raw: The NBT data
    :return: A dictionary representation of the inventory data
    """
    nbtData: NBTFile = decodeBase64NBT(raw)
    nbtDataDict: dict = {}

    for _, item in enumerate(nbtData['i']):
        itemData: dict = exploreNBTTagsIteratively(item)
        nbtDataDict.update(decodeItemData(itemData))

    # dictToJSON(nbtDataDict, f"data/hypixel_data/nbt_data/{raw[:10]}_inventory_data.json")
    return nbtDataDict


def decodeInventory(raw: str) -> dict:
    """
    Decode the inventory data of the entire inventory of a player, returning a dictionary with keys as the item slot
    and values as the item data. The keys start at 0, where 0 to 8 indicate the hotbar, 9 to 35 indicate the main
    inventory
    :param raw: The NBT data of the inventory
    :return: A dictionary representation of the inventory data
    """
    nbtData: NBTFile = decodeBase64NBT(raw)
    inventory: dict = {}

    for i, item in enumerate(nbtData['i']):
        itemData: dict = exploreNBTTagsIteratively(item)
        inventory[i] = decodeItemData(itemData)

    # dictToJSON(inventory, f"hypixel_data/inventory_data/{raw[:10]}_inventory_data.json")
    return inventory


def decodeBackpack(backpackIcons: dict, backpackContent: dict) -> dict:
    """
    Decode the backpack data of a player, returning a dictionary with keys as the backpack slot and values as the
    backpack data.

    :param backpackIcons: The data about the different backpack icons (their texture and name)
    :param backpackContent: All the content of the backpacks
    :return: A dictionary representation of the backpack data
    """
    sortedBackpackIcons: dict = {int(key): value for key, value in backpackIcons.items()}
    sortedBackpackContent: dict = {int(key): value for key, value in backpackContent.items()}

    backpackData: dict = {}
    for key in sortedBackpackIcons.keys():
        iconData: dict = processSingleItemNBT(sortedBackpackIcons[key]['data'])
        contentData: dict = decodeInventory(sortedBackpackContent[key]['data'])

        backpackData[key] = {
            'icon': iconData,
            'content': contentData
        }

    # dictToJSON(backpackData, f"hypixel_data/backpack_data/backpack_data.json")
    return backpackData
