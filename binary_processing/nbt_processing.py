from nbt.nbt import NBTFile, TAG_Compound, TAG_List
from io import BytesIO
from base64 import b64decode
from collections import deque
from json import JSONDecodeError, loads as json_loads


def decodeBase64NBT(raw: str) -> NBTFile:
    """
    Decode base64 encoded NBT data.
    :param raw: The base64 encoded NBT data
    :return: The decoded NBT data as an NBTFile object
    """
    decodedData: bytes = b64decode(raw)
    return NBTFile(fileobj=BytesIO(decodedData))


def exploreNBTTagsIteratively(nbtData: NBTFile) -> dict:
    """
    Explore NBT tags iteratively, remove 'i[0]' and '.tag' parts from the path,
    and return a flat dictionary representation of the NBT data.
    :param nbtData: The NBT data as an NBTFile object
    :return: A flat dictionary representation of the NBT data
    """
    queue: deque = deque([(nbtData, '')])
    result: dict = {}

    while queue:
        currentTag: TAG_Compound or TAG_List
        path: str
        currentTag, path = queue.popleft()

        if isinstance(currentTag, TAG_Compound):
            for tag in currentTag.tags:
                newPath: str = f"{path}.{tag.name}" if path else tag.name
                queue.append((tag, newPath))

        elif isinstance(currentTag, TAG_List):
            for i, tag in enumerate(currentTag):
                newPath: str = f"{path}[{i}]"
                queue.append((tag, newPath))

        else:
            cleanedPath: str = path.replace('i[0].', '').replace('.tag', '')
            result[cleanedPath] = currentTag.value

    return result


def processSkullOwner(skullOwner: dict) -> dict:
    """
    Process the SkullOwner data, decode the base64 encoded texture value, and return the processed data.
    :param skullOwner: The SkullOwner dictionary
    :return: A dictionary with the processed SkullOwner data
    """
    try:
        textureValue = skullOwner['Properties']['textures[0]']['Value']
        padding = '=' * ((4 - len(textureValue) % 4) % 4)   # Add padding to the base64 string if necessary
        decodedTexture = b64decode(textureValue + padding).decode('utf-8')
        return {'ExtraData': json_loads(decodedTexture)}
    except (KeyError, JSONDecodeError):
        return {}
