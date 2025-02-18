from typing import Union, Any
from time import time as get_current_time
from requests import get
from requests.models import Response
from re import search as re_search
from utils.data_processing.data_processing import decodeInventory
from utils.helper_functions import loadSecret, getUUID, getLastPlayedProfile, dictToJSON, JSONToDict, returnFileLife
from utils.hypixel_code.skills.skill_functions import calculateDungeonLevel


def getBazaarInformation() -> dict:
    """
    This function makes a request to the Hypixel API to get the current Bazaar information.

    :return: The Bazaar information
    """
    # Verify that the file exists and its not older than 10m (600s)
    if JSONToDict('data/hypixel_data/bazaar_data/bazaar.json'):
        if get_current_time() - returnFileLife('data/hypixel_data/bazaar_data/bazaar.json') < 600:
            return JSONToDict('data/hypixel_data/bazaar_data/bazaar.json')

    link: str = 'https://api.hypixel.net/v2/skyblock/bazaar'
    response: Response = get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token')})
    if response.status_code == 200:
        data: dict = response.json()

        # Summary the bazaar data, so that it is only Item Name : {quick_status}
        data: dict = data['products']
        for key in data.keys():
            data[key] = data[key]['quick_status']

        dictToJSON(data, 'data/hypixel_data/bazaar_data/bazaar.json')
        return data

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return {}


def makeRequest(link: str, paramType: str, paramValue) -> Response:
    """
    This function will make a request to the given link1
    :param link: The link to make the request to
    :param paramType: The type of the parameter to type into the request
    :param paramValue: The value of the parameter

    :return: The response object
    """
    if paramType == 'uuid':
        username = paramValue.lower()
        uuid: str = getUUID(username)
        if uuid == "":
            return Response()

        return get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token'),
                                               'uuid': uuid})

    elif paramType == 'profile':
        return get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token'),
                                               'profile': paramValue})

    return get(link, params={'key': loadSecret('data/secrets.json', 'hypixel-token')})


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


