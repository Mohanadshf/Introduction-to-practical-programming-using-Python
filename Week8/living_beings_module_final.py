"""
Ecosystem Simulator - Living Beings Module

This module contains the hierarchy for all entities in the simulation:
LivingBeing (Base), Plant, and Animal with all their specialized subclasses.
"""

__author__ = "8636650, Kara, 8658986, Al-Ramessi"

import random
from abc import ABC, abstractmethod


class LivingBeing(ABC):
    """
    Abstract base class for every entity in the ecosystem.

    The purpose of this class is to provide a unified interface
    for all living objects. Methods such as 'grow' and 'get_info'
    are defined as abstract because plants and animals differ
    fundamentally in their growth and reporting logic.

    Using an abstract base class enforces specific implementations
    in subclasses and prevents the instantiation of generic,
    non-functional 'LivingBeing' objects.

    >>> # This test proves that you cannot create a generic LivingBeing:
    >>> try:
    ...     lb = LivingBeing("Mystery")
    ... except TypeError:
    ...     print("Caught expected error: Cannot instantiate ABC")
    Caught expected error: Cannot instantiate ABC
    """

    def __init__(self, name):
        """
        initializes living being
        """
        # Basic attributes shared by plants and animals
        self.name = name
        self.age = 0
        self.is_alive = True

    @abstractmethod
    def grow(self):
        """Must be implemented by subclasses to handle aging/growth."""
        pass

    def die(self):
        """Sets the status to dead. Dead objects are removed by the Habitat."""
        self.is_alive = False

    # @abstractmethod , stopped using it because it made the docstrings crash
    # it is only a saftey net so the code is the same
    def get_info(self):
        """Returns a string representation of the object's status."""
        pass


class Plant(LivingBeing):
    """
    Base class for all vegetation.

    >>> p = Plant("TestPlant", min_size=5, max_size=20, growth_rate=2)
    >>> p.current_size
    5
    >>> p.be_eaten(2) # because size is smaller that min_size
    False
    >>> p.current_size
    3
    >>> p.be_eaten(5)
    False
    >>> p.is_alive
    False

    """

    def __init__(self, name, min_size, max_size, growth_rate=2,
                 space_needed=5, needs_ground=True, reproduction_interval=5):
        """
        initializes the Plant
        """
        super().__init__(name)
        self.min_size = min_size
        self.max_size = max_size
        self.current_size = min_size
        self.growth_rate = growth_rate
        self.space_needed = space_needed  # Used for habitat capacity logic
        # Distinguishes ground plants from epiphytes
        self.needs_ground = needs_ground
        self.reproduction_interval = reproduction_interval
        self.rounds_since_reproduction = 0
        self.max_age = 50  # Default lifespan for plants

    def grow(self, weather_factor=1.0):
        """
        Increases size based on growth rate and environmental factors.
        """
        if not self.is_alive:
            return 0

        # RANDOMIZED ASPECT:
        # Growth varies slightly every round (0.7 to 1.3 multiplier)
        growth = int(self.growth_rate * weather_factor *
                     random.uniform(0.7, 1.3))

        # Ensure the plant doesn't exceed its maximum natural size
        new_size = min(self.current_size + growth, self.max_size)
        actual_growth = new_size - self.current_size
        self.current_size = new_size
        self.age += 1  # Plants age every time they grow

        if self.age > self.max_age:
            self.is_alive = False
            print(f"{self.name} has withered away due to old age.")
        return actual_growth

    def be_eaten(self, amount):
        """
        Reduces size when an animal grazes on the plant.
        If size drops below minimum, the plant dies.
        """
        self.current_size -= amount
        if self.current_size < self.min_size:
            self.die()
            return False  # Plant died
        return True  # Plant survived

    def can_reproduce(self, habitat=None):
        """
        Logic for plant spreading. Requires enough size and a cooldown period.
        The 'habitat' parameter is optional for the base class.
        """
        # Cooldown check to prevent exponential overgrowth
        if self.rounds_since_reproduction < self.reproduction_interval:
            self.rounds_since_reproduction += 1
            return False

        # Plant must be mature (80% of max size) to reproduce
        can_repro = (self.current_size >= self.max_size * 0.8 and self.age > 3)

        if can_repro:
            self.rounds_since_reproduction = 0  # Reset cooldown

        return can_repro

    def get_info(self):
        """
        gets the plats's info
        """
        status = "alive" if self.is_alive else "dead"
        return (f"{self.name} (Plant): Size {self.current_size}/"
                f"{self.max_size}, Age {self.age}, {status}")


