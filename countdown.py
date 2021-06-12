from functools import reduce
from itertools import permutations, product
from operator import add, mul, sub
from random import randrange, sample

BIGS = reduce(add, ([(i+1)*25] for i in range(4)))
LITTLES = reduce(add, ([i+1] * 2 for i in range(10)))


SCALAR = 0
ADD = 1
MULTIPLY = 2

class Expression(object):
    def __init__(self, op, value, negated=False, inverted=False):
        self._negated = negated
        self._inverted = inverted
        self._op = op
        if self._op == SCALAR:
            self._value = value
        else:
            self._value = []
            for child in value:
                if child._op == self._op:
                    for gc in child._value:
                        if child._negated:
                            gc = gc.negated()
                        if child._inverted:
                            gc = gc.inverted()
                        self._value.append(gc)
                else:
                    self._value.append(child)

    def negated(self):
        return Expression(self._op, self._value, not self._negated, self._inverted)

    def inverted(self):
        return Expression(self._op, self._value, self._negated, not self._inverted)

    def __repr__(self):
        if self._negated or self._inverted:
            raise ValueError()
        elif self._op == SCALAR:
            return self._value
        elif self._op == ADD:
            left, right = [], []
            for c in self._value:
                if c._negated:
                    right.append(repr(c.negated()))
                else:
                    left.append(repr(c))
            left.sort()
            right.sort()
            return '%s%s%s%s%s' % (''.join(left), '+' * (len(left) - 1), ''.join(right), '+' * (len(right) - 1), '-' if len(right) else '')
        elif self._op == MULTIPLY:
            left, right = [], []
            for c in self._value:
                if c._inverted:
                    right.append(repr(c.inverted()))
                else:
                    left.append(repr(c))
            left.sort()
            right.sort()
            return '%s%s%s%s%s' % (''.join(left), '*' * (len(left) - 1), ''.join(right), '*' * (len(right) - 1), '/' if len(right) else '')
        else:
            raise ValueError()


        # return '%s%s%s' % (
        #     '-' if self._negated else '',
        #     '1/' if self._inverted else '',
        #     self._value if self._op == SCALAR else ('(%s)' % ('*' if self._op == MULTIPLY else '+').join(sorted(repr(c) for c in self._value))),
        # )

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

def rpn(inputs):
    s = []
    for z in inputs:
        if callable(z):
            r = z(s[-2], s[-1])
            s = s[:-2] + [r]
        else:
            r = Expression(SCALAR, z)
            s.append(r)
        yield r

def find(deck, target):
    deck=list(chr(ord('a') + i) for i in range(6))
    c = 0
    for d in permutations(deck):
        for order in op_v_numbers(len(deck)):
            for ops in product([
                    lambda a, b: Expression(ADD, [a, b]),                 # add
                    lambda a, b: Expression(ADD, [a, b.negated()]),       # subtract
                    lambda a, b: Expression(MULTIPLY, [a, b]),            # multiply
                    lambda a, b: Expression(MULTIPLY, [a, b.inverted()]), # divide
            ], repeat=len(deck)-1):
                for r in rpn(zip_streams([iter(d), iter(ops)], order)):
                    print(repr(r))
                    c += 1
    #print(c)
    return


    print('Searching for %i in' % target, deck)


42 * 6 * 5 * 4 * 3 * 2 * 1 * 4 * 4 * 4 * 4 * 4


find([3, 6, 25, 50, 75, 100], 952)

# * / + * +
# 0 0 1 0 1 0 0 1 1 0 1
# 75 6 * 50 / 100 3 + * 25 +



# for i in range(100):
#     find(sample(BIGS, 2) + sample(LITTLES, 4), randrange(100, 1001))
