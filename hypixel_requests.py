from helper_functions import *
from requests import get

"""
TODO:
    - Fix the imports, to import only what is necessary
    - Reduce code redundancy. Currently a lot of the request functions have the same identical structure, and all that changes is 1 word in the URL.
"""

def getPlayerStatus(username: str) -> bool:
    """
    This function will return the online status of a player
    :param username: the username of the player to search for
    :return: A boolean value of the player's online status (False if there was an error with the request)
    """
    link: str = 'https://api.hypixel.net/v2/status'
    secretToken: str = loadSecret('secrets.json', 'hypixel-token')
    uuid: str = getUUID(username)
    if uuid == "":
        return False

    params: dict = {
        'key': secretToken,
        'uuid': uuid
    }

    response: Response = get(link, params=params)
    if response.status_code == 200:
        print(response.json())
        return response.json()['session']['online']
    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return False


def getPlayerProfiles(username: str) -> dict:
    """
    This function will save the player's profile data into a JSON file
    :param username:
    :return: The dictionary of the player's profiles
    """
    username = username.lower()
    link: str = 'https://api.hypixel.net/v2/skyblock/profiles'
    secretToken: str = loadSecret('secrets.json', 'hypixel-token')
    uuid: str = getUUID(username)
    if uuid == "":
        return {}

    params: dict = {
        'key': secretToken,
        'uuid': uuid
    }

    response: Response = get(link, params=params)
    if response.status_code == 200:
        data: dict = response.json()

        dictToJSON(data, f'hypixel_data/profile_data/{username}-all-profiles.json')

        profileDict: dict = {
            username: []
        }

        for profile in data['profiles']:
            profileInfoDict: dict = {
                'profile_id': profile['profile_id'],
                'game_mode': profile.get('game_mode', "regular"),
                'profile_name': profile['cute_name'],
                'last_played': profile['selected']
            }

            profileDict[username].append(profileInfoDict)

        dictToJSON(profileDict, f'hypixel_data/profile_data/{username}-profiles.json')
        return profileDict

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        print(response.json())
        return {}


def getProfileByID(profileID: str) -> dict:
    """
    This function will return the profile data of a player using the profile ID
    :param profileID: the profile ID of the player
    :return: the corresponding profile data
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/profile'
    secretToken: str = loadSecret('secrets.json', 'hypixel-token')

    params: dict = {
        'key': secretToken,
        'profile': profileID
    }

    response: Response = get(link, params=params)
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, f'hypixel_data/profile_data/raw/{profileID[:16]}.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        print(response.json())
        return {}

def getMuseumData(profileID: str) -> dict:
    """
    This function will save the museum data for a player's profile into a JSON file
    :param profileID:
    :return:
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/museum'
    secretToken: str = loadSecret('secrets.json', 'hypixel-token')
    params: dict = {
        'key': secretToken,
        'profile': profileID
    }

    response: Response = get(link, params=params)
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, f'hypixel_data/museum_data/{profileID[:16]}-museum.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        print(response.json())
        return {}


def getGameNews() -> None:
    """
    This function will fetch the news available from the API (it's something like the latest 10 updates)
    :return: Nothing, but could be changed to be a dictionary of the news articles, to then be furthered processed.
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/news'
    secretToken: str = loadSecret('secrets.json', 'hypixel-token')
    params: dict = {
        'key': secretToken
    }

    response: Response = get(link, params=params)
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, 'hypixel_data/news_data/news.json')
    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        print(response.json())
        return
