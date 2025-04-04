import numpy as np
from customer_simulation import Customer
from q_learning import DQNAgent, Env


env = Env(100)
state_size = Customer.STATE_SIZE
action_size = len(env.rewards)

# Charger le modèle sauvegardé pour l'évaluation
agent = DQNAgent(state_size, action_size)
agent.load("model.keras")

agent.epsilon = 0

# Évaluation du modèle
num_test_episodes = 5
total_percentage = 0

for episode in range(num_test_episodes):
    print(f"Test Episode {episode + 1}/{num_test_episodes}")
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    score = 0

    max_score = 50

    for t in range(50):
        action = agent.act(state)
        next_state, reward, done = env.step(action)

        if next_state is not None:
            next_state = np.reshape(next_state, [1, state_size])

        score += reward
        state = next_state

    percentage = (score / max_score) * 100
    total_percentage += percentage

average_percentage = total_percentage / num_test_episodes
print(f"Performance moyenne sur {num_test_episodes} épisodes de test : {average_percentage:.2f}%")
