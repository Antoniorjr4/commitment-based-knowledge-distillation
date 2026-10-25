// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../src/CertifiedDistillationArbiter.sol";

contract CertifiedDistillationArbiterTest is Test {
    CertifiedDistillationArbiter arbiter;

    function setUp() public {
        arbiter = new CertifiedDistillationArbiter();
    }

    function _row(uint256 n) internal pure returns (int8[] memory r) {
        r = new int8[](n);
        for (uint256 i; i < n; ++i) r[i] = int8(int256((i % 11)) - 5);
    }

    function _input(uint256 n) internal pure returns (int8[] memory x) {
        x = new int8[](n);
        for (uint256 i; i < n; ++i) x[i] = int8(int256((i % 13)) - 6);
    }

    // Build a synthetic proof/root consistent with rowIndex=0.
    // Each sibling is deterministic; root is derived from the same path.
    function _proofAndRoot(
        uint256 rowIndex,
        int8[] memory row,
        uint256 depth
    ) internal view returns (bytes32[] memory proof, bytes32 root) {
        proof = new bytes32[](depth);
        bytes32 node = arbiter.leafForRow(rowIndex, row);
        uint256 idx = rowIndex;
        for (uint256 j; j < depth; ++j) {
            proof[j] = keccak256(abi.encodePacked("sibling", j));
            node = (idx & 1) == 0
                ? keccak256(abi.encodePacked(node, proof[j]))
                : keccak256(abi.encodePacked(proof[j], node));
            idx >>= 1;
        }
        root = node;
    }

    function testDetectsDishonestPublisher() public {
        int8[] memory row = _row(48);
        int8[] memory input = _input(48);
        (bytes32[] memory proof, bytes32 root) = _proofAndRoot(0, row, 14);

        int8 correct = arbiter.postProcess(arbiter.dotInt8(row, input));
        int8 falseClaim = correct == 127 ? int8(126) : correct + 1;

        (bool fault, int8 computed) =
            arbiter.arbitrate(root, 0, row, proof, input, falseClaim);

        assertTrue(fault);
        assertEq(computed, correct);
    }

    function testHonestPublisherPasses() public {
        int8[] memory row = _row(48);
        int8[] memory input = _input(48);
        (bytes32[] memory proof, bytes32 root) = _proofAndRoot(0, row, 14);
        int8 correct = arbiter.postProcess(arbiter.dotInt8(row, input));

        (bool fault,) = arbiter.arbitrate(root, 0, row, proof, input, correct);
        assertFalse(fault);
    }

    function testTamperedWeightFailsMerkle() public {
        int8[] memory row = _row(48);
        int8[] memory input = _input(48);
        (bytes32[] memory proof, bytes32 root) = _proofAndRoot(0, row, 14);
        row[0] += 1;

        vm.expectRevert(CertifiedDistillationArbiter.BadMerkleProof.selector);
        arbiter.arbitrate(root, 0, row, proof, input, 0);
    }

    // forge test --gas-report will report these separately.
    function testGas_D64_P14() public { _bench(64,14); }
    function testGas_D128_P14() public { _bench(128,14); }
    function testGas_D256_P14() public { _bench(256,14); }
    function testGas_D512_P14() public { _bench(512,14); }
    function testGas_D1024_P14() public { _bench(1024,14); }

    function testGas_D256_P5() public { _bench(256,5); }
    function testGas_D256_P10() public { _bench(256,10); }
    function testGas_D256_P20() public { _bench(256,20); }

    function _bench(uint256 dim, uint256 depth) internal {
        int8[] memory row = _row(dim);
        int8[] memory input = _input(dim);
        (bytes32[] memory proof, bytes32 root) = _proofAndRoot(0, row, depth);
        int8 correct = arbiter.postProcess(arbiter.dotInt8(row, input));

        uint256 g0 = gasleft();
        (bool fault,) = arbiter.arbitrate(root, 0, row, proof, input, correct);
        uint256 used = g0 - gasleft();

        emit log_named_uint("dimension", dim);
        emit log_named_uint("merkle_depth", depth);
        emit log_named_uint("arbitrate_gas_internal", used);
        assertFalse(fault);
    }
}
