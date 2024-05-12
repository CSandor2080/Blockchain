// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./RewardSystem.sol";
import "./AddressLib.sol";

contract LoyaltyPoints is RewardSystem {
    using AddressLib for address;

    mapping(address => uint256) public pointsBalance;
    address private owner;
    address private beverageContractAddress;

    event PointsIssued(address indexed customer, uint points);
    event PointsRedeemed(address indexed customer, uint points);

    modifier onlyOwner() {
        require(owner.isOwner(msg.sender), "Only the owner can perform this action");
        _;
    }

    modifier onlyBeverageContract() {
        require(msg.sender == beverageContractAddress, "Unauthorized access");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setBeverageContract(address _address) public onlyOwner {
        beverageContractAddress = _address;
    }

    function issuePoints(address customer, uint256 points) override external onlyBeverageContract {
        pointsBalance[customer] += points;
        emit PointsIssued(customer, points);
    }

    function redeemPoints(address customer, uint256 points) override external onlyBeverageContract {
        require(pointsBalance[customer] >= points, "Insufficient points");
        pointsBalance[customer] -= points;
        emit PointsRedeemed(customer, points);
    }

    function getPointsBalance(address customer) public view returns (uint256) {
        return pointsBalance[customer];
    }
}