# --- Specialized Plant Classes ---

class Tree(Plant):
    """
    Trees grow large and slowly.
    SPECIAL RULE: They provide Apples for Rabbits and Bears.

    >>> # Testing initialization
    >>> t = Tree("Appletree_1")
    >>> t.current_size
    10
    >>> t.space_needed # Trees occupy ground space based on size
    15
    >>> # Test reproduction check (cooldown is 5 rounds)
    >>> t.can_reproduce()
    False
    """

    def __init__(self, name):
        """
        initializes the Tree as plant
        """
        super().__init__(name, min_size=10, max_size=100,
                         growth_rate=1, space_needed=15, needs_ground=True,
                         reproduction_interval=10)

    def grow(self, weather_factor=1.0):
        """
        grows the tree
        """
        super().grow(weather_factor)

        if self.age % 2 == 0:
            # drop an apple every 2 rounds
            return Apple(f"Apple from {self.name}")
        return None

    def can_reproduce(self, habitat=None):
        """
        checks if the tree can reproduce
        """
        return super().can_reproduce(habitat)


class Grass(Plant):
    """
    Grass grows fast but stays small.
    SPECIAL RULE: High drought resistance helps it survive bad weather.

    >>> # Testing initialization and space usage
    >>> g = Grass("Meadow_1")
    >>> g.current_size
    2
    >>> g.space_needed
    3
    >>> # Test growth with weather factor 1.0
    >>> # Growth rate for Grass is 4
    >>> # since the grow method in the father class is
    >>> # randomized we couldn't write a suitable docstring for it
    """

    def __init__(self, name):
        """
        initializes Grass as plant
        """
        super().__init__(name, min_size=2, max_size=10,
                         growth_rate=4, space_needed=3, needs_ground=True,
                         reproduction_interval=3)
        self.drought_resistance = random.randint(3, 7)

    def grow(self, weather_factor=1.0):
        """
        grows the grass
        """
        # Grass compensates for bad weather using its resistance trait
        if weather_factor < 0.6:
            weather_factor += self.drought_resistance * 0.05
        return super().grow(weather_factor)

    def can_reproduce(self, habitat):
        """
        SPECIAL RULE: Emergency Regrowth.
        If grass is nearly extinct, it reproduces much faster.
        Even if it hasn't reached maturity.
        This prevents a mass extinction of grass and stabilizes the ecosystem.
        """
        # count current living grass plants in the habitat
        grass_count = len([p for p in habitat.plants
                           if isinstance(p, Grass) and p.is_alive])

        # If there are fewer than 5 grass plants, allow immediate reproduction
        if grass_count < 5:
            return True  # Emergency regrowth

        # Otherwise, use standard reproduction logic
        return super().can_reproduce()


class Eucalyptus(Plant):
    """
    SPECIAL RULE: Toxic to most, only Koalas can eat this.

    >>> # Testing initialization and growth
    >>> e = Eucalyptus("Euca_1")
    >>> e.current_size
    8
    >>> e.space_needed
    12
    >>> e.be_eaten(5) # Koala eats 5 units
    False
    >>> e.current_size
    3
    """

    def __init__(self, name):
        """
        initializes eucalyptus attributes
        """
        super().__init__(name, min_size=8, max_size=60,
                         growth_rate=2, space_needed=12, needs_ground=True,
                         reproduction_interval=7)


