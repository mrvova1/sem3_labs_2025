from contextlib import contextmanager
import time

class cm_timer_1():
    def __init__(self):
        self.timer = 0

    def __enter__(self):
        self.timer = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(time.time() - self.timer)


@contextmanager
def cm_timer_2():
    timer = time.time()
    try:
        yield None
    finally:
        print(time.time() - timer)

# with cm_timer_1():
#     time.sleep(5.5)
#
# with cm_timer_2():
#     time.sleep(5.5)