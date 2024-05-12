// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface RewardSystem {
    function issuePoints(address customer, uint256 points) external;
    function redeemPoints(address customer, uint256 points) external;
}
