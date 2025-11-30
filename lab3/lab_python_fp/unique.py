from lab3.lab_python_fp.gen_random import gen_random

class Unique(object):
    def __init__(self, items, **kwargs):
        if "ignore_case" not in kwargs:
            kwargs["ignore_case"] = False
        # Нужно реализовать конструктор
        # В качестве ключевого аргумента, конструктор должен принимать bool-параметр ignore_case,
        # в зависимости от значения которого будут считаться одинаковыми строки в разном регистре
        # Например: ignore_case = True, Aбв и АБВ - разные строки
        #           ignore_case = False, Aбв и АБВ - одинаковые строки, одна из которых удалится
        # По-умолчанию ignore_case = False
        res = []
        if kwargs["ignore_case"]:
            for i in items:
                if str(i).lower() not in res:
                    res.append(i)
        else:
            for i in items:
                if str(i) not in res:
                    res.append(i)
        self.res = res

    def __next__(self):
        # Нужно реализовать __next__   :
        self.iter += 1
        self.value = self.res[self.iter]
        return self

    def __iter__(self):
        self.iter = 0
        self.value = self.res[0]
        return self

    def __str__(self):
        return f"{self.res}"

data = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
Unique(data)
data = gen_random(10, 1, 20)
a = Unique(data, ignore_case=True)
s = iter(a)

