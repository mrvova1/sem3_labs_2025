class Programming_library:
    def __init__(self, ID: int, name: str, programming_language_ID: int, upload_count: int):
        self.ID = ID
        self.name = name
        self.programming_language_ID = programming_language_ID
        self.upload_count = upload_count

class Programming_language:
    def __init__(self: int, ID, name: str, last_version: str):
        self.ID = ID
        self.name = name
        self.last_version = last_version


class Programming_library_of_language:
    def __init__(self, Programming_language_ID, Programming_library_ID):
        self.Programming_language_ID = Programming_language_ID
        self.Programming_library_ID = Programming_library_ID

def Task1(list_prog_lib: list, list_prog_lan: list):
    for i in list_prog_lib:
        if i.name[0] == "A" or i.name[0] == "А":
            print(i.name, [j.name for j in list_prog_lan if j.ID == i.programming_language_ID][0])

def Task2(list_prog_lib: list, list_prog_lan: list):
    for i in sorted([[min([j.upload_count for j in list_prog_lib if j.programming_language_ID == i.ID]), i.name] for i in list_prog_lan]):
        print(i[0], i[1])

def Task3(list_library_of_language: list, list_prog_lib: list, list_prog_lan: list):
    for i in sorted(list_library_of_language, key=lambda x: [[j.name for j in list_prog_lib if j.ID == x.Programming_library_ID], [j.name for j in list_prog_lan if j.ID == x.Programming_language_ID]]):
        print([j.name for j in list_prog_lib if j.ID == i.Programming_library_ID][0], [j.name for j in list_prog_lan if j.ID == i.Programming_language_ID][0])


list_prog_lib = [
    Programming_library(0, 'Pandas', 0, 10000),
    Programming_library(1, 'Mathlib', 2, 250000),
    Programming_library(2, 'QT5', 0, 32000),
    Programming_library(3, 'sys', 1, 123000),
    Programming_library(4, 'os', 1, 322200),
    Programming_library(5, 'iostream', 2, 3000),
    Programming_library(6, 'A_something', 3, 200),
    Programming_library(7, 'Json', 3, 990000),
    Programming_library(8, 'Aio', 1, 20),
]

list_prog_lan = [
    Programming_language(0, 'Python', '1.231'),
    Programming_language(1, 'JSCode', '2.23'),
    Programming_language(2, 'C++', '3.2'),
    Programming_language(3, 'C#', '1.1'),
]

list_prog_lib_lan = [
    Programming_library_of_language(0, 1),
    Programming_library_of_language(0, 2),
    Programming_library_of_language(0, 4),
    Programming_library_of_language(0, 7),
    Programming_library_of_language(1, 2),
    Programming_library_of_language(1, 4),
    Programming_library_of_language(1, 3),
    Programming_library_of_language(1, 0),
    Programming_library_of_language(2, 1),
    Programming_library_of_language(2, 5),
    Programming_library_of_language(2, 6),
    Programming_library_of_language(2, 7),
    Programming_library_of_language(3, 0),
    Programming_library_of_language(3, 1),
    Programming_library_of_language(3, 2),
    Programming_library_of_language(3, 3),
    Programming_library_of_language(3, 6),
]

print("Task1")
print("Библиотеки начинающиеся с буквы А (англ\русской)")
Task1(list_prog_lib, list_prog_lan)
print()

print("Task2")
print("Минимальное количество скачиваний библиотек")
Task2(list_prog_lib, list_prog_lan)
print()

print("Task3")
print("Все языки программирования и их библиотеки (отсортированные по называнию библиотеки и языка)")
Task3(list_prog_lib_lan, list_prog_lib, list_prog_lan)
print()
