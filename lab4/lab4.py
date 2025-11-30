from copy import deepcopy
from typing import Any, Dict, List, Optional


class HealthService():
    def get_initial_health(self, species: str, age: int) -> int: pass


class Animal:
    def __init__(self, species: str = "unknown", name: str = "", age: int = 0, health: int = 100) -> None:
        self.species = species
        self.name = name
        self.age = age
        self.health = health
        self.accessories: List[str] = []

    def __repr__(self) -> str:
        return f"Animal(species={self.species!r}, name={self.name!r}, age={self.age!r}, health={self.health!r}, accessories={self.accessories!r})"

    def _get_state(self) -> Dict[str, Any]:
        return {
            "species": self.species,
            "name": self.name,
            "age": self.age,
            "health": self.health,
            "accessories": deepcopy(self.accessories),
        }

    def _set_state(self, state: Dict[str, Any]) -> None:
        self.species = state["species"]
        self.name = state["name"]
        self.age = state["age"]
        self.health = state["health"]
        self.accessories = deepcopy(state["accessories"])

    def create_memento(self) -> "AnimalMemento":
        return AnimalMemento(self._get_state())

    def restore_memento(self, m: "AnimalMemento") -> None:
        self._set_state(m.get_state())


class AnimalMemento:
    def __init__(self, state: Dict[str, Any]) -> None:
        self._state = deepcopy(state)

    def get_state(self) -> Dict[str, Any]:
        return deepcopy(self._state)


class Caretaker:
    def __init__(self) -> None:
        self._mementos: List[AnimalMemento] = []

    def save(self, m: AnimalMemento) -> int:
        self._mementos.append(m)
        return len(self._mementos) - 1

    def get(self, index: int) -> AnimalMemento:
        return self._mementos[index]

    def last(self) -> AnimalMemento:
        return self._mementos[-1]


class AnimalBuilder(HealthService):
    def set_species(self, species: str) -> "AnimalBuilder": raise NotImplementedError
    def set_name(self, name: str) -> "AnimalBuilder": raise NotImplementedError
    def set_age(self, age: int) -> "AnimalBuilder": raise NotImplementedError
    def set_health(self, health: int) -> "AnimalBuilder": raise NotImplementedError
    def add_accessory(self, accessory: str) -> "AnimalBuilder": raise NotImplementedError
    def build(self) -> Animal: raise NotImplementedError


class ConcreteAnimalBuilder(AnimalBuilder):
    def __init__(self, health_service: Optional[HealthService] = None) -> None:
        self.health_service = health_service
        self.reset()

    def reset(self) -> None:
        self._animal = Animal()

    def set_species(self, species: str) -> "ConcreteAnimalBuilder":
        self._animal.species = species
        return self

    def set_name(self, name: str) -> "ConcreteAnimalBuilder":
        self._animal.name = name
        return self

    def set_age(self, age: int) -> "ConcreteAnimalBuilder":
        self._animal.age = age
        return self

    def set_health(self, health: int) -> "ConcreteAnimalBuilder":
        self._animal.health = health
        return self

    def add_accessory(self, accessory: str) -> "ConcreteAnimalBuilder":
        self._animal.accessories.append(accessory)
        return self

    def compute_health_from_service(self) -> "ConcreteAnimalBuilder":
        if self.health_service is not None:
            self._animal.health = self.health_service.get_initial_health(self._animal.species, self._animal.age)
        return self

    def build(self) -> Animal:
        built = self._animal
        self.reset()
        return built


class Director:
    def __init__(self, builder: AnimalBuilder) -> None:
        self._builder = builder

    def build_pet_dog(self, name: str, age: int, accessories: Optional[List[str]] = None) -> Animal:
        self._builder.set_species("dog").set_name(name).set_age(age)
        if hasattr(self._builder, "compute_health_from_service"):
            getattr(self._builder, "compute_health_from_service")()
        if accessories:
            for a in accessories:
                self._builder.add_accessory(a)
        return self._builder.build()