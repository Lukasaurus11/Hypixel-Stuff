from utils.helper_functions import JSONToDict, dictToJSON, getUUID
from utils.hypixel_code.hypixel_requests import getPlayerProfiles, getMuseumData
from utils.data_processing import extractJSONFields


player: str = "Lukasaurus_"
profiles, lastPlayed = getPlayerProfiles(player)

references = extractJSONFields(lastPlayed, getUUID(player), {})
print(references['ender_chest'])