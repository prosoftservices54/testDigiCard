import numpy as np
import csv

# -------------------------------------- Meta parameters --------------------------------------
# Global preferences for each reward
# The global preference is a value between 0 and 1
global_preference = {
    1: 0.2,
    2: 0.4,
    3: 0.3,
    4: 0.4,
    5: 0.5,
}
std_preference = {
    1: 0.09,
    2: 0.15,
    3: 0.1,
    4: 0.1,
    5: 0.3
}
rewards = list(global_preference.keys())


# Number of commands per client
mean_number_of_rewards = 20
std_number_of_rewards = 8


# Max and min preference
MAX_PREFERENCE = 0.975
MIN_PREFERENCE = 0.025


class Customer:
    """
    A customer is defined by its number and its preferences for each reward.
    """

    HISTORY_SIZE = 10
    STATE_SIZE = HISTORY_SIZE*2

    def __init__(self, number):
        """
        Constructor of the class Customer.
        The preferences are randomly generated for each reward based on the global preferences.
        They must be unknown to the agent.
        :param number:
        """
        self.number = number
        self.number_of_rewards_done = 0
        self.number_of_rewards_to_have = int(np.random.normal(mean_number_of_rewards, std_number_of_rewards))
        self.preferences = {}
        self.history = []
        for reward in global_preference:
            preference = np.random.normal(global_preference[reward], std_preference[reward])
            if preference < MIN_PREFERENCE:
                preference = MIN_PREFERENCE
            if preference > MAX_PREFERENCE:
                preference = MAX_PREFERENCE
            self.preferences[reward] = preference


    @staticmethod
    def generate_customers(number_of_customers):
        """
        Generate a list of customers.
        :param number_of_customers:
        :return:
        """
        clients = []
        for i in range(number_of_customers):
            clients.append(Customer(i))
        return clients


    def get_preference(self, reward):
        """
        Return the satisfaction of the customer for a reward.
        :param reward:
        :return:
        """
        return self.preferences[reward]


    def get_state(self):
        """
        Return the state of the customer. The state is the history of rewards and satisfaction in the last 30 commands.
        The format of the state is a list of 60 values: 30 rewards and 30 satisfactions in one vector.
        :return:
        """
        reward_history = [reward for reward, _ in self.history]
        satisfaction_history = [satisfaction for _, satisfaction in self.history]

        if len(reward_history) > self.HISTORY_SIZE:
            reward_history = reward_history[-self.HISTORY_SIZE:]
            satisfaction_history = satisfaction_history[-self.HISTORY_SIZE:]

        while len(reward_history) < self.HISTORY_SIZE:
            reward_history = [0] + reward_history
            satisfaction_history = [0] + satisfaction_history

        state = reward_history + satisfaction_history

        return np.array(state)


    def is_coming_with_reward(self, reward):
        """
        The customer decides if he comes with a reward.
        The decision is based on the satisfaction of the customer for the reward.
        :param reward:
        :return:
        """
        is_coming = np.random.random() <= self.preferences[reward]
        is_coming = 1 if is_coming else 0
        self.history.append((reward, is_coming))
        return is_coming
