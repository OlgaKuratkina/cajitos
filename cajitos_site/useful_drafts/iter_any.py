# You could simply use an iterator over the sequence and check that any on the iterator returns always True for n-times:


def check(it, num):
    it = iter(it)
    return all(any(it) for _ in range(num))

#  check([1, 1, 0], 2)
# True

# check([1, 1, 0], 3)
# False

# If you want to have it even faster than a solution based on map and itertools.repeat can be slightly faster:
from itertools import repeat

def check_map(it, num):
    return all(map(any, repeat(iter(it), num)))