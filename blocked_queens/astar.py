"""A* për Blocked N-Queens (mbretëreshat vendosen rresht pas rreshti)."""
import heapq, time
from heuristics import free_cols, INF

def astar(n, blocked, h):
    """Kthen (placement ose None, statistikat). f = g + h, g = k. Barazim: g më i madh (më i thellë) së pari."""
    t0, counter, expanded, generated = time.time(), 0, 0, 1
    start = ()
    h0 = h(n, blocked, start)
    frontier = [(h0, 0, counter, start)]          # (f, -g, numërues, placement)
    max_frontier = 1
    while frontier:
        f, negg, _, placement = heapq.heappop(frontier)
        k = len(placement)
        if k == n:                                # goal test
            return list(placement), {"expanded": expanded, "generated": generated,
                                     "max_frontier": max_frontier, "cost": k, "time": round(time.time() - t0, 3)}
        expanded += 1
        for c in free_cols(n, blocked, placement, k):
            child = placement + (c,)
            hv = h(n, blocked, child)
            if hv == INF: continue                # gjendje pa zgjidhje: s'ka kuptim ta ruash
            counter += 1; generated += 1
            heapq.heappush(frontier, (len(child) + hv, -len(child), counter, child))
        max_frontier = max(max_frontier, len(frontier))
    return None, {"expanded": expanded, "generated": generated, "max_frontier": max_frontier,
                  "cost": None, "time": round(time.time() - t0, 3)}

def true_h(n, blocked, placement):
    """h* e vërtetë: n-k nëse gjendja ka zgjidhje (çdo zgjidhje kërkon n-k veprime të tjera), përndryshe INF.
    Llogaritet me DFS të plotë. Përdoret vetëm për kontrollin e admissibility."""
    k = len(placement)
    if k == n: return 0
    for c in free_cols(n, blocked, placement, k):
        if true_h(n, blocked, placement + (c,)) != INF: return n - k
    return INF