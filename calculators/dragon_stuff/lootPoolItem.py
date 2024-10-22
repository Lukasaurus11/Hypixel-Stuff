from calculators.calculator_helper_functions import (calculateMagicFindBoostedDropChanceWithPetLuck,
                                                     calculateMagicFindBoostedDropChance)


class LootPoolItem:
    def __init__(self, quality: int, unique: bool, chance: float, pet: bool) -> None:
        self.quality = quality
        self.unique = unique
        self.chance = chance
        self.pet = pet

    def setChanceBasedOnEyes(self, eyes: int) -> None:
        self.chance = self.chance * eyes

    def setChance(self, magicFind: float, petLuck: float) -> None:
        if self.pet:
            self.chance = calculateMagicFindBoostedDropChanceWithPetLuck(self.chance, magicFind, petLuck)
        else:
            self.chance = calculateMagicFindBoostedDropChance(self.chance, magicFind)

    def getQuality(self) -> int:
        return self.quality

    def getChance(self) -> float:
        return self.chance

    def isUnique(self) -> bool:
        return self.unique
