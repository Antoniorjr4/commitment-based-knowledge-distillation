# Baseline V1 — EVM Benchmark Results

These are the frozen measurements reported in the October 2026 working paper.

## Environment

- Forge: 1.8.6
- Solidity: 0.8.24
- Optimizer: enabled
- Optimizer runs: 200
- via-IR: enabled
- Execution environment: local Foundry EVM
- Primary metric: `gasleft()` difference around an external `arbitrate()` call

## Vector-dimension benchmark

| Dimension | Merkle depth | Isolated arbitration-call gas | Isolated <450k target |
|---:|---:|---:|:---:|
| 64 | 14 | 132,874 | PASS |
| 128 | 14 | 222,450 | PASS |
| 256 | 14 | 400,913 | PASS |
| 512 | 14 | 758,018 | FAIL |
| 1,024 | 14 | 1,470,772 | FAIL |

At dimension 256, the measured value is 49,087 gas below the isolated 450,000-gas target, a margin of approximately 10.9%.

**Important:** PASS applies exclusively to the instrumented isolated arbitration-call metric. It is not a complete transaction-gas result.

## Merkle-depth benchmark at dimension 256

| Dimension | Merkle depth | Isolated arbitration-call gas |
|---:|---:|---:|
| 256 | 5 | 392,334 |
| 256 | 10 | 397,111 |
| 256 | 14 | 400,913 |
| 256 | 20 | 406,637 |

From depth 5 to 20, 15 additional levels added 14,303 gas, approximately 954 gas per level over this tested interval.

## Native Forge gas report

| Function | Min | Avg | Median | Max |
|---|---:|---:|---:|---:|
| `arbitrate` | 74,574 | 359,431 | 345,371 | 1,293,770 |
| `dotInt8` | 22,434 | 129,230 | 116,242 | 462,610 |
| `leafForRow` | 8,013 | 41,237 | 39,968 | 159,419 |
| `postProcess` | 381 | 393 | 397 | 397 |

The native report aggregates calls across different dimensions and Merkle depths. It is a supporting metric and should not be mixed numerically with the custom per-configuration `gasleft()` measurements because their accounting contexts differ.

The report also showed `Deployment Cost: 0` and deployment size 1,398 bytes. The zero deployment cost is a test-setup artifact and must not be interpreted as real zero deployment gas.

## Interpretation

The dominant observed scaling factor is vector dimension relative to Merkle depth. This does **not** establish that arithmetic instructions alone dominate total cost. Increasing vector dimension also increases ABI/data handling, hashing, and related processing.

## Scope limitation

These values are isolated external-call execution measurements in a local Foundry EVM. They do not separately measure full transaction intrinsic gas, complete transaction-level calldata costs, deployment gas, or production-network conditions.
