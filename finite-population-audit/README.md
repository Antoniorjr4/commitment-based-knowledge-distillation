> **Canonical repository:** This distinct study is now maintained at [auditable-teacher-student-fidelity](https://github.com/Antoniorjr4/auditable-teacher-student-fidelity). This folder and the original release are retained for provenance. Use the dedicated repository for current publication and citation metadata.

# Finite-population Teacher–Student fidelity audit — audit-large-v1.0.0

**Reproduction release accompanying the manuscript. No arXiv submission or peer-review acceptance is asserted.**

Antonio Rufino — Independent Researcher, Brazil. ORCID: https://orcid.org/0009-0004-1767-8165.

Code: MIT. Author-controlled article/data: CC BY 4.0. Model/third-party notices: see [LICENSES.md](LICENSES.md).

A committed population of 2,048 maintenance reports, a CPU-run Qwen2.5-1.5B Student, and an API Teacher were evaluated with a fixed 768-item sample derived from drand quicknet round 33,515,062.

- Primary sample: 64/768 disagreements.
- One-sided 95% fixed-table upper bound: 200/2,048 = 9.765625%.
- Prespecified target: at most 10%; passed.
- Subsequent census: 158/2,048 = 7.71484375%.
- Human-reviewed labels existed for every input.
- No inference that the same certificate controls a stochastic service's expected disagreement is made.

## Replay without a model or an API key

Use Python 3.12. Dependency installation may require network access; the replay itself does not.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-replay.txt
python verification/reproduce.py --output results/my_replay
```

On Windows, activate the environment using the appropriate shell command. The archive is read in memory; archived code is never imported or executed. No archive members are written to the filesystem. The script checks safe member names, exact hashes, records, BLS signatures and a wrong-round control; reconstructs the sample independently; and recomputes bounds, power and exploratory diagnostics.

Expected output includes `status: PASS`, 6,336 inventoried files, 2,048 records per model, sample k = 64, census K = 158, upper total = 200 and 36 fingerprints. The bundled `results/replayed/summary.json` records the actual environment used here. Minor floating-point differences in exploratory calculations can occur across environments; the pinned replay dependencies reproduce the reported version's calculations.

`--permutations` defaults to 100000. Changing it changes only the fingerprint diagnostic and its Monte Carlo precision, never the registered certificate. The default random seed is fixed in the replayer.

## Contents

- `paper/manuscript_en.pdf`: typeset English manuscript.
- `paper/manuscript_en.md`, `.tex`, and `header.tex`: editable sources.
- `paper/manuscript_pt_v0_3_frozen.md`: unchanged Portuguese basis.
- `paper/figures/`: scientific figure and reusable formats.
- `evidence/audit_large_review.tar.gz`: exact original review archive, including registered code, raw records and adapter.
- `verification/reproduce.py`: new standalone offline replayer, separate from committed executors.
- `results/`: actual replay output and credential-pattern scan.
- `docs/FINAL_REVIEW_PT.md`: historical RC1 review; see RELEASE_NOTES.md for current publication status.
- `docs/PUBLICATION_DECISIONS.md`: historical RC1 proposal, retained for provenance; superseded by LICENSES.md and RELEASE_NOTES.md.
- `SHA256SUMS`: hashes for this release, excluding the checksum file itself.

## Frozen evidence and scope

Evidence archive SHA256:

`92a6fcedc7561c78e9159c50a2709862d0b2b86e22c25c466ece38bb49b4c2a4`

The evidence includes 6,336 inventoried files plus its inventory and review README. It includes the selected adapter but not base-model weights. The latter are identified as `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.

This release reproduces the completed **audit**, not training from scratch. Historical training metadata is supporting evidence. Reexecuting inference or the remote Teacher is a separate task; the remote alias cannot guarantee the same future responses. The old executor files are evidence: do not rerun their collection stages as a way of verifying the existing result.

The proof assumes a fixed disagreement table and uniform sampling without replacement. API stationarity, provenance of the provider's responses, an external pre-beacon timestamp, and resistance to selecting among hidden runs are not established by replaying hashes. The reference binomial/KL/Hoeffding values use a separately stated iid model.

## Integration and publication

Existing project repository: https://github.com/Antoniorjr4/commitment-based-knowledge-distillation

It contains earlier work. This audit is maintained in `finite-population-audit/`, without replacing the historical EVM and earlier statistical baselines. The designated release is `audit-large-v1.0.0`. A verified CI workflow checks the release before creating its GitHub release. If the existing Zenodo integration is enabled, the GitHub release can trigger an archive; the DOI must be verified rather than inferred. No new Zenodo DOI is claimed before confirmation.

Earlier baseline: https://doi.org/10.5281/zenodo.23644783. This is the old baseline DOI, not the DOI of the present audit. The manuscript can also be deposited as a separate related publication record.

Historical RC1 documents are retained as dated preparation records; current licenses and status are in LICENSES.md and RELEASE_NOTES.md.
