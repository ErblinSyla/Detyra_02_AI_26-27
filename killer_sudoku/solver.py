"""Zgjidhësi CSP: backtracking + propagim kufizimesh + MRV."""
from model import UNITS, cage_combos

POP = lambda m: bin(m).count("1")
LOW = lambda m: (m & -m).bit_length() - 1

class Killer:
    def __init__(self, cages):
        self.cages = cages
        self.cage_of = {}
        for k, (s, cells) in enumerate(cages):
            for c in cells: self.cage_of[c] = k
        self.combos = [cage_combos(len(cells), s) for s, cells in cages]
        # «shokët» e një qelize: ata që nuk mund të kenë të njëjtën vlerë (rresht, kolonë, kuti, kafaz)
        self.peers = [set() for _ in range(81)]
        for u in UNITS:
            for a in u: self.peers[a].update(u)
        for s, cells in cages:
            for a in cells: self.peers[a].update(cells)
        for i in range(81): self.peers[i].discard(i)
        self.nodes = 0

    # ---------- propagimi ----------
    def propagate(self, dom, queue):
        """Zbaton kufizimet deri në fixpoint. Kthen False nëse ndonjë domain boshatiset."""
        while queue:
            i = queue.pop()
            if POP(dom[i]) == 1:                       # qeliza e caktuar -> hiq vlerën nga shokët
                v = dom[i]
                for j in self.peers[i]:
                    if dom[j] & v:
                        dom[j] &= ~v
                        if not dom[j]: return False
                        queue.append(j)
            k = self.cage_of[i]
            if not self.prune_cage(dom, k, queue): return False
        # vlera e fshehur (hidden single) në çdo njësi
        for u in UNITS:
            seen, twice = 0, 0
            for c in u:
                twice |= seen & dom[c]; seen |= dom[c]
            if seen != 0b1111111110: return False       # ndonjë shifër s'ka ku të shkojë
            once = seen & ~twice
            if once:
                for c in u:
                    m = dom[c] & once
                    if m and m != dom[c]:
                        if POP(m) > 1: return False
                        dom[c] = m; queue.append(c)
                if queue: return self.propagate(dom, queue)
        return True

    def prune_cage(self, dom, k, queue):
        """Kufizimi i shumës: lër vetëm kombinimet e shifrave që përputhen me domain-et aktuale."""
        s, cells = self.cages[k]
        assigned = 0
        for c in cells:
            if POP(dom[c]) == 1: assigned |= dom[c]
        free = [c for c in cells if POP(dom[c]) > 1]
        allowed = 0
        union_free = 0
        for c in free: union_free |= dom[c]
        for m in self.combos[k]:
            if m & assigned == assigned and (m & ~assigned) & ~union_free == 0:
                allowed |= m
        if not allowed:
            return False
        for c in cells:
            nd = dom[c] & allowed
            if not nd: return False
            if nd != dom[c]:
                dom[c] = nd; queue.append(c)
        return True

    # ---------- kërkimi ----------
    def solve(self, givens=None, limit=1):
        dom = [0b1111111110] * 81
        queue = list(range(81))
        sols = []
        if not self.propagate(dom, queue): return sols
        self._search(dom, sols, limit)
        return sols

    def _search(self, dom, sols, limit):
        self.nodes += 1
        # MRV: qeliza me domain më të vogël >1
        best, bs = -1, 10
        for i in range(81):
            p = POP(dom[i])
            if 1 < p < bs: best, bs = i, p
        if best < 0:
            sols.append([LOW(d) for d in dom]); return
        m = dom[best]
        while m and len(sols) < limit:
            v = m & -m; m ^= v
            nd = dom[:]; nd[best] = v
            if self.propagate(nd, [best]): self._search(nd, sols, limit)

def valid_solution(cages, grid):
    ok = all(sorted(grid[c] for c in u) == list(range(1, 10)) for u in UNITS)
    return ok and all(sum(grid[c] for c in cells) == s and len({grid[c] for c in cells}) == len(cells) for s, cells in cages)