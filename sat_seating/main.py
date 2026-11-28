import sys, itertools
from instance import random_instance
from encoder import encode, to_dimacs

def decode(model, G, T, x):
    pos = set(l for l in model if l > 0)
    return [[t for t in range(T) if x(g, t) in pos] for g in range(G)]

def verify(inst, seating, T, cap, d):
    """Kontroll i pavarur i zgjidhjes kundrejt kushteve origjinale (jo kundrejt formulës)."""
    if any(len(s) != 1 for s in seating): return "mysafir pa tavolinë ose në disa"
    tab = [s[0] for s in seating]
    groups = [[g for g in range(len(tab)) if tab[g] == t] for t in range(T)]
    if any(len(g) != cap for g in groups): return "kapacitet i shkelur"
    if any(tab[a] == tab[b] for a, b in inst["conflicts"]): return "çift i ndaluar bashkë"
    if any(tab[a] != tab[b] for a, b in inst["together"]): return "çift i detyruar i ndarë"
    for g in groups:
        w = sum(inst["gender"][i] == "F" for i in g)
        if abs((len(g) - w) - w) > d: return "dallim gjinie > d"
    return "OK"

def brute(inst, T, cap, d):
    """Kontroll për instanca të vogla: provon të gjitha ndarjet (vetëm për testim të kodimit)."""
    G = inst["guests"]
    for tab in itertools.product(range(T), repeat=G):
        seating = [[t] for t in tab]
        if verify(inst, seating, T, cap, d) == "OK": return True
    return False

if __name__ == "__main__":
    T, cap, d = 10, 10, 3
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    inst = random_instance(100, 50, 40, 10, seed)
    cnf, x = encode(inst, T, cap, d)
    print(f"variabla={cnf.n} (mysafirë*tavolina={100 * T}, ndihmëse={cnf.n - 100 * T}), klauzola={len(cnf.clauses)}")
    to_dimacs(cnf, "seating.cnf"); print("DIMACS u ruajt te seating.cnf")
    try:
        from pysat.solvers import Glucose3
    except ImportError:
        sys.exit("Instalo zgjidhësin: pip install python-sat  (ose zgjidh seating.cnf me çfarëdo SAT solver)")
    s = Glucose3(bootstrap_with=cnf.clauses)
    if not s.solve(): sys.exit("UNSAT: nuk ekziston ulje që i plotëson kushtet")
    seating = decode(s.get_model(), 100, T, x)
    print("Verifikimi i pavarur:", verify(inst, seating, T, cap, d))
    for t in range(T):
        gs = [g for g in range(100) if seating[g] == [t]]
        print(f"Tavolina {t + 1}: " + " ".join(f"{g}{inst['gender'][g]}" for g in gs))
    # Kontroll i kodimit mbi instancë të vogël: SAT dhe brute-force duhet të japin të njëjtin përgjigje (SAT/UNSAT)
    ok = True
    for sd in range(6):
        small = random_instance(6, 3, 3, 1, sd)
        c, xs = encode(small, 2, 3, 1)
        sat = Glucose3(bootstrap_with=c.clauses).solve()
        ok &= (sat == brute(small, 2, 3, 1))
    print("Kodimi përputhet me brute-force në 6 instanca të vogla:", ok)