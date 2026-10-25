# Commitment-Based Knowledge Distillation

Reproducibility package for the working paper:

**Commitment-Based Knowledge Distillation: Statistical Certification and Optimistic Verification for Trust-Minimized Model Serving**

**Author:** Antonio Rufino — Independent Researcher, Brazil  
**Status:** Technical Report and Working Paper  
**Baseline:** V1, October 2026

## What this repository is

This repository preserves the frozen experimental baseline used in the paper. The project studies how cryptographic commitments, bounded statistical certification, deterministic integer arithmetic, and optimistic dispute resolution can be combined for trust-minimized publication of distilled models.

The current evidence is component-level. It does **not** constitute an integrated production system, a proof of full frontier-model execution, or a constant-size cryptographic proof of model equivalence.

## Baseline V1 EVM arbiter

`src/CertifiedDistillationArbiter.sol` implements the deterministic single-step settlement primitive used in the EVM benchmark:

- Merkle authentication of a committed weight row;
- INT8 × INT8 multiplication;
- INT32 accumulation/range enforcement;
- deterministic ReLU;
- integer division by 8;
- INT8 saturation;
- comparison against the publisher's claimed output.

The Baseline V1 ABI uses dynamic `int8[]` arrays. This is intentional and frozen. Packed encodings are future optimization work.

## Reproduce the EVM baseline

Install Foundry and verify the expected toolchain:

```bash
forge --version
```

The reported baseline used:

```text
forge Version: 1.8.6
Commit SHA: 6bad0a66de7c83f7b33695044138f0f5fa4c5990
Build Timestamp: 2026-10-21T17:56:11.890310850Z (1792605371)
Build Profile: dist
```

Compiler configuration is frozen in `foundry.toml`:

```text
Solidity 0.8.24
optimizer = true
optimizer_runs = 200
via_ir = true
```

Run:

```bash
forge test -vv
forge test --gas-report -vv
```

The original baseline execution reported **11 tests passed, 0 failed, 0 skipped**.

> Note: the exact original Solidity test harness that generated the reported per-configuration values should be preserved verbatim before claiming independent one-command reproduction of every benchmark number. The contract, compiler configuration, protocol, and frozen reported outputs are already preserved here.

## Frozen reported EVM results

| Vector dimension | Merkle depth | Isolated arbitration-call gas | Isolated <450k target |
|---:|---:|---:|:---:|
| 64 | 14 | 132,874 | PASS |
| 128 | 14 | 222,450 | PASS |
| 256 | 14 | 400,913 | PASS |
| 512 | 14 | 758,018 | FAIL |
| 1,024 | 14 | 1,470,772 | FAIL |

At d=256 and depth 14, the measured value is 49,087 gas below the isolated 450,000-gas target, approximately a 10.9% margin.

The PASS designation applies **only** to the instrumented isolated external-call metric. It must not be interpreted as a complete transaction-gas result.

At fixed d=256, increasing Merkle depth from 5 to 20 increased the measured isolated-call cost from 392,334 to 406,637 gas, or approximately 954 gas per added level over that tested interval.

See [`BENCHMARK_RESULTS.md`](BENCHMARK_RESULTS.md) for the complete frozen result table and native Forge gas report.

## Measurement scope

The primary benchmark used `gasleft()` immediately before and after an external call to `arbitrate()` in a local Foundry EVM:

```text
G_arb = G_before - G_after
```

This measures isolated external-call execution in the test context. It does not separately measure complete transaction intrinsic gas, full transaction-level calldata costs, deployment gas, or production-network conditions.

See [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) before comparing these numbers with transaction receipts or other EVM benchmarks.

## Other reported prototype results

The paper also reports separate component-level prototypes that are not yet integrated into this repository's EVM baseline:

### Statistical certificate prototype

- committed synthetic corpus: N = 4,096;
- audit sample: n = 1,024;
- observed student/teacher disagreement: 56/1,024 = 5.47%;
- delta = 0.05;
- implemented Hoeffding-style radius: 0.038246;
- resulting upper bound: approximately 9.29%;
- full synthetic corpus disagreement: approximately 5.15%;
- certificate size: approximately 3.75 MiB;
- verification median: approximately 36.978 ms;
- verification mean: approximately 37.039 ms.

Because 25% of the finite corpus is sampled without replacement, finite-population bounds such as Serfling are relevant future refinements. The reported 9.29% value is intentionally retained as the implemented baseline result.

### Interactive bisection prototype

- deterministic three-layer integer network;
- corrupted state: state 2, element 7, sample 317;
- binary bisection isolated state 1 → state 2 in 2 rounds;
- honest output: 0;
- publisher claim: 9;
- verdict: `PUBLISHER_FAULT`;
- Merkle tamper test: PASS;
- 1,000 local arbitration runs: mean 52.05 μs, median 19.17 μs, p95 118.84 μs.

These prototypes are separate from the Solidity arbiter and should not be described as an end-to-end integrated implementation.

## Repository map

```text
.
├── src/
│   └── CertifiedDistillationArbiter.sol
├── foundry.toml
├── BENCHMARK_PROTOCOL.md
├── BENCHMARK_RESULTS.md
├── manifest.json
├── LICENSE
└── README.md
```

## Scientific interpretation

The measured EVM results support the following limited conclusion:

> Under the tested local-EVM measurement methodology, bounded deterministic arbitration is feasible within the isolated-call target for moderate vector dimensions, while larger operators require further decomposition or representation optimization.

The dominant observed scaling factor is vector dimension relative to Merkle depth. The dimension-dependent cost reflects both arithmetic execution and data handling; the results do not establish that arithmetic instructions alone dominate total cost.

## Known limitations

- commitments establish integrity, not provenance;
- dataset representativeness is not established by Merkle commitments;
- the statistical PoC used reproducible pseudorandom sampling, not a live public randomness beacon;
- agreement with a teacher is not equivalent to correctness;
- optimistic verification assumes challenger availability;
- the economic security model is not complete;
- EVM values are isolated-call measurements, not complete transaction gas;
- the statistical certificate, bisection prototype, and EVM arbiter are not integrated end-to-end;
- the current statistical and bisection experiments are synthetic;
- the current Merkle certificate is not O(1) in size.

## Planned follow-up experiments

Baseline V1 should remain frozen. Future work should be performed in separate versions/branches and may include:

- packed `bytes` representation instead of ABI `int8[]`;
- d=512 and d=1,024 optimization experiments;
- segmented arbitration;
- complete transaction-level gas including calldata;
- deployment gas;
- compiler sensitivity;
- repeated statistical audits and empirical coverage;
- finite-population bounds such as Serfling;
- live public randomness beacon integration;
- adversarial challenge simulations;
- economic-security modeling;
- integration of the independent components;
- real model/dataset evaluation;
- Tier-C cryptographic proof systems.

## AI assistance disclosure

Generative AI research-assistance tools were used during code development, experimental-design refinement, output interpretation, literature-oriented revision, technical writing, and manuscript editing. Additional generative AI systems were used for independent critique and review.

No AI system is an author. All reported experimental executions were performed and reviewed by the human author, who made the final methodological decisions, accepted or rejected AI-generated suggestions, verified the reported numerical results, and assumes responsibility for the content and conclusions.

## License

The software in this repository is released under the MIT License. See [`LICENSE`](LICENSE).
