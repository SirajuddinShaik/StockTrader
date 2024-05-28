# Custom Environment Definition
import numpy as np

class StockMarketEnv:
    def __init__(self, num_stocks, sampler, history_len = 10, min_balance = 30000, initial_cash = 150000):
        self.num_stocks = num_stocks
        self.h_l = history_len
        self.initial_cash = initial_cash
        self.close = 3
        self.min_balance = min_balance
        self.sampler = sampler
        self.reset(init = True)

    def reset(self,init = False):
        self.cash = self.initial_cash
        self.stocks = np.array(np.zeros(self.num_stocks),dtype=np.int16)
        if self.sampler.pointer > self.sampler.samples -55:
            self.sampler.reset()
        self.portfolio_value = self.initial_cash
        self.previous_portfolio_value = self.portfolio_value
        self.data = [np.concatenate((self.stocks, [self.cash], [self.portfolio_value], self.sampler.sample())) for i in range(self.h_l)]
        self.current_step = 0
        if not init:
            return self.get_observation()

    def take_action(self, action):
        if np.isnan(action).any():
            raise ValueError("Action contains NaN values")
        action_arr = action[0]

        buy = action[1]
        sell = action[2]
        sell_stocks = np.array(sell * self.stocks, dtype=np.int16)
        # print(action_arr,buy,sell)
        # new_stocks = action[:-1] * (self.cash + np.sum(self.data[-1][26:].reshape((self.num_stocks,5))[:, self.close] * self.stocks) - 10000)
        # new_stocks = np.round(new_stocks / np.maximum(self.data[-1][26:].reshape((20,5))[:, self.close], 1e-8))  # Avoid division by zero
        # print(f"New stocks: {np.array(new_stocks,dtype=np.int16)}")

        # self.stocks = tf.squeeze(new_stocks)
        for i in range(self.num_stocks):
            stock_price = self.data[-1][26:].reshape(20,5)[i][self.close]
            if stock_price < 1e-8:
                stock_price = 1e-8
            if action_arr[i] == 1:  # Sell
                quantity = sell_stocks[i]
                revenue = quantity * stock_price
                self.stocks[i] -= quantity
                brokerage = 20
                stt = 0.1 / 100 * revenue
                transaction_charge = 0.00325 / 100 * revenue
                gst = 18 / 100 * brokerage
                sebi_fee = 0.0001 / 100 * revenue
                stamp_duty = 0.015 / 100 * revenue
                total_cost = brokerage + stt + transaction_charge + gst + sebi_fee + stamp_duty
                self.cash += revenue - total_cost
        if self.cash > self.min_balance:
            new_stocks = buy * (self.cash - self.min_balance)
            new_stocks = np.array(new_stocks / np.maximum(self.data[-1][26:].reshape((20,5))[:, self.close], 1e-8),dtype=np.int16)
            for i in range(self.num_stocks):
                stock_price = self.data[-1][26:].reshape(20,5)[i][self.close]
                if stock_price < 1e-8:
                    stock_price = 1e-8  # Avoid issues with zero prices
                if action_arr[i] == 0: # Buy
                    quantity = new_stocks[i]
                    self.stocks[i] += quantity
                    cost = quantity * stock_price
                    brokerage = 20
                    stt = 0.1 / 100 * cost
                    transaction_charge = 0.00325 / 100 * cost
                    gst = 18 / 100 * brokerage
                    sebi_fee = 0.0001 / 100 * cost
                    stamp_duty = 0.015 / 100 * cost
                    total_cost = cost + brokerage + stt + transaction_charge + gst + sebi_fee + stamp_duty
                    self.cash -= total_cost

        if np.isnan(self.portfolio_value):
            raise ValueError("Portfolio value contains NaN values")

    def step(self, action):
        self.update_curr_prices()
        self.take_action(action)

        # Recalculate the portfolio value
        # self.update_portfolio()

        # Calculate reward as the change in portfolio value
        reward = self.portfolio_value - self.previous_portfolio_value

        # Calculate the Sharpe ratio
        risk_free_rate = 0.01
        excess_return = reward - risk_free_rate
        standard_deviation = np.std([self.previous_portfolio_value, self.portfolio_value]) if self.current_step > 0 else 1
        sharpe_ratio = excess_return / standard_deviation if standard_deviation != 0 else 0

        if np.isnan(reward):
            raise ValueError("Reward contains NaN values")

        self.current_step += 1
        obs = self.get_observation()

        return (obs, sharpe_ratio, 1.0)


    def get_observation(self):
        observation = np.array(self.data)
        if np.isnan(observation).any():
            raise ValueError("Observation contains NaN values")
        return observation.astype(np.float32)

    def update_curr_prices(self):
        new_data = self.sampler.sample()
        self.update_portfolio(new_data)
        self.data.pop(0)
        concat = np.concatenate((
            self.stocks,
            [self.cash],
            [self.portfolio_value],
            new_data))
        self.data.append(concat)
        if np.isnan(np.array(self.data)).any():
            raise ValueError("Current prices contain NaN values")


    def update_portfolio(self,new_data):
        self.previous_portfolio_value = self.portfolio_value
        self.portfolio_value = self.cash + np.sum(self.stocks * new_data[4:].reshape((self.num_stocks,5))[:, self.close])
        if np.isnan(self.portfolio_value) or self.portfolio_value < 0:
            raise ValueError("Portfolio value contains NaN values or is negative")

    def render(self, mode='human', close=False):
        profit = self.portfolio_value - self.initial_cash
        print(f'Step: {self.current_step}, Cash: {self.cash}, Stocks: {self.stocks}, Portfolio Value: {self.portfolio_value}, Profit: {profit}')
