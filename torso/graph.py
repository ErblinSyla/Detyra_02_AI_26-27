"""Leximi i grafit nga skedari me listë skajesh (çdo rresht: «u v») dhe gjenerim i rastit për testim."""
import random

def load(path):
    edges = set()
    for line in open(path):
        p = line.split()
        if len(p) == 2 and p[0].isdigit() and p[1].isdigit() and p[0] != p[1]:
            u, v = int(p[0]), int(p[1]); edges.add((min(u, v), max(u, v)))
    return build(edges)

def build(edges):
    n = max(max(e) for e in edges) + 1
    adj = [set() for _ in range(n)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    return n, [sorted(a) for a in adj]

def random_graph(n=300, m=700, seed=0):
    rng, edges = random.Random(seed), set()
    for v in range(1, n): edges.add((rng.randrange(v), v))      # peme -> grafi është i lidhur
    while len(edges) < m:
        u, v = rng.sample(range(n), 2); edges.add((min(u, v), max(u, v)))
    return build(edges)