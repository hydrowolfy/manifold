"""Small numerical helpers."""
import math


def linfit(xs, ys):
    """Least-squares slope and intercept."""
    n = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    inter = (sy - slope * sx) / n
    return slope, inter


def pearson(xs, ys):
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    sy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return cov / (sx * sy) if sx * sy else 0.0


def mean(xs):
    return sum(xs) / len(xs) if xs else float('nan')