def getPlayerProfiles(username: str) -> dict:
    """
    This function will save the player's profile data into a JSON file
    :param username:
    :return: The dictionary of the player's profiles
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/profiles'

    response: Response = makeRequest(link, 'uuid', username)
    if response.status_code == 200:
        data: dict = response.json()

        if not data['profiles']:
            return {}

        dictToJSON(data, f'data/hypixel_data/profile_data/{username}-all-profiles.json')

        profileDict: dict = {
            username: {}
        }

        for i, profile in enumerate(data['profiles']):
            profileInfoDict: dict = {
                'profile_id': profile['profile_id'],
                'game_mode': profile.get('game_mode', "regular"),
                'profile_name': profile['cute_name'],
                'last_played': profile['selected']
            }

            profileDict[username][i] = profileInfoDict

        dictToJSON(profileDict, f'data/hypixel_data/profile_data/{username}-profiles.json')
        return profileDict

    else:
        print(f'An error occurred with the request\n'
              f'{response.status_code}')
        return {}


# Could technically be merged with the getMuseumData function as theres only 1 word that changes within the URL link TBD
def getProfileByID(profileID: str) -> dict:
    """
    This function will return the profile data of a player using the profile ID
    :param profileID: the profile ID of the player
    :return: the corresponding profile data
    """
    link: str = 'https://api.hypixel.net/v2/skyblock/profile'
    response: Response = makeRequest(link, 'profile', profileID)
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, f'data/hypixel_data/profile_data/raw/{profileID[:16]}.json')
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
    response: Response = makeRequest(link, 'profile', profileID)
    if response.status_code == 200:
        data: dict = response.json()
        dictToJSON(data, f'data/hypixel_data/museum_data/{profileID[:16]}-museum.json')
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


# There's definitely a better way to approach the checking aspect
def getPlayerInfo(username: str, activity: str, *args) -> Union[None, dict, dict[Any, Any]]:
    """
    This functions returns the player's information based on the activity
    (available activities: diana, dungeon, kuudra)

    example:
    - getPlayerInfo('Lukasaurus_', 'diana')
        - returns total mythological ritual kills, if looting 5 in Daedalus axe, if hyperion.

    :param username: The username of the player to search for
    :param activity: The activity to search for
    :param args: Additional arguments to pass in (for example floor being run in dungeons)
    :return: The dictionary of the player's information
    """

    availableActivities: dict = {
        'diana': {
            'Hyperion': False,
            'L5-Daedalus': False,
            'Total Kills': 0
        },
        'dungeon': {
            'Catacombs Level': 0,
            "Floor-Clears": 0,
            'Terminator': False,
            'Hyperion': False,
            'Wither-Set': False,
            'Total-Secrets': 0
        },
        'kuudra': {
            'Kuudra-Clears': 0,
            'Terminator': {
                "Power-Level": 0,
                "Cubism-Level": 0,
                "Duplex": False
            },
            'Hyperion': False,
            'Terror-Set': False,
            'Aurora-Set': False,
            'Deployable': False
        }
    }

    if activity in availableActivities.keys():
        # Target data
        targetData: dict = availableActivities[activity]

        # Get the player's profile data
        profileData: dict = getPlayerProfiles(username)
        if profileData == {}:
            return {}

        lastPlayedProfile: str = getLastPlayedProfile(profileData)
        playerUUID: str = getUUID(username)
        profileData: dict = getProfileByID(lastPlayedProfile)

        inventory: str = profileData['profile']['members'][playerUUID]['inventory']['inv_contents']['data']
        inventory: dict = decodeInventory(inventory)

        # Go through the inventory data, using regex to match what we are interested in
        # For example, if the player has a Hyperion, with Wither Impact , we will set the Hyperion key to True
        if activity == 'diana':
            for _, value in inventory.items():
                if len(value) == 0:
                    continue
                else:
                    if re_search(r'\bHyperion\b', value['tag']['display']['Name']):
                        # Check for Wither Impact
                        if re_search(r'\bWither Impact\b', value['tag']['display']['Lore']):
                            targetData['Hyperion'] = True

                    if re_search(r'\bDaedalus Axe\b', value['tag']['display']['Name']):
                        # Check for Looting 5
                        if re_search(r'\bLooting V\b', value['tag']['display']['Lore']):
                            targetData['L5-Daedalus'] = True

            # Check for total kills
            bestiaryKills: dict = profileData['profile']['members'][playerUUID]['bestiary']['kills']
            mythologicalRitualMobs = ['gaia_construct', 'minos_champion', 'minos_hunter', 'minos_inquisitor', 'minotaur', 'siamese_lynx']

            for key, value in bestiaryKills.items():
                for mob in mythologicalRitualMobs:
                    if re_search(rf'^{mob}', key):
                        targetData['Total Kills'] += value

        elif activity == 'dungeon':
            for _, value in inventory.items():
                if len(value) == 0:
                    continue
                else:
                    if re_search(r'\bHyperion\b', value['tag']['display']['Name']):
                        # Check for Wither Impact
                        if re_search(r'\bWither Impact\b', value['tag']['display']['Lore']):
                            targetData['Hyperion'] = True

                    if re_search(r'\bTerminator\b', value['tag']['display']['Name']):
                        targetData['Terminator'] = True

            catacombsLevel: int = profileData['profile']['members'][playerUUID]['dungeons']['dungeon_types']['catacombs']['experience']
            targetData['Catacombs Level'] = calculateDungeonLevel(catacombsLevel)

            # /profiles/0/members/a581006093874931a33f9f6ce9e227bd/dungeons/secrets
            secrets: int = profileData['profile']['members'][playerUUID]['dungeons']['secrets']
            targetData['Total-Secrets'] = secrets

            # Get clears for the requested floor (should be passed as the 1st argument in kwargs)
            if args:
                floor: str = args[0][1:]
                if 'm' in args[0]:
                    # /profiles/0/members/a581006093874931a33f9f6ce9e227bd/dungeons/dungeon_types/master_catacombs/tier_completions/5
                    clears: int = profileData['profile']['members'][playerUUID]['dungeons']['dungeon_types']['master_catacombs']['tier_completions'][floor]
                    targetData['Floor-Clears'] = (args[0], clears)

                else:
                    clears: int = profileData['profile']['members'][playerUUID]['dungeons']['dungeon_types']['catacombs']['tier_completions'][floor]
                    targetData['Floor-Clears'] = (args[0], clears)


        return targetData
