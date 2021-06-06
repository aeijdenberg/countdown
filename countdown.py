from functools import reduce
from itertools import permutations, product
from operator import add, mul, sub
from random import randrange, sample

BIGS = reduce(add, ([(i+1)*25] for i in range(4)))
LITTLES = reduce(add, ([i+1] * 2 for i in range(10)))

def cddiv(a, b):
    if b[0] == 0:
        raise ZeroDivisionError()
    
    if a[0] % b[0] != 0:
        raise ZeroDivisionError()

    return a[0] // b[0], '( %s / %s )' % (a[1], b[1])

def cdadd(a, b):
    return a[0] + b[0], '( %s + %s )' % (a[1], b[1])

def cdmul(a, b):
    return a[0] * b[0], '( %s * %s )' % (a[1], b[1])

def cdsub(a, b):
    return a[0] - b[0], '( %s - %s )' % (a[1], b[1])

def valid_stream(t):
    c = 0
    for z in t:
        if z:
            if c < 2:
                return False
            c -= 1
        else:
            c += 1
    return c == 1

def op_v_numbers(n):
    for t in product([0, 1], repeat=n+n-1):
        if valid_stream(t):
            yield t

def zip_streams(streams, order):
    for o in order:
        yield next(streams[o])

def rpn(inputs, target):
    try:
        s = []
        for z in inputs:
            if callable(z):
                r = z(s[-2], s[-1])
                s = s[:-2] + [r]
            else:
                r = (z, str(z))
                s.append(r)
            if r[0] == target:
                print(r[1], target)
    except ZeroDivisionError:
        return



def find(deck, target):
    print('Searching for %i in' % target, deck)
    orders = list(op_v_numbers(len(deck)))
    prods = product([cdadd, cdmul, cdsub, cddiv], repeat=len(deck)-1)
    cross_prod = list(product(list(product([cdadd, cdmul, cdsub, cddiv], repeat=len(deck)-1)), list(op_v_numbers(len(deck)))))
    for d in permutations(deck):
        for ops, order in cross_prod:
            rpn(zip_streams([iter(d), iter(ops)], order), target)


find([3, 6, 25, 50, 75, 100], 952)

# * / + * +
# 0 0 1 0 1 0 0 1 1 0 1
# 75 6 * 50 / 100 3 + * 25 +



# for i in range(100):
#     find(sample(BIGS, 2) + sample(LITTLES, 4), randrange(100, 1001))
