# Baseline V1 — Original Experimental Run

This directory documents the original EVM benchmark execution used for the Baseline V1 results reported in the working paper.

## Execution provenance

- Human experimenter: Antonio Rufino
- Date documented: 2026-10-25
- Environment: WSL / Ubuntu on Windows
- Project path shown in the execution record: `/mnt/c/projetos/certified_distillation_evm`
- Forge version: 1.8.6
- Forge commit: `6bad0a66de7c83f7b33695044138f0f5fa4c5990`
- Build timestamp: `2026-10-21T17:56:11.890310850Z (1792605371)`
- Build profile: `dist`
- Solidity: 0.8.24
- Optimizer: enabled
- Optimizer runs: 200
- via-IR: enabled

## Commands executed

```bash
forge test -vv
forge test --gas-report -vv
forge --version
```

Both test executions reported:

```text
11 passed; 0 failed; 0 skipped
```

## Instrumented Baseline V1 values

| Vector dimension | Merkle depth | arbitrate_gas_internal |
|---:|---:|---:|
| 64 | 14 | 132874 |
| 128 | 14 | 222450 |
| 256 | 5 | 392334 |
| 256 | 10 | 397111 |
| 256 | 14 | 400913 |
| 256 | 20 | 406637 |
| 512 | 14 | 758018 |
| 1024 | 14 | 1470772 |

These values are the custom `gasleft()`-based isolated external-call measurements reported by the test harness. They are not complete standalone transaction-gas measurements.

## Native Forge gas report

The original `forge test --gas-report -vv` execution reported:

| Function | Min | Avg | Median | Max | Calls |
|---|---:|---:|---:|---:|---:|
| arbitrate | 74574 | 359431 | 345371 | 1293770 | 11 |
| dotInt8 | 22434 | 129230 | 116242 | 462610 | 10 |
| leafForRow | 8013 | 41237 | 39968 | 159419 | 11 |
| postProcess | 381 | 393 | 397 | 397 | 10 |

The report also displayed deployment size 1398 bytes and deployment cost 0. The latter is a test-environment artifact and must not be interpreted as real deployment gas.

## Evidence handling

The original screenshots of this execution are retained by the author as primary experiment records. This metadata file transcribes the visible command, toolchain, pass/fail, instrumented gas, and native gas-report information. The GitHub Actions workflow in this repository is a separate clean-environment reproduction layer and does not replace the provenance of the original run.
