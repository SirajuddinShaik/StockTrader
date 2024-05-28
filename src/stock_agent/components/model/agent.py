import os
import tensorflow as tf
import tensorflow.keras as keras # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
import numpy as np

from stock_agent.components.model.networks import create_actor_model_3, create_critic_model
from stock_agent.components.model.reply_buffer import ReplayBuffer


class Agent:
    def __init__(self, input_dims, action_dims, save_dir, alpha=0.001, beta=0.002, gamma=0.99, max_size=250, tau=0.005, batch_size=64, re_train=False):
        self.gamma = gamma
        self.tau = tau
        self.memory = ReplayBuffer(max_size, input_dims, action_dims)
        self.batch_size = batch_size
        self.save_dir = save_dir
        self.re_train = re_train
        self.actor = create_actor_model_3(input_dims)
        self.target_actor = create_actor_model_3(input_dims)
        self.critic = create_critic_model(input_dims,action_dims)
        self.target_critic = create_critic_model(input_dims,action_dims)

        self.actor.compile(optimizer=Adam(learning_rate=alpha))
        self.critic.compile(optimizer=Adam(learning_rate=beta))
        self.target_actor.compile(optimizer=Adam(learning_rate=alpha))
        self.target_critic.compile(optimizer=Adam(learning_rate=beta))

        self.update_network_parameters(tau=1)

    def update_network_parameters(self, tau=None):
        if tau is None:
            tau = self.tau

        new_weights = []
        target_variables = self.target_actor.weights
        for i, variable in enumerate(self.actor.weights):
            new_weights.append(tau * variable + (1 - tau) * target_variables[i])
        self.target_actor.set_weights(new_weights)

        new_weights = []
        target_variables = self.target_critic.weights
        for i, variable in enumerate(self.critic.weights):
            new_weights.append(tau * variable + (1 - tau) * target_variables[i])
        self.target_critic.set_weights(new_weights)

        if self.re_train:
            self.load_models()

    def remember(self, state, action, reward, new_state):
        self.memory.store_transition(state, action, reward, new_state)

    def save_models(self):
        self.actor.save_weights(os.path.join(self.save_dir, 'actor.h5'))
        self.target_actor.save_weights(os.path.join(self.save_dir, 'target_actor.h5'))
        self.critic.save_weights(os.path.join(self.save_dir, 'critic.h5'))
        self.target_critic.save_weights(os.path.join(self.save_dir, 'target_critic.h5'))

    def load_models(self):
        self.actor.load_weights(os.path.join(self.save_dir, 'actor.h5'))
        self.target_actor.load_weights(os.path.join(self.save_dir, 'target_actor.h5'))
        self.critic.load_weights(os.path.join(self.save_dir, 'critic.h5'))
        self.target_critic.load_weights(os.path.join(self.save_dir, 'target_critic.h5'))

    def choose_action(self, observation):
        state = tf.convert_to_tensor([observation], dtype=tf.float32)
        actions = self.actor(state)
        return actions[0]

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        state, action, reward, new_state = self.memory.sample_buffer(self.batch_size)

        states = tf.convert_to_tensor(state, dtype=tf.float32)
        states_ = tf.convert_to_tensor(new_state, dtype=tf.float32)
        rewards = tf.convert_to_tensor(reward, dtype=tf.float32)
        actions = tf.convert_to_tensor(action, dtype=tf.float32)

        # Critic learning step
        with tf.GradientTape() as tape:
            target_actions = self.target_actor(states_)
            critic_value_ = tf.squeeze(self.target_critic([states_, target_actions]), 1)
            critic_value = tf.squeeze(self.critic([states, actions]), 1)
            target = rewards + self.gamma * critic_value_
            critic_loss = keras.losses.MSE(target, critic_value)

        critic_network_gradient = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic.optimizer.apply_gradients(zip(critic_network_gradient, self.critic.trainable_variables))

        # Actor learning step
        with tf.GradientTape() as tape:
            new_policy_actions = self.actor(states)
            actor_loss = -self.critic([states, new_policy_actions])
            actor_loss = tf.math.reduce_mean(actor_loss)

        actor_network_gradient = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor.optimizer.apply_gradients(zip(actor_network_gradient, self.actor.trainable_variables))

        self.update_network_parameters()
