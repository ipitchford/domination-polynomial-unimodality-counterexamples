"""Exact checks for the extensions in the revised manuscript.

Run with Python 3.9 or later (standard library only). Every comparison is made
with integers or fractions, and every failed check exits with status 1, also
under ``python -O``. Results are written as JSON (``--output``).

Checks:
  transfer  transfer-matrix value and derivative against direct enumeration of
            the split graphs G_{m,s} for (m,s) = (2,1), (3,1), (4,1), (2,2);
  mode      certified average size of a dominating set of G_{128,20} and an
            interval around it that contains no global mode (Theorem 3.3);
  peaks     the explicit parameters of Section 5 for K = 2, 4, 8, 16;
  sharp     small instances of the Section 9 graphs (even and odd order):
            regularity / degrees and pairwise closed-neighbourhood intersections,
            and the explicit analytic inequalities used for n >= 2^20 (even) and
            n >= 2^40 (odd).
"""
import argparse
import json
import sys
from fractions import Fraction
from itertools import combinations
from math import comb, log2, floor

FAILURES = []


def check(condition, label):
    if not condition:
        FAILURES.append(label)
        print("FAIL:", label)


def ceil_div(num, den):
    return -(-num // den)


# ---------------------------------------------------------------- transfer
def split_enumeration(m, s):
    """Return (D(1), D'(1)) for G_{m,s} by summing over variable selections."""
    # variables: cell i has singletons L_i (s) and triples R_i (s triples)
    var = 0
    L, R = [], []
    for i in range(m):
        L.append(list(range(var, var + s)))
        var += s
        triples = []
        for _ in range(s):
            triples.append((var, var + 1, var + 2))
            var += 3
        R.append(triples)
    clauses = []
    for i in range(m):
        singles = L[i] + L[(i + 1) % m]
        for t in R[i]:
            for u in singles:
                for q in combinations(t, 2):
                    clauses.append((1 << u) | (1 << q[0]) | (1 << q[1]))
    P = len(clauses)
    check(P == 6 * m * s * s, f"clause count m={m} s={s}")
    total = 0
    deriv = 0  # sum over dominating sets of their size
    for sel in range(1 << var):
        F = sum(1 for c in clauses if not (c & sel))
        w = 1 << (P - F)
        total += w
        # size = |sel| + F + (P-F)/2 on average over the free clauses
        deriv += w * (2 * (sel.bit_count() + F) + (P - F))
    return P, total, Fraction(deriv, 2)


def exact_transfer(m, s):
    """Exact tr(T^m) and its z-derivative (unnormalised: entries C(s,b) f^s)."""
    def f(c):
        return 4 + Fraction(3, 2 ** c) + Fraction(1, 2 ** (3 * c))

    def fp(c):
        return 9 + Fraction(3, 2 ** c) + Fraction(3 * c, 2 ** (c + 1)) + Fraction(3 * c, 2 ** (3 * c + 1))

    dim = s + 1
    T = [[comb(s, b) * f(a + b) ** s for b in range(dim)] for a in range(dim)]
    Tp = [[comb(s, b) * ((s - b) * f(a + b) ** s + s * f(a + b) ** (s - 1) * fp(a + b))
           for b in range(dim)] for a in range(dim)]
    A = [[Fraction(int(i == j)) for j in range(dim)] for i in range(dim)]
    Ap = [[Fraction(0)] * dim for _ in range(dim)]
    for _ in range(m):
        A, Ap = ([[sum(A[i][k] * T[k][j] for k in range(dim)) for j in range(dim)] for i in range(dim)],
                 [[sum(A[i][k] * Tp[k][j] + Ap[i][k] * T[k][j] for k in range(dim)) for j in range(dim)]
                  for i in range(dim)])
    return sum(A[i][i] for i in range(dim)), sum(Ap[i][i] for i in range(dim))


def run_transfer():
    rows = []
    for m, s in [(2, 1), (3, 1), (4, 1), (2, 2)]:
        P, total, deriv = split_enumeration(m, s)
        tr, trp = exact_transfer(m, s)
        # D(1) = 2^P * tr(T^m) and D'(1)/D(1) = P/2 + trp/tr
        ok_total = tr * 2 ** P == total
        mean_enum = deriv / total
        mean_tr = Fraction(P, 2) + trp / tr
        check(ok_total, f"transfer total m={m} s={s}")
        check(mean_enum == mean_tr, f"transfer mean m={m} s={s}")
        rows.append({"m": m, "s": s, "total": total, "mean": f"{mean_enum.numerator}/{mean_enum.denominator}",
                     "mean_float": float(mean_enum), "total_matches": ok_total,
                     "mean_matches": mean_enum == mean_tr})
        print(f"transfer m={m} s={s}: total {total} matches={ok_total}; mean {float(mean_enum):.6f} matches={mean_enum == mean_tr}")
    return rows


# ---------------------------------------------------------------- mode
def dual_bounds(m, s, bits, up):
    """Dyadic bound (rounded down if up=False, up if up=True) on tr(T^m) and its
    derivative, with T normalised by 8^s per entry. All entries are nonnegative."""
    unit = 1 << bits

    def rnd(x):
        return ceil_div(x.numerator * unit, x.denominator) if up else (x.numerator * unit) // x.denominator

    def f(c):
        return (4 + Fraction(3, 2 ** c) + Fraction(1, 2 ** (3 * c))) / 8

    def fp(c):
        return (9 + Fraction(3, 2 ** c) + Fraction(3 * c, 2 ** (c + 1)) + Fraction(3 * c, 2 ** (3 * c + 1))) / 8

    dim = s + 1
    T = [[rnd(comb(s, b) * f(a + b) ** s) for b in range(dim)] for a in range(dim)]
    Tp = [[rnd(comb(s, b) * ((s - b) * f(a + b) ** s + s * f(a + b) ** (s - 1) * fp(a + b)))
           for b in range(dim)] for a in range(dim)]

    def div(x):
        return ceil_div(x, unit) if up else x // unit

    def mul(A, Ap, B, Bp):
        cols = list(zip(*B))
        colsp = list(zip(*Bp))
        C = [[div(sum(x * y for x, y in zip(row, col))) for col in cols] for row in A]
        Cp = [[div(sum(x * y for x, y in zip(row, colp)) + sum(x * y for x, y in zip(rowp, col)))
               for col, colp in zip(cols, colsp)] for row, rowp in zip(A, Ap)]
        return C, Cp

    acc, accp = None, None
    base, basep = T, Tp
    e = m
    while e:
        if e & 1:
            if acc is None:
                acc, accp = base, basep
            else:
                acc, accp = mul(acc, accp, base, basep)
        e >>= 1
        if e:
            base, basep = mul(base, basep, base, basep)
    return sum(acc[i][i] for i in range(dim)), sum(accp[i][i] for i in range(dim)), unit


def mixed_binomial_coefficient(u, h, degree):
    """Coefficient of z^degree in (1+z)^u (3+z)^h (exact integers)."""
    lo = max(0, degree - u)
    hi = min(h, degree)
    if lo > hi:
        return 0
    j = degree - lo
    first = comb(u, j)
    second = comb(h, lo) * 3 ** (h - lo)
    total = 0
    for ell in range(lo, hi + 1):
        total += first * second
        if ell < hi:
            first = first * j // (u - j + 1)
            second = second * (h - ell) // (3 * (ell + 1))
            j -= 1
    return total


def run_mode(m=128, s=20, bits=80):
    h, P = m * s, 6 * m * s * s
    n = P + 4 * h
    # validate the rounded dual computation on a small case against exact arithmetic
    tr_e, trp_e = exact_transfer(4, 2)
    lo_t, lo_tp, u = dual_bounds(4, 2, 60, up=False)
    up_t, up_tp, _ = dual_bounds(4, 2, 60, up=True)
    scale = Fraction(8 ** (2 * 4))  # normalisation 8^s per block, m blocks
    check(Fraction(lo_t, u) <= tr_e / scale <= Fraction(up_t, u), "dual rounding brackets trace (4,2)")
    check(Fraction(lo_tp, u) <= trp_e / scale <= Fraction(up_tp, u), "dual rounding brackets derivative (4,2)")

    lo_t, lo_tp, unit = dual_bounds(m, s, bits, up=False)
    up_t, up_tp, _ = dual_bounds(m, s, bits, up=True)
    mean_lo = Fraction(P, 2) + Fraction(lo_tp, up_t)
    mean_hi = Fraction(P, 2) + Fraction(up_tp, lo_t)
    print(f"avd(G_{{{m},{s}}}) in [{float(mean_lo):.6f}, {float(mean_hi):.6f}]")
    check(mean_hi - mean_lo < 1, "mean interval shorter than one")

    # coefficient bracket, as in verify_witness.py (valid for every k)
    phase = 1 << (P + 3 * h)
    trace_up, unit2 = up_t, unit
    excess = ceil_div(phase * (trace_up - 2 * unit2), unit2) + (phase >> h)
    free = P - 2 * h
    upper_error = ceil_div(excess * comb(free, free // 2), 1 << free) + (phase >> h)
    lower_error = (phase >> h) + 8 * h * (phase >> (4 * s))

    def pure(k):
        return comb(P + 3 * h, k - h) + mixed_binomial_coefficient(P + h, h, k - 2 * h)

    # best certified lower bound over a grid around the two phase centres
    mu_A, mu_C = P // 2 + 5 * h // 2, P // 2 + 11 * h // 4
    best_k, best_low = None, -1
    for k in list(range(mu_A - 200, mu_A + 201, 10)) + list(range(mu_C - 200, mu_C + 201, 10)):
        low = pure(k) - lower_error
        if low > best_low:
            best_k, best_low = k, low
    # scan outwards from the mean interval
    centre_lo = mean_lo.numerator // mean_lo.denominator          # floor
    centre_hi = ceil_div(mean_hi.numerator, mean_hi.denominator)  # ceil
    excluded_lo = centre_lo
    k = centre_lo
    while pure(k) + upper_error < best_low:
        excluded_lo = k
        k -= 1
    excluded_hi = centre_hi
    k = centre_hi
    while pure(k) + upper_error < best_low:
        excluded_hi = k
        k += 1
    ok_centre = all(pure(j) + upper_error < best_low for j in range(centre_lo, centre_hi + 1))
    check(ok_centre, "indices around the average are not modes")
    r_left = mean_lo - excluded_lo   # every k >= excluded_lo, k <= excluded_hi is excluded
    r_right = excluded_hi - mean_hi
    radius = min(r_left, r_right)
    print(f"best lower bound at k={best_k}: {(10 ** 6 * best_low) // phase} e-6 H (floor)")
    print(f"no global mode in [{excluded_lo}, {excluded_hi}]; distance from avd > {float(radius):.3f}")
    check(radius > 88, "mode-mean distance greater than 88")
    return {
        "m": m, "s": s, "order": n,
        "avd_lower": f"{mean_lo.numerator}/{mean_lo.denominator}", "avd_lower_float": float(mean_lo),
        "avd_upper": f"{mean_hi.numerator}/{mean_hi.denominator}", "avd_upper_float": float(mean_hi),
        "best_lower_index": best_k, "best_lower_millionths_H": (10 ** 6 * best_low) // phase,
        "excluded_interval": [excluded_lo, excluded_hi],
        "distance_lower_bound_float": float(radius),
        "distance_lower_bound_floor": int(radius),
    }


# ---------------------------------------------------------------- peaks
def run_peaks():
    rows = []
    for a in [1, 2, 3, 4]:
        K = 2 ** a
        m = 4096 * K
        s = 16 * (-(-4 * a // 1))  # 16*ceil(4 log2 K), log2 K = a
        q = -(-int(s ** 0.5 * 10 ** 0) // 1)
        q = 1
        while q * q < s:
            q += 1  # q = ceil(sqrt s)
        e = (Fraction(2, 2 ** s) * sum(comb(s, j) for j in range(q))
             + 2 * sum(comb(s, j) * (Fraction(1, 2) + Fraction(1, 2 ** (j + 1))) ** s for j in (1, 2, 3))
             + Fraction(25, 32) ** s)
        theta = Fraction(1, 2 ** (q * q))
        rhos = []
        lemma_ok = True
        for i in range(a):
            mi = 2 ** i * m
            C = mi * (mi + 1)
            if not (C * e < 1 and C * theta < 1):
                lemma_ok = False
                break
            rhos.append(1 / ((1 - C * e) * (1 - C * theta)) - 1)
        if not lemma_ok:
            rows.append({"K": K, "lemma_hypotheses": False})
            continue
        rho = max(rhos)
        residual = a * rho * (2 + rho) ** (a - 1)
        v = (Fraction(3, 2) * s * s + s) * m * (K - 1)
        d = Fraction(m * s, 4)
        ratio = v / (d * d)
        loss = Fraction(4 * m * s * (K - 1), 2 ** (4 * s))   # bipartite union bound
        outer = 1 - 16 * ratio - loss
        middle = 40 * ratio + residual
        n = (6 * s * s + 4 * s) * m * (K - 1)
        ok = ratio < Fraction(1, 160) and outer > middle
        check(ok, f"Section 5 windows K={K}")
        rows.append({"K": K, "m": m, "s": s, "q": q, "order": n, "max_degree_bipartite": 6 * s + 2,
                     "v_over_d2": float(ratio), "rho_max": float(rho), "residual_over_W": float(residual),
                     "outer_lower_over_W": float(outer), "middle_upper_over_W": float(middle), "valid": ok})
        print(f"peaks K={K}: n={n}, s={s}, q={q}, rho_max={float(rho):.3e}, outer>={float(outer):.4f}, middle<={float(middle):.4f}, valid={ok}")
    return rows


# ---------------------------------------------------------------- sharp
def sidon_shifts(b):
    return [2 * b * b * j + j * j for j in range(b - 1)]


def even_graph(b, half):
    """Bipartite circulant graph on two copies of Z_half; returns closed neighbourhoods."""
    shifts = sidon_shifts(b)
    nb = [set([v]) for v in range(2 * half)]
    for x in range(half):
        for d in shifts:
            y = half + (x + d) % half
            nb[x].add(y)
            nb[y].add(x)
    return nb


def odd_graph(b, half, M):
    nb = even_graph(b, half)
    v = len(nb)
    nb.append(set([v]))
    for i in range(b - 1):
        x = i * M
        nb[v].add(x)
        nb[x].add(v)
    return nb


def max_pair_intersection(nb):
    n = len(nb)
    # pairs at distance <= 2 are the only ones that can intersect
    best = 0
    for u in range(n):
        near = set()
        for w in nb[u]:
            near |= nb[w]
        for w in near:
            if w > u:
                best = max(best, len(nb[u] & nb[w]))
    return best


def connected(nb):
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for w in nb[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(nb)


def run_sharp():
    rows = []
    for b in [4, 5, 6]:
        maxd = max(sidon_shifts(b))
        half = 4 * maxd + 1
        nb = even_graph(b, half)
        degs = {len(x) - 1 for x in nb}
        inter = max_pair_intersection(nb)
        ok = degs == {b - 1} and inter <= 2 and connected(nb)
        check(ok, f"even Section 9 graph b={b}")
        M = 2 * maxd + 1
        half_o = max(half, (b - 1) * M + M)
        nbo = odd_graph(b, half_o, M)
        dego = sorted({len(x) - 1 for x in nbo})
        intero = max_pair_intersection(nbo)
        ok_o = len(nbo) % 2 == 1 and min(dego) == b - 1 and max(dego) == b and intero <= 2 and connected(nbo)
        check(ok_o, f"odd Section 9 graph b={b}")
        rows.append({"b": b, "even_order": len(nb), "even_max_intersection": inter, "even_ok": ok,
                     "odd_order": len(nbo), "odd_degrees": dego, "odd_max_intersection": intero, "odd_ok": ok_o})
        print(f"sharp b={b}: even n={len(nb)} max|N[u]^N[w]|={inter} ok={ok}; odd n={len(nbo)} degrees={dego} max={intero} ok={ok_o}")

    # Explicit analytic inequalities (Section 9), evaluated on a grid of L = log2 n.
    def even_bound(L):
        b = floor(L + log2(L) - 2)
        n = 2 ** L
        return (4 * b / L) * (1 - b * b / n) * (1 - 8 / L - 32 * (b + 1) ** 2 / (n * L)), b

    def odd_bound(L):
        b = floor(L + log2(L) - 3)
        n = 2 ** L
        return (4 * b / L) * (1 - (b + 1) * (b + 2) / n) * (1 - 16 / L - 64 * (b + 2) ** 2 / (n * L)), b

    grid_even = [20 + 0.25 * i for i in range(0, 4 * 200)]
    grid_odd = [40 + 0.25 * i for i in range(0, 4 * 200)]
    min_even = min(even_bound(L)[0] for L in grid_even)
    min_odd = min(odd_bound(L)[0] for L in grid_odd)
    dist_even = all(4 * (2 * b * b * (b - 2) + (b - 2) ** 2) < 2 ** L for L in grid_even for b in [even_bound(L)[1]])
    check(min_even > 1, "even analytic bound > 1 on grid")
    check(min_odd > 2, "odd analytic bound > 2 on grid")
    check(dist_even, "distinct differences modulo n/2 on grid")
    print(f"sharp analytic: min even bound {min_even:.4f} (>1), min odd bound {min_odd:.4f} (>2)")
    return {"instances": rows, "even_grid_min": min_even, "odd_grid_min": min_odd}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=None)
    parser.add_argument("--skip-mode", action="store_true")
    args = parser.parse_args()
    out = {"python": sys.version.split()[0]}
    out["transfer"] = run_transfer()
    if not args.skip_mode:
        out["mode"] = run_mode()
    out["peaks"] = run_peaks()
    out["sharp"] = run_sharp()
    out["failures"] = FAILURES
    if args.output:
        with open(args.output, "w") as fh:
            json.dump(out, fh, indent=2)
    if FAILURES:
        print("FAILED:", FAILURES)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
