

// Converts JSON to HTML list
function jsonToHtmlList(data) {
    let html = '<ul class="list-disc ml-6">';
    for (const key in data) {
        const value = typeof data[key] === 'object' ? jsonToHtmlList(data[key]) : data[key];
        html += `<li><strong>${key}:</strong> ${value}</li>`;
    }
    html += '</ul>';
    return html;
}

// All previous function definitions: getWallets, getAccountBalance, etc.
    const apiBaseUrl = 'http://127.0.0.1:8080'; // Replace with your FastAPI backend URL

    // Utility function to convert objects to HTML lists
    function jsonToHtmlList(data) {
        let html = '<ul class="list-disc ml-6">';
        for (const key in data) {
            const value = typeof data[key] === 'object' ? jsonToHtmlList(data[key]) : data[key];
            html += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        html += '</ul>';
        return html;
    }

    // Fetch and display the list of wallets
    async function getWallets() {
        const response = await fetch(`${apiBaseUrl}/wallets`);
        const data = await response.json();
        document.getElementById('walletsOutput').innerHTML = jsonToHtmlList(data);
    }

    // Fetch and display the balance of a specific account
    async function getAccountBalance() {
        const account = document.getElementById('balanceAccount').value;
        const response = await fetch(`${apiBaseUrl}/balance/${account}`);
        const data = await response.json();
        document.getElementById('balanceOutput').innerHTML = jsonToHtmlList(data);
    }

    // Issue loyalty points to a specified address
    async function issuePoints() {
        const to = document.getElementById('issueTo').value;
        const points = document.getElementById('issuePoints').value;
        const response = await fetch(`${apiBaseUrl}/issue-points/${to}/${points}`, { method: 'POST' });
        const data = await response.json();
        document.getElementById('issueOutput').innerHTML = jsonToHtmlList(data);
    }

    // Redeem points for a specified address
    async function redeemPoints() {
        const to = document.getElementById('redeemTo').value;
        const points = document.getElementById('redeemPoints').value;
        const response = await fetch(`${apiBaseUrl}/redeem-points/${to}/${points}`, { method: 'POST' });
        const data = await response.json();
        document.getElementById('redeemOutput').innerHTML = jsonToHtmlList(data);
    }

    // Purchase a beverage, issuing points to the customer
    async function purchaseBeverage() {
        const customer = document.getElementById('purchaseCustomer').value;
        const response = await fetch(`${apiBaseUrl}/purchase-beverage/${customer}`, { method: 'POST' });
        const data = await response.json();
        document.getElementById('purchaseOutput').innerHTML = jsonToHtmlList(data);
    }

    // Redeem beverages for points
    async function redeemBeverage() {
        const customer = document.getElementById('redeemBevCustomer').value;
        const points = document.getElementById('redeemBevPoints').value;
        const response = await fetch(`${apiBaseUrl}/redeem-beverage/${customer}/${points}`, { method: 'POST' });
        const data = await response.json();
        document.getElementById('redeemBevOutput').innerHTML = jsonToHtmlList(data);
    }

    // Fetch and display the balance of loyalty points
    async function getPointsBalance() {
        const account = document.getElementById('balancePoint').value;
        const response = await fetch(`${apiBaseUrl}/points-balance/${account}`);
        const data = await response.json();
        document.getElementById('pointsBalanceOutput').innerHTML = jsonToHtmlList(data);
    }