import random

import numpy as np
from keras.src.layers import Dense, Input
from keras.src.losses import MeanSquaredError
from keras.src.optimizers import Adam
from keras.src.saving import load_model

from customer_simulation import Customer
import customer_simulation
from collections import deque
from keras.models import Sequential


class Env:
    def __init__(self, number_of_clients):
        """
        Initialize the environment.
        """
        clients = Customer.generate_customers(number_of_clients)

        # Generate the list of clients in random order that will have a reward (they will come multiple times)
        self.client_data_queue = []
        while len(clients) > 0:
            random_client = random.choice(clients)
            random_client.number_of_rewards_done += 1
            if random_client.number_of_rewards_done >= random_client.number_of_rewards_to_have:
                clients.remove(random_client)
            self.client_data_queue.append(random_client)

        self.current_reward_index = 0
        self.rewards = customer_simulation.rewards


    def reset(self):
        """Reset l'environnement et renvoie l'état initial."""
        self.current_reward_index = 0
        return self.client_data_queue[self.current_reward_index].get_state()

    def step(self, action):
        """
        Effectue une action et renvoie l'état suivant, la récompense, et si l'épisode est terminé.
        action : indice de la récompense choisie
        """
        client = self.client_data_queue[self.current_reward_index]


        reward_name = self.rewards[action]
        model_reward = client.is_coming_with_reward(reward_name)
        #print(model_reward)

        # Calculer le coût de la récompense TODO
        # cost = self.reward_costs[action]

        # Passer au client suivant
        self.current_reward_index += 1
        done = self.current_reward_index >= len(self.client_data_queue)

        return self.client_data_queue[self.current_reward_index].get_state() if not done else None, model_reward, done


class DQNAgent:
    """
    Agent utilisant un réseau de neurones pour apprendre à optimiser les récompenses.
    """
    def __init__(self, state_size, action_size):
        """
        Initialize the agent.
        :param state_size:
        :param action_size:
        """
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()

    def _build_model(self):
        """
        Build the neural network model.
        :return:
        """
        model = Sequential()
        model.add(Input(shape=(self.state_size,)))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(optimizer=Adam(), loss=MeanSquaredError())
        return model


    def remember(self, state, action, reward, next_state, done):
        """
        Store a transition in the memory.
        :param state:
        :param action:
        :param reward:
        :param next_state:
        :param done:
        :return:
        """
        self.memory.append((state, action, reward, next_state, done))


    def act(self, state):
        """
        Choose an action to take.
        :param state:
        :return:
        """
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def save(self, filepath):
        """
        Save the model to a file.
        :param filepath:
        :return:
        """
        self.model.save(filepath)

    def load(self, filepath):
        """
        Load the model from a file.
        :param filepath:
        :return:
        """
        self.model = load_model(filepath)

    def replay(self, batch_size):
        """
        Replay a batch of transitions.
        :param batch_size:
        :return:
        """
        minibatch = random.sample(self.memory, batch_size)

        states = np.array([transition[0] for transition in minibatch])  # états
        actions = np.array([transition[1] for transition in minibatch])  # actions
        rewards = np.array([transition[2] for transition in minibatch])  # récompenses
        next_states = np.array([transition[3] for transition in minibatch])  # next_states
        dones = np.array([transition[4] for transition in minibatch])  # done flags


        for i in range(batch_size):
            state = states[i]
            action = actions[i]
            reward = rewards[i]
            next_state = next_states[i]
            done = dones[i]
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



if __name__ == "__main__":
    env = Env(40)

    state_size = Customer.STATE_SIZE
    action_size = len(env.rewards)

    agent = DQNAgent(state_size, action_size)

    batch_size = 32
    num_episodes = 5

    for episode in range(num_episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])

        for t in range(50):
            print("ITERATION", t, "EPISODE", episode)
            action = agent.act(state)
            next_state, reward, done = env.step(action)

            if next_state is not None:  # Vérifier si next_state n'est pas None
                next_state = np.reshape(next_state, [1, state_size])

            agent.remember(state, action, reward, next_state, done)

            state = next_state

            if done:
                print("episode: {}/{}, score: {}".format(episode, num_episodes, t))
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    agent.save("model.keras")