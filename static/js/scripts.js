document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch portfolio data
    function fetchPortfolio() {
        fetch('/api/portfolio')
            .then(response => response.json())
            .then(data => {
                // Update portfolio table
                const portfolio = document.getElementById("portfolio-value");
                portfolio.textContent = `$${data.toFixed(2)}`;
            })
            .catch(error => console.error('Error fetching portfolio:', error));
    }

    // Function to fetch cash balance
    function fetchProfit() {
        fetch('/api/profit')
            .then(response => response.json())
            .then(data => {
                // Update cash balance
                document.getElementById("profit-loss").textContent = `$${data.toFixed(2)}`;
            })
            .catch(error => console.error('Error fetching cash balance:', error));
    }

    function fetchCash() {
        fetch('/api/cash')
            .then(response => response.json())
            .then(data => {
                // Update cash balance
                document.getElementById("account-cash").textContent = `$${data.toFixed(2)}`;
            })
            .catch(error => console.error('Error fetching cash balance:', error));
    }

    // Function to fetch last 10 transactions
    function fetchTransactions() {
        fetch('/api/transactions')
            .then(response => response.json())
            .then(data => {
                // Update transaction history
                const transactionHistoryList = document.getElementById("transaction-history");
                transactionHistoryList.innerHTML = '';
                data.forEach(transaction => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td><strong>${transaction.type.toUpperCase()}</strong></td> 
                        <td>${transaction.stock}</td>
                        <td>${transaction.quantity}</td>
                        <td>$${transaction.price}</td>
                        <td>$${transaction.total_tax}</td>
                        <td>${transaction.message.toUpperCase()}</td>
                    `;
                    transactionHistoryList.appendChild(row);
                });
            })
    }
    function fetchStockData() {
        fetch('/api/get_stock_data')
            .then(response => response.json())
            .then((data)=>{
            updateStockTable(data.stocks);
        })
        .catch(error => console.error('Error fetching transactions:', error));
    }

    function updateStockTable(stocks) {
        const stocksTableBody = document.getElementById('stocks-table-body');
        stocksTableBody.innerHTML = '';  // Clear the existing table body content

        for (const [stockName, stockDetails] of Object.entries(stocks)) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${stockName}</td>
                <td>$${stockDetails.current_price.toFixed(2)}</td>
                <td>${stockDetails.quantity}</td>
            `;
            stocksTableBody.appendChild(row);
        }
    }

    // Fetch initial data on page load
    fetchTransactions();
    fetchPortfolio();
    fetchCash();
    fetchProfit();
    fetchStockData();
});
