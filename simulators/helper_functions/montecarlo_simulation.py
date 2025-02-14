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
                beaconBuff=0.11, fuelType=2, mithrilInfused=True, eyesDrop=True, postCard=True, freewill=True)
        In the diana burrow simulation case:
            - monteCarloSimulation(1000, simulateChain, isEnderSlayerNine=True)
        In the glossy simulation case:
            - monteCarloSimulation(1000, simulateMining, gemstone='RUBY', refinedMind=5, miningSpeed=8200)

    :param trials: The number of trials to run
    :param simulationFunc: The simulation function to run
    :param scoringFunc: The scoring function to use (default is None)
    :param kwargs: The parameters to pass to the simulation function

    :return: The results of the simulation
    """
    totalResults: dict = {"iteration_results": {}, "aggregated_results": {}, "average_results": {}}

    for i in range(trials):
        result: dict = simulationFunc(**kwargs)
        score: float = scoringFunction(scoringFunc, **result) if scoringFunc else None
        totalResults["iteration_results"][i] = {"result": result, "score": score}

    def aggregateAndAverageResults(results: list) -> tuple[dict, dict]:
        """
        Function to aggregate and average the results of a MonteCarlo Simulation
        :param results: The results to process
        :return: The aggregation and average results
        """
        aggregatedResults: dict = {}
        for res in results:
            for key, value in res.items():
                if isinstance(value, dict):
                    aggregatedResults.setdefault(key, {})
                    for sub_key, sub_value in value.items():
                        aggregatedResults[key].setdefault(sub_key, []).append(sub_value)
                else:
                    aggregatedResults.setdefault(key, []).append(value)

        averagedResults: dict = {}
        for key, values in aggregatedResults.items():
            if isinstance(values, dict):
                averagedResults[key] = {sub_key: sum(sub_values) / len(sub_values) for sub_key, sub_values in values.items()}
            elif all(isinstance(v, (int, float)) for v in values):
                averagedResults[key] = sum(values) / len(values)

        return aggregatedResults, averagedResults

    iterationResults: list = [
        {**res["result"], "score": res["score"]} if res["score"] is not None else res["result"]
        for res in totalResults["iteration_results"].values()
    ]

    aggregated: dict
    averages: dict
    aggregated, averages = aggregateAndAverageResults(iterationResults)

    totalResults["aggregated_results"] = aggregated
    totalResults["average_results"] = averages

    return totalResults
