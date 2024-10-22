class Dragon:
    def __init__(self, lootPool: dict, spawnChance: float) -> None:
        self.lootPool = lootPool
        self.spawnChance = spawnChance

    def getLootPool(self) -> dict:
        for key, val in self.lootPool.items():
            print(f'{key}: {val.getQuality()} {val.getChance()} {val.isUnique()}')
        return self.lootPool

    def getSpawnChance(self) -> float:
        return self.spawnChance
