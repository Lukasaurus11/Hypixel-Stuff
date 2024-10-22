import numpy as np
import matplotlib.pyplot as plt

# Define your items with their base drop chances and unique status
items = [
    {"name": "Dragon Horn", "baseChance": 0.3, "unique": True},
    {"name": "Dragon Claw", "baseChance": 0.08, "unique": True},
    {"name": "Epic Ender Dragon", "baseChance": 0.002, "unique": True},
    {"name": "Legendary Ender Dragon", "baseChance": 0.0004, "unique": True},
]

# Define your theoretical max values
MAX_MAGIC_FIND = 500  # Example: Set a maximum magic find value you want to test up to
MAX_PET_LUCK = 100  # The maximum pet luck you can achieve


# Function to calculate boosted drop chance (only magic find boost for non-dragon items)
def calculate_magic_find_boosted_chance(baseChance, magicFind):
    return baseChance * (1 + magicFind / 100)


# Function to calculate boosted drop chance (magic find + pet luck for dragon items)
def calculate_magic_find_and_pet_luck_boosted_chance(baseChance, magicFind, petLuck):
    return baseChance * (1 + (magicFind + petLuck) / 100)


# Score function to balance maximizing dragons and minimizing horn/claw
def calculate_score(legendary_chance, epic_chance, horn_chance, claw_chance, horn_weight=10, claw_weight=5):
    # Maximize dragons, minimize horns/claws (weighted heavily)
    return (legendary_chance + epic_chance) - (horn_weight * horn_chance + claw_weight * claw_chance)


# Function to run the simulation and calculate drop chances
def simulate_drop_chances(magicFind_range, petLuck_range):
    best_combination = {"magicFind": 0, "petLuck": 0, "score": float("-inf")}
    best_scores = []

    for magicFind in magicFind_range:
        for petLuck in petLuck_range:
            # Calculate the boosted drop chance for each item
            horn_chance = calculate_magic_find_boosted_chance(items[0]["baseChance"], magicFind)
            claw_chance = calculate_magic_find_boosted_chance(items[1]["baseChance"], magicFind)
            legendary_dragon_chance = calculate_magic_find_and_pet_luck_boosted_chance(items[3]["baseChance"],
                                                                                       magicFind, petLuck)
            epic_dragon_chance = calculate_magic_find_and_pet_luck_boosted_chance(items[2]["baseChance"], magicFind,
                                                                                  petLuck)

            # Calculate the score based on the tradeoff
            score = calculate_score(legendary_dragon_chance, epic_dragon_chance, horn_chance, claw_chance)

            # Track the best combination based on the score
            if score > best_combination["score"]:
                best_combination = {
                    "magicFind": magicFind,
                    "petLuck": petLuck,
                    "score": score,
                    "Legendary Ender Dragon": legendary_dragon_chance,
                    "Epic Ender Dragon": epic_dragon_chance,
                    "Dragon Horn": horn_chance,
                    "Dragon Claw": claw_chance,
                }
            best_scores.append(score)

    return best_combination, best_scores


# Generate magicFind and petLuck values to test
magicFind_range = np.linspace(10, MAX_MAGIC_FIND, 50)  # Magic find from 0 to MAX_MAGIC_FIND
petLuck_range = np.linspace(1, MAX_PET_LUCK, 50)  # Pet luck from 0 to MAX_PET_LUCK

# Run the simulation
best_combination, best_scores = simulate_drop_chances(magicFind_range, petLuck_range)

print(best_scores)

# Print the best combination (balanced for maximizing dragons and minimizing horn/claw)
print(f"Best combination:\nMagic Find = {best_combination['magicFind']}, Pet Luck = {best_combination['petLuck']}\n"
      f"Legendary Ender Dragon Drop Chance = {best_combination['Legendary Ender Dragon']}\n"
      f"Epic Ender Dragon Drop Chance = {best_combination['Epic Ender Dragon']}\n"
      f"Dragon Horn Drop Chance = {best_combination['Dragon Horn']}\n"
      f"Dragon Claw Drop Chance = {best_combination['Dragon Claw']}\n"
      f"Score = {best_combination['score']}")

# Plot the score as a function of magicFind and petLuck
plt.figure(figsize=(8, 6))
plt.plot(np.linspace(0, len(best_scores), len(best_scores)), best_scores, label="Score")
plt.title("Score (Maximizing Dragons and Minimizing Horn/Claw)")
plt.xlabel("Simulation Iterations")
plt.ylabel("Score")
plt.legend()
plt.show()
