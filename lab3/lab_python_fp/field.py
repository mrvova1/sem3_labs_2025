

def field(items, *args):
    assert len(args) > 0
    # Необходимо реализовать генератор
    res = []
    if len(args) == 1:
        for i in items:
            res.append(i[args[0]])
    else:
        for i in items:
            r = {}
            for j in args:
                r[j] = i[j]
            res.append(r)
    print(res)
    return res



# goods = [
#    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
#    {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
# ]
# field(goods, 'title')
# field(goods, 'title', 'price')