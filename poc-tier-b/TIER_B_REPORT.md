# Tier B Optimistic Dispute Prototype

## What was implemented
This experiment prototypes the paper's Tier B mechanics at reduced scale: committed intermediate
states, binary bisection to isolate the first divergent transition, Merkle opening of a disputed
weight row, and deterministic single-step INT8/INT32 arbitration.

The paper describes hierarchical k-ary descent from layer to sub-block to operator and then a
single matrix-vector row product. This PoC implements the same logical pattern on a three-layer
integer network, without claiming equivalence to a transformer-scale deployment.

## Dishonest-publisher experiment
A publisher trace was deliberately corrupted at state 2, element 7, for evaluation item 317.
The publisher propagated that forged state forward, so the final state remained internally linked to
the false intermediate state.

Binary bisection isolated transition **state 1 -> state 2** in **2 round(s)**.
The arbiter then opened weight row 7 against its Merkle root and recomputed one deterministic
operator.

- Honest arbiter output: **0**
- Publisher claimed output: **9**
- Verdict: **PUBLISHER_FAULT**
- Weight-opening tamper test: **PASS** (mutation invalidated the Merkle opening)

## Measured local arbitration cost
1000 repetitions of the reduced single-step verifier:
- Mean: **52.05 µs**
- Median: **19.17 µs**
- p95: **118.84 µs**

These are Python/host measurements, not blockchain gas measurements.

## Bisection scaling
For 32 transitions, worst-case rounds are:
- k=2: 5
- k=4: 3
- k=8: 2
- k=16: 2

For 4096 transitions:
- k=2: 12
- k=4: 6
- k=8: 4
- k=16: 3

This demonstrates logarithmic *round-count scaling* in the abstract dispute tree. It does not by
itself establish total communication/gas optimality because larger k requires more information per round.

## Merkle proof scaling
A tree committing 16,384 weight rows has depth 14, requiring
448 bytes of sibling hashes per ordinary binary Merkle opening,
excluding indices/ABI overhead.

## EVM claim status
No measured gas result is reported. The approximate packed challenge payload in this toy case is
368 bytes, whose worst-case calldata component alone is 5888 gas under a
16-gas-per-nonzero-byte assumption. Execution, memory, ABI, storage, transaction, and hashing
costs are not included. The paper's <450,000 gas target therefore remains **untested** until an
actual Solidity/EVM implementation is deployed and benchmarked.

## Scientific interpretation
This PoC supports the feasibility of the *logical dispute mechanism*: if honest and dishonest
parties commit to different intermediate traces, logarithmic search can isolate a disputed
transition, and a small deterministic operator can decide that transition using committed data.

It does not yet establish the paper's stronger production claims. In particular, a complete Tier B
implementation still needs challenge-window/staking logic, commitments to all relevant intermediate
states, an authenticated input opening, a real settlement contract, transformer-specific operator
decomposition, and measured testnet gas.
