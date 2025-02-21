# Hypixel Related-code

Welcome to what started as a simple API project to do with the Hypixel API but slowly turned into a project centered around simulating different aspects around the Hypixel Skyblock game. 
This project is still in development (adding features as I get them requested, or find a need for them) so feel free to ask for anything you might want to see!

## Features
- Hypixel API integration in the `api` folder
- Simulators:
  - Located in the simulators folder
  - Currently, includes:
    - Diana (burrows with and without Eman Slayer 9)
    - Dragon (to find what would be the best combo between pet luck and magic find)
    - Mining (to find the best gemstone to mine for glossy gemstones (🪦 their price))
    - Minion (currently only offering simulating an inferno minion to see what to expect from a day of running it)
- Some functions to see why you are truly not the unluckiest player in this game @CoverlessDev


## Installation
1. Clone the repository
    ```bash
    git clone https://github.com/Lukasaurus11/Hypixel-Stuff
    cd hypixel-stuff
    ```

2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the setup script
    ```bash
    python setup.py
    ```
   
## Usage
The code is meant to be run from ```scripts/main.py``` for now. To run any simulations. Below are examples on how to run the different simulations, and if any doubts about the methodology,
you can check the `simulators/helper_functions/montecarlo_simulation.py` file.

### Simulations:
* Diana:
```python
from simulators import monteCarloSimulation, simulateChain

result: dict = monteCarloSimulation(1000, simulateChain, isEnderSlayerNine=True)
```

* Dragon:
```python
from simulators import monteCarloSimulation, simulateDragonFight, dragonScoringFunction

result: dict = monteCarloSimulation(1000, simulateDragonFight, dragonScoringFunction, magic_find=100, pet_luck=100, eyes_placed=4)
```

* Inferno Minion:
```python
from simulators import monteCarloSimulation, simulateInfernoMinion

result: dict = monteCarloSimulation(1000, simulateInfernoMinion, level=10, nMinion=10, minionExpanders=0, flycatchers=2,
                beaconBuff=0.11, fuelType=2, mithrilInfused=True, eyesDrop=True, postCard=True, freewill=True)
```

* Glossy Gemstone Mining:
```python
from simulators import monteCarloSimulation, simulateMining

result: dict = monteCarloSimulation(1000, simulateMining, gemstone='RUBY', refinedMind=5, miningSpeed=8200)
```

### API:
There aren't a lot of API functions yet, as I add them as I need them. But currently we offer this ones:
* Getting a Minecraft player's UUID (using Mojang's free API):
```python
from api import getUUID

playerUUID: str = getUUID('Lukasaurus_')
```

* Get players profiles:
```python
from api import getPlayerProfiles

summarizedProfileInformation: dict
lastPlayedProfile: dict

summarizedProfileInformation, lastPlayedProfile = getPlayerProfiles('Lukasaurus_')
```

* Get players profile information given a profile name (or the last played profile):
```python
from api import getPlayerProfiles, getProfileInformationByProfileName

summarizedProfileInformation: dict
summarizedProfileInformation, _ = getPlayerProfiles('Lukasaurus_')
profileInformation: dict = getProfileInformationByProfileName(summarizedProfileInformation)    # If no profile name is given, it will return the last played profile
profileInformation: dict = getProfileInformationByProfileName(summarizedProfileInformation, 'Blueberry')   # If a profile name is given, it will return that profile
```

* Get Bazaar Information:
```python
from api import getBazaarInformation

bazaarInformation: dict = getBazaarInformation()    # There's a 10-minute cooldown set to update this file, so 
                                                    # that the API is not overloaded with requests (although it could be lowered substantially)
```

* Get Museum data for a given profile:
```python
from api import getPlayerProfiles, getMuseumData

summarizedProfileInformation: dict
summarizedProfileInformation, _ = getPlayerProfiles('Lukasaurus_')
museumData: dict = getMuseumData(summarizedProfileInformation)    # If no profile name is given, it will return the last played profile
museumData: dict = getMuseumData(summarizedProfileInformation, 'Blueberry')   # If a profile name is given, it will return that profile
```

* Get the status of a player in the Hypixel Network:
```python
from api.hypixel_requests.hypixel_requests import getPlayerStatus

playerStatus: bool = getPlayerStatus('Lukasaurus_')
```

* Get the latest game news from Skyblock:
```python
from api.hypixel_requests.hypixel_requests import getGameNews

getGameNews()   # This function does not return anything, but saves the latest game news
```

### Other relevant functions:
There are 2 main functions to decode encoded data retrieved from the API, for example the inventory_data or ender_chest. There is a special function for the wardrobe, so that information is returned in an organized way
```python
from api import getPlayerProfiles, getUUID
from utils.data_processing import extractJSONFields, decodeData, decodeWardrobe

player: str = 'Lukasaurus_'
lastPlayedProfile: dict
_, lastPlayedProfile = getPlayerProfiles(player)
playerUUID: str = getUUID(player)

references: dict = extractJSONFields(lastPlayedProfile, playerUUID)

inventoryData: dict = decodeData(references['inventory'])
enderChestData: dict = decodeData(references['ender_chest'])

wardrobeData: dict = decodeWardrobe(references['wardrobe'], references['equipped_wardrobe_slot'], references['equipped_armor'])
```

## Contributing
If you want to contribute to this project, or want a feature to be added feel free to reach out on discord, or in game and we can discuss it further. In general I'm open to any suggestions, so don't worry about it.