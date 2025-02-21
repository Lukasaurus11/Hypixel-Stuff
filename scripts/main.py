from api import getUUID
from api.hypixel_requests.hypixel_requests import getPlayerProfiles
from utils import decodeData, decodeWardrobe
from utils.data_processing import extractJSONFields
from simulators import monteCarloSimulation, simulateMining
from simulators.mining.glossy import plotSimulationResults
from utils.hypixel_code.constants.gemstone_constants import THRESHOLDS

player: str = "Lukasaurus_"
profiles, lastPlayed = getPlayerProfiles(player)

references = extractJSONFields(lastPlayed, getUUID(player), {})

print(decodeWardrobe(references['wardrobe'], references['equipped_wardrobe_slot'], references['equipped_armor']))