class Apple(Plant):
    """
    Represents a fruit dropped by a Tree.
    Does not grow or reproduce,
    but serves as a temporary food source on the ground.

    >>> a = Apple()
    >>> a.current_size
    5
    >>> a.space_needed
    0
    >>> a.age
    0
    """

    def __init__(self, name="Apple"):
        """
        initializes Apple as plant
        """
        # growth_rate=0: Apples do not increase in size once fallen
        # space_needed=0: Essential so that fruit doesn't block tree growth
        # reproduction_interval=999: Apples cannot create more apples
        super().__init__(name, min_size=1, max_size=5, growth_rate=0,
                         space_needed=0, needs_ground=True,
                         reproduction_interval=999)
        self.current_size = 5
        self.max_age = 3  # Lifespan in rounds before the apple rots

    def grow(self, weather_factor=1.0):
        """
        Overrides the growth method to implement a decay mechanism.
        The apple stays at a fixed size but dies after its max_age is reached.
        """
        if not self.is_alive:
            return 0

        self.age += 1

        # Natural decay logic: if not eaten, it disappears after 3 rounds
        if self.age > self.max_age:
            self.die()

        return 0  # No physical growth added to the habitat


# --- Animal Logic ---

class Animal(LivingBeing):
    """
    Abstract base class for all mobile creatures.
    >>> a = Rabbit("TestBunny")
    >>> a.hunger # Startet satt
    0
    >>> a.metabolic_rate # Intervall 1 -> 1.0 Hunger pro Runde
    1.0
    >>> a.grow()
    >>> a.hunger
    1.0
    """

    def __init__(self, name, max_hunger=10, strength=5, feeding_interval=1):
        """
        initializes Animal as Livingbeing
        """
        super().__init__(name)
        self.hunger = 0
        self.max_hunger = max_hunger  # Death occurs if hunger reaches this
        self.strength = strength     # Used for hunting success or defense
        self.hibernating = False
        self.feeding_interval = feeding_interval    # Rounds between meals
        self.rounds_since_eating = 0
        self.max_age = 50  # Default lifespan for animals

        # LOGIC: Instead of fixed hunger values, we calculate a rate.
        # This eliminates 'Magic Numbers' and makes the simulation scalable.
        # Interval 1 (small animals) = 1.0 hunger/round
        # Interval 2 (medium animals) = 0.5 hunger/round
        # Interval 3 (large animals) = 0.33 hunger/round
        self.metabolic_rate = 1.0 / self.feeding_interval

        # Logic: Named constant for metabolic energy saved during hibernation.
        # This makes it easy to adjust the survival bonus in one central place.
        self.hibernation_bonus = 2

        # Reproduction attributes
        self.repro_cooldown = 0        # Current timer (starts at 0)
        self.cooldown_duration = 5     # Rounds to wait after having a baby
        self.min_repro_age = 4         # Age needed to be mature enough
        self.hunger_threshold = 5      # Maximum hunger allowed to reproduce

    @abstractmethod
    def eat(self, habitat):
        """Each animal type has a different way of finding food."""
        pass

    def check_starvation(self, habitat):
        """
        Kills the animal if it hasn't eaten enough.
        Animals are protected from death by starvation, if there are only
        3 or fewer of their species remaining in the habitat.
        This was implemented to prevent extinction.
        """
        # Count living animals of the same species in the habitat
        species_count = len([a for a in habitat.animals
                             if isinstance(a, type(self)) and a.is_alive])

        # if only 3 or fewer of the species remain, they are protected
        # to help maintain biodiversity in the habitat and prevent extinction
        if species_count <= 3:
            return False
        if self.hunger >= self.max_hunger:
            self.die()
            return True

        return False

    def enter_hibernation(self):
        """
        controls the hibernaiton of Animals
        """
        self.hibernating = True
        # Logic: Reduce hunger by the defined bonus
        # to simulate slower metabolism
        self.hunger = max(0, self.hunger - self.hibernation_bonus)

    def wake_up(self):
        """Wakes the animal from hibernation."""
        self.hibernating = False

    def grow(self):
        """
        Increments age and calculates hunger increase based on metabolism.
        """
        self.age += 1
        if not self.hibernating:
            # Logic: We use the precalculated rate dependend on size/interval.
            # This ensure consistent hunger growth.
            self.hunger += self.metabolic_rate
            self.rounds_since_eating += 1

    def can_reproduce(self):
        """Standard reproduction logic for all animals."""
        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1
            return False

        is_ready = (
            self.age > self.min_repro_age and
            self.hunger < self.hunger_threshold
        )

        if is_ready:
            self.repro_cooldown = self.cooldown_duration
            return True
        return False

    def check_aging(self, habitat):
        """
        Checks if the animal has exceeded its maximum age.
        Animals are protected from death, if there are only 3 or fewer
        of their species remaining in the habitat.
        This was implemented to prevent extinction.
        """
        species_count = len([a for a in habitat.animals
                             if isinstance(a, type(self)) and a.is_alive])

    # If only 3 or fewer of the species remain, they are protected from death
    # To help maintain biodiversity in the habitat and prevent extinction
        if species_count <= 3:
            return False

        if self.age > self.max_age:
            self.is_alive = False
            return True  # Died of old age
        return False

    def get_info(self):
        """Returns a detailed string about the animal's current state."""
        status = "alive" if self.is_alive else "dead"
        hibernate_str = ", Hibernating" if self.hibernating else ""

        # We use self.__class__.__name__
        # to get "Wolf", "Bear", etc. automatically
        return (f"{self.name} ({self.__class__.__name__}): "
                f"Age {self.age}, Hunger {self.hunger:.1f}/{self.max_hunger}, "
                f"{status}{hibernate_str}")


