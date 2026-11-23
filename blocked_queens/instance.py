"""Instanca e Blocked N-Queens: madhësia N dhe katrorët e bllokuar."""
import random, re

def parse_asp(text):
    """Lexon formatin e ASP Competition: num(1). ... block(i,j). (indekset 1..N) -> (N, set e (r,c) 0-based)."""
    n = len(re.findall(r"num\(\d+\)", text))
    blocked = {(int(i) - 1, int(j) - 1) for i, j in re.findall(r"block\((\d+),\s*(\d+)\)", text)}
    return n, blocked

def random_instance(n, k, seed=0):
    """N katrorë të bllokuar të rastit (k copë)."""
    rng = random.Random(seed)
    cells = [(r, c) for r in range(n) for c in range(n)]
    return n, set(rng.sample(cells, k))

EXAMPLE = "num(1). num(2). num(3). num(4). block(1,1). block(2,2). block(4,3)."   # shembulli i faqes

def show(n, blocked, queens):
    """queens[r] = kolona e mbretëreshës në rreshtin r. X = e bllokuar, Q = mbretëreshë."""
    for r in range(n):
        print(" ".join("Q" if queens[r] == c else "X" if (r, c) in blocked else "." for c in range(n)))