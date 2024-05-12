// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IBeverage.sol";
import "./RewardSystem.sol";

contract BeverageContract is IBeverage {
    address private owner;
    RewardSystem private loyaltySystem;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    constructor(address _loyaltySystem) {
        owner = msg.sender;
        loyaltySystem = RewardSystem(_loyaltySystem);
    }

    function purchase(address customer) external payable override {
        require(msg.value >= 0.01 ether, "Insufficient ETH sent for purchase");
        loyaltySystem.issuePoints(customer, msg.value / 0.01 ether); // 1 point per 0.01 ETH spent
    }

    function redeem(address customer, uint points) external override {
        require(msg.sender == address(loyaltySystem), "Unauthorized access");
        require(points >= 10, "At least 10 points are required to redeem a beverage");
        loyaltySystem.redeemPoints(customer, 10); // Redeem points for a beverage
    }
}
