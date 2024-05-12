// 2_deploy_contracts.js
const LoyaltyPoints = artifacts.require("LoyaltyPoints");
const BeverageContract = artifacts.require("BeverageContract");

module.exports = function (deployer) {
    deployer.deploy(LoyaltyPoints).then(function(instance) {
        return deployer.deploy(BeverageContract, instance.address);
    });
};
