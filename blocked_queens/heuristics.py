"""Heuristikat për A*. Gjendja = (k, placement): mbretëreshat janë vendosur në rreshtat 0..k-1,
placement[r] = kolona. Kosta e çdo veprimi = 1, pra g = k dhe h vlerëson sa mbetet (N - k)."""
INF = float("inf")

def free_cols(n, blocked, placement, r):
    """Kolonat e lira (jo të bllokuara, jo të sulmuara) në rreshtin r, si listë."""
    att = set()
    for i, c in enumerate(placement):
        d = r - i
        att.update((c, c + d, c - d))
    return [c for c in range(n) if c not in att and (r, c) not in blocked]

def h1(n, blocked, placement):
    """H1 (e thjeshtë): rreshtat e mbetur. Admissible dhe konsistente, por pa informacion shtesë."""
    return n - len(placement)

def h2(n, blocked, placement):
    """H2 (forward checking): nëse një rresht i mbetur nuk ka asnjë katror të lirë, gjendja nuk ka zgjidhje
    -> h = INF. Përndryshe N - k. Admissible (INF vetëm kur h* = INF)."""
    k = len(placement)
    for r in range(k, n):
        if not free_cols(n, blocked, placement, r): return INF
    return n - k

def h3(n, blocked, placement):
    """H3 (informuese, JO admissible): N - k + Σ 1/liri(r) mbi rreshtat e mbetur. Sa më pak katrorë të lirë,
    aq më e madhe h, kështu A* i shmang gjendjet e ngushta. Mbivlerëson, pra s'është admissible."""
    k = len(placement); total = n - k
    for r in range(k, n):
        f = len(free_cols(n, blocked, placement, r))
        if f == 0: return INF
        total += 1.0 / f
    return total

def h_adm(n, blocked, placement):
    """H* e propozuar (admissible): si H2, plus kushti i Hall-it: rreshtat e mbetur kanë nevojë për kolona të
    ndryshme, pra bashkimi i kolonave të lira duhet të ketë të paktën aq kolona sa rreshta mbeten.
    Të dyja janë kushte të domosdoshme për zgjidhje -> INF vetëm për gjendje pa zgjidhje, përndryshe N - k."""
    k = len(placement); union = set()
    for r in range(k, n):
        f = free_cols(n, blocked, placement, r)
        if not f: return INF
        union.update(f)
    return INF if len(union) < n - k else n - k

HEURISTICS = {"H1": h1, "H2": h2, "H3": h3, "H_adm": h_adm}