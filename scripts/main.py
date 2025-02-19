from utils.data_processing.data_processing import extractJSONFields, decodeData, decodeWardrobe
from utils.helper_functions import JSONToDict, dictToJSON, getUUID
from utils.hypixel_code.hypixel_requests import getPlayerProfiles


player: str = "Lukasaurus_"
# getPlayerProfiles(player)

data: dict = JSONToDict(f"data/hypixel_data/profile_data/{player}-all-profiles.json")
profiles: dict = JSONToDict(f"data/hypixel_data/profile_data/{player}-profiles.json")
uuid: str = getUUID(player)

references: dict = extractJSONFields(data, uuid, profiles)

talismans: dict = decodeData(references['talismans'])
dictToJSON(talismans, f"data/hypixel_data/inventory_data/{player}-talismans.json")

wardrobe: dict = decodeWardrobe(references['wardrobe'], references['equipped_wardrobe_slot'], references['equipped_armor'])
dictToJSON(wardrobe, f"data/hypixel_data/inventory_data/{player}-wardrobe.json")
