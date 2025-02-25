from api import getPlayerProfiles, getUUID
from utils.data_processing.data_processing import searchBestiaryMobs


def main():
    _, lastPlayed = getPlayerProfiles("Lukasaurus_")
    uuid: str = getUUID("Lukasaurus_")
    bestiary: dict = searchBestiaryMobs(lastPlayed, uuid, "earthworm")

    print(bestiary['mob_totals'])


if __name__ == "__main__":
    main()
