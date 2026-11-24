# AI index: Domination polynomials with many peaks (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is
a plain introduction with a plan of the paper). DOI 10.5281/zenodo.24511988 (concept 10.5281/zenodo.24511987).
Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

Graphs finite, simple, undirected; n = number of vertices. S dominates G when every vertex is in S or adjacent to a
vertex of S. d_k(G) = number of dominating sets of size k; D_G(z) = sum_k d_k z^k (domination polynomial).
avd(G) = D_G'(1)/D_G(1) (average size of a uniform dominating set). Global mode = index of a largest d_k. Peak region =
maximal run of indices forming a local maximum, separated from the next by a strictly lower coefficient.
G_{m,s} (split) and B_{m,s} (bipartite): Section 2; h = ms, P = 6ms^2, N = P + 4h vertices; pure families A and C have
H = 2^{P+3h} members each. The explicit example is m = 128, s = 20: N = 317,440, H = 2^314880. log2 = binary logarithm.
AP = Alikhani-Peng, arXiv:0905.2251 (Ars Combin. 114 (2014)). BB = Beaton-Brown, doi:10.1007/s00373-022-02487-x.
BK = Bhattacharyya-Kahn, doi:10.37236/3034. Omar = arXiv:2601.14494.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A (main) | Connected split graph G_{128,20} and connected bipartite graph B_{128,20} on 317,440 vertices with d_160080 > d_160320 < d_160560 (AP conjecture false) | Theorem 1.1; Sections 2-3 | exact integer certificate plus written proof of the reduction; new |
| B | Larger graph (order 202,375,168) shown nonunimodal without a computer | Proposition 4.2; Section 4 | written proof |
| C (main) | Connected split and bipartite graphs with at least c sqrt(n)/log n peak regions; bipartite with maximum degree O(log n); explicit four peaks at n = 4,857,004,032 (also 8 and 16 peaks) | Theorem 1.2; Section 5 | written proof; explicit instances checked exactly; analogue of a BK remark for independent sets |
| D (main) | Every global mode at distance >= cn from avd for infinitely many n (constant of order 1e-25) | Theorem 1.3(a); Section 6; Remark 6.1 | written proof; answers the second half of BB's question |
| E (main) | For G_{128,20}: 160323.034984 <= avd <= 160323.034985; no global mode in [160217, 160412]; every global mode differs from avd by more than 88 | Theorem 1.3(b); Section 3.4 | certified computation (outward-rounded dual numbers, exact scan of the excluded interval); answers the first half of BB's question |
| F | Single-site Glauber dynamics on dominating sets mixes in time e^{Omega(n)} on the Section 6 graphs | Proposition 6.3 | written proof |
| G (main) | Nonunimodal connected split and bipartite graphs with delta/log2 n -> 1/2 | Theorem 1.4(i); Section 7, Lemma 7.1 | written proof |
| H (main) | sum_v (deg v + 2) 2^{-deg v - 1} <= 1 implies unimodal with a global mode at ceil(n/2); hence delta >= log2 n + log2 log2 n + 1 suffices for n >= 4 | Theorem 1.4(ii); Section 8; Corollary 8.2 | written proof; rising half is BB Proposition 2.4, union bound is Omar Proposition 9 (credited); repair bound new |
| I (main) | Least degree c(n) forcing a central global mode: L + log2 L - 3 <= c(n) <= L + log2 L + 2 (even n >= 2^20), L + log2 L - 4 <= c(n) <= L + log2 L + 2 (odd n >= 2^40), L = log2 n | Theorem 1.4(iii); Section 9, Lemma 9.1 | written proof; concerns the position of the maximum, not unimodality |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| Dyadic upper bound R = 2465924464317133610055229/2^80 on tr(T^128); integer bounds 1556-1615, 1482-1541, 1565-1624 (units 1e-6 H) at k = 160080, 160320, 160560; valley 1541 < 1556 and 1541 < 1565 | [code/verify_witness.py](code/verify_witness.py) | [results/certificate-output.txt](results/certificate-output.txt) | exact integers; holds for both graphs |
| Edge list of B_{128,20} (shipped as plain text; check_graph.py reads the gzip form written by graph_family.py): 921,600 edges, bipartition 10,240 / 307,200, degrees 3..120 (every clause vertex degree 3), connected, SHA-256 0654a33f...a77e | [code/check_graph.py](code/check_graph.py) + [data/](data/) | [results/graph-check-output.txt](results/graph-check-output.txt) | exact |
| Edge list generated from the construction; decompressed output equals the shipped plain text (SHA-256 in data/graph-metadata.json) | [code/graph_family.py](code/graph_family.py) | [data/bipartite-example.edgelist](data/bipartite-example.edgelist) | exact |
| G_{m,s}, B_{m,s} for (m, s) = (2, 1): every coefficient by enumeration of all 2^20 subsets equals inclusion-exclusion; split totals 614369, 480239953, 376038400961 for m = 2, 3, 4 | [code/smallcheck.py](code/smallcheck.py) | [results/smallcheck-output.txt](results/smallcheck-output.txt) | exact |
| Section 8 bound on all 33,867 labelled graphs of orders 1-6; 63 satisfy the weighted criterion, each with a decreasing central tail; Section 9 circulant parameters b = 4..79 | [code/check_criteria.py](code/check_criteria.py) | [results/criteria-output.txt](results/criteria-output.txt) | exact |
| Transfer identity and mean against enumeration for (2,1), (3,1), (4,1), (2,2); certified avd of G_{128,20} and the excluded interval [160217, 160412]; K = 4, 8, 16 peak instances (outer >= 0.929 W, middle <= 0.177 W at K = 4); Section 9 instances b = 4, 5, 6 and grid minima 2.6142 (even), 2.5094 (odd) | [code/check_extensions.py](code/check_extensions.py) | [results/extensions-output.txt](results/extensions-output.txt), [results/extensions.json](results/extensions.json) | exact integers, fractions and outward-rounded dyadics; float fields are printed summaries |

Numbers quoted on the release page: 317,440 vertices; indices 160,080, 160,320, 160,560; intervals 1556-1615,
1482-1541, 1565-1624; average size about 160,323 with no most frequent size within 88 of it; four peaks at
4,857,004,032 vertices; minimum degree about (1/2) log2 n for counterexamples and log2 n + log2 log2 n + 1 for
unimodality; previous requirement 2 log2 n. All in results/ or proved.

## Limits

The explicit example is large and not minimised. Theorem 1.3(a) needs astronomically large n and has a constant of
order 1e-25. The least minimum degree forcing unimodality lies between (1/2 + o(1)) log2 n and
log2 n + log2 log2 n + 1. Theorem 1.4(iii) concerns the central mode only. Trees and forests remain open. Open problems
in Section 10.

## Replay and records

Replay commands and cross-platform policy (text outputs byte for byte; in extensions.json the interpreter field is
excluded and float summaries compared to 1e-9 relative): [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt),
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI [.github/workflows/replay.yml](.github/workflows/replay.yml). Review:
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
Bibliography: [refs.bib](refs.bib). Licences: [LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff).
Hashes: [MANIFEST.sha256](MANIFEST.sha256).
