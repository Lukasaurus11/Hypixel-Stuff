from api import getUUID
from api.hypixel_requests.hypixel_requests import getPlayerProfiles
from utils.data_processing import extractJSONFields
from simulators import monteCarloSimulation, simulateMining
from simulators.mining.glossy import plotSimulationResults
from utils.hypixel_code.constants.gemstone_constants import THRESHOLDS

"""
player: str = "Lukasaurus_"
profiles, lastPlayed = getPlayerProfiles(player)

references = extractJSONFields(lastPlayed, getUUID(player), {})
print(references['ender_chest'])
"""

