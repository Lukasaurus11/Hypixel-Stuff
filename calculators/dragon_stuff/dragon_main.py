from dragon import Dragon
from lootPoolItem import LootPoolItem


def main():
    eyesPlaced = 4
    magicFind = 190
    petLuck = 90

    # All possible items to drop
    dragonHorn: LootPoolItem = LootPoolItem(452, True, 0.3, False)
    dragonHorn.setChance(magicFind, petLuck)

    dragonClaw: LootPoolItem = LootPoolItem(451, True, 0.02, False)
    dragonClaw.setChanceBasedOnEyes(eyesPlaced)
    dragonClaw.setChance(magicFind, petLuck)

    epicEnderDragon: LootPoolItem = LootPoolItem(450, True, 0.0005, True)
    epicEnderDragon.setChanceBasedOnEyes(eyesPlaced)
    epicEnderDragon.setChance(magicFind, petLuck)

    legendaryEnderDragon: LootPoolItem = LootPoolItem(450, True, 0.0001, True)
    legendaryEnderDragon.setChanceBasedOnEyes(eyesPlaced)
    legendaryEnderDragon.setChance(magicFind, petLuck)

    dragonChestplate: LootPoolItem = LootPoolItem(410, True, 0.3, False)
    dragonChestplate.setChance(magicFind, petLuck)

    dragonLeggings: LootPoolItem = LootPoolItem(360, True, 0.3, False)
    dragonLeggings.setChance(magicFind, petLuck)

    dragonHelmet: LootPoolItem = LootPoolItem(295, True, 0.3, False)
    dragonHelmet.setChance(magicFind, petLuck)

    dragonBoots: LootPoolItem = LootPoolItem(290, True, 0.3, False)
    dragonBoots.setChance(magicFind, petLuck)

    dragonFragment: LootPoolItem = LootPoolItem(22, False, 1, False)

    enchantedEnderPearl: LootPoolItem = LootPoolItem(15, False, 1, False)

    enderPearl: LootPoolItem = LootPoolItem(5, False, 1, False)

    superiorLootPool: dict = {
        'Dragon Horn': dragonHorn,
        'Dragon Claw': dragonClaw,
        'Epic Ender Dragon': epicEnderDragon,
        'Legendary Ender Dragon': legendaryEnderDragon,
        'Superior Dragon Chestplate': dragonChestplate,
        'Superior Dragon Leggings': dragonLeggings,
        'Superior Dragon Helmet': dragonHelmet,
        'Superior Dragon Boots': dragonBoots,
        'Superior Dragon Fragment': dragonFragment,
        'Enchanted Ender Pearl': enchantedEnderPearl,
        'Ender Pearl': enderPearl
    }

    superiorDragon: Dragon = Dragon(superiorLootPool, 0.0001)
    superiorDragon.getLootPool()


main()
