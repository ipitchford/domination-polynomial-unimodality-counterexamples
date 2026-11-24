"""Read the supplied edge list and independently check the finite graph."""
import gzip
import hashlib
import json
from pathlib import Path

def require(condition, label):
    """Fail loudly (also under python -O) when a check does not hold."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {label}")

directory = Path(__file__).resolve().parent.parent / "data"
metadata = json.loads((directory/"graph-metadata.json").read_text())
n = metadata["vertices"]
boundary = metadata["bipartition_sizes"][0]
parents = list(range(n))
sizes = [1]*n
degrees = [0]*n


def find(vertex):
    while parents[vertex] != vertex:
        parents[vertex] = parents[parents[vertex]]
        vertex = parents[vertex]
    return vertex


def union(left, right):
    a, b = find(left), find(right)
    if a == b:
        return
    if sizes[a] < sizes[b]:
        a, b = b, a
    parents[b] = a
    sizes[a] += sizes[b]


count = 0
digest = hashlib.sha256()
with gzip.open(directory/"bipartite-example.edgelist.gz", "rb") as stream:
    for line in stream:
        digest.update(line)
        if line.startswith(b"#"):
            continue
        left, right = map(int, line.split())
        require(0 <= left < boundary <= right < n, '0 <= left < boundary <= right < n')
        degrees[left] += 1
        degrees[right] += 1
        union(left, right)
        count += 1

require(digest.hexdigest() == metadata["uncompressed_sha256"], 'digest.hexdigest() == metadata["uncompressed_sha256"]')
require(count == metadata["edges"], 'count == metadata["edges"]')
require(min(degrees) == metadata["minimum_degree"], 'min(degrees) == metadata["minimum_degree"]')
require(max(degrees) == metadata["maximum_degree"], 'max(degrees) == metadata["maximum_degree"]')
require(all(degree == 3 for degree in degrees[boundary:]), 'all(degree == 3 for degree in degrees[boundary:])')
require(len({find(vertex) for vertex in range(n)}) == 1, 'len({find(vertex) for vertex in range(n)}) == 1')
print(f"PASS: {n} vertices, {count} edges, connected and bipartite.")
print(f"Degree range {min(degrees)} to {max(degrees)}.")
print(f"Uncompressed SHA-256 {digest.hexdigest()}")
