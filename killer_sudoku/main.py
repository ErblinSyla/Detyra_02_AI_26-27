import sys, time
from model import parse
from solver import Killer, valid_solution
from puzzles import PUZZLES

def show(g):
    for r in range(9):
        if r % 3 == 0 and r: print("------+-------+------")
        row = g[9 * r:9 * r + 9]
        print(" | ".join(" ".join(map(str, row[k:k + 3])) for k in (0, 3, 6)))

if __name__ == "__main__":
    for lvl in (sys.argv[1:] or list(PUZZLES)):
        cages = parse(*PUZZLES[lvl])
        k = Killer(cages); t = time.time()
        sols = k.solve(limit=2)                 # limit=2: kontrollon edhe unicitetin
        print(f"\n== {lvl} | kafaze={len(cages)} | zgjidhje të gjetura (max 2)={len(sols)} | "
              f"nyje kërkimi={k.nodes} | {time.time() - t:.2f}s | e vlefshme={valid_solution(cages, sols[0])}")
        show(sols[0])