const Shop = artifacts.require("Shop");
const LoyaltyPoints = artifacts.require("LoyaltyPoints");

contract("Shop", (accounts) => {
    let shop;
    const owner = accounts[0];
    const buyer = accounts[1];

    beforeEach(async () => {
        shop = await Shop.new(owner, { from: owner });
    });

    it("should allow the owner to add a product", async () => {
        const name = "Product 1";
        const price = web3.utils.toWei("1", "ether");

        await shop.addProduct(name, price, { from: owner });

        const product = await shop.getProduct(0);
        assert.equal(product.name, name, "Product name mismatch");
        assert.equal(product.price, price, "Product price mismatch");

        const productAddedEvent = await shop.getPastEvents("ProductAdded", {
            fromBlock: 0,
            toBlock: "latest",
        });
        assert.equal(productAddedEvent.length, 1, "ProductAdded event not emitted");
        assert.equal(productAddedEvent[0].returnValues.productId, 0, "Product ID mismatch");
        assert.equal(productAddedEvent[0].returnValues.name, name, "Event product name mismatch");
        assert.equal(productAddedEvent[0].returnValues.price, price, "Event product price mismatch");
    });

    it("should allow a buyer to purchase a product without loyalty points", async () => {
        const name = "Product 2";
        const price = web3.utils.toWei("2", "ether");

        await shop.addProduct(name, price, { from: owner });

        const initialOwnerBalance = await web3.eth.getBalance(owner);
        const initialBuyerBalance = await web3.eth.getBalance(buyer);

        const tx = await shop.buyProduct(0, false, { from: buyer, value: price });

        const finalOwnerBalance = await web3.eth.getBalance(owner);
        const finalBuyerBalance = await web3.eth.getBalance(buyer);

        assert.equal(
            web3.utils.toBN(finalOwnerBalance).toString(),
            web3.utils.toBN(initialOwnerBalance).add(web3.utils.toBN(price)).toString(),
            "Owner balance mismatch"
        );
        assert.isBelow(
            Number(finalBuyerBalance),
            Number(initialBuyerBalance) - Number(price),
            "Buyer balance mismatch"
        );

        const loyaltyPointsEarned = (price * 5) / 100;
        const buyerLoyaltyPoints = await shop.pointsBalance(buyer);
        assert.equal(
            buyerLoyaltyPoints.points.toString(),
            loyaltyPointsEarned.toString(),
            "Loyalty points mismatch"
        );

        const productPurchasedEvent = await shop.getPastEvents("ProductPurchased", {
            fromBlock: 0,
            toBlock: "latest",
        });
        assert.equal(productPurchasedEvent.length, 1, "ProductPurchased event not emitted");
        assert.equal(productPurchasedEvent[0].returnValues.buyer, buyer, "Event buyer address mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.productId, 0, "Event product ID mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.price, price, "Event product price mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.loyaltyPointsEarned, loyaltyPointsEarned, "Event loyalty points mismatch");
    });

    it("should allow a buyer to purchase a product using loyalty points", async () => {
        const name = "Product 3";
        const price = web3.utils.toWei("3", "ether");

        await shop.addProduct(name, price, { from: owner });

        // Issue loyalty points to the buyer
        await shop.issuePoints(buyer, web3.utils.toWei("1", "ether"), "QmTestHash", { from: owner });

        const initialOwnerBalance = await web3.eth.getBalance(owner);
        const initialBuyerBalance = await web3.eth.getBalance(buyer);

        const tx = await shop.buyProduct(0, true, { from: buyer, value: price });

        const finalOwnerBalance = await web3.eth.getBalance(owner);
        const finalBuyerBalance = await web3.eth.getBalance(buyer);

        assert.equal(
            web3.utils.toBN(finalOwnerBalance).toString(),
            web3.utils.toBN(initialOwnerBalance).add(web3.utils.toBN(price).sub(web3.utils.toBN(web3.utils.toWei("1", "ether")))).toString(),
            "Owner balance mismatch"
        );
        assert.isBelow(
            Number(finalBuyerBalance),
            Number(initialBuyerBalance) - Number(price) + Number(web3.utils.toWei("1", "ether")),
            "Buyer balance mismatch"
        );

        const loyaltyPointsEarned = (price * 5) / 100;
        const buyerLoyaltyPoints = await shop.pointsBalance(buyer);
        assert.equal(
            buyerLoyaltyPoints.points.toString(),
            loyaltyPointsEarned.toString(),
            "Loyalty points mismatch"
        );

        const productPurchasedEvent = await shop.getPastEvents("ProductPurchased", {
            fromBlock: 0,
            toBlock: "latest",
        });
        assert.equal(productPurchasedEvent.length, 1, "ProductPurchased event not emitted");
        assert.equal(productPurchasedEvent[0].returnValues.buyer, buyer, "Event buyer address mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.productId, 0, "Event product ID mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.price, price, "Event product price mismatch");
        assert.equal(productPurchasedEvent[0].returnValues.loyaltyPointsEarned, loyaltyPointsEarned, "Event loyalty points mismatch");
    });
});
