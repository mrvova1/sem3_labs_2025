import pytest
from unittest.mock import Mock
import sys
import os
# Добавляем путь к исходному коду
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab4 import (
    Animal,
    AnimalMemento,
    Caretaker,
    ConcreteAnimalBuilder,
    Director,
)


def test_memento_save_and_restore():
    a = Animal(species="cat", name="Whiskers", age=3, health=80)
    a.accessories.append("collar")

    caretaker = Caretaker()
    m1 = a.create_memento()
    idx = caretaker.save(m1)

    a.name = "Mittens"
    a.age = 4
    a.accessories.append("hat")

    a.restore_memento(caretaker.get(idx))

    assert a.name == "Whiskers"
    assert a.age == 3
    assert a.accessories == ["collar"]


def test_builder_uses_health_service_mock():
    health_service = Mock()
    health_service.get_initial_health.return_value = 92

    builder = ConcreteAnimalBuilder(health_service=health_service)
    director = Director(builder)

    dog = director.build_pet_dog(name="Rex", age=2, accessories=["ball"])

    health_service.get_initial_health.assert_called_once_with("dog", 2)
    assert dog.species == "dog"
    assert dog.name == "Rex"
    assert dog.age == 2
    assert dog.health == 92
    assert "ball" in dog.accessories