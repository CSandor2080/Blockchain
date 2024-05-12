
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IBeverage {
    function purchase(address customer) external payable;
    function redeem(address customer, uint points) external;
}
