# Replay receipt (0.1.0-candidate, 24 November 2026)

**Environment.** macOS arm64; CPython 3.12.11 (uv-managed, `uv run --no-project --python 3.12 python`; the version was
printed inside the run with `sys.version`); standard library only. Each run used a fresh copy of the approved
candidate, cwd = package root, `PYTHONDONTWRITEBYTECODE=1`. The lead's pre-release replay ran under CPython 3.14.7
(the `python3` shim); both produced matching outputs.

| Run | Command | Exit | Output vs `results/` |
|---|---|---|---|
| coefficient certificate, plain and -O | `python [-O] -I -B code/verify_witness.py` | 0, 0 | byte-identical to `certificate-output.txt` |
| supplied graph, plain and -O | `python [-O] -I -B code/check_graph.py` | 0, 0 | byte-identical to `graph-check-output.txt` |
| small instances, plain and -O | `python [-O] -I -B code/smallcheck.py` | 0, 0 | byte-identical to `smallcheck-output.txt` |
| degree criterion, plain and -O | `python [-O] -I -B code/check_criteria.py` | 0, 0 | byte-identical to `criteria-output.txt` |
| extensions, -O (22 minutes on this host) | `python -O -I -B code/check_extensions.py --output new.json` | 0 | stdout byte-identical to `extensions-output.txt`; JSON equal to `extensions.json` under the declared policy |
| edge-list generator, -O | `python -O -I -B code/graph_family.py --m 128 --s 20 --output new.gz` | 0 | byte-identical to the candidate's compressed edge list, which decompresses to the shipped `data/bipartite-example.edgelist` |

**Negative controls (under -O).**
1. `verify_witness.py` with the middle index 160320 changed to 160081 (next to the left index): "CHECK FAILED:
   rows[1][1] < min(rows[0][0], rows[2][0])", exit 1.
2. The last edge deleted from the compressed edge list `data/bipartite-example.edgelist.gz` (re-compressed); `check_graph.py`: "CHECK FAILED:
   digest.hexdigest() == metadata["uncompressed_sha256"]", exit 1.
3. `check_criteria.py` with the expected number of graphs meeting the criterion changed from 63 to 64: "CHECK FAILED:
   sufficient_condition_count == 64", exit 1.

**After the replay** only the title-page DOI line of `manuscript.tex`, the rebuilt PDF (three pdflatex passes, 18 pages)
and the release records changed; the code, data, figure and recorded outputs are byte-identical to the replayed
candidate, except that the edge list ships uncompressed (`data/bipartite-example.edgelist`, byte-identical to the
decompressed candidate file, SHA-256 0654a33f...a77e) so that every archive member is plain inspectable text; the
replay above ran on the candidate's compressed file, which `graph_family.py` regenerates byte for byte.

**Cross-platform policy** (declared before tagging; see ENVIRONMENT.txt): text outputs are compared byte for byte.
In `results/extensions.json` the field `python` (interpreter version) is excluded and float-valued summary fields are
compared to a relative tolerance of 1e-9; every other value is compared exactly. The GitHub Actions workflow
`.github/workflows/replay.yml` reruns the four quick checks and the generator under `python -O` on Linux, compares byte
for byte and runs the three negative controls (blocking); `check_extensions.py` runs in a separate non-blocking job
under the same policy, to keep the slow suite off the critical path.

**Scope.** The computations certify the finite example, its average size and the explicit instances exactly. The
proofs carry the asymptotic theorems.
