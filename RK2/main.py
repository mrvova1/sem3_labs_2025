# lib_module.py
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class ProgrammingLibrary:
    ID: int
    name: str
    programming_language_ID: int
    upload_count: int


@dataclass
class ProgrammingLanguage:
    ID: int
    name: str
    last_version: str


@dataclass
class ProgrammingLibraryOfLanguage:
    Programming_language_ID: int
    Programming_library_ID: int


def task1(list_prog_lib: List[ProgrammingLibrary],
          list_prog_lan: List[ProgrammingLanguage]) -> List[Tuple[str, str]]:
    result: List[Tuple[str, str]] = []
    for lib in list_prog_lib:
        if lib.name and lib.name[0] in ("A", "А"):
            lang_name = next((l.name for l in list_prog_lan if l.ID == lib.programming_language_ID), None)
            if lang_name is not None:
                result.append((lib.name, lang_name))
    return result


def task2(list_prog_lib: List[ProgrammingLibrary],
          list_prog_lan: List[ProgrammingLanguage]) -> List[Tuple[int, str]]:
    res: List[Tuple[int, str]] = []
    for lang in list_prog_lan:
        uploads = [lib.upload_count for lib in list_prog_lib if lib.programming_language_ID == lang.ID]
        min_upload = min(uploads) if uploads else 0
        res.append((min_upload, lang.name))
    return sorted(res)


def task3(list_library_of_language: List[ProgrammingLibraryOfLanguage],
          list_prog_lib: List[ProgrammingLibrary],
          list_prog_lan: List[ProgrammingLanguage]) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    for mapping in list_library_of_language:
        lib_name: Optional[str] = next((lib.name for lib in list_prog_lib if lib.ID == mapping.Programming_library_ID), None)
        lang_name: Optional[str] = next((lang.name for lang in list_prog_lan if lang.ID == mapping.Programming_language_ID), None)
        if lib_name is not None and lang_name is not None:
            pairs.append((lib_name, lang_name))
    pairs.sort(key=lambda x: (x[0], x[1]))
    return pairs

