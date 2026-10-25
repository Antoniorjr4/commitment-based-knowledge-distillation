# Baseline V1 Benchmark Protocol

This document defines the measurement scope used for the EVM results reported in the October 2026 working paper **Commitment-Based Knowledge Distillation: Statistical Certification and Optimistic Verification for Trust-Minimized Model Serving**.

## Goal

Evaluate whether a bounded deterministic, Merkle-authenticated single-step arbitration call can satisfy the experimental target:

`G_arb < 450,000 gas`

The target applies only to the instrumented isolated arbitration call described below.

## Frozen compiler configuration

```toml
[profile.default]
src = "src"
test = "test"
script = "script"
solc_version = "0.8.24"
optimizer = true
optimizer_runs = 200
via_ir = true
```

`via_ir = true` is part of the baseline configuration. It was enabled after the initial non-via-IR build encountered `Stack too deep`.

## Arbitration semantics

The baseline arbiter:

1. reconstructs the committed row leaf as `keccak256(abi.encode(rowIndex, row))`;
2. verifies the supplied Merkle authentication path;
3. computes a deterministic INT8 × INT8 dot product with INT32 range enforcement;
4. applies ReLU, integer division by 8, and INT8 saturation;
5. compares the recomputed result with the publisher claim.

The ABI intentionally uses dynamic `int8[]` arrays in Baseline V1. Packed encodings are future experimental treatments and must not be substituted into this baseline.

## Primary measurement

For each configuration, gas is measured around an external call to `arbitrate()`:

```text
G_arb = G_before - G_after
```

where `G_before` and `G_after` are obtained with `gasleft()` immediately before and after the call in the Foundry test environment.

This is **isolated external-call execution gas in a local Foundry EVM**. It is not complete standalone L1 transaction gas.

## Tested configurations

Vector-dimension series at Merkle depth 14:

- d = 64
- d = 128
- d = 256
- d = 512
- d = 1,024

Merkle-depth series at d = 256:

- depth = 5
- depth = 10
- depth = 14
- depth = 20

## Functional checks

The baseline test suite includes checks that:

- an honest publisher is accepted;
- a dishonest publisher is detected;
- a tampered weight row fails Merkle authentication;
- all benchmark configurations execute.

The original run reported 11 tests passed, 0 failed, 0 skipped.

## Reproduction commands

```bash
forge --version
forge test -vv
forge test --gas-report -vv
```

The expected Forge version for the reported baseline is 1.8.6.

## Measurement caveats

Do not reinterpret the reported custom gas values as total transaction gas. The measurement does not separately account for complete transaction-level calldata costs, transaction intrinsic/base gas, deployment gas, or production-network conditions in the same manner as an actual broadcast transaction receipt.

The native Forge gas report is supplementary. Because it aggregates calls across configurations and uses its own accounting context, its maxima must not be substituted for the custom per-configuration values.

## Baseline preservation rule

Baseline V1 is frozen for scientific comparison. Optimizations such as packed `bytes`, segmented arbitration, alternate ABI layouts, or compiler changes should be implemented as separate versions/branches and compared against this baseline using the same test matrix and acceptance criteria.
