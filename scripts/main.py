from utils.hypixel_code.hypixel_requests import getPlayerProfiles, getProfileByID, getBazaarInformation
from simulators.diana.burrow_chain_simulator import simulateChain
from utils.helper_functions import getLastPlayedProfile, dictToJSON
from simulators.helper_functions.montecarlo_simulation import monteCarloSimulation
from simulators.dragon_stuff.find_best_stat_combo import dragonScoringFunction, simulateDragonFight
from simulators.minion.inferno_minion.inferno_minion_simulator import simulateInfernoMinion
from utils.hypixel_code.constants.skills_constants import HEART_OF_THE_MOUNTAIN

# Total powder x type
# {'mithril': 12658220, 'gemstone': 31150666, 'glacite': 34479533}


temp = monteCarloSimulation(3, simulateDragonFight, dragonScoringFunction, magic_find=100, pet_luck=100, eyes_placed=4)
print(temp['average_results'])

"""
data = getPlayerProfiles('Lukasaurus_')

lastPlayedProfile: str
playerUUID: str

lastPlayedProfile = getLastPlayedProfile(data)
profileData = getProfileByID(lastPlayedProfile)

dictToJSON(profileData, f"data/hypixel_data/profile_data/Lukasaurus.json")
"""
