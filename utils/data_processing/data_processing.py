from collections import defaultdict
from re import sub as re_sub
from nbt.nbt import NBTFile
from utils.data_processing.nbt_processing import decodeBase64NBT, exploreNBTTagsIteratively, processSkullOwner

"""
Changelog:
    - 19-02-2025 - Finally got into fixing this file. Added extractJSONFields, renamed function to decodeData (from decodeInventory),
    added decodeWardrobe. Updated function docstrings (as necessary).
    - 20-02-2025 - Updated the function extractJSONFields to work with the new Profile JSON result.
"""

def decodeItemData(itemData: dict) -> dict:
    """
    Process individual item data, including cleaning escape sequences and handling SkullOwner data (this function
    pretty much does miracles at this point).

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

                for key in list(display.keys()):  # Remove individual lore tags
                    if key.startswith('Lore['):
                        del display[key]

        if 'ExtraAttributes' in groupedData['tag']:
            extraAttributes: dict = groupedData['tag']['ExtraAttributes']

            if 'recipient_name' in extraAttributes:
                extraAttributes['recipient_name'] = cleanEscapeSequences(extraAttributes['recipient_name'])

            if 'name' in extraAttributes:
                extraAttributes['name'] = cleanEscapeSequences(extraAttributes['name'])

            if 'new_year_cake_bag_data' in extraAttributes:
                extraAttributes['cakes'] = {}
                data: NBTFile = decodeBase64NBT(extraAttributes['new_year_cake_bag_data'])
                for i, cake in enumerate(data['i']):
                    cakeData: dict = exploreNBTTagsIteratively(cake)
                    extraAttributes['cakes'][i] = decodeItemData(cakeData)

                del extraAttributes['new_year_cake_bag_data']


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

    :param display: The display dictionary in which the lore tags are stored

    :return: A single string containing all the lore tags
    """
    loreList: list = [(int(key[5:-1]), display[key]) for key in display.keys() if key.startswith('Lore[')]
    sortedLore: list = [text for _, text in sorted(loreList)]
    return '\n'.join(cleanEscapeSequences(line) for line in sortedLore)


def extractJSONFields(jsonData: dict, uuid: str, profiles: dict) -> dict:
    """
    Extract different (predefined) information from a JSON dict for easy processing. Should probably add some sort of
    checking in case the API for a component is off

    :param jsonData: The JSON dictionary to extract information from to then be processed
    :param uuid: The UUID of the player (in case they are in a coop)
    :param profiles: The profile slot of the player
    :return: The information from the JSON string
    """

    return {
        'inventory': jsonData['profile']['members'][uuid]['inventory']['inv_contents']['data'],
        'ender_chest': jsonData['profile']['members'][uuid]['inventory']['ender_chest_contents']['data'],
        'potions': jsonData['profile']['members'][uuid]['inventory']['bag_contents']['potion_bag']['data'],
        'talismans': jsonData['profile']['members'][uuid]['inventory']['bag_contents']['talisman_bag']['data'],
        'fishing_bag': jsonData['profile']['members'][uuid]['inventory']['bag_contents']['fishing_bag']['data'],
        'sacks_bag': jsonData['profile']['members'][uuid]['inventory']['bag_contents']['sacks_bag']['data'],
        'quiver': jsonData['profile']['members'][uuid]['inventory']['bag_contents']['quiver']['data'],
        'equipped_armor': jsonData['profile']['members'][uuid]['inventory']['inv_armor']['data'],
        'equipped_equipment': jsonData['profile']['members'][uuid]['inventory']['equipment_contents']['data'],
        'personal_vault': jsonData['profile']['members'][uuid]['inventory']['personal_vault_contents']['data'],
        'backpack': {
            'icons': {key: jsonData['profile']['members'][uuid]['inventory']['backpack_icons'][key]['data']
                      for key in sorted(jsonData['profile']['members'][uuid]['inventory']['backpack_icons'], key=int)},
            'content': {key: jsonData['profile']['members'][uuid]['inventory']['backpack_contents'][key]['data']
                        for key in sorted(jsonData['profile']['members'][uuid]['inventory']['backpack_contents'],key=int)}
        },
        'equipped_wardrobe_slot': jsonData['profile']['members'][uuid]['inventory']['wardrobe_equipped_slot'],
        'wardrobe': jsonData['profile']['members'][uuid]['inventory']['wardrobe_contents']['data'],
    }


def decodeData(raw: str) -> dict:
    """
    Decode the raw NBT data of multiple items into a dictionary representation, everything 0-indexed by a slot number,
    unless there is only one item.

    Tested for:
        - Inventory
        - Ender Chest
        - Backpack (both icons and content)
        - Personal Vault
        - Potions
        - Talismans
        - Fishing Bag
        - Sacks Bag
        - Quiver
        - Equipped Armor
        - Equipped Equipment
        - Wardrobe (Better use the decodeWardrobe function for this)

    :param raw: The raw NBT data to decode

    :return: A dictionary representation of the NBT data
    """
    nbtData: NBTFile = decodeBase64NBT(raw)
    inventory: dict = {}

    for i, item in enumerate(nbtData['i']):
        itemData: dict = exploreNBTTagsIteratively(item)
        inventory[i] = decodeItemData(itemData)

    return inventory[0] if len(inventory) == 1 else inventory


def decodeWardrobe(wardrobeData: str, currentEquippedSlot: int, currentArmor: str) -> dict:
    """
    This function receives the raw wardrobe data, as fetched from the API profile, and decodes it into a dictionary

    :param wardrobeData: The raw wardrobe data from the API
    :param currentEquippedSlot: The currently equipped wardrobe slot (to fill the missing slot)
    :param currentArmor: The raw data of the currently equipped armor from the API (to fill the missing slot)

    :return: The dictionary representation of the wardrobe data
    """
    wardrobeItems: dict = decodeData(wardrobeData)
    wardrobePages: dict = {
        0: {index: armorPiece for index, armorPiece in wardrobeItems.items() if 0 <= index <= 35},
        1: {index - 36: armorPiece for index, armorPiece in wardrobeItems.items() if 36 <= index <= 71},
    }

    finalWardrobeInfo: dict = {
        (page * 9) + i: {
            'helmet': items.get(i),
            'chestplate': items.get(i + 9),
            'leggings': items.get(i + 18),
            'boots': items.get(i + 27),
        } for page, items in wardrobePages.items() for i in range(9)
    }

    currentArmor: dict = decodeData(currentArmor)
    finalWardrobeInfo[currentEquippedSlot - 1] = dict(zip(['helmet', 'chestplate', 'leggings', 'boots'],
                                                          reversed(currentArmor.values())))

    return finalWardrobeInfo
