from typing import Optional, Callable


def scoringFunction(scoringFunc: Optional[Callable[..., float]] = None, **kwargs) -> float:
    """
    Function use to score a MonteCarlo Simulation

    example:
        In the dragon fight case:
        - scoringFunction(scoringFunc=dragonScoringFunction, horn_chance=0.1, claw_chance=0.1,
            item_name='Superior Dragon Helmet', eyes_placed=4, legendary_chance=0.008, epic_chance=0.02, total_weight=100)

    :param scoringFunc: The scoring function to use (default is None)
    :param kwargs: The parameters to pass to the scoring function

    :return: The score of the simulation
    """

    return scoringFunc(**kwargs)


def monteCarloSimulation(trials: int, simulationFunc: Callable[..., dict],
                         scoringFunc: Optional[Callable[..., float]] = None, **kwargs) -> dict:
    """
    Function to run a MonteCarlo Simulation

    example:
        In the dragon fight case:
            - monteCarloSimulation(1000, simulateDragonFight, dragonScoringFunction, magic_find=100, pet_luck=100, eyes_placed=4)
        In the inferno minion case:
            - monteCarloSimulation(1000, simulateInfernoMinion, level=10, nMinion=10, minionExpanders=0, flycatchers=2,
                beaconBuff=0.11, fuelType=2, mithrilInfused=True, eyesDrop=True, postCard=True, freewill=True))
        In the diana burrow simulation case:
            - monteCarloSimulation(1000, simulateChain, isEnderSlayerNine=True)

    :param trials: The number of trials to run
    :param simulationFunc: The simulation function to run
    :param scoringFunc: The scoring function to use (default is None)
    :param kwargs: The parameters to pass to the simulation function

    :return: The results of the simulation
    """
    totalResults: dict = {"iteration_results": {}}

    for i in range(trials):
        result: dict = simulationFunc(**kwargs)

        if scoringFunc:
            score: float = scoringFunction(scoringFunc, **result)
            totalResults["iteration_results"][i] = {"result": result, "score": score}
        else:
            totalResults["iteration_results"][i] = {"result": result}

    keys: dict = totalResults["iteration_results"][0]["result"].keys()
    totalResults["aggregated_results"] = {k: [] for k in keys}

    for i in range(trials):
        for k in keys:
            totalResults["aggregated_results"][k].append(totalResults["iteration_results"][i]["result"][k])

    if scoringFunc:
        totalResults["average_results"] = {
            k: sum(totalResults["iteration_results"][i]["score"] for i in range(trials)) / trials for k in ["score"]
        }

    return totalResults
