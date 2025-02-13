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


### Installation
1. Clone the repository
    ```bash
    git clone https://github.com/Lukasaurus11/Hypixel-Stuff
    cd hypixel-stuff
    ```

2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the setup script (not yet a thing)
    ```bash
    python setup.py
    ```
   
### Usage
The code is main to be run from ```scripts/main.py```, for now, but eventually there will be examples of how to use the code in the main README.md file. To run any simulations, 
you can simply go read the ```simulators/helper_functions/montecarlo_simulation.py```, as it has examples on how to run all the simulations. No real documentation has been written 
yet for the API related functions, but we will get there eventually.