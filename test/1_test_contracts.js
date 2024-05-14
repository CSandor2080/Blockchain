const LoyaltyPoints = artifacts.require("LoyaltyPoints");
const RewardSystem = artifacts.require("RewardSystem");
const AddressLib = artifacts.require("AddressLib");

contract("LoyaltyPoints", accounts => {
  const [owner, beverageContract, customer, other] = accounts;

  let loyaltyPoints;

  beforeEach(async () => {
    // Deploy libraries
    const addressLib = await AddressLib.new();
    // Link libraries
    await LoyaltyPoints.link("AddressLib", addressLib.address);
    // Deploy LoyaltyPoints contract
    loyaltyPoints = await LoyaltyPoints.new(owner, beverageContract);
  });

  it("should issue points to a customer", async () => {
    await loyaltyPoints.issuePoints(customer, 100, { from: beverageContract });
    const balance = await loyaltyPoints.getPointsBalance(customer);
    assert.equal(balance.toNumber(), 100, "Points balance should be 100");
  });

  it("should not issue points from non-beverage contract address", async () => {
    try {
      await loyaltyPoints.issuePoints(customer, 100, { from: other });
      assert.fail("Expected revert not received");
    } catch (error) {
      assert(error.message.includes("Unauthorized access"), `Expected "Unauthorized access" but got ${error.message}`);
    }
  });

  it("should redeem points from a customer", async () => {
    await loyaltyPoints.issuePoints(customer, 100, { from: beverageContract });
    await loyaltyPoints.redeemPoints(customer, 50, { from: beverageContract });
    const balance = await loyaltyPoints.getPointsBalance(customer);
    assert.equal(balance.toNumber(), 50, "Points balance should be 50");
  });

  it("should not redeem more points than available", async () => {
    await loyaltyPoints.issuePoints(customer, 50, { from: beverageContract });
    try {
      await loyaltyPoints.redeemPoints(customer, 100, { from: beverageContract });
      assert.fail("Expected revert not received");
    } catch (error) {
      assert(error.message.includes("Insufficient points"), `Expected "Insufficient points" but got ${error.message}`);
    }
  });

  it("should allow owner to set beverage contract address", async () => {
    await loyaltyPoints.setBeverageContract(other, { from: owner });
    const newAddress = await loyaltyPoints.getBvAddress();
    assert.equal(newAddress, other, "Beverage contract address should be updated");
  });

  it("should not allow non-owner to set beverage contract address", async () => {
    try {
      await loyaltyPoints.setBeverageContract(other, { from: other });
      assert.fail("Expected revert not received");
    } catch (error) {
      assert(error.message.includes("Only the owner can perform this action"), `Expected "Only the owner can perform this action" but got ${error.message}`);
    }
  });
});
