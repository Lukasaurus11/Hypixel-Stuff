from utils.hypixel_code.hypixel_requests import getPlayerProfiles, getProfileByID, getBazaarInformation
from simulators.diana.burrow_chain_simulator import simulateChain
from utils.helper_functions import getLastPlayedProfile, dictToJSON
from simulators.helper_functions.montecarlo_simulation import monteCarloSimulation
from simulators.dragon.find_best_stat_combo import dragonScoringFunction, simulateDragonFight
from simulators.minion.inferno_minion.inferno_minion_simulator import simulateInfernoMinion
from utils.hypixel_code.constants.skills_constants import HEART_OF_THE_MOUNTAIN
from simulators.mining.glossy import simulateMining


result = monteCarloSimulation(2, simulateChain, isEnderSlayerNine=True)

# Pretty print the results
for key, value in result.items():
    print(key, value)

