// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract CertifiedDistillationArbiter {
    error LengthMismatch();
    error BadMerkleProof();
    error Int32Overflow();

    event Arbitration(
        bytes32 indexed weightRoot,
        uint256 indexed rowIndex,
        int8 claimedOutput,
        int8 computedOutput,
        bool publisherFault
    );

    function leafForRow(uint256 rowIndex, int8[] calldata row)
        public pure returns (bytes32)
    {
        return keccak256(abi.encode(rowIndex, row));
    }

    function verifyMerkle(
        bytes32 leaf,
        uint256 index,
        bytes32[] calldata proof,
        bytes32 root
    ) public pure returns (bool) {
        bytes32 x = leaf;
        uint256 i = index;
        for (uint256 p; p < proof.length; ++p) {
            bytes32 sibling = proof[p];
            x = (i & 1) == 0
                ? keccak256(abi.encodePacked(x, sibling))
                : keccak256(abi.encodePacked(sibling, x));
            i >>= 1;
        }
        return x == root;
    }

    function dotInt8(int8[] calldata row, int8[] calldata input)
        public pure returns (int32 acc)
    {
        if (row.length != input.length) revert LengthMismatch();

        int256 sum;
        for (uint256 i; i < row.length; ++i) {
            sum += int256(row[i]) * int256(input[i]);
        }
        if (sum < type(int32).min || sum > type(int32).max) revert Int32Overflow();
        return int32(sum);
    }

    function postProcess(int32 dot) public pure returns (int8) {
        int256 z = dot;
        if (z < 0) z = 0;
        z /= 8;
        if (z > 127) z = 127;
        return int8(z);
    }

    function arbitrate(
        bytes32 weightRoot,
        uint256 rowIndex,
        int8[] calldata weightRow,
        bytes32[] calldata weightProof,
        int8[] calldata input,
        int8 publisherClaim
    ) external returns (bool publisherFault, int8 computedOutput) {
        bytes32 leaf = leafForRow(rowIndex, weightRow);
        if (!verifyMerkle(leaf, rowIndex, weightProof, weightRoot)) {
            revert BadMerkleProof();
        }

        int32 dot = dotInt8(weightRow, input);
        computedOutput = postProcess(dot);
        publisherFault = computedOutput != publisherClaim;

        emit Arbitration(
            weightRoot, rowIndex, publisherClaim, computedOutput, publisherFault
        );
    }
}
