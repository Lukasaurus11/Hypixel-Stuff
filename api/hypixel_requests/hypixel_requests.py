from time import time as time_current
from requests import get
from requests.models import Response
from utils import decodeData, loadSecret, dictToJSON, JSONToDict
from utils.helper_functions import  returnFileLife
from api import getUUID, getProfileIDFromProfileName

"""
Changelog:
    - 20-02-2025 
        - Redid a bunch of functions inside of the file
        - Moved file to the api/hypixel_requests folder
"""

def getBazaarInformation() -> dict:
    """
    This function makes a request to the Hypixel API to get the current Bazaar information.

    :return: The Bazaar information
    """
    # Verify that the file exists and its not older than 10m (600s)
    if JSONToDict('data/hypixel_data/bazaar_data/bazaar.json'):
        if time_current() - returnFileLife('data/hypixel_data/bazaar_data/bazaar.json') < 600:
            return JSONToDict('data/hypixel_data/bazaar_data/bazaar.json')

    link: str = 'https://api.hypixel.net/v2/skyblock/bazaar'
    response: Response = get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token')})
    if response.status_code == 200:
        data: dict = response.json()

        data: dict = data['products']
        for key in data.keys():
            data[key] = data[key]['quick_status']

        dictToJSON(data, 'data/hypixel_data/bazaar_data/bazaar.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return {}


def getPlayerStatus(username: str) -> bool:
    """
    This function will return the online status of a player

    :param username: the username of the player to search for
    :return: A boolean value of the player's online status (False if there was an error with the request)
    """
    link: str = 'https://api.hypixel.net/v2/status'
    secretToken: str = loadSecret('data/secrets.json', 'hypixel-token')
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


def getProfileInformationByProfileName(profilesDict: dict, profileName: str=None) -> dict:
    """
    Updated version of the previous function, getProfileByID, where the profile ID is gathered directly from the profiles
    submitted, based on the profile we are interested in. This function will return the profile data for the given profile

    :param profilesDict: The profiles information (gathered from the getPlayerProfiles function)
    :param profileName: The name of the profile to get the data of
    :return: The profile information for the given profile
    """
    profileID: str = getProfileIDFromProfileName(profilesDict, profileName)
    response: Response = get("https://api.hypixel.net/v2/skyblock/profile",
                             params={
                                 'key': loadSecret('data/secrets.json', 'hypixel-token'),
                                 'profile': profileID
                             })

    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, f'data/hypixel_data/profile_data/{list(profilesDict.keys())[0]}-{profileName if None else "last-played"}.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return {}


def getPlayerProfiles(username: str) -> [dict, dict]:
    """
    Updated version of the previous function, getPlayerProfiles, where instead of saving the data of all profiles, it
    will save only the data of the last played profile. This change was done to save data storage (temporary feature?),
    and make it easier to read and process.

    :param username: The username to get the profiles of
    :return: The union of the profiles data, and the information of the last played profile
    """
    response: Response = get("https://api.hypixel.net/v2/skyblock/profiles",
                             params={
                                    'key': loadSecret('data/secrets.json', 'hypixel-token'),
                                    'uuid': getUUID(username)
                             })
    if response.status_code == 200:
        data: dict = response.json()
        if not data['profiles']: return {}

        profileDict: dict = {
            profile['cute_name']: {
                'profile_id': profile['profile_id'],
                'game_mode': profile.get('game_mode', "regular"),
                'last_played': profile['selected']
            } for profile in data['profiles']
        }
        profileDict = {username: profileDict}

        dictToJSON(profileDict, f'data/hypixel_data/profile_data/{username}-summarized-profiles.json')
        lastPlayedProfileInformation: dict = getProfileInformationByProfileName(profileDict)

        return profileDict, lastPlayedProfileInformation


def getMuseumData(profilesDict: dict, profileName: str=None) -> dict:
    """
    This function returns the museum data for a specific profile, given the full profile data, and the profile name to look for

    :param profilesDict: The profiles information (gathered from the getPlayerProfiles function)
    :param profileName: The name of the profile to get the data of
    :return: The museum data for the given profile
    """
    playerName: str = list(profilesDict.keys())[0]
    profileID: str = getProfileIDFromProfileName(profilesDict, profileName)
    uuid: str = getUUID(playerName)

    response: Response = get('https://api.hypixel.net/v2/skyblock/museum',
                             params={
                                 'key': loadSecret('data/secrets.json', 'hypixel-token'),
                                 'profile': profileID
                             })

    if response.status_code == 200:
        data: dict = response.json()
        data = data['members'][uuid]['items']

        for key, value in data.items():
            data[key]['items']['data'] = decodeData(value['items']['data'])


        dictToJSON(data, f'data/hypixel_data/museum_data/{playerName}-museum.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return {}


def getGameNews() -> None:
    """
    This function will fetch the news available from the API (it's something like the latest 10 updates)
    :return: Nothing, but could be changed to be a dictionary of the news articles, to then be furthered processed.
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/news'
    response: Response = get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token')})
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, 'data/hypixel_data/news_data/news.json')
        return

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        print(response.json())
        return

