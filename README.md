# Commitment-Based Knowledge Distillation

Reproducibility package for the working paper:

**Commitment-Based Knowledge Distillation: Statistical Certification and Optimistic Verification for Trust-Minimized Model Serving**

**Author:** Antonio Rufino — Independent Researcher, Brazil  
**Status:** Technical Report and Working Paper  
**Baseline:** V1, October 2026

## Scope

This repository preserves the frozen experimental baseline used in the paper. It contains three separate component-level prototypes:

1. a statistical certificate prototype for bounded student/teacher disagreement;
2. an optimistic interactive bisection prototype;
3. an EVM single-step arbitration benchmark.

These components are **not** an integrated production system. The repository does not claim a proof of full frontier-model execution, provenance from commitments alone, or a constant-size proof of model equivalence.

## 1. Statistical certificate prototype

Source and report are preserved under `poc-statistical/`. The original ZIP is also preserved verbatim at `certified_distillation_poc.zip`; its SHA-256 is recorded in `ARTIFACT_HASHES.sha256`.

Frozen reported results:

- committed synthetic corpus: N = 4,096;
- audit sample: n = 1,024;
- disagreement: 56/1,024 = 5.47%;
- delta = 0.05;
- implemented Hoeffding-style radius: 0.038246;
- upper bound: approximately 9.29%;
- full-corpus disagreement: approximately 5.15%;
- certificate size: approximately 3.75 MiB;
- verification median: approximately 36.978 ms;
- verification mean: approximately 37.039 ms;
- tamper detection: PASS.

The prototype uses reproducible pseudorandom sampling, not a live public randomness beacon. Because 25% of the finite corpus is sampled without replacement, finite-population bounds such as Serfling are relevant future refinements. The 9.29% result remains the implemented baseline and is not retroactively replaced.

The current Merkle certificate is not O(1) in size.

## 2. Interactive bisection prototype

Source, report, and result data are preserved under `poc-tier-b/`.

Frozen reported results:

- deterministic three-layer integer network;
- corrupted state: state 2, element 7, sample 317;
- binary bisection isolated state 1 → state 2 in 2 rounds;
- honest output: 0;
- publisher claim: 9;
- verdict: `PUBLISHER_FAULT`;
- Merkle tamper test: PASS;
- 1,000 local arbitration runs: mean 52.05 μs, median 19.17 μs, p95 118.84 μs.

This prototype demonstrates dispute localization; it is not integrated with the statistical prototype or a complete neural-network execution trace.

## 3. Baseline V1 EVM arbiter

`src/CertifiedDistillationArbiter.sol` implements the deterministic single-step settlement primitive used in the EVM benchmark:

- Merkle authentication of a committed weight row;
- INT8 × INT8 multiplication;
- INT32 accumulation/range enforcement;
- deterministic ReLU;
- integer division by 8;
- INT8 saturation;
- comparison against the publisher's claimed output.

The Baseline V1 ABI uses dynamic `int8[]` arrays. This is intentional and frozen. Packed encodings are future optimization work.

### Reproduce the EVM baseline

Frozen toolchain:

```text
forge Version: 1.8.6
Commit SHA: 6bad0a66de7c83f7b33695044138f0f5fa4c5990
Build Timestamp: 2026-10-21T17:56:11.890310850Z (1792605371)
Build Profile: dist
```

Compiler configuration in `foundry.toml`:

```text
Solidity 0.8.24
optimizer = true
optimizer_runs = 200
via_ir = true
```

The automated reproduction uses Ubuntu 24.04 and pins `forge-std` to:

```text
f3dae6e6ee381f25eb6a246f7da9b85c91a68219
```

Run locally:

```bash
forge test -vv
forge test --gas-report -vv
```

The original experimental execution and a clean GitHub Actions reproduction both reported **11 tests passed, 0 failed, 0 skipped**. The automated run reproduced the frozen instrumented gas values exactly. The original test harness is preserved at `test/CertifiedDistillationArbiter.t.sol`.

### Frozen EVM results

