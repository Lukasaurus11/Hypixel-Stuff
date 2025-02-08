from json import dump as json_dump, load as json_load, JSONDecodeError
from requests import Response, post
from os import getcwd, makedirs
from os.path import abspath, dirname, isdir, join as os_join, getmtime


def findRepoRoot() -> str:
    """
    Finds the root directory of the repository by looking for a .git folder.
    :return: the absolute path of the root directory.
    """
    currentDirectory: str = abspath(getcwd())

    while currentDirectory != dirname(currentDirectory):  # Stop at filesystem root
        if isdir(os_join(currentDirectory, ".git")):

            return currentDirectory

        currentDirectory = dirname(currentDirectory)  # Move up one level

    raise FileNotFoundError("Could not find the repository root. Make sure you're inside a Git repository.")


def returnFileLife(filename: str) -> float:
    """
    Returns the time since the file was last modified

    :param filename: the name of the file to check
    :return: the time since the file was last modified
    """
    try:
        repoRoot: str = findRepoRoot()
        filePath: str = os_join(repoRoot, filename)

        return getmtime(filePath)

    except Exception as e:
        print(f'Error getting file life of {filename}\n'
              f'{e}')
        return -1


def dictToJSON(data: dict, filename: str) -> None:
    """
    Save a dictionary to a JSON file

    :param data: the dictionary to save
    :param filename: the name of the file to save to
    :return: Nothing (Could change to a bool)
    """
    try:
        repoRoot: str = findRepoRoot()
        filePath: str = os_join(repoRoot, filename)

        makedirs(dirname(filePath), exist_ok=True)

        with open(filePath, "w") as f:
            print(f'Saving data to {filePath}')
            json_dump(data, f, indent=4)

    except Exception as e:
        print(f'Error saving data to {filename}\n'
              f'{e}')


def JSONToDict(filename: str) -> dict:
    """
    Load a dictionary from a JSON file relative to the repository root.
    :param filename: the name of the file to load from
    :return: the dictionary loaded from the file (or an empty dictionary if the file does not exist)
    """
    try:
        repoRoot: str = findRepoRoot()
        filePath: str = os_join(repoRoot, filename)

        with open(filePath, "r") as f:
            return json_load(f)

    except FileNotFoundError:
        print(f'File {filename} not found in repository root.')
        return {}

    except JSONDecodeError:
        print(f'Error decoding JSON in {filename}.')
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
    UUIDCache: dict = JSONToDict("data/UUID-cache.json")

    username = username.lower()
    if username in UUIDCache.keys():
        return UUIDCache[username]

    header: dict = {
        'Content-Type': 'application/json'
    }
    body: list = [
        username
    ]
    response: Response = post("https://api.mojang.com/profiles/minecraft", headers=header, json=body)

    if response.status_code == 200:
        data: dict = response.json()
        if len(data) == 0:
            print(f"Failed to get UUID for {username}\n"
                  f"Player not found")
            return ""

        else:
            UUIDCache[username] = data[0]["id"]
            dictToJSON(UUIDCache, "data/UUID-cache.json")
            return data[0]["id"]
    else:
        print(f"Failed to get UUID for {username}\n"
              f"{response.text}")
        return ""


def getLastPlayedProfile(profiles: dict) -> str:
    """
    The function returns which profile is the last played by the player
    :param profiles: The data of all the players profiles, given by the getPlayerProfiles function
    :return: The profile id and the users UUID (located under the UUID-cache.json file)
    """
    player: str = list(profiles.keys())[0]

    lastPlayed: str = ""
    for profile in profiles[player]:
        print(profile)
        if profile['last_played']:
            lastPlayed = profile['profile_id']
            break

    return lastPlayed
