"""Generate the bipartite graph from the manuscript by a streaming edge list."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

def require(condition, label):
    """Fail loudly (also under python -O) when a check does not hold."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {label}")


def edges(m, s):
    """Use vertices 0..4*m*s-1 for variables and consecutive clause IDs."""
    clause = 4*m*s
    for i in range(m):
        for j in (i, (i+1) % m):
            for a in range(s):
                singleton = 4*s*j+a
                for b in range(s):
                    triple = [4*s*i+s+3*b+c for c in range(3)]
                    for first, second in ((0, 1), (0, 2), (1, 2)):
                        yield singleton, clause
                        yield triple[first], clause
                        yield triple[second], clause
                        clause += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m", type=int, default=128)
    parser.add_argument("--s", type=int, default=20)
    parser.add_argument("--output", type=Path, default=Path("bipartite-example.edgelist.gz"))
    args = parser.parse_args()
    m, s = args.m, args.s
    if m < 2 or s < 1:
        parser.error("m must be at least 2 and s must be positive")
    variables = 4*m*s
    clauses = 6*m*s*s
    n = variables+clauses
    degree = [0]*n
    total = 0
    digest = hashlib.sha256()
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            header = f"# {n} vertices, {3*clauses} edges, zero-based labels\n".encode()
            stream.write(header)
            digest.update(header)
            for u, v in edges(m, s):
                require(0 <= u < variables <= v < n, '0 <= u < variables <= v < n')
                row = f"{u} {v}\n".encode()
                stream.write(row)
                digest.update(row)
                degree[u] += 1
                degree[v] += 1
                total += 1
    require(total == 3*clauses, 'total == 3*clauses')
    require(all(d == 3 for d in degree[variables:]), 'all(d == 3 for d in degree[variables:])')
    for i in range(m):
        require(degree[4*s*i:4*s*i+s] == [6*s]*s, 'degree[4*s*i:4*s*i+s] == [6*s]*s')
        require(degree[4*s*i+s:4*s*(i+1)] == [4*s]*(3*s), 'degree[4*s*i+s:4*s*(i+1)] == [4*s]*(3*s)')
    print(json.dumps({
        "m": m, "s": s, "vertices": n, "edges": total,
        "bipartition_sizes": [variables, clauses],
        "minimum_degree": min(degree), "maximum_degree": max(degree),
        "uncompressed_sha256": digest.hexdigest(),
        "output": args.output.name
    }, indent=2))


if __name__ == "__main__":
    main()
