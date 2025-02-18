from utils.data_processing.data_processing import extractJSONFields, decodeInventory
from utils.helper_functions import JSONToDict, dictToJSON
from utils.hypixel_code.hypixel_requests import getPlayerProfiles


player: str = "mynamesosig"
getPlayerProfiles(player)

data: dict = JSONToDict(f"data/hypixel_data/profile_data/{player}-all-profiles.json")
profiles: dict = JSONToDict(f"data/hypixel_data/profile_data/{player}-profiles.json")

# references: dict = extractJSONFields(data, "e9a2a6c6037f4315af0ccc76313a6cf9", profiles)    # Lukasaurus_
# references: dict = extractJSONFields(data, "40ad096bbac3437481c174be657a99e8", profiles)    # rxin__
references: dict = extractJSONFields(data, "dd593e2d557545d0b4b9e7f5d5538597", profiles)    # mynamesosig

quiver: dict = decodeInventory(references['quiver'])
dictToJSON(quiver, f"data/hypixel_data/inventory_data/{player}-quiver.json")

equippedArmor: dict = decodeInventory(references['equipped_armor'])
dictToJSON(equippedArmor, f"data/hypixel_data/inventory_data/{player}-equipped_armor.json")
