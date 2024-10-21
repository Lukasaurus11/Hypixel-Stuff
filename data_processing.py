from nbt.nbt import NBTFile
from nbt_processing import decodeBase64NBT, exploreNBTTagsIteratively, processSkullOwner
from helper_functions import dictToJSON, groupKeys, cleanEscapeSequences, mergeLoreTags


def processItemData(itemData: dict) -> dict:
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


def processNBT(raw: str) -> dict:
    """
    Process the NBT data of an item
    :param raw: The NBT data
    :return: A dictionary representation of the inventory data
    """
    nbtData: NBTFile = decodeBase64NBT(raw)
    nbtDataDict: dict = {}

    for _, item in enumerate(nbtData['i']):
        itemData: dict = exploreNBTTagsIteratively(item)
        nbtDataDict.update(processItemData(itemData))

    dictToJSON(nbtDataDict, f"hypixel_data/nbt_data/{raw[:10]}_inventory_data.json")
    return nbtDataDict


def inventoryData(raw: str) -> dict:
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
        inventory[i] = processItemData(itemData)

    dictToJSON(inventory, f"hypixel_data/inventory_data/{raw[:10]}_inventory_data.json")
    return inventory


def processBackpackData(backpackIcons: dict, backpackContent: dict) -> dict:
    """

    :param backpackIcons:
    :param backpackContent:
    :return:
    """
    sortedBackpackIcons: dict = {int(key): value for key, value in backpackIcons.items()}
    sortedBackpackContent: dict = {int(key): value for key, value in backpackContent.items()}

    backpackData: dict = {}
    for key in sortedBackpackIcons.keys():
        iconData: dict = processNBT(sortedBackpackIcons[key]['data'])
        contentData: dict = inventoryData(sortedBackpackContent[key]['data'])

        backpackData[key] = {
            'icon': iconData,
            'content': contentData
        }

    dictToJSON(backpackData, f"hypixel_data/backpack_data/backpack_data.json")
    return backpackData


def processSingleItem(raw: str) -> dict:
    """
    FUNCTION IN PROGRESS, THIS DOES NOT WORK PROPERLY CURRENTLY
    Process a single item from a base64 encoded NBT string.
    :param raw: The base64 encoded NBT data of the item
    :return: A dictionary representation of the processed item data
    """
    nbtData: NBTFile = decodeBase64NBT(raw)
    itemData: dict = exploreNBTTagsIteratively(nbtData)

    dictToJSON(itemData, f"hypixel_data/single_item_data/{raw[:10]}_item_data.json")
    return processItemData(itemData)
