import random
def gen_random(num_count, begin, end):
    return [random.randint(begin, end) for _ in range(num_count)]

# print(gen_random(10, 10, 1000))