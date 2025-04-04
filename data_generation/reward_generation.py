import numpy as np
import csv

# -------------------------------------- Meta parameters --------------------------------------
# Global preferences for each reward
# The global preference is a value between 0 and 1
global_preference = {
    "R001": 0.2,
    "R002": 0.6,
    "R003": 0.4,
    "R004": 0.4,
    "R005": 0.8
}
std_preference = {
    "R001": 0.1,
    "R002": 0.2,
    "R003": 0.1,
    "R004": 0.1,
    "R005": 0.05
}
rewards = list(global_preference.keys())

number_of_clients = 400

# Number of commands per client
mean_number_of_rewards = 15
std_number_of_rewards = 8


# Max and min preference
MAX_PREFERENCE = 0.975
MIN_PREFERENCE = 0.025


# -------------------------------------- Data generation --------------------------------------

with open("data.csv", 'w+', newline='') as data_file:
    writer = csv.writer(data_file)

    for client in range(number_of_clients):
        # Generate the number of rewards for the client
        number_of_rewards_for_client = int(np.random.normal(mean_number_of_rewards, std_number_of_rewards))

        # Prevent the number of rewards to be less than 1
        if number_of_rewards_for_client < 1:
            number_of_rewards_for_client = 1

        # Generate the preferences for the client
        preferences = {}
        for reward in global_preference:
            preference = np.random.normal(global_preference[reward], std_preference[reward])
            if preference < MIN_PREFERENCE:
                preference = MIN_PREFERENCE
            if preference > MAX_PREFERENCE:
                preference = MAX_PREFERENCE
            preferences[reward] = preference


        # Generate the commands for the client
        for command in range(number_of_rewards_for_client):
            reward_for_client = np.random.choice(rewards)
            is_client_coming = np.random.random() <= preferences[reward_for_client]
            row = [client, reward_for_client, is_client_coming]
            writer.writerow(row)
