from prog import CompoundStm, AssignStm, PrintStm, OpExp, IdExp, NumExp, EseqExp, PairExpList, LastExpList

class Prog:
    """Sample program"""
    prog = CompoundStm(AssignStm("a",OpExp(NumExp(5), OpExp.plus, NumExp(3))),
            CompoundStm(AssignStm("b",
               EseqExp(PrintStm(PairExpList(IdExp("a"),
                    LastExpList(OpExp(IdExp("a"), OpExp.minus, NumExp(1))))),
                                 OpExp(NumExp(10), OpExp.times, IdExp("a")))),PrintStm(LastExpList(IdExp("b")))))


### Exercise 1
def maxargs(prog, ma = 0):
    match prog:
        case PrintStm():
            ma = max(prog.exl.length(), ma)
            return maxargs(prog.exl, ma)
        case CompoundStm():
            return max(maxargs(prog.stm1, ma), maxargs(prog.stm2,ma))
        case AssignStm():
            return maxargs(prog.exp, ma)
        case OpExp():
            return max(maxargs(prog.left, ma), maxargs(prog.right,ma))
        case EseqExp():
            return max(maxargs(prog.exp, ma), maxargs(prog.stm,ma))
        case PairExpList():
            return max(maxargs(prog.head, ma), maxargs(prog.tail,ma))
        case LastExpList():
            return maxargs(prog.head, ma) 
        # IdExp and NumExp
        case _:
            return ma

print(maxargs(Prog.prog))


### Exercise 2
class IntAndTable():
    def __init__(self, t, i):
        self.table = t
        self.i = i

    def interpStm(self, stm, t):
        self.i += 1
        match stm:
            case CompoundStm():
                self.interpStm(stm.stm1,t)
                self.interpStm(stm.stm2,t)
            case AssignStm():
                t[stm.id] = self.interpExp(stm.exp,t)
            case PrintStm():
                self.interpExp(stm.exl,t) 
            case _:
                self.interpExp(stm,t)
        self.table = t

    def interpExp(self, exp, t):
        self.i += 1
        match exp:
            case IdExp():
                return self.table[exp.id]
            case NumExp():
                return exp.num
            case OpExp():
                match exp.oper:
                    case 1:
                        return self.interpExp(exp.left, t) + self.interpExp(exp.right, t)
                    case 2:
                        return self.interpExp(exp.left, t) - self.interpExp(exp.right, t)
                    case 3:
                        return self.interpExp(exp.left, t) * self.interpExp(exp.right, t)
                    case 4:
                        return self.interpExp(exp.left, t) / self.interpExp(exp.right, t)
            case EseqExp():
                self.interpStm(exp.stm, t)
                return self.interpExp(exp.exp, t)
            case PairExpList():
                self.interpExp(exp.head, t)
                return self.interpExp(exp.tail, t)
            case LastExpList():
                return self.interpExp(exp.head, t)
        self.table = t

    def lookup(self, table, key):
        return table[key]

iat = IntAndTable({},0)
print(iat.table, iat.i)
iat.interpStm(Prog.prog, iat.table)
print(iat.table, iat.i)
