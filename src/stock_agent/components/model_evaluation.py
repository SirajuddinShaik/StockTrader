import pandas as pd
import numpy as np
import tensorflow as tf


from stock_agent.components.model.data_provider import DataProvider
from stock_agent.components.model.environment import StockMarketEnv
from stock_agent import logger
from stock_agent.components.model.networks import create_actor_model_3


class ModelEvaluation:
    def __init__(self,config):
        self.config = config
        data = pd.read_csv(self.config.data_dir)
        sampler = DataProvider(data)
        self.steps = sampler.samples
        self.env = StockMarketEnv(
            num_stocks=20,
            sampler=sampler,
            history_len=self.config.history_len 
        )
        self.actor = create_actor_model_3(self.env.get_observation().shape)
        self.actor.load_weights(config.model)
    
    def eval(self):
        state = self.env.get_observation()
        rewards = []
        for i in range(self.steps-50):
            action = tf.squeeze(self.actor(np.expand_dims(state,0)))
            observation_, reward, info = self.env.step(action)
            rewards.append(reward)
            state = observation_
        avg_reward = np.mean(rewards)
        logger.info(f">>>>>>>>> Avg Reward: {avg_reward} <<<<<<<<<<")
        logger.info(self.env.render())
