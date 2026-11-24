"""Integer certificate for three coefficients of two ordinary domination polynomials.

Run with Python 3.9 or later. Assertions implement all comparisons as integers.
Numbers in the output table are bounds in millionths of one pure-family count.
"""
from math import comb

def require(condition, label):
    """Fail loudly (also under python -O) when a check does not hold."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {label}")


def ceil_div(num, den):
    return -(-num // den)


def matrix_upper_trace(s, m, bits=80):
    """Return a dyadic upper bound on the normalised partition function."""
    unit = 1 << bits
    dim = s + 1
    def entry(a, b):
        deg = a + b
        num = (4 << (3 * deg)) + (3 << (2 * deg)) + 1
        den = 8 << (3 * deg)
        return ceil_div(unit * comb(s, b) * num**s, den**s)

    def multiply(left, right):
        columns = list(zip(*right))
        return [[ceil_div(sum(x*y for x, y in zip(row, col)), unit)
                 for col in columns] for row in left]

    base = [[entry(a, b) for b in range(dim)] for a in range(dim)]
    acc = [[unit * int(i == j) for j in range(dim)] for i in range(dim)]
    while m:
        if m % 2:
            acc = multiply(acc, base)
        m //= 2
        if m:
            base = multiply(base, base)
    return sum(acc[i][i] for i in range(dim)), unit


def mixed_binomial_coefficient(u, h, degree):
    """Coefficient of (1+z)^u (3+z)^h, using neighbouring binomial ratios."""
    lo = max(0, degree-u)
    hi = min(h, degree)
    if lo > hi:
        return 0
    j = degree-lo
    first = comb(u, j)
    second = comb(h, lo) * 3**(h-lo)
    total = 0
    for ell in range(lo, hi+1):
        total += first * second
        if ell < hi:
            first = first * j // (u - j + 1)
            second = second * (h-ell) // (3*(ell+1))
            j -= 1
    return total


def main():
    s, m = 20, 128
    h, p = m*s, 6*m*s*s
    scale = 10**6
    phase = 1 << (p + 3*h)
    trace, unit = matrix_upper_trace(s, m)
    # split count H*(trace(T^m)-2+2^-h) outside both pure families
    excess = ceil_div(phase * (trace-2*unit), unit) + (phase >> h)
    free = p - 2*h
    peak_numerator = comb(free, free//2)
    # Low-forcing and high-forcing residuals, respectively.
    upper_error = ceil_div(excess*peak_numerator, 1 << free) + (phase >> h)
    # Remove the overlap, and a union bound on uncovered variables in each
    # of two pure families of the graph without clique edges.
    lower_error = (phase >> h) + 8*h*(phase >> (4*s))
    print(f"m={m} s={s} P={p} V={p+4*h} H=2^{p+3*h}")
    print(f"trace numerator {trace} denominator {unit}")
    print("index   lower   upper   (units of H/1000000)")
    rows = []
    for k in (160080, 160320, 160560):
        pure = comb(p+3*h, k-h) + mixed_binomial_coefficient(p+h, h, k-2*h)
        lower = scale*(pure-lower_error)//phase
        upper = ceil_div(scale*(pure+upper_error), phase)
        rows.append((lower, upper))
        print(k, lower, upper)
    require(rows[1][1] < min(rows[0][0], rows[2][0]), 'rows[1][1] < min(rows[0][0], rows[2][0])')


if __name__ == "__main__":
    main()
