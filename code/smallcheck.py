"""Independent ordinary domination polynomial checks for the majority construction."""
from itertools import combinations
from math import comb

def require(condition, label):
    """Fail loudly (also under python -O) when a check does not hold."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {label}")


def incidence(m):
    # Label four variables per cell: one left singleton, then three right variables.
    clauses = []
    for i in range(m):
        right = [4*i+j for j in [1,2,3]]
        for left in [4*i,4*((i+1)%m)]:
            for y,z in combinations(right,2):
                clauses.append((1<<left) | (1<<y) | (1<<z))
    return 4*m, clauses


def closed_neighbourhoods(k, clauses, split):
    variable_mask=(1<<k)-1
    neighbourhoods=[variable_mask if split else 1<<i for i in range(k)]
    for j,mask in enumerate(clauses,k):
        neighbourhoods.append((1<<j)|mask)
        for i in range(k):
            if mask & (1<<i): neighbourhoods[i] |= 1<<j
    return neighbourhoods


def brute(k, clauses, split):
    cells=closed_neighbourhoods(k,clauses,split)
    counts=[0]*(len(cells)+1)
    for selected in range(1<<len(cells)):
        if all(mask & selected for mask in cells):
            counts[selected.bit_count()]+=1
    return counts


def inclusion_exclusion(k, clauses, split):
    n=k+len(clauses)
    variable_mask=(1<<k)-1
    counts=[0]*(n+1)
    for selected in range(1<<k):
        forced=[q for q in clauses if not (q&selected)]
        missing=0 if split and selected else variable_mask^selected
        for q in forced: missing &= ~q
        base=selected.bit_count()+len(forced)
        forbidden=missing
        while True:
            # Each forbidden variable has NO selected independent neighbour.
            free=len(clauses)-len(forced)-sum(bool(q&forbidden) for q in clauses)
            sign=(-1)**forbidden.bit_count()
            for j in range(free+1):
                counts[base+j]+=sign*comb(free,j)
            if not forbidden: break
            forbidden=(forbidden-1)&missing
    return counts


if __name__=='__main__':
    for m in [2,3]:
        k,clauses=incidence(m)
        for split in [False,True]:
            counts=inclusion_exclusion(k,clauses,split)
            if m==2: require(brute(k,clauses,split)==counts, 'brute force equals inclusion-exclusion')
            print(m,'split' if split else 'bipartite',counts)
    # A third independent transfer fingerprint, by summing variable selections.
    for m, expected in [(2, 614369), (3, 480239953), (4, 376038400961)]:
        k, clauses = incidence(m)
        total = 0
        for selected in range(1 << k):
            forced = sum(not (clause & selected) for clause in clauses)
            total += 1 << (len(clauses) - forced)
        require(total == expected, 'total == expected')
        print(f"m={m}, s=1, split total={total}")
