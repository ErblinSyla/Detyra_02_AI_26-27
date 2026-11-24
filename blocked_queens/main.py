import sys, random
from instance import parse_asp, random_instance, EXAMPLE, show
from heuristics import HEURISTICS, INF
from astar import astar, true_h

def valid(n, blocked, q):
    return (len(q) == n and len(set(q)) == n and all((r, c) not in blocked for r, c in enumerate(q))
            and all(abs(q[i] - q[j]) != j - i for i in range(n) for j in range(i + 1, n)))

def check_admissible(n, blocked, samples=300, seed=1):
    """Kontroll empirik: h(s) <= h*(s) për gjendje të rastit (përfshirë ato pa zgjidhje: h* = INF)."""
    rng, bad = random.Random(seed), {k: 0 for k in HEURISTICS}
    from heuristics import free_cols
    for _ in range(samples):
        pl = ()
        for _ in range(rng.randint(0, n)):
            f = free_cols(n, blocked, pl, len(pl))
            if not f: break
            pl += (rng.choice(f),)
        hs = true_h(n, blocked, pl)
        for name, h in HEURISTICS.items():
            if h(n, blocked, pl) > hs + 1e-9: bad[name] += 1
    return bad

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        n, blocked = parse_asp(EXAMPLE)
    elif len(sys.argv) > 1 and sys.argv[1].endswith(".lp"):
        n, blocked = parse_asp(open(sys.argv[1]).read())
    else:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        k = int(sys.argv[2]) if len(sys.argv) > 2 else n
        seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        n, blocked = random_instance(n, k, seed)
    print(f"N={n}, të bllokuara={sorted((r + 1, c + 1) for r, c in blocked)}")
    for name, h in HEURISTICS.items():
        sol, st = astar(n, blocked, h)
        ok = sol is not None and valid(n, blocked, sol)
        print(f"{name:6} | zgjidhje={'po' if sol else 'jo'} e vlefshme={ok} | {st}")
        if sol and name == "H_adm": show(n, blocked, sol)
    print("Shkelje të admissibility (h > h*) mbi 300 gjendje:", check_admissible(n, blocked))