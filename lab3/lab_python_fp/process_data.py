import json
import sys
# Сделаем другие необходимые импорты
from field import field
from cm_timer import cm_timer_1
from gen_random import gen_random
from print_result import print_result
from unique import Unique

path = "data.txt"

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

with open(path) as f:
    data = json.load(f)

# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    # print(sorted(Unique(arg).res[0], key=lambda x: x["work name"]))
    return sorted(Unique(arg).res[0], key=lambda x: x["work name"])


@print_result
def f2(arg):
    # print(arg)
    # s = [i for i in arg if "программист" in str(field(i, "work name")).lower()]
    # print([i for i in arg if "программист" in str(field(i, "work name")).lower()])
    # print([i for i in arg])
    # for i in arg:
    #     print(f"{i}:", str(field(i, "work name")).lower())
    s = [i for i in arg[0] if "3" in i["work name"].lower()]
    # print('s: ', s)
    return s


@print_result
def f3(arg):
    # print(arg)
    return list(map(lambda x: x['work name'] + " с опытом Python", arg[0]))


@print_result
def f4(arg):
    return list(zip(arg[0], [f"зарплата {i} руб" for i in gen_random(len(arg[0]), 100000, 1000000)]))

print(f1(data))
if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))