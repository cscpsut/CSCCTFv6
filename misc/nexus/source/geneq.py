import random
from z3 import *
from icecream import ic


def generate():
    def generate_equation(var1, var2, var3):
        op = random.choice(ops)
        return f"{var1} {op} {var2} == {var3}"

    ops = ["+", "-", "*", "/"]

    variables = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]

    eq1 = generate_equation(variables[0], variables[1], variables[2])
    eq2 = generate_equation(variables[3], variables[4], variables[5])
    eq3 = generate_equation(variables[6], variables[7], variables[8])
    eq4 = generate_equation(variables[0], variables[3], variables[6])
    eq5 = generate_equation(variables[1], variables[4], variables[7])
    eq6 = generate_equation(variables[2], variables[5], variables[8])

    eqs = [eq1, eq2, eq3, eq4, eq5, eq6]

    symbols = random.sample("a1 a2 a3 a4 a5 a6 a7 a8 a9".split(), k=4)
    sym_vval = {}
    for s in symbols:
        sym_vval[s] = random.randint(1, 100)
    t = []
    for eq in eqs:
        for s in symbols:
            eq = eq.replace(s, str(sym_vval[s]))
        t.append(eq)

    return t


def solve(eqs):
    solver = Solver()
    a1, a2, a3, a4, a5, a6, a7, a8, a9 = Ints("a1 a2 a3 a4 a5 a6 a7 a8 a9")
    eq1, eq2, eq3, eq4, eq5, eq6 = eqs

    solver.add(eval(eq1.replace("==", "==")))
    solver.add(eval(eq2.replace("==", "==")))
    solver.add(eval(eq3.replace("==", "==")))
    solver.add(eval(eq4.replace("==", "==")))
    solver.add(eval(eq5.replace("==", "==")))
    solver.add(eval(eq6.replace("==", "==")))

    if solver.check() == sat:
        if "div0" in str(solver.model()):
            return 0
        return solver.model()
    else:
        return 0


def test():
    c = 0
    for i in range(1000):
        eqs = generate()
        if s := solve(eqs):
            # ic(eqs)
            # ic(s)
            c += 1
    print(c)


def find_eqs(stop_case=1):
    c = 0
    while True:
        eqs = generate()
        if s := solve(eqs):
            # ic(eqs)
            # ic(s)
            c += 1
            with open("eqs.txt", "a") as f:
                f.write(str(c) + "\n")
                f.write(str(eqs) + "\n")
                f.write(str(s) + "\n")
        if c == stop_case:
            break
    return eqs, s


def main():
    # test()
    find_eqs(10)


if __name__ == "__main__":
    main()
