"""
Ecosystem Simulator - Habitat Module

This module contains the Habitat class, which manages the entire
ecosystem and executes the simulation steps.
"""

__author__ = "8636650, Kara, 8658986, Al-Ramessi"

import random
# Importing the living beings from your first module
# to check docstrings
from living_beings_module_final import Bear, Apple, Grass, Rabbit, Wolf


class Habitat:
    """
    The habitat for the ecosystem.
    """

    def __init__(self, total_space=200):
        """
        Initializes the habitat with a maximum capacity.

        >>> h = Habitat(100)
        >>> h.total_space
        100
        >>> h.used_space
        0
        >>> len(h.plants)
        0
        """
        self.total_space = total_space  # Max capacity for ground-based plants
        self.used_space = 0             # Currently occupied space
        self.plants = []                # List to store all plant objects
        self.animals = []               # List to store all animal objects
        self.round_counter = 0          # Round tracker
        self.season = "Spring"          # Starting season
        self.weather_factor = 1.0       # Influences growth (standard: 1.0)

    def add_plant(self, plant):
        """
        Adds a plant if space is available.

        >>> h = Habitat(10)
        >>> g = Grass("G1")
        >>> h.add_plant(g) # Test 1: Successful add
        True
        >>> h.used_space
        3
        >>> h.add_plant(Grass("G2")) # Test 2: Adding more
        True
        >>> h.add_plant(Grass("G3")) # Test 3: Succeed (space: 3+3+3+3 > 10)
        True
        """
        # Logic: Does the plant occupy ground space? (e.g., Grass/Trees)
        if plant.needs_ground:
            # Check if there is enough space left in the habitat
            if self.used_space + plant.space_needed <= self.total_space:
                self.plants.append(plant)
                self.used_space += plant.space_needed  # Occupy space
                return True
            return False

    def remove_plant(self, plant):
        """
        Removes a plant and updates used space.


        >>> h = Habitat(100)
        >>> g = Grass("G1")
        >>> h.add_plant(g)
        True
        >>> h.remove_plant(g) # Test 1: Successful removal
        >>> len(h.plants)
        0
        >>> h.used_space # Test 2: Space is freed
        0
        >>> h.remove_plant(g) # Test 3: Removing non-existent (safe)
        """
        if plant in self.plants:
            self.plants.remove(plant)
            # If it was a ground plant, free up the space
            if plant.needs_ground:
                self.used_space -= plant.space_needed

    def add_animal(self, animal):
        """
        Adds an animal to the habitat.

        >>> h = Habitat()
        >>> r = Rabbit("TestRabbit")
        >>> h.add_animal(r)  # Test 1: Add first animal
        >>> len(h.animals)
        1
        >>> w = Wolf("TestWolf")
        >>> h.add_animal(w)  # Test 2: Add second animal
        >>> len(h.animals)
        2
        >>> b = Bear("TestBear")
        >>> h.add_animal(b)  # Test 3: Add third animal
        >>> len(h.animals)
        3
        """
        self.animals.append(animal)

    def remove_animal(self, animal):
        """
        Removes an animal from the habitat list.

        >>> h = Habitat()
        >>> r = Rabbit("Bugs")
        >>> h.animals.append(r)
        >>> len(h.animals)
        1
        >>> h.remove_animal(r) # Test 1: Successful removal
        >>> len(h.animals)
        0
        >>> h.remove_animal(r) # Test 2: Removing non-existent (should stay 0)
        >>> len(h.animals)
        0
        """

        if animal in self.animals:
            self.animals.remove(animal)

    def change_season(self):
        """
        Rotates seasons every 10 rounds.

        >>> h = Habitat()
        >>> h.round_counter = 10
        >>> h.change_season() # Test 1: Switches to Summer
        >>> h.season
        'Summer'
        >>> h.round_counter = 20
        >>> h.change_season() # Test 2: Switches to Autumn
        >>> h.season
        'Autumn'
        >>> h.weather_factor # Test 3: Factor updated
        0.9
        """
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        # Modulo check: Every 10 rounds, move to the next season
        if self.round_counter > 0 and self.round_counter % 10 == 0:
            current_idx = seasons.index(self.season)
            self.season = seasons[(current_idx + 1) % 4]

            # SPECIAL RULE: Weather influence on plant growth
            factors = {"Spring": 1.1, "Summer": 1.3,
                       "Autumn": 0.9, "Winter": 0.6}
            self.weather_factor = factors[self.season]

    def check_space_competition(self):
        """
        SPECIAL RULE: Smallest plants die if habitat is over 90% full.
        Naturtural selection due to space competition.

        >>> h = Habitat(10)
        >>> h.add_plant(Grass("G1"))
        True
        >>> h.add_plant(Grass("G2"))
        True
        >>> h.add_plant(Grass("G3")) # Total 9 space (90%)
        True
        >>> h.check_space_competition() # Test 1: Safe
        >>> len(h.plants)
        3
        >>> h.total_space = 9 # Now 9 is 100% capacity
        >>> h.check_space_competition() # Test 2: Competition starts
        >>> len(h.plants) < 3
        True
        >>> h.used_space < 9 # Test 3: Space freed
        True
        """
        # If more than 90% of the space is occupied
        if self.used_space > self.total_space * 0.9:
            ground_plants = [p for p in self.plants if p.needs_ground]
            if ground_plants:
                # Sort by size: The smallest/weakest die first
                ground_plants.sort(key=lambda p: p.current_size)
                # Remove 10% of the plant population
                num_to_remove = max(1, len(ground_plants) // 10)
                for i in range(num_to_remove):
                    plant = ground_plants[i]
                    plant.die()
                    self.remove_plant(plant)

    def simulate_round(self):
        """
        The core loop of the simulation. Executes one round of growth,
        eating, reproduction, and death for all plants and animals.

        >>> h = Habitat(100)
        >>> r = Rabbit("Shorty")
        >>> h.add_animal(r)
        >>> # Force the rabbit to be near death
        >>> r.hunger = 5.9
        >>> r.max_hunger = 6.0
        >>>
        >>> # After one round, metabolic rate (1.0) is added
        >>> h.simulate_round()
        >>>
        >>> # The rabbit should have died and been removed
        >>> len(h.animals)
        1
        """
        # Increment round and update environment
        self.round_counter += 1
        self.change_season()
        self.check_space_competition()

        # PHASE 1: PLANTS
        # Count current Grass for special reproduction rule
        grass_count = len([p for p in self.plants if isinstance(p, Grass)])

        # We use [:] to iterate over a copy so we can safely remove dead plants
        for plant in self.plants[:]:
            # Capture return value:
            # Can be actual_growth (int), an Apple object, or None
            result = plant.grow(self.weather_factor)

            if not plant.is_alive:
                self.remove_plant(plant)
                continue

            # Check if a Tree produced an Apple
            if isinstance(result, Apple):
                self.add_plant(result)

            # Reproduction Check
            repro_chance = 0.2

            if isinstance(plant, Grass):
                # SPECIAL RULE: Grass reproduction depends on current count
                # Emergency measure to prevent grass extinction
                if grass_count < 5:
                    repro_chance = 1.0  # Higher chance if few grasses
                elif grass_count < 10:
                    repro_chance = 0.8  # Lower chance if many grasses

            if plant.can_reproduce(self) and random.random() < repro_chance:
                # Check space before adding offspring
                if (self.used_space + plant.space_needed
                        <= self.total_space):
                    offspring = type(plant)(f"{plant.name}_child")
                    self.add_plant(offspring)

        # PHASE 2: ANIMALS
        for animal in self.animals[:]:
            if animal.is_alive:
                # SPECIAL RULE: Bear hibernation check
                if isinstance(animal, Bear):
                    animal.prepare_hibernation(self.season)

                # Animal ages/grows
                animal.grow()

                if animal.age > animal.max_age:
                    print(f"{animal.name} died of old age.")
                    animal.is_alive = False
                else:
                    animal.eat(self)  # Animal searches for food

                # Reproduction check
                if animal.is_alive and animal.can_reproduce():
                    offspring = type(animal)(f"{animal.name}_baby")
                    self.animals.append(offspring)

                # Check for starvation
                if animal.check_starvation(self):
                    if animal in self.animals:
                        self.animals.remove(animal)
            else:
                # Remove animals that were killed (e.g. eaten or natural death)
                if animal in self.animals:
                    self.animals.remove(animal)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()

    if results.failed == 0:
        print(f"Success! All {results.attempted} tests passed.")
    else:
        print(f"Oops! {results.failed} tests failed.")
