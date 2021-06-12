#!/usr/bin/env python3

class Val(object):
    def __init__(self, value, working=None):
        self._value, self._working = value, working if working else str(value)
    def __mul__(self, other):
        return Val(self._value * other._value, '(%s*%s)' % (self._working, other._working))
    def __sub__(self, other):
        return Val(self._value - other._value, '(%s-%s)' % (self._working, other._working)) if self._value > other._value else None
    def __add__(self, other):
        return Val(self._value + other._value, '(%s+%s)' % (self._working, other._working))
    def __truediv__(self, other):
        return Val(self._value // other._value, '(%s/%s)' % (self._working, other._working)) if self._value % other._value == 0 else None

def append_with_working(todo, working, answers, vals):
    s = '|'.join([str(x._value) for x in sorted(vals, key=lambda y: y._value)])
    if s in working:
        return
    for v in vals:
        soln = answers.get(v._value)
        if soln is None or len(v._working) < len(soln):
            answers[v._value] = v._working
    todo.append(s)
    working[s] = vals

def each_two(deck):
    if len(deck) >= 2:
        for i in range(len(deck)):
            for j in range(i+1, len(deck)):
                yield deck[i], deck[j], deck[:i] + deck[i+1:j] + deck[j+1:]

def find(deck, targets):
    todo = []
    working = {}
    answers = {}
    append_with_working(todo, working, answers, [Val(x) for x in deck])
    while todo:
        for a, b, remaining in each_two(working[todo.pop()]):
            for t in [a + b, a * b, a - b, b - a, a / b, b / a]:
                if t:
                    append_with_working(todo, working, answers, remaining + [t])
    for target in targets:
        print("%d -> %s" % (target, answers.get(target)))

if __name__ == '__main__':
    import sys
    find([int(x) for x in sys.argv[1:-1]], [int(sys.argv[-1])])
