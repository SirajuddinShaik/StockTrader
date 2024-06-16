document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch all data
    function fetchAllData() {
        fetch('/api/all_data')
            .then(response => response.json())
            .then(data => {
                // Update portfolio value
                document.getElementById("portfolio-value").textContent = `₹${data.portfolio.toFixed(2)}`;
                
                // Update profit/loss
                if(data.profit > 0){
                    document.getElementById("profit-loss").style.color = "#29d145";
                }else{
                    document.getElementById("profit-loss").style.color = "red";
                }
                document.getElementById("profit-loss").textContent = `₹${data.profit.toFixed(2)}`;

                // Update cash balance
                document.getElementById("account-cash").textContent = `₹${data.cash.toFixed(2)}`;
                document.getElementById("min-cash").textContent = `₹${data.minCash.toFixed(2)}`;

                // Update investment
                document.getElementById("investment").textContent = `₹${data.investment.toFixed(2)}`;

                // Update last prediction date
                document.getElementById("last-prediction-date").textContent = `${data.lastPrediction}`;

                // Update start date
                document.getElementById("start-date").textContent = `${data.startDate}`;

                // Update transaction history
                const transactionHistoryList = document.getElementById("transaction-history");
                transactionHistoryList.innerHTML = '';
                data.transactions.forEach(transaction => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td><strong>${transaction.type.toUpperCase()}</strong></td> 
                        <td>${transaction.stock}</td>
                        <td>${transaction.quantity}</td>
                        <td>₹${transaction.price.toFixed(2)}</td>
                        <td>₹${transaction.total_tax.toFixed(2)}</td>
                        <td>${transaction.time_step}</td>
                        <td>${transaction.message.toUpperCase()}</td>
                    `;
                    transactionHistoryList.appendChild(row);
                });

                // Update stock data
                const stocksTableBody = document.getElementById('stocks-table-body');
                stocksTableBody.innerHTML = '';  // Clear the existing table body content
                for (const [stockName, stockDetails] of Object.entries(data.stocks)) {
                    const row = document.createElement('tr');
                    if(stockDetails.current_price >= stockDetails.previous_price ){
                        color = "#29d145";
                    }else{
                        color = "red";
                    }
                    row.innerHTML = `
                        <td>${stockName}</td>
                        <td>₹${stockDetails.previous_price.toFixed(2)}</td>
                        <td style="color: ${color};">₹${stockDetails.current_price.toFixed(2)}</td>
                        <td>${stockDetails.quantity}</td>
                    `;
                    stocksTableBody.appendChild(row);
                }
                

        const lmctx = document.getElementById('lastMonthChart').getContext('2d');
        
        // Create the chart
        const mylmChart = new Chart(lmctx, {
            type: 'line', // Specify the chart type
            data: {
                labels: data.history.date,
                datasets: [{
                    label: 'Last Month',
                    data: data.history.date,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        ticks: {
                            callback: function(value) {
                                return Number.isInteger(value) ? value : null;
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return Number.isInteger(value) ? value : null;
                            }
                        }
                    }
                }
            }
        });

        const ctx = document.getElementById('allTimeChart').getContext('2d');
        
        // Create the chart
        const myalChart = new Chart(ctx, {
            type: 'line', // Specify the chart type
            data: {
                labels: data.history.date,
                datasets: [{
                    label: 'All Time Profit',
                    data: data.history.date,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        ticks: {
                            callback: function(value) {
                                return Number.isInteger(value) ? value : null;
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return Number.isInteger(value) ? value : null;
                            }
                        }
                    }
                }
            }
        });

            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Fetch initial data on page load
    fetchAllData();
});
