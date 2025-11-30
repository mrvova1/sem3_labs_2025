# tests/steps/test_bdd_animals.py
from behave import given, when, then
from unittest.mock import Mock
from lab4 import ConcreteAnimalBuilder, Director, Caretaker

@given('сервис здоровья который возвращает {health:d} для "{species}" с возрастом {age:d}')
def step_health_service(context, health, species, age):
    context.health_service = Mock()
    context.health_service.get_initial_health.return_value = health

@when('я создаю собаку с именем "{name}" возрастом {age:d} и аксессуаром "{accessory}"')
def step_create_dog(context, name, age, accessory):
    builder = ConcreteAnimalBuilder(health_service=context.health_service)
    director = Director(builder)
    context.animal = director.build_pet_dog(name=name, age=age, accessories=[accessory])

@then('животное должно иметь вид "{species}" и имя "{name}" и здоровье {health:d} и аксессуар "{accessory}"')
def step_check_animal(context, species, name, health, accessory):
    assert context.animal.species == species, f"expected species {species}, got {context.animal.species}"
    assert context.animal.name == name, f"expected name {name}, got {context.animal.name}"
    assert context.animal.health == health, f"expected health {health}, got {context.animal.health}"
    assert accessory in context.animal.accessories, f"expected accessory {accessory} in {context.animal.accessories}"

@when('я сохраняю состояние животного и изменяю имя на "{new_name}" и возраст на {new_age:d}')
def step_save_and_modify(context, new_name, new_age):
    context.caretaker = Caretaker()
    m = context.animal.create_memento()
    context.idx = context.caretaker.save(m)
    context.animal.name = new_name
    context.animal.age = new_age

@then('после восстановления имя животного должно быть "{name}" и возраст {age:d}')
def step_restore_and_check(context, name, age):
    context.animal.restore_memento(context.caretaker.get(context.idx))
    assert context.animal.name == name, f"expected restored name {name}, got {context.animal.name}"
    assert context.animal.age == age, f"expected restored age {age}, got {context.animal.age}"
