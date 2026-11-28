"""Killer Sudoku si CSP.

Variablat:  81 qelizat (indeksi i = 9*rreshti + kolona).
Domain:     {1..9} për secilën (përfaqësohet si bitmask: bit d ndezur = vlera d e mundshme).
Kufizimet:  (1) all-different në 9 rreshta, 9 kolona, 9 kuti 3x3;
            (2) për çdo kafaz (cage): vlerat e qelizave të tij janë të ndryshme dhe shuma e tyre = shuma e kafazit.
"""
from itertools import combinations

ROWS = [[9 * r + c for c in range(9)] for r in range(9)]
COLS = [[9 * r + c for r in range(9)] for c in range(9)]
BOXES = [[9 * (3 * br + r) + 3 * bc + c for r in range(3) for c in range(3)] for br in range(3) for bc in range(3)]
UNITS = ROWS + COLS + BOXES

def parse(layout, sums):
    """layout: 9 rreshta me 9 shkronja/shifra (id e kafazit të çdo qelize); sums: {id: shuma}. -> listë (shuma, [qelizat])."""
    cells = {}
    for r, row in enumerate(layout):
        for c, ch in enumerate(row): cells.setdefault(ch, []).append(9 * r + c)
    assert set(cells) == set(sums), "çdo kafaz duhet të ketë shumë"
    assert sum(sums.values()) == 405, "shuma e të gjitha kafazeve duhet të jetë 405"
    return [(sums[k], cells[k]) for k in sorted(cells)]

def cage_combos(n, s):
    """Të gjitha bashkësitë e n shifrave të ndryshme (1..9) me shumë s, si bitmask-e."""
    return [sum(1 << d for d in comb) for comb in combinations(range(1, 10), n) if sum(comb) == s]