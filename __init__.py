__version__ = "0.1.0"
__author__ = "Lukasaurus11"
__description__ = "A small project designed around Hypixel Skyblock"

from .simulators import (monteCarloSimulation, simulateChain, dragonScoringFunction, simulateDragonFight,
                         simulateInfernoMinion, simulateMining)

__all__ = ['monteCarloSimulation', 'simulateChain', 'dragonScoringFunction', 'simulateDragonFight',
           'simulateInfernoMinion', 'simulateMining']