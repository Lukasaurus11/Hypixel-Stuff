# Hypixel Related-code

Welcome to what started as a simple API project to do with the Hypixel API but slowly turned into a project centered around simulating different aspects around the Hypixel Skyblock game. 
This project is still in development (adding features as I get them requested, or find a need for them) so feel free to ask for anything you might want to see!

## Features
- Hypixel API integration (code located inside the ```utils``` folder)
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
The code is main to be run from ```scripts/main.py``` for now. To run any simulations. Below are examples on how to run the different simulations, and if any doubts about the methodology,
you can check the `simulators/helper_functions/montecarlo_simulation.py` file. No real documentation has been written yet for the API related functions, but I will get there eventually.

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
TBA

## Contributing
If you want to contribute to this project, or want a feature to be added feel free to reach out on discord, or in game and we can discuss it further. In general I'm open to any suggestions, so don't worry about it.