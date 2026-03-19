"""
Ecosystem Simulator - User Interface Module
"""

__author__ = "8636650, Kara, 8658986, Al-Ramessi"

from habitat_final import Habitat
from living_beings_module_final import (Tree, Grass, Eucalyptus,
                                        Apple, Rabbit, Koala, Bear, Wolf)


# --- Initialization Functions ---
def get_int_input(prompt, min_value=None, max_value=None):
    """Prompt user until they provide a valid integer in range."""
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or \
               (max_value is not None and value > max_value):
                print(f"Please enter a number between "
                      f"{min_value} and {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def initialize_habitat():
    """
    initializes habitat, duh"""
    print("Welcome to the Ecosystem Simulator!")
    total_space = get_int_input("Enter total habitat space (e.g., 100): ",
                                10, 1000)
    habitat = Habitat(total_space)

    # --- Add plants ---
    plant_types = [Tree, Grass, Eucalyptus, Apple]

    print("\n[Plant Setup]")
    for PlantClass in plant_types:
        count = get_int_input(f"How many {PlantClass.__name__} shall start? ",
                              0, 50)
        for i in range(count):
            plant = PlantClass(f"{PlantClass.__name__}_{i+1}")
            habitat.add_plant(plant)

    # --- Add animals ---
    # We now use the standard classes directly instead of UI-prefixed wrappers
    animal_types = {
        "Wolves": Wolf,
        "Bears": Bear,
        "Rabbits": Rabbit,
        "Koalas": Koala
    }

    print("\n[Animal Setup]")
    for name, SpeciesClass in animal_types.items():
        count = get_int_input(f"How many {name} to start with? ", 0, 50)
        for i in range(count):
            # Create object with name, e.g., "Wolf_1"
            animal = SpeciesClass(f"{SpeciesClass.__name__}_{i+1}")
            habitat.animals.append(animal)

    return habitat


# --- Display Functions ---
def display_status(habitat):
    """
    desplays the status of habitat
    """
    print("\n--- Habitat Status ---")
    print(f"Round: {habitat.round_counter}, Season: {habitat.season}, "
          f"Used space: {habitat.used_space}/{habitat.total_space}")

    print("\nPlants:")
    for plant in habitat.plants:
        # This now works because get_info is no longer abstract
        print(f"  {plant.get_info()}")

    print("\nAnimals:")
    for animal in habitat.animals:
        # This now works because get_info is no longer abstract
        print(f"  {animal.get_info()}")

    print("\n--- Population Summary ---")

    # Count plants by type
    tree_count = len(
        [p for p in habitat.plants if isinstance(p, Tree) and p.is_alive])
    grass_count = len(
        [p for p in habitat.plants if isinstance(p, Grass) and p.is_alive])
    eucalyptus_count = len(
        [p for p in habitat.plants if isinstance(p, Eucalyptus) and p.is_alive]
        )
    apple_count = len(
        [p for p in habitat.plants if isinstance(p, Apple) and p.is_alive])

    # Count animals by type (Directly using the base classes)
    wolf_count = len(
        [a for a in habitat.animals if isinstance(a, Wolf) and a.is_alive])
    bear_count = len(
        [a for a in habitat.animals if isinstance(a, Bear) and a.is_alive])
    rabbit_count = len(
        [a for a in habitat.animals if isinstance(a, Rabbit) and a.is_alive])
    koala_count = len(
        [a for a in habitat.animals if isinstance(a, Koala) and a.is_alive])

    # Display counts
    print(f"Plants: Trees={tree_count}, Grass={grass_count}, "
          f"Eucalyptus={eucalyptus_count}, Apples={apple_count}")
    print(f"Animals: Wolves={wolf_count}, Bears={bear_count}, "
          f"Rabbits={rabbit_count}, Koalas={koala_count}")
    print(f"Total living beings: {len(habitat.plants)} plants, "
          f"{len(habitat.animals)} animals")

    print("---------------------\n")


# --- Simulation Loop ---
def run_simulation(habitat):
    """
    starts the simulation
    """
    while True:
        choice = input("Options: [R]un round, [M]ultiple rounds, "
                       "[S]tatus, [Q]uit: ").strip().lower()
        if choice == "r":
            habitat.simulate_round()
            display_status(habitat)
        elif choice == "m":
            rounds = get_int_input("How many rounds to simulate? ", 1, 1000)
            for _ in range(rounds):
                habitat.simulate_round()
            display_status(habitat)
        elif choice == "s":
            display_status(habitat)
        elif choice == "q":
            print("Exiting simulation.")
            break
        else:
            print("Invalid option. Please enter R, M, S, or Q.")


def main():
    """
    the code's main method
    """
    habitat = initialize_habitat()
    display_status(habitat)
    run_simulation(habitat)


if __name__ == "__main__":
    main()
