"""Instanca: mysafirët, gjinia, çiftet e ndaluara dhe çiftet që duhet të ulen bashkë."""
import random

def random_instance(guests=100, women=50, conflicts=40, together=10, seed=1):
    """Gjenerim i rastit. Mysafirët 0..guests-1; të parët `women` janë gra (F), të tjerët burra (M)."""
    rng = random.Random(seed)
    gender = ["F"] * women + ["M"] * (guests - women)
    pairs = set()
    while len(pairs) < conflicts + together:
        a, b = rng.sample(range(guests), 2)
        pairs.add((min(a, b), max(a, b)))
    pairs = sorted(pairs); rng.shuffle(pairs)
    return {"guests": guests, "gender": gender, "conflicts": pairs[:conflicts], "together": pairs[conflicts:]}