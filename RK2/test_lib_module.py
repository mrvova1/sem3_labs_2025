# test_lib_module.py
import pytest
from main import (
    ProgrammingLibrary,
    ProgrammingLanguage,
    ProgrammingLibraryOfLanguage,
    task1,
    task2,
    task3,
)


@pytest.fixture
def sample_data():
    list_prog_lib = [
        ProgrammingLibrary(0, 'Pandas', 0, 10000),
        ProgrammingLibrary(1, 'Mathlib', 2, 250000),
        ProgrammingLibrary(2, 'QT5', 0, 32000),
        ProgrammingLibrary(3, 'sys', 1, 123000),
        ProgrammingLibrary(4, 'os', 1, 322200),
        ProgrammingLibrary(5, 'iostream', 2, 3000),
        ProgrammingLibrary(6, 'A_something', 3, 200),
        ProgrammingLibrary(7, 'Json', 3, 990000),
        ProgrammingLibrary(8, 'Aio', 1, 20),
    ]

    list_prog_lan = [
        ProgrammingLanguage(0, 'Python', '1.231'),
        ProgrammingLanguage(1, 'JSCode', '2.23'),
        ProgrammingLanguage(2, 'C++', '3.2'),
        ProgrammingLanguage(3, 'C#', '1.1'),
    ]

    list_prog_lib_lan = [
        ProgrammingLibraryOfLanguage(0, 1),
        ProgrammingLibraryOfLanguage(0, 2),
        ProgrammingLibraryOfLanguage(0, 4),
        ProgrammingLibraryOfLanguage(0, 7),
        ProgrammingLibraryOfLanguage(1, 2),
        ProgrammingLibraryOfLanguage(1, 4),
        ProgrammingLibraryOfLanguage(1, 3),
        ProgrammingLibraryOfLanguage(1, 0),
        ProgrammingLibraryOfLanguage(2, 1),
        ProgrammingLibraryOfLanguage(2, 5),
        ProgrammingLibraryOfLanguage(2, 6),
        ProgrammingLibraryOfLanguage(2, 7),
        ProgrammingLibraryOfLanguage(3, 0),
        ProgrammingLibraryOfLanguage(3, 1),
        ProgrammingLibraryOfLanguage(3, 2),
        ProgrammingLibraryOfLanguage(3, 3),
        ProgrammingLibraryOfLanguage(3, 6),
    ]

    return list_prog_lib, list_prog_lan, list_prog_lib_lan


def test_task1_returns_libraries_starting_with_A(sample_data):
    libs, langs, _ = sample_data
    res = task1(libs, langs)
    expected = [
        ('A_something', 'C#'),
        ('Aio', 'JSCode'),
    ]
    assert res == expected


def test_task2_min_uploads_per_language_sorted(sample_data):
    libs, langs, _ = sample_data
    res = task2(libs, langs)
    # expected sorted by min upload count (ascending)
    expected = [
        (20, 'JSCode'),    # Aio
        (200, 'C#'),       # A_something
        (3000, 'C++'),     # iostream
        (10000, 'Python'), # Pandas
    ]
    assert res == expected


def test_task3_returns_sorted_library_language_pairs(sample_data):
    libs, langs, mappings = sample_data
    res = task3(mappings, libs, langs)
    expected = [
        ('A_something', 'C#'),
        ('A_something', 'C++'),
        ('Json', 'C++'),
        ('Json', 'Python'),
        ('Mathlib', 'C#'),
        ('Mathlib', 'C++'),
        ('Mathlib', 'Python'),
        ('Pandas', 'C#'),
        ('Pandas', 'JSCode'),
        ('QT5', 'C#'),
        ('QT5', 'JSCode'),
        ('QT5', 'Python'),
        ('iostream', 'C++'),
        ('os', 'JSCode'),
        ('os', 'Python'),
        ('sys', 'C#'),
        ('sys', 'JSCode'),
    ]
    assert res == expected