| Vector dimension | Merkle depth | Isolated arbitration-call gas | Isolated <450k target |
|---:|---:|---:|:---:|
| 64 | 14 | 132,874 | PASS |
| 128 | 14 | 222,450 | PASS |
| 256 | 14 | 400,913 | PASS |
| 512 | 14 | 758,018 | FAIL |
| 1,024 | 14 | 1,470,772 | FAIL |

At d=256/depth 14, the measured value is 49,087 gas below the isolated 450,000-gas target, approximately a 10.9% margin.

**The PASS designation applies only to the instrumented isolated external-call metric. It is not a complete transaction-gas result.**

At fixed d=256, Merkle depth 5 → 20 increased the isolated-call measurement from 392,334 to 406,637 gas, approximately 954 gas per added level over the tested interval.

See `BENCHMARK_RESULTS.md` and `BENCHMARK_PROTOCOL.md` for the frozen measurements and methodology.

### Measurement scope

The benchmark used `gasleft()` immediately before and after an external call to `arbitrate()` in a local Foundry EVM:

```text
G_arb = G_before - G_after
```

This measures isolated external-call execution in the test context. It does not separately measure complete transaction intrinsic gas, complete transaction-level calldata cost, deployment gas, or production-network conditions.

## Artifact integrity

`ARTIFACT_HASHES.sha256` records hashes for the original experimental archives and their constituent files. In particular, the original statistical PoC archive is preserved in this repository as:

```text
certified_distillation_poc.zip
```

Its frozen SHA-256 is:

```text
ca73d8a12d4441706864744534b66bb1d0027ada1750a8433a934c4e9df7b557
```

The hash record is the integrity reference; moving or renaming an unchanged archive does not change its SHA-256.

## Repository map

```text
.
├── .github/workflows/
│   └── reproduce-baseline.yml
├── poc-statistical/
│   ├── verify.py
│   └── REPORT.md
├── poc-tier-b/
│   ├── verify_tier_b.py
│   ├── TIER_B_REPORT.md
│   └── tier_b_results.json
├── results/original-run/
│   └── RUN_METADATA.md
├── src/
│   └── CertifiedDistillationArbiter.sol
├── test/
│   └── CertifiedDistillationArbiter.t.sol
├── certified_distillation_poc.zip
├── ARTIFACT_HASHES.sha256
├── BENCHMARK_PROTOCOL.md
├── BENCHMARK_RESULTS.md
├── CITATION.cff
├── foundry.toml
├── manifest.json
├── LICENSE
└── README.md
```

## Scientific interpretation

The measured EVM results support the limited conclusion that, under the tested local-EVM methodology, bounded deterministic arbitration is feasible within the isolated-call target for moderate vector dimensions, while larger operators require further decomposition or representation optimization.

The dominant observed scaling factor is vector dimension relative to Merkle depth. Dimension-dependent cost includes arithmetic execution and data handling; the measurements do not establish that arithmetic instructions alone dominate total cost.

## Known limitations

- commitments establish integrity, not provenance;
- Merkle commitments do not establish dataset representativeness;
- the statistical PoC used reproducible pseudorandom sampling, not a live public randomness beacon;
- agreement with a teacher is not equivalent to correctness;
- a single audit does not empirically establish nominal 95% coverage;
- optimistic verification assumes challenger availability;
- the economic-security model is incomplete;
- EVM values are isolated-call measurements, not complete transaction gas;
- the three prototypes are not integrated end-to-end;
- statistical and bisection experiments are synthetic;
- the current Merkle certificate is not O(1) in size.

## Frozen baseline and future work

Baseline V1 is frozen. Future experiments should be performed in separate versions or branches and may include packed `bytes`, d=512/d=1,024 optimization, segmented arbitration, complete transaction-level gas including calldata, deployment gas, compiler sensitivity, repeated statistical audits, Serfling evaluation, live public randomness, adversarial challenge simulations, economic-security modeling, component integration, real models/datasets, edge hardware, and Tier-C cryptographic proofs.

## Citation

Citation metadata is provided in `CITATION.cff`. No DOI or preprint identifier is claimed until one is actually assigned.

## License

The software in this repository is released under the MIT License. See `LICENSE`.
