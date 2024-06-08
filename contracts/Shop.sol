// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./LoyaltyPoints.sol";

contract Shop is LoyaltyPoints {
    struct Product {
        string name;
        uint256 price;
    }

    Product[] public products;
    uint256 public constant LOYALTY_RATE = 5;

    event ProductAdded(uint256 productId, string name, uint256 price);
    event ProductPurchased(address indexed buyer, uint256 productId, uint256 price, uint256 loyaltyPointsEarned);

    constructor(address _owner) LoyaltyPoints(_owner) {}

    function addProduct(string memory name, uint256 price) public onlyOwner {
        products.push(Product(name, price));
        uint256 productId = products.length - 1;
        emit ProductAdded(productId, name, price);
    }

    function buyProduct(uint256 productId, bool usePoints) public payable {
        require(productId < products.length, "Invalid product ID");
        Product memory product = products[productId];
        uint256 price = product.price;

        if (usePoints) {
            uint256 points = pointsBalance[msg.sender].points;
            if (points > 0) {
                uint256 discount = points; // Assuming 1 point = 1 wei for simplicity
                if (discount > price) {
                    discount = price;
                }
                pointsBalance[msg.sender].points -= discount;
                price -= discount;
            }
        }

        require(msg.value >= price, "Insufficient Ether sent");

        uint256 loyaltyPointsEarned = (product.price * LOYALTY_RATE) / 100;
        pointsBalance[msg.sender].points += loyaltyPointsEarned;

        emit ProductPurchased(msg.sender, productId, product.price, loyaltyPointsEarned);

        // Send the Ether to the owner
        payable(owner).transfer(price);
        if (msg.value > price) {
            payable(msg.sender).transfer(msg.value - price); // Refund overpayment
        }
    }

    function getProduct(uint256 productId) public view returns (string memory name, uint256 price) {
        require(productId < products.length, "Invalid product ID");
        Product memory product = products[productId];
        return (product.name, product.price);
    }
}
