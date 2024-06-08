const LoyaltyPoints = artifacts.require("LoyaltyPoints");
const Shop = artifacts.require("Shop");

module.exports = async function (deployer, network, accounts) {
    const ownerAddress = accounts[0]; // Use the first account as the owner

    // Deploy LoyaltyPoints contract
    await deployer.deploy(LoyaltyPoints, ownerAddress);
    const loyaltyPointsInstance = await LoyaltyPoints.deployed();

    // Deploy Shop contract with the address of the deployed LoyaltyPoints contract
    await deployer.deploy(Shop, ownerAddress);
    const shopInstance = await Shop.deployed();

    console.log('Deployment successful');
    console.log('LoyaltyPoints address:', loyaltyPointsInstance.address);
    console.log('Shop address:', shopInstance.address);
};
