"""Kodimi i problemit të ulëseve në formulë CNF (SAT).

Variablat:  x(g,t) = «mysafiri g ulet në tavolinën t»  ->  id = g*T + t + 1.
Klauzolat:
 1. Çdo mysafir ulet në të paktën një tavolinë:        (x(g,0) v ... v x(g,T-1))
 2. Çdo mysafir ulet në më së shumti një tavolinë:     (-x(g,t) v -x(g,u))  për t<u
 3. Çdo tavolinë ka më së shumti `cap` mysafirë:       AtMost(cap) mbi x(0,t)..x(G-1,t)   (sequential counter)
 4. Çifti (a,b) i ndaluar:    për çdo t:  (-x(a,t) v -x(b,t))
 5. Çifti (a,b) i detyruar:   për çdo t:  (-x(a,t) v x(b,t)) ^ (x(a,t) v -x(b,t))        (x(a,t) <-> x(b,t))
 6. Gjinia |burra - gra| <= d: kur çdo tavolinë është plot (G = T*cap, nga 1-3 çdo tavolinë ka saktësisht cap),
    |cap - 2*gra| <= d  <=>  lo <= gra <= hi.  Kodohet me AtMost(hi) mbi gratë dhe AtMost(cap-lo) mbi burrat.
"""

class CNF:
    def __init__(self, nvars):
        self.n, self.clauses = nvars, []
    def new_var(self):
        self.n += 1
        return self.n
    def add(self, *lits):
        self.clauses.append(list(lits))

def at_most(cnf, lits, k):
    """Sequential counter (Sinz 2005): AtMost-k mbi `lits`. s[i][j] = «të paktën j+1 nga lits[0..i] janë të vërteta»."""
    n = len(lits)
    if k >= n: return
    if k == 0:
        for x in lits: cnf.add(-x)
        return
    s = [[cnf.new_var() for _ in range(k)] for _ in range(n - 1)]
    cnf.add(-lits[0], s[0][0])
    for j in range(1, k): cnf.add(-s[0][j])
    for i in range(1, n - 1):
        cnf.add(-lits[i], s[i][0])
        cnf.add(-s[i - 1][0], s[i][0])
        for j in range(1, k):
            cnf.add(-lits[i], -s[i - 1][j - 1], s[i][j])
            cnf.add(-s[i - 1][j], s[i][j])
        cnf.add(-lits[i], -s[i - 1][k - 1])
    cnf.add(-lits[n - 1], -s[n - 2][k - 1])

def encode(inst, tables=10, cap=10, max_diff=3):
    G = inst["guests"]
    assert G == tables * cap, "formulimi supozon që tavolinat mbushen plotësisht (G = tavolina * karrige)"
    x = lambda g, t: g * tables + t + 1
    cnf = CNF(G * tables)
    for g in range(G):
        cnf.add(*[x(g, t) for t in range(tables)])                       # 1
        for t in range(tables):
            for u in range(t + 1, tables): cnf.add(-x(g, t), -x(g, u))   # 2
    for t in range(tables):
        at_most(cnf, [x(g, t) for g in range(G)], cap)                   # 3
    for a, b in inst["conflicts"]:
        for t in range(tables): cnf.add(-x(a, t), -x(b, t))              # 4
    for a, b in inst["together"]:
        for t in range(tables):
            cnf.add(-x(a, t), x(b, t)); cnf.add(x(a, t), -x(b, t))       # 5
    lo, hi = -(-(cap - max_diff) // 2), (cap + max_diff) // 2            # ceil((cap-d)/2), floor((cap+d)/2)
    women = [g for g in range(G) if inst["gender"][g] == "F"]
    men = [g for g in range(G) if inst["gender"][g] == "M"]
    for t in range(tables):
        at_most(cnf, [x(g, t) for g in women], hi)                       # 6: gra <= hi
        at_most(cnf, [x(g, t) for g in men], cap - lo)                   # 6: burra <= cap-lo  (gra >= lo)
    return cnf, x

def to_dimacs(cnf, path):
    with open(path, "w") as f:
        f.write(f"p cnf {cnf.n} {len(cnf.clauses)}\n")
        for c in cnf.clauses: f.write(" ".join(map(str, c)) + " 0\n")