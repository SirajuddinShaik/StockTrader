from datetime import datetime
import os
import time
import numpy as np
import pymongo
from pymongo import MongoClient
import requests

from stock_agent.components.deployment.environment import DeploymentStockMarketEnv
from stock_agent.utils.common import get_symbols

class StockTransactionManager:
    def __init__(self, connection_string, db_name):
        # Connect to MongoDB
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.stocks_collection = self.db['stocks']
        self.transactions_collection = self.db['transactions']
        self.account_collection = self.db['account']
        self.api_key1 = os.environ["TWELVE_DATA_API"]
        self.api_key2 = os.environ["TWELVE_DATA_API2"]
        self.api_key3 = os.environ["TWELVE_DATA_API3"]
        self.symbols = get_symbols()
        self.prices = [0]*20
        self.previous_prices = [0]*20
        self.day = -1

        # Initialize the account if not exists
        if self.account_collection.count_documents({}) == 0:
            self.account_collection.insert_one({
                "_id": "9949",
                "cash": 0,
                "stocks": {self.symbols[i]: {"quantity": 0, "current_price": 0, "previous_price": 0} for i in range(20)},
                "portfolio": 0,
                "investment" : 0,
                "cash" : 0,
                "history" : {"date":[],"profit":[]},
                "h_l" : 10,
                "previous_portfolio_value" : 0,
                "data" : [i.tolist() for i in np.zeros((20,))],
                "current_step" : 3,
                "prices" : self.prices,
                "last_pred_time_stamp" : "time_step",
            })
        self.history=self.get_history()

    def get_account_state(self):
        return self.account_collection.find_one({"_id": "9949"})

    def update_account_state(self, env:DeploymentStockMarketEnv):
        time_step = datetime.now()
        time_step = time_step.strftime("%d-%m-%Y %H:%M:%S")
        self.account_collection.update_one({"_id": "9949"},{"$set":{
                "stocks": {self.symbols[i]: {"quantity": int(env.stocks[i]), "current_price": self.prices[i], "previous_price" :self.previous_prices[i]} for i in range(20)},
                "portfolio": env.portfolio_value,
                "investment" : env.initial_cash,
                "min_balance" : env.min_balance,
                "cash" : env.cash,
                "num_stocks" :env.num_stocks,
                "h_l" : env.h_l,
                "previous_portfolio_value" : env.previous_portfolio_value,
                "data" : [i.tolist() for i in env.data],
                "current_step" : env.current_step,
                "prices" : self.prices,
                "history" : self.history,
                "last_pred_time_stamp" : time_step,
            }})
    
    def set_account_state(self, env:DeploymentStockMarketEnv):
        account_state = self.account_collection.find_one({"_id": "9949"})
        if account_state:
            env.stocks = np.array([account_state["stocks"].get(symbol, {}).get("quantity", 0) for symbol in self.symbols])
            env.portfolio_value = account_state.get("portfolio", 0)
            env.initial_cash = account_state.get("investment", 0)
            env.min_balance = account_state.get("min_balance", 0)
            env.cash = account_state.get("cash", 0)
            env.num_stocks = account_state.get("num_stocks", 0)
            env.h_l = account_state.get("h_l", 0)
            env.previous_portfolio_value = account_state.get("previous_portfolio_value", 0)
            env.data = [np.array(data) for data in account_state.get("data", [])]
            env.current_step = account_state.get("current_step", 0)
            self.prices = account_state.get("prices", [0]*20)
            self.history = account_state.get("history", {"date":[],"profit":[]})
    
    def transaction(self, type, stock, quantity, price, total_tax, message):
        self.transactions_collection.insert_one({
                "type": type,
                "stock": stock,
                "quantity": quantity,
                "price" : price,
                "total_tax" : total_tax,
                "time_step" : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "message" : message,

            })


    def get_transactions(self):
        return list(self.transactions_collection.find())

    def get_portfolio(self):
        account_state = self.get_account_state()
        return account_state['portfolio']
    def get_profit(self):
        account_state = self.get_account_state()
        return account_state['portfolio'] - account_state['investment']

    def get_history(self):
        account_state = self.get_account_state()
        return account_state['history']

    def get_cash(self):
        account_state = self.get_account_state()
        return account_state['cash']
    
    def get_last_10_transactions(self):
        transactions = list(self.transactions_collection.find().sort('_id', -1).limit(10))
        # Convert ObjectId to string for JSON serialization
        for transaction in transactions:
            transaction['_id'] = str(transaction['_id'])
        return transactions

    def get_curr_prices(self):
        # return np.zeros((104,))
        try:
            dt_str = datetime.now()
            dt_str = dt_str.strftime("%Y-%m-%d %H:%M:%S")
            components = dt_str.replace('-', ' ').replace(':', ' ').split()[:-2]
            day = int("".join([str(i) for i in components[:3]]))
            if self.day != day:
                self.previous_prices = self.prices[:]
                self.day = day
                self.history["date"].append(day)
                self.history["profit"].append(self.get_profit())

            exchange_api = os.environ["Exchange_API"]
            exc = f"https://v6.exchangerate-api.com/v6/{exchange_api}/latest/USD"
            current_price = requests.get(exc).json()["conversion_rates"]["INR"]
            print(f"current -----sdfsdfsdfsdfds------------>{current_price}")
            for i,symbol in enumerate(self.symbols):
                uri = f"https://api.twelvedata.com/time_series?apikey={self.api_key1}&interval=1min&format=JSON&outputsize=1&type=stock&symbol={symbol}&end_date={dt_str}"
                response = requests.get(uri).json()
                if response["status"] == "error":
                    uri = f"https://api.twelvedata.com/time_series?apikey={self.api_key2}&interval=1min&format=JSON&outputsize=1&type=stock&symbol={symbol}&end_date={dt_str}"
                    response = requests.get(uri).json()
                if response["status"] == "error":
                    uri = f"https://api.twelvedata.com/time_series?apikey={self.api_key3}&interval=1min&format=JSON&outputsize=1&type=stock&symbol={symbol}&end_date={dt_str}"
                    response = requests.get(uri).json()
                if response["status"] == "error":
                    time.sleep(61)
                    response = requests.get(uri).json()
                data = response["values"][0]
                self.prices[i] =  float(data["close"]) * current_price
                for type in ["open", "high", "low", "close", "volume"]:
                    if type == "volume":
                        components.append(data[type])
                    else:
                        components.append(float(data[type]) * current_price)

            components = list(map(float, components))
            print(len(components),components)
            return components
        except Exception as e:
            print(e)
            return False
# Example usage
if __name__ == "__main__":
    api_key = os.environ["mongo_db"]
    CONNECTION_STRING = f"mongodb+srv://{api_key}@cluster0.acdf1pn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "stock_db"

    manager = StockTransactionManager("mongodb://localhost:27017/?retryWrites=false&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000", "stock_db")
    # manager = StockTransactionManager(CONNECTION_STRING, DB_NAME)
    
    # Example operations
    manager.deposit_cash(10000)
    manager.buy_stock("1", 10, 50, 5)
    manager.sell_stock("1", 5, 55, 2)
    manager.withdraw_cash(500)
    
    # print("Account State:", manager.get_account_state())
    # print("Transactions:", manager.get_transactions())
    # print("Portfolio:", manager.get_portfolio())
    # print("Cash:", manager.get_cash())
    print("Last 10 Transactions:", manager.get_last_10_transactions())
