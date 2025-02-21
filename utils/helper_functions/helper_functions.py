from json import dump as json_dump, load as json_load, JSONDecodeError
from os import getcwd, makedirs
from os.path import abspath, dirname, isdir, join as os_join, getmtime

"""
Changelog:
    - 20-02-2025 - Redid the getProfileIDFromLastPlayed function to getProfileIDFromProfileName
"""

def findRepoRoot() -> str:
    """
    Finds the root directory of the repository by looking for a .git folder.
    :return: the absolute path of the root directory.
    """
    currentDirectory: str = abspath(getcwd())

    while currentDirectory != dirname(currentDirectory):
        if isdir(os_join(currentDirectory, ".git")):

            return currentDirectory

        currentDirectory = dirname(currentDirectory)

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
