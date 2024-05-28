import numpy as np
import pandas as pd

from stock_agent.components.model.agent import Agent
from stock_agent.components.model.data_provider import DataProvider
from stock_agent.components.model.environment import StockMarketEnv
from stock_agent.entity.config_entity import ModelTrainerConfig
from stock_agent import logger

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config
        data = pd.read_csv(self.config.data_dir)
        sampler = DataProvider(data)
        self.env = StockMarketEnv(
            num_stocks=20,
            sampler=sampler,
            history_len=self.config.history_len 
        )
        self.agent = Agent(
            input_dims=self.env.get_observation().shape,
            action_dims=(3,20),
            alpha=self.config.alpha,
            beta=self.config.beta,
            gamma=self.config.gamma,
            max_size=self.config.max_size,
            tau=self.config.tau,
            batch_size=self.config.batch_size,
            save_dir = self.config.root_dir,
            re_train = self.config.re_train,
        )
        self.N = 30
        f = open(self.config.best_score_file)
        score =f.readline().strip()
        if score == "":
            self.best_score = 0
        else:
            self.best_score = float(score)
        self.score_history = []
        self.state=""


    def train_episode(self, epoch):
        observation = self.env.reset()
        n_steps = 0
        score = 0
        while self.env.portfolio_value > self.env.initial_cash - 50000 and n_steps < 300:
            action = self.agent.choose_action(observation)
            observation_, reward, info = self.env.step(action)
            score += reward
            n_steps+=1
            self.agent.remember(observation, action, reward, observation_)
            # if not load_checkpoint:
            if n_steps % self.N == 0:
                self.agent.learn()
                print(self.env.render())
            observation = observation_

        self.score_history.append(score)
        avg_score = np.mean(self.score_history[-100:])

        if avg_score > self.best_score:
            self.best_score = avg_score
            self.agent.save_models()

        self.state=f"episode:{epoch}, {'score %.1f' % score}, {'avg score %.1f' % avg_score}"
        print(self.state)

    def train(self):
        for epoch in range(self.config.epochs):
            self.train_episode(epoch)
        f = open(self.config.best_score_file,"w")
        f.write(str(self.best_score))
        logger.info(self.state)
        logger.info(self.env.render())
        # self.agent.save_models()