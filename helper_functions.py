from re import sub as re_sub
from json import dump as json_dump, load as json_load
from requests import Response, post
from collections import defaultdict


def dictToJSON(data: dict, filename: str) -> None:
    """
    Save a dictionary to a JSON file
    :param data: the dictionary to save
    :param filename: the name of the file to save to
    :return: Nothing (Could change to a bool)
    """
    with open(filename, "w") as f:
        print(f'Saving data to {filename}')
        json_dump(data, f)


def JSONToDict(filename: str) -> dict:
    """
    Load a dictionary from a JSON file
    :param filename: the name of the file to load from
    :return: the dictionary loaded from the file (or an empty dictionary if the file does not exist)
    """
    try:
        with open(filename, "r") as f:
            return json_load(f)

    except FileNotFoundError:
        print(f'File {filename} not found.')
        return {}


def loadSecret(filename: str, secretKey: str) -> str:
    """
    Load a secret from a JSON file
    :param filename: the name of the file to load from
    :param secretKey: the key of the secret to load
    :return: The secret loaded from the file (or an empty string if the file/key does not exist)
    """
    data: dict = JSONToDict(filename)
    return data.get(secretKey, "")


def getUUID(username: str) -> str:
    """
    Get the UUID of a player using Mojang's API
    :param username: The username of the player
    :return: The UUID of the player (or an empty string if the request fails)
    """
    UUIDCache: dict = JSONToDict("UUID-cache.json")

    username = username.lower()
    if username in UUIDCache.keys():
        return UUIDCache[username]

    header: dict = {
        'Content-Type': 'application/json'
    }
    body: list = [
        username
    ]
    response: Response = (
        post("https://api.mojang.com/profiles/minecraft", headers=header, json=body))

    if response.status_code == 200:
        data: dict = response.json()
        if len(data) == 0:
            print(f"Failed to get UUID for {username}\n"
                  f"Player not found")
            return ""

        else:
            UUIDCache[username] = data[0]["id"]
            dictToJSON(UUIDCache, "UUID-cache.json")
            return data[0]["id"]
    else:
        print(f"Failed to get UUID for {username}\n"
              f"{response.text}")
        return ""


def getLastPlayedProfile(profiles: dict) -> (str, str):
    """
    The function returns which profile is the last played by the player
    :param profiles: The data of all the players profiles, given by the getPlayerProfiles function
    :return: The profile id and the users UUID (located under the UUID-cache.json file)
    """
    player: str = list(profiles.keys())[0]
    playersUUID: str = getUUID(player)

    lastPlayed: str = ""
    for profile in profiles[player]:
        if profile['last_played']:
            lastPlayed = profile['profile_id']
            break

    return lastPlayed, playersUUID


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
