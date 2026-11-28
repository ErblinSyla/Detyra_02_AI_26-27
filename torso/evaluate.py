"""Vlerësimi i një permutacioni π: lojë eliminimi (elimination game).

Skano π nga e majta në të djathtë. Kur takon u, fqinjët e tij PAS tij në π (outdegree) lidhen në klikë,
skajet e reja orientohen sipas π. Torso = n-t elementet e fundit. Gjerësia e torso = outdegree maksimal brenda torso.
Implementim: pozicionet janë bit-e në numra të plotë (bitset), kështu çdo bashkim bëhet me një operacion.
"""
try:
    popcount = int.bit_count
except AttributeError:
    popcount = lambda x: bin(x).count("1")

def outdegrees(order, adj):
    """outdeg[i] = outdegree i vertex-it në pozicionin i (përfshirë skajet e reja nga eliminimi)."""
    n = len(order)
    pos = [0] * n
    for i, v in enumerate(order): pos[v] = i
    bits = [0] * n                                   # bits[i] = fqinjët e vertex-it në pozicionin i, si pozicione
    for i, v in enumerate(order):
        b = 0
        for w in adj[v]: b |= 1 << pos[w]
        bits[i] = b
    out = [0] * n
    for i in range(n):
        higher = bits[i] >> (i + 1) << (i + 1)       # vetëm fqinjët me pozicion > i
        if higher:
            out[i] = popcount(higher)
            p = (higher & -higher).bit_length() - 1  # prindi = fqinji më i hershëm; trashëgon të tjerët (fill-in)
            bits[p] |= higher & ~(1 << p)
    return out

def suffix_max(out):
    """sw[t] = gjerësia e torso nëse prerja është t = max e outdegrees nga pozicioni t e tutje."""
    sw, m = [0] * len(out), 0
    for t in range(len(out) - 1, -1, -1):
        m = max(m, out[t]); sw[t] = m
    return sw

def area(sw, cap=501):
    """Σ_t min(sw[t], cap). Sa më e vogël, aq më i mirë fronti (ekuivalent me hipervëllimin: HV = Σ(cap - sw[t]))."""
    return sum(min(w, cap) for w in sw)

def evaluate(order, adj):
    out = outdegrees(order, adj); sw = suffix_max(out)
    return area(sw), sw