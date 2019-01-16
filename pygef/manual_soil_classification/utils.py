import random


def randomColor():
    return "%06x" % random.randint(0, 0xFFFFFF)

