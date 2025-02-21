from utils import JSONToDict, dictToJSON
from requests import post, Response

"""
Changelog:
    - 20-02-2025 - Created file and moved the getUUID and getProfileIDFromProfileName functions from utils.helper_functions.helper_functions.py
        as they made more sense here (imo)
"""

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


def getProfileIDFromProfileName(profilesInformation: dict, profileName: str=None) -> str:
    """
    This function will return the profile ID of the profile with the given name, replacing the function getProfileIDFromLastPlayed

    :param profilesInformation: The information of the profiles
    :param profileName: The name of the profile we are looking for
    :return: The profile ID of the profile with the given name
    """
    for profiles in profilesInformation.values():
        for name, profile in profiles.items():
            if profileName is None:
                if profile['last_played']:
                    return profile['profile_id']
            else:
                if profileName == name:
                    return profile['profile_id']

    return ""