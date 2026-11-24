"""Exact small checks for the pivotal criterion and the circulant construction.

Run with Python 3. No third-party packages are required.
These checks supplement the proofs in Sections 8 and 9 of manuscript.tex.
"""

from itertools import combinations
from math import comb, gcd

def require(condition, label):
    """Fail loudly (also under python -O) when a check does not hold."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {label}")


def domination_coefficients(closed_neighbourhoods):
    """Enumerate every vertex subset using its closed-neighbourhood union."""
    order = len(closed_neighbourhoods)
    all_vertices = (1 << order) - 1
    unions = [0] * (1 << order)
    coefficients = [0] * (order + 1)
    for selected in range(1, 1 << order):
        last_bit = selected & -selected
        vertex = last_bit.bit_length() - 1
        unions[selected] = (
            unions[selected ^ last_bit] | closed_neighbourhoods[vertex]
        )
        if unions[selected] == all_vertices:
            coefficients[selected.bit_count()] += 1
    return coefficients


def check_pivotal_criterion():
    graph_count = 0
    sufficient_condition_count = 0
    for order in range(1, 7):
        edges = list(combinations(range(order), 2))
        binomials = [
            [comb(top, k) if k <= top else 0 for k in range(order + 1)]
            for top in range(order + 1)
        ]
        for edge_selection in range(1 << len(edges)):
            closed = [1 << vertex for vertex in range(order)]
            for position, (left, right) in enumerate(edges):
                if edge_selection & (1 << position):
                    closed[left] |= 1 << right
                    closed[right] |= 1 << left
            coefficients = domination_coefficients(closed)
            sizes = [neighbourhood.bit_count() for neighbourhood in closed]
            for k in range(order):
                crossing = (
                    (k + 1) * coefficients[k + 1]
                    - (order - k) * coefficients[k]
                )
                upper_bound = sum(
                    size * binomials[order - size][k] for size in sizes
                )
                require(0 <= crossing <= upper_bound, '0 <= crossing <= upper_bound')

            # Multiply the sufficient inequality by 2**order to stay exact.
            weighted_sum = sum((size + 1) << (order - size) for size in sizes)
            if weighted_sum <= 1 << order:
                sufficient_condition_count += 1
                for k in range((order + 1) // 2, order):
                    require(coefficients[k + 1] <= coefficients[k], (order, edge_selection, k))
            graph_count += 1

    require(graph_count == 33867, 'graph_count == 33867')
    require(sufficient_condition_count == 63, 'sufficient_condition_count == 63')
    print(f"Pivotal bound passed for all {graph_count} labelled graphs of orders 1–6.")
    print(
        "The weighted degree condition holds for "
        f"{sufficient_condition_count} graphs, each with a decreasing central tail."
    )


def check_circulant_differences():
    for closed_neighbourhood_size in range(4, 80):
        b = closed_neighbourhood_size
        shifts = [2 * b * b * j + j * j for j in range(b - 1)]
        differences = [
            first - second
            for first in shifts
            for second in shifts
            if first != second
        ]
        require(len(set(differences)) == len(differences), 'len(set(differences)) == len(differences)')
        modulus = 4 * max(shifts) + 1
        require(len({difference % modulus for difference in differences}) == len(differences), b)
        require(gcd(shifts[1], shifts[2]) == 1, 'gcd(shifts[1], shifts[2]) == 1')
    print("Circulant difference and connectivity checks passed for b = 4, …, 79.")


if __name__ == "__main__":
    check_pivotal_criterion()
    check_circulant_differences()
