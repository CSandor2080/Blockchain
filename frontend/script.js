document.addEventListener("DOMContentLoaded", async () => {
    const productList = document.getElementById("product-list");
    const buyModal = document.getElementById("buyModal");
    const buyerAddressInput = document.getElementById("buyerAddress");
    const usePointsCheckbox = document.getElementById("usePoints");
    const cancelButton = document.getElementById("cancelButton");
    const confirmButton = document.getElementById("confirmButton");

    const shopTab = document.getElementById("shopTab");
    const walletsTab = document.getElementById("walletsTab");
    const shopPage = document.getElementById("shopPage");
    const walletsPage = document.getElementById("walletsPage");
    const getWalletInfoButton = document.getElementById("getWalletInfoButton");
    const walletAddressInput = document.getElementById("walletAddress");
    const walletInfo = document.getElementById("walletInfo");
    const ethBalanceSpan = document.getElementById("ethBalance");
    const loyaltyPointsSpan = document.getElementById("loyaltyPoints");

    let selectedProductId = null;

    shopTab.addEventListener("click", () => {
        shopPage.classList.remove("hidden");
        walletsPage.classList.add("hidden");
    });

    walletsTab.addEventListener("click", () => {
        shopPage.classList.add("hidden");
        walletsPage.classList.remove("hidden");
    });

    const getIcon = (productType) => {
        switch (productType) {
            case 'coffee':
                return '<span class="material-icons">local_cafe</span>';
            case 'beer':
                return '<span class="material-icons">sports_bar</span>';
            case 'burger':
                return '<span class="material-icons">fastfood</span>';
            case 'pasta':
                return '<span class="material-icons">restaurant</span>';
            case 'pizza':
                return '<span class="material-icons">local_pizza</span>';
            default:
                return '<span class="material-icons">shopping_cart</span>';
        }
    };

    const fetchProducts = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8080/get-products");
            const products = response.data;
            products.forEach(product => {
                const productCard = document.createElement("div");
                productCard.className = "bg-white p-6 rounded-lg shadow-lg";
                productCard.innerHTML = `
                    <div class="flex items-center mb-4">
                        ${getIcon(product.product_type)}
                        <h3 class="text-xl font-bold ml-2">${product.name}</h3>
                    </div>
                    <p class="text-gray-700 mb-4">${product.price} ETH</p>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded buy-button" data-id="${product.product_id}">Buy</button>
                `;
                productList.appendChild(productCard);
            });

            document.querySelectorAll(".buy-button").forEach(button => {
                button.addEventListener("click", (event) => {
                    selectedProductId = event.target.dataset.id;
                    buyerAddressInput.value = "";
                    usePointsCheckbox.checked = false;
                    buyModal.classList.remove("hidden");
                });
            });
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    };

    const buyProduct = async (productId, buyerAddress, usePoints) => {
        try {
            const response = await axios.post(`http://127.0.0.1:8080/buy-product/${productId}`, null, {
                params: {
                    buyer_address: buyerAddress,
                    use_points: usePoints
                }
            });
            alert("Product purchased successfully!");
            buyModal.classList.add("hidden");
        } catch (error) {
            console.error("Error buying product:", error);
            alert("Error buying product!");
        }
    };

    confirmButton.addEventListener("click", () => {
        const buyerAddress = buyerAddressInput.value;
        const usePoints = usePointsCheckbox.checked;
        buyProduct(selectedProductId, buyerAddress, usePoints);
    });

    cancelButton.addEventListener("click", () => {
        buyModal.classList.add("hidden");
    });

    const getWalletInfo = async (walletAddress) => {
        try {
            const balanceResponse = await axios.get(`http://127.0.0.1:8080/balance/${walletAddress}`);
            const pointsResponse = await axios.get(`http://127.0.0.1:8080/points-balance/${walletAddress}`);

            ethBalanceSpan.textContent = balanceResponse.data.balance;
            loyaltyPointsSpan.textContent = pointsResponse.data.points;
            walletInfo.classList.remove("hidden");
        } catch (error) {
            console.error("Error fetching wallet info:", error);
            alert("Error fetching wallet info!");
        }
    };

    getWalletInfoButton.addEventListener("click", () => {
        const walletAddress = walletAddressInput.value;
        getWalletInfo(walletAddress);
    });

    fetchProducts();
});
