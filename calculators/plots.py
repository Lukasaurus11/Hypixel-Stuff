import matplotlib.pyplot as plt


def plotDistribution(probFunction, eventChance, pointsX, pointsY, plotLabel):
    """
    Plot the cumulative distribution function for the geometric distribution with the given parameters.
    :return: Nothing
    """
    maxX = max(pointsX)
    x = range(1, maxX + 1)
    y = [probFunction(eventChance, i) for i in x]

    plt.plot(x, y)
    plt.xlabel("Number of Trials")
    plt.ylabel("Cumulative Probability")
    plt.title(plotLabel)

    # Plot the points for the trials that we are interested in, and their corresponding trial number | probabilities
    plt.scatter(pointsX, pointsY, color='red')

    # Rightmost x value (furthest point inside the graph)
    max_x = max(x)

    for i, txt in enumerate(pointsY):
        textToAnnotation = f"{pointsX[i]:,} | {txt:.4f}"
        # Annotate at the furthest right x (max_x) but keep the same y (pointsY[i])
        plt.annotate(textToAnnotation,
                     (max_x, pointsY[i]), textcoords="offset points", xytext=(-10, 0),
                     ha='right')  # Align to the right of max_x

    plt.show()


def plotGroupScenarioDistribution(probFunction, pointsX, additivePointsX, pointsY, plotLabel, argumentsList):
    """
    Plot the cumulative distribution function for the group scenario with the given parameters.
    :return: Nothing
    """
    argumentDict = {
        'spawnChance': argumentsList[0],
        'probSinglePlayer': argumentsList[1],
        'lootshareProb': argumentsList[2],
        'trials': argumentsList[3],
        'totalTrials': argumentsList[4]
    }

    maxX = max(pointsX)
    x = range(1, maxX + 1)

    # Unfinished for now
    y = [probFunction(argumentDict['spawnChance'], argumentDict['probSinglePlayer'], argumentDict['lootshareProb'],
                      i, i * 6) for i in x]

    plt.plot(x, y)
    plt.xlabel("Number of Trials")
    plt.ylabel("Cumulative Probability")
    plt.title(plotLabel)

    # Plot the points for the trials that we are interested in, and their corresponding trial number | probabilities
    plt.scatter(pointsX, pointsY, color='red')

    # Rightmost x value (furthest point inside the graph)
    max_x = max(x)

    for i, txt in enumerate(pointsY):
        textToAnnotation = f"{pointsX[i]:,} ({additivePointsX[i]:,}) | {txt:.4f}"
        # Annotate at the furthest right x (max_x) but keep the same y (pointsY[i])
        plt.annotate(textToAnnotation,
                     (max_x, pointsY[i]), textcoords="offset points", xytext=(-10, 0),
                     ha='right')  # Align to the right of max_x

    plt.show()
