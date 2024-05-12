// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library AddressLib {
    function isOwner(address _owner, address _sender) internal pure returns (bool) {
        return _owner == _sender;
    }
}
