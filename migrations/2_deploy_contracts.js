const LoyaltyPoints = artifacts.require("LoyaltyPoints");
const BeverageContract = artifacts.require("BeverageContract");

module.exports = async function (deployer, network, accounts) {
    const ownerAddress = accounts[0]; // Use the first account as the owner

    // Deploy LoyaltyPoints contract with a dummy address for beverageContractAddress
    await deployer.deploy(LoyaltyPoints, ownerAddress, ownerAddress);
    const loyaltyPointsInstance = await LoyaltyPoints.deployed();

    // Deploy BeverageContract with the address of the deployed LoyaltyPoints contract
    // await deployer.deploy(BeverageContract, ownerAddress, ownerAddress);
    // const beverageContractInstance = await BeverageContract.deployed();

    // Update the LoyaltyPoints contract to set the correct beverageContractAddress
    //await loyaltyPointsInstance.setBeverageContract(beverageContractInstance.address);

    console.log('Deployment successful');
    console.log('LoyaltyPoints address:', loyaltyPointsInstance.address);
    //console.log('BeverageContract address:', beverageContractInstance.address);
};