class Herbivore(Animal):
    """
    Eats plants. Found in the habitat's plant list.

    >>> # Testing the basic attributes of a Herbivore using a Rabbit
    >>> h = Rabbit("Thumper")
    >>> h.strength
    2
    >>> # Most small herbivores have a feeding_interval of 1
    >>> h.metabolic_rate
    1.0
    >>> h.hunger
    0
    >>> h.grow()
    >>> h.hunger
    1.0
    """

    def eat(self, habitat):
        """
        controls the feeding of herbivores
        """
        # We store conditions in descriptive variables for better readability
        is_unable_to_eat = self.hibernating
        is_still_full = self.rounds_since_eating < self.feeding_interval

        # Early Exit: If the animal is asleep or not hungry yet, we stop here
        if is_unable_to_eat or is_still_full:
            return False

        # Search for any edible plant in the environment
        # 'p' is our placeholder for each plant in the list
        edible_plants = [p for p in habitat.plants
                         if p.is_alive and not isinstance(p, Tree)]
        if edible_plants:
            plant = random.choice(edible_plants)
            eat_amount = random.randint(1, 4)
            # Try to eat the plant
            if plant.be_eaten(eat_amount):
                self.hunger = max(0, self.hunger - eat_amount)
                self.rounds_since_eating = 0
                return True
            else:
                # Plant died from overgrazing, remove it
                habitat.remove_plant(plant)
                self.hunger = max(0, self.hunger - eat_amount)
                self.rounds_since_eating = 0
                return True
        return False


