const LoyaltyPoints = artifacts.require("LoyaltyPoints");

contract("LoyaltyPoints", accounts => {
    const owner = accounts[0];
    const customer = accounts[1];
    const anotherAccount = accounts[2];

    let loyaltyPoints;

    beforeEach(async () => {
        loyaltyPoints = await LoyaltyPoints.new(owner);
    });

    it("should be deployed and initialized with correct owner", async () => {
        const contractOwner = accounts[0]
        assert.equal(contractOwner, owner, "Owner is not set correctly");
    });

    it("should not redeem more points than available", async () => {
        const points = 50;
        const redeemPoints = 100;
        const ipfsHash = "QmHash";

        await loyaltyPoints.issuePoints(customer, points, ipfsHash, { from: owner });

        try {
            await loyaltyPoints.redeemPoints(customer, redeemPoints, ipfsHash, { from: owner });
            assert.fail("Redeemed more points than available");
        } catch (error) {
            assert(error.message.includes("Insufficient points"), "Expected insufficient points error");
        }
    });

    it("should not allow non-owner to issue points", async () => {
        const points = 100;
        const ipfsHash = "QmHash";

        try {
            await loyaltyPoints.issuePoints(customer, points, ipfsHash, { from: anotherAccount });
            assert.fail("Non-owner was able to issue points");
        } catch (error) {
            assert(error.message.includes("Only the owner can perform this action"), "Expected owner restriction error");
        }
    });

    it("should not allow non-owner to redeem points", async () => {
        const points = 50;
        const ipfsHash = "QmHash";

        try {
            await loyaltyPoints.redeemPoints(customer, points, ipfsHash, { from: anotherAccount });
            assert.fail("Non-owner was able to redeem points");
        } catch (error) {
            assert(error.message.includes("Only the owner can perform this action"), "Expected owner restriction error");
        }
    });

    it("should emit PointsIssued event when points are issued", async () => {
        const points = 100;
        const ipfsHash = "QmHash";

        const result = await loyaltyPoints.issuePoints(customer, points, ipfsHash, { from: owner });

        assert.equal(result.logs.length, 1, "Expected one event to be emitted");
        assert.equal(result.logs[0].event, "PointsIssued", "Expected PointsIssued event");
        assert.equal(result.logs[0].args.customer, customer, "Customer address is incorrect in event");
        assert.equal(result.logs[0].args.points.toNumber(), points, "Points value is incorrect in event");
        assert.equal(result.logs[0].args.ipfsHash, ipfsHash, "IPFS hash is incorrect in event");
    });

    it("should emit PointsRedeemed event when points are redeemed", async () => {
        const points = 100;
        const ipfsHash = "QmHash";

        await loyaltyPoints.issuePoints(customer, points, ipfsHash, { from: owner });
        const result = await loyaltyPoints.redeemPoints(customer, points, ipfsHash, { from: owner });

        assert.equal(result.logs.length, 1, "Expected one event to be emitted");
        assert.equal(result.logs[0].event, "PointsRedeemed", "Expected PointsRedeemed event");
        assert.equal(result.logs[0].args.customer, customer, "Customer address is incorrect in event");
        assert.equal(result.logs[0].args.points.toNumber(), points, "Points value is incorrect in event");
        assert.equal(result.logs[0].args.ipfsHash, ipfsHash, "IPFS hash is incorrect in event");
    });
});
