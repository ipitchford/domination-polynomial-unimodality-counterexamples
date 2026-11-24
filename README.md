# Domination polynomials with many peaks

*Counterexamples to the Alikhani–Peng conjecture and the minimum-degree scale for a central mode*

Explicit 317,440-vertex graphs whose dominating-set counts dip and rise again, with an exact integer certificate.

Version 0.1.0-candidate. DOI [10.5281/zenodo.24511988](https://doi.org/10.5281/zenodo.24511988) (all versions:
[10.5281/zenodo.24511987](https://doi.org/10.5281/zenodo.24511987)). Release page:
https://evidencepress.org/releases/domination-polynomial-unimodality-counterexamples/

**Status: unrefereed research candidate.** Author: Anonymous. Text CC0-1.0; code MIT (see [LICENSE.md](LICENSE.md)).

## What this is about

**The problem.** A *dominating set* in a network is a set of nodes such that every node is either in the set or
directly linked to one that is. Think of placing guards, transmitters or monitors so that every site is covered.
Counting the dominating sets of each size k gives a sequence d_0, d_1, ..., d_n (the coefficients of the *domination
polynomial*). For every network anyone had checked, this sequence rises to a single peak and then falls: it is
*unimodal*. Alikhani and Peng conjectured in 2009 that this is always so. Shape questions of this kind are basic for
graph polynomials and remain open for many of them.

**What was known.** The sequence always rises up to half the number of nodes, so any dip must happen in the upper half.
The conjecture was proved for paths, cycles, complete multipartite graphs, powers of paths and cycles, threshold graphs,
large graphs with a universal vertex, and graphs in which every node has at least 2 log2 n neighbours. Recent papers
found trees where the stronger property of log-concavity fails, but unimodality itself was listed as open.

**What is new.**
1. **The conjecture is false.** Two explicit connected networks with 317,440 nodes, one *split* (a clique plus an
   independent set) and one *bipartite*, have more dominating sets of size 160,080 than of size 160,320, and more of
   size 160,560 than of size 160,320: d_160080 > d_160320 < d_160560. An exact integer computation proves it. In units
   of one millionth of 2^314880, the three counts lie in the intervals 1556–1615, 1482–1541 and 1565–1624, so the middle
   one sits below both neighbours (Theorem 1.1).
2. **Many peaks.** The same idea gives connected networks whose counts have many separate peaks, growing like
   sqrt(n)/log n; an explicit example with four peaks has 4,857,004,032 nodes (Theorem 1.2).
3. **The most common size need not sit next to the average.** Beaton and Brown asked whether it always does. For the
   explicit split network the average size of a dominating set lies between 160323.034984 and 160323.034985, yet no size
   within distance 88 of it is a most common size. In other, astronomically large networks the gap is a fixed fraction
   of the number of nodes, with a very small constant (Theorem 1.3).
4. **High minimum degree is not enough.** Counterexamples exist even when every node has about (1/2) log2 n
   neighbours (Theorem 1.4(i)).
5. **A sufficient degree condition.** If every node has at least log2 n + log2 log2 n + 1 neighbours (n >= 4), the
   sequence is unimodal with its peak exactly at the middle, ceil(n/2). This halves the previous requirement, and for
   the peak to sit exactly at the middle it is best possible up to an additive constant (Theorem 1.4(ii)–(iii)).
6. **A side consequence.** The simplest random sampler of dominating sets, which adds or removes one node at a time,
   can take exponentially long on these networks (Proposition 6.3).

**The idea.** Build a network with two large families of dominating sets that have *exactly* the same number of
members but different typical sizes, while all other dominating sets are negligible in number. The size of a random
dominating set then has two humps, and the count dips between them. Bhattacharyya and Kahn used the same principle in
2013 for independent sets; the new work is making it exact under the covering rule of domination and certifying the
finite example in exact arithmetic.

**Limits.** The explicit example is large and has not been minimised. The fixed-fraction gap in item 3 is proved only
for astronomically large networks with a constant of order 10^-25; the explicit gap of more than 88 is for the
317,440-node network. The least minimum degree that forces unimodality is still open: it lies between about
(1/2) log2 n and log2 n + log2 log2 n + 1. The sharp result in item 5 is about where the peak sits, not about
unimodality. Trees remain open.

## Contents

| Path | What |
|---|---|
| `manuscript.pdf`, `manuscript.tex` | The paper (18 pages); Section 1 is a plain introduction with a plan of the paper |
| `figures/coefficient-bounds.pdf`, `.png` | Figure 1: the three certified intervals |
| `data/bipartite-example.edgelist` | The bipartite example B_{128,20}: a header line and 921,600 edges, one `u v` pair per line (plain text, 10.7 MB; SHA-256 0654a33f...a77e, as in the metadata) |
| `data/graph-metadata.json` | Size, bipartition, degrees and the SHA-256 of the uncompressed edge list |
| `code/verify_witness.py` | The integer certificate for d_160080 > d_160320 < d_160560 (both graphs) |
| `code/check_graph.py` | Independent check of the edge list (it reads the gzip-compressed form `data/bipartite-example.edgelist.gz`, which `graph_family.py` writes): hash of the uncompressed text, edge count, degrees 3..120, bipartition, connectivity |
| `code/graph_family.py` | Generates the edge list for any (m, s); with `--m 128 --s 20` it writes the compressed file that `check_graph.py` reads |
| `code/smallcheck.py` | Brute-force enumeration of small instances against the inclusion–exclusion formula |
| `code/check_criteria.py` | The degree criterion on all 33,867 labelled graphs of order at most six; circulant parameters b = 4..79 |
| `code/check_extensions.py` | Transfer identity; certified average size and exclusion of every index near it as a most common size; the explicit four-, eight- and sixteen-peak instances; the sharp-threshold constructions |
| `code/make_figure.py` | Draws Figure 1 (needs matplotlib) |
| `results/` | Recorded outputs of the checks |
| `refs.bib` | The manuscript's nine references |
| `AI_INDEX.md` | Machine-oriented map of claims, evidence and limits |
| `RESEARCH_GATES.json` | Prior-art searches, sources read, limitation triage |
| `REVIEW_SUMMARY.md` | Internal review: objections and how they were handled |
| `REPLAY_RECEIPT.md`, `ENVIRONMENT.txt` | Release replay and the cross-platform comparison policy |
| `MANIFEST.sha256` | SHA-256 of every file |

## Replay

From the package root, with CPython 3.12 or later (standard library only; no packages to install):

```sh
python -I -B -O code/verify_witness.py   > results/certificate-output.txt     # about 15 s
python -I -B -O code/graph_family.py --m 128 --s 20 --output data/bipartite-example.edgelist.gz
gunzip -c data/bipartite-example.edgelist.gz | cmp - data/bipartite-example.edgelist   # generated = shipped
python -I -B -O code/check_graph.py      > results/graph-check-output.txt     # about 2 s
python -I -B -O code/smallcheck.py       > results/smallcheck-output.txt      # about 2 s
python -I -B -O code/check_criteria.py   > results/criteria-output.txt        # about 1 s
python -I -B -O code/check_extensions.py --output results/extensions.json > results/extensions-output.txt  # 12-25 min
```

Every script exits with status 1 on any failed check, also under `python -O` (no `assert` statements). All certificate
arithmetic is exact (integers, fractions and outward-rounded dyadic numbers), so the results do not depend on the
platform. The edge list ships as plain text so that every file in the archive can be inspected directly;
`check_graph.py` reads the gzip-compressed form, which `graph_family.py` regenerates (gzip with modification time 0; the
comparison is made on the decompressed text).

**Cross-platform policy** (declared before tagging; the same in CI, ENVIRONMENT.txt and REPLAY_RECEIPT.md): every
`results/*.txt` file is compared byte for byte. In `results/extensions.json` the field `python` (the interpreter
version) is excluded, the fields holding floats (`*_float`, `v_over_d2`, `rho_max`, `residual_over_W`,
`outer_lower_over_W`, `middle_upper_over_W`, `even_grid_min`, `odd_grid_min`) are printed summaries of exact
quantities and are compared to a relative tolerance of 1e-9, and every other value is compared exactly. On macOS arm64
under CPython 3.12.11 every output matched. GitHub Actions on Linux runs the four quick checks and three negative
controls as a blocking job, and runs the slow `check_extensions.py` (12 to 25 minutes) as a separate, non-blocking job.

## Assurance

Written proofs with exact-arithmetic certificates. Internal AI-assisted review only: five Claude reviewer roles
(editor, methodology, domain, perspective, devil's advocate) run as two combined passes, in which two reviewers
recomputed the main certificate independently in exact arithmetic; a clean byte-for-byte replay by the lead; one
revision round with extensions; then a verification re-review and a proof audit of the new and rewritten proofs. No
second-model (Astra/Codex) review took place. This is not peer review, independent reproduction or formal
verification. See [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).

## Cite

Anonymous (2026). *Domination polynomials with many peaks: counterexamples to the Alikhani–Peng conjecture and the
minimum-degree scale for a central mode* (Version 0.1.0-candidate). Evidence Press.
https://doi.org/10.5281/zenodo.24511988