class Carnivore(Animal):
    """
    Hunting logic for carnivores.
    Protects own species but allows hunting of weaker animals.

    >>> # Testing the basic attributes of a Carnivore
    >>> c = Wolf("Isegrim")
    >>> c.strength
    10
    >>> # Carnivores typically have a feeding_interval of 2
    >>> c.metabolic_rate
    0.5
    >>> c.hunger
    0
    >>> c.grow()
    >>> c.hunger
    0.5
    """

    def __init__(self, name, max_hunger=12, strength=8, feeding_interval=2):
        """
        initializes carnivores special attributes
        """
        super().__init__(name, max_hunger, strength, feeding_interval)
        self.hunt_skill = random.randint(5, 10)  # Individual hunting ability
        self.meat_reward = 10  # Hunger reduction per successful hunt

    def eat(self, habitat):
        """
        controls carnivores feeding
        """
        is_sleeping = self.hibernating
        is_not_hungry_yet = self.rounds_since_eating < self.feeding_interval

        # If the carnivore is asleep or still full, it won't hunt
        if is_sleeping or is_not_hungry_yet:
            return False

        # Look for prey (any living animal that isn't a carnivore)
        prey_list = []
        for animal in habitat.animals:
            if type(animal) is type(self):
                continue  # Skip own species to avoid cannibalism
            is_alive = animal.is_alive
            is_not_me = animal != self
            is_not_carnivore = not isinstance(animal, Carnivore)
            is_not_omnivore = not isinstance(animal, Omnivore)

            if (is_alive and is_not_me and is_not_carnivore
                    and is_not_omnivore):
                # Ensure population control: only hunt if more than 3 of the
                species_count = len([a for a in habitat.animals
                                     if isinstance(a, type(animal))
                                     and a.is_alive])

                if species_count > 3:  # Ensure there's enough of the species
                    prey_list.append(animal)

        # Safety Check: If no prey is found, stop here (prevents IndexError)
        if not prey_list:
            return False

        # RANDOMIZED ASPECT: Seasonal hunting success
        prey = random.choice(prey_list)
        success_chance = (self.hunt_skill + self.strength) / 20

        # Seasons modify how easy it is to find prey
        modifiers = {"Winter": 0.8, "Spring": 1.1,
                     "Summer": 1.05, "Autumn": 1.0}
        success_chance *= modifiers.get(habitat.season, 1.0)

        if random.random() < success_chance:
            prey.die()
            habitat.remove_animal(prey)  # Animal is consumed
            self.hunger = max(0, self.hunger - self.meat_reward)
            self.rounds_since_eating = 0
            return True
        return False


class Omnivore(Animal):
    """""
    Omnivore - A flexible eater that chooses between plants and meat
    based on its current hunger level.

    >>> # Example using a Bear as a concrete Omnivore
    >>> b = Bear("Baloo")
    >>> b.metabolic_rate # Interval 3 -> 0.33 hunger per round
    0.3333333333333333
    >>> b.hunger = 0.0
    >>> b.grow()
    >>> round(b.hunger, 2)
    0.33
    >>> b.strength
    10
    """

    def __init__(self, name, max_hunger=12, strength=8, feeding_interval=2):
        """
        initializes omnivores with their special attributes
        """
        super().__init__(name, max_hunger, strength, feeding_interval)
        # Define the bite size once for the whole class
        self.plant_bite_size = 2  # Hunger reduction when eating plants
        self.meat_reward = 10  # Hunger reduction per successful hunt

    def eat(self, habitat):
        """
        controls omnivore's feeding
        """
        is_sleeping = self.hibernating
        is_still_full = self.rounds_since_eating < self.feeding_interval

        # Early Exit: If the animal shouldn't eat, stop here
        if is_sleeping or is_still_full:
            return False

        is_very_hungry = self.hunger > (self.max_hunger * 0.7)

        if is_very_hungry:
            # Hunting logic (similar to Carnivore)
            potential_prey = []
            for animal in habitat.animals:
                if type(animal) is type(self):
                    continue  # Skip own species to avoid cannibalism
                is_alive = animal.is_alive
                is_not_self = animal != self
                is_weaker = animal.strength < self.strength

                # The hunt is only possible if all criteria are met
                if is_alive and is_not_self and is_weaker:
                    species_count = len([a for a in habitat.animals
                                         if isinstance(a, type(animal))
                                         and a.is_alive])
                    # Ensure enough of the species remain
                    if species_count > 3:
                        potential_prey.append(animal)

            if potential_prey:
                target = random.choice(potential_prey)
                target.die()
                habitat.remove_animal(target)
                self.hunger = max(0, self.hunger - self.meat_reward)
                self.rounds_since_eating = 0
                return True

        else:
            plant_list = [p for p in habitat.plants if p.is_alive
                          and not isinstance(p, Tree)
                          and not isinstance(p, Eucalyptus)]
            if plant_list:
                # Select a random food source from the available plants
                plant = random.choice(plant_list)
                # Interaction:
                # Reduce plant size by the omnivore's specific bite size
                plant.be_eaten(self.plant_bite_size)
                # Update animal stats:
                # decrease hunger and reset the feeding timer
                self.hunger = max(0, self.hunger - self.plant_bite_size)
                self.rounds_since_eating = 0
                return True
        # Return False if no food was found or if the animal chose not to eat
        return False


# --- Specialized Animal Classes ---

