from hypixel_requests import *
from data_processing import *

def main():
    """
    mining_core -> where the heart of the mountain stuff is. Need to build skill tree 1st (take tree from wiki)
    :return:
    """

    data = getPlayerProfiles('Deathstreeks')

    lastPlayedProfile: str
    playerUUID: str

    lastPlayedProfile, playerUUID = getLastPlayedProfile(data)
    profileData = getProfileByID(lastPlayedProfile)

    inventory = profileData['profile']['members'][playerUUID]['inventory']['bag_contents']['talisman_bag']['data']
    # backpackIcons = profileData['profile']['members'][playerUUID]['inventory']['backpack_icons']
    # backpackContent = profileData['profile']['members'][playerUUID]['inventory']['backpack_contents']
    # print(processBackpackData(backpackIcons, backpackContent))


    getGameNews()

if __name__ == '__main__':
    main()
