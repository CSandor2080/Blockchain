// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./RewardSystem.sol";
import "./AddressLib.sol";

contract LoyaltyPoints is RewardSystem {
    using AddressLib for address;

    struct PointsData {
        uint256 points;
        string ipfsHash;
    }

    mapping(address => PointsData) public pointsBalance;
    address public  owner;

    event PointsIssued(address indexed customer, uint256 points, string ipfsHash);
    event PointsRedeemed(address indexed customer, uint256 points, string ipfsHash);

    modifier onlyOwner() {
        require(owner.isOwner(msg.sender), "Only the owner can perform this action");
        _;
    }


    constructor(address _owner) {
        owner = _owner;
    }

    // Implementing RewardSystem interface
    function issuePoints(address customer, uint256 points, string calldata ipfsHash) override external onlyOwner {
        pointsBalance[customer].points += points;
        pointsBalance[customer].ipfsHash = ipfsHash;
        emit PointsIssued(customer, points, ipfsHash);
    }

    function redeemPoints(address customer, uint256 points, string calldata ipfsHash) override external onlyOwner {
        require(pointsBalance[customer].points >= points, "Insufficient points");
        pointsBalance[customer].points -= points;
        pointsBalance[customer].ipfsHash = ipfsHash;
        emit PointsRedeemed(customer, points, ipfsHash);
    }

    function getPointsBalance(address customer) public view returns (uint256, string memory) {
        PointsData memory data = pointsBalance[customer];
        return (data.points, data.ipfsHash);
    }
}