class Rabbit(Herbivore):
    """
    SPECIAL RULE: Fast metabolism, reproduces quickly.

    >>> r = Rabbit("Bugs")
    >>> r.hunger
    0
    >>> r.metabolic_rate
    1.0
    >>> r.grow() # After one round, hunger should be 1.0
    >>> r.hunger
    1.0
    >>> r.max_hunger
    6
    >>> r.cooldown_duration # Quick reproduction cycle
    2
    """

    def __init__(self, name):
        """
        initializes rabbits attributes
        """
        super().__init__(name, max_hunger=6, strength=2, feeding_interval=1)

        # These attributes define the reproduction strategy of the rabbit.
        # We override the defaults from the Animal base class.
        self.repro_cooldown = 0
        self.cooldown_duration = 2     # Rounds to wait after having babies
        self.min_repro_age = 2         # Age needed to reach sexual maturity
        self.hunger_threshold = 3      # Maximum hunger allowed to reproduce

    def can_reproduce(self):
        """
        checks if rabbits are ready to reproduce
        """
        # Rabbits need to be adult and not starving to reproduce
        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1
            return False

        # Logic: Rabbits need to be mature and not too hungry.
        is_ready = (
            self.age > self.min_repro_age and
            self.hunger < self.hunger_threshold
        )

        if is_ready:
            self.repro_cooldown = self.cooldown_duration
            return True

        return False


class Koala(Herbivore):
    """
    SPECIAL RULE: Diet specialist.
    Only searches for Eucalyptus objects in the habitat.

    >>> k = Koala("Sid")
    >>> k.hunger
    0
    >>> k.metabolic_rate
    0.5
    >>> # After 2 rounds of growing without eating, hunger should be 1.0
    >>> k.grow()
    >>> k.grow()
    >>> k.hunger
    1.0
    >>> k.max_hunger
    8
    """

    def __init__(self, name):
        """
        initializes koala's attributes
        """
        super().__init__(name, max_hunger=8, strength=3, feeding_interval=2)

    def eat(self, habitat):
        """
        controls feeding of koalas
        """
        eucs = [p for p in habitat.plants
                if isinstance(p, Eucalyptus) and p.is_alive]
        if eucs:
            # Koala specific eating logic...
            if eucs:
                plant = random.choice(eucs)
                eat_amount = 2
            if plant.be_eaten(eat_amount):
                self.hunger = max(0, self.hunger - eat_amount)
                self.rounds_since_eating = 0
                return True

        return False


class Bear(Omnivore):
    """
    SPECIAL RULE: Hibernation.
    Enters a state of sleep during Winter rounds where it doesn't eat.

    >>> b = Bear("Baloo")
    >>> b.hunger = 5.0
    >>> b.hibernating
    False
    >>> b.prepare_hibernation("Winter") # Gehe in den Winterschlaf
    >>> b.hibernating
    True
    >>> b.hunger # Hunger sollte um den hibernation_bonus (2) sinken
    3.0
    >>> b.prepare_hibernation("Spring") # Wache im Frühling auf
    >>> b.hibernating
    False
    """

    def __init__(self, name):
        """
        initializes bears attributes
        """
        super().__init__(name, max_hunger=15, strength=10, feeding_interval=3)

    def prepare_hibernation(self, season):
        """
        control bears hibernation
        """
        if season == "Winter" and not self.hibernating:
            self.enter_hibernation()
        elif season != "Winter" and self.hibernating:
            self.wake_up()


class Wolf(Carnivore):
    '''
    no special rules for him

    >>> w = Wolf("Sinan")
    >>> w.hunger  # Should start at 0.0
    0
    >>> w.metabolic_rate
    0.5
    >>> w.grow()  # Increases hunger by metabolic_rate
    >>> w.hunger
    0.5
    '''

    def __init__(self, name):
        """
        initializes wolfs attributes
        """
        super().__init__(name, max_hunger=15, strength=10, feeding_interval=2)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()

    if results.failed == 0:
        print(f"Success! All {results.attempted} tests passed.")
    else:
        print(f"Oops! {results.failed} tests failed.")
