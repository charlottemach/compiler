# Python adaption of prog.java
class Stm:
    def __init__(self,s1):
        self.stm1 = s1

class CompoundStm(Stm):
    def __init__(self, s1, s2):
        self.stm1 = s1
        self.stm2 = s2

class AssignStm(Stm):
    def __init__(self, i, e):
        self.id = i
        self.exp = e

class PrintStm(Stm):
    def __init__(self, exps):
        self.exl = exps

class Exp:
    def __init__(self):
        self.self = self

class IdExp(Exp):
    def __init__(self, i):
        self.id = i

class NumExp(Exp):
    def __init__(self, n):
        self.num = n

class OpExp(Exp):
    plus = 1
    minus = 2
    times = 3
    div = 4
    def __init__(self, l, o, r):
        self.left = l
        self.oper = o
        self.right = r

class EseqExp(Exp):
    def __init__(self, s, e):
        self.stm = s
        self.exp = e

class ExpList():
    def __init__(self):
        self.self = self

class PairExpList(ExpList):
    def __init__(self, h, t):
        self.head = h
        self.tail = t

    def length(self):
        return 1 + self.tail.length()

class LastExpList(ExpList):
    def __init__(self, h):
        self.head = h

    def length(self):
        return 1


