import json
import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.999884, min_epsilon=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.Q = {}
        self.reset = False
        self.rewards = 0
        self.done_ = False
        self.episodes_per_update = 1
        self.episode_counter = 0

    def get_q_value(self, state, action):
        if (state, action) not in self.Q:
            self.Q[(state, action)] = 0.0
        return self.Q[(state, action)]

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        else:
            q_values = [self.get_q_value(state, a) for a in range(self.action_size)]
            best_action = np.argmax(q_values)
            return best_action

    def update_q_table(self, state, action, reward, next_state):
        learning_rate = self.alpha * (1 + np.log1p(self.episode_counter/1000000))
        old_q = self.Q.get((state, action), 0)
        
        max_next_q = max([self.Q.get((next_state, a), 1.0) for a in range(self.action_size)])
        
        new_q = old_q + learning_rate * (reward + self.gamma * max_next_q - old_q)
        self.Q[(state, action)] = new_q

    def decay_epsilon(self):
        self.episode_counter += 1
        if self.episode_counter % self.episodes_per_update == 0:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.min_epsilon, self.epsilon)

    def log_episode_result(self, reward, done):
        self.rewards = reward
        self.done_ = done
        if done:
            self.reset = True

    def reset_rewards(self):
        self.rewards = 0

    def reset_done(self):
        self.reset = False
        self.done_ = False

    def done(self):
        return self.done_
    
    def save(self, name):
        with open(name + "_q_table.pkl", "wb") as f:
            pickle.dump(self.Q, f)

        with open(name + "_config.json", "w") as f:
            json.dump({
                "epsilon": self.epsilon,
                "epsilon_min": self.min_epsilon,
                "epsilon_decay": self.epsilon_decay,
                "episode_counter": self.episode_counter,
                "episodes_per_update": self.episodes_per_update
            }, f)

    def load(self, name):
        try:
            with open(name + "_q_table.pkl", "rb") as f:
                self.Q = pickle.load(f)
        except FileNotFoundError:
            print("Q-table file not found. Starting with a new Q-table.")

        try:
            with open(name + "_config.json", "r") as f:
                data = json.load(f)
                self.epsilon = data.get("epsilon", self.epsilon)
                self.min_epsilon = data.get("epsilon_min", self.min_epsilon)
                self.epsilon_decay = data.get("epsilon_decay", self.epsilon_decay)
                self.episode_counter = data.get("episode_counter", self.episode_counter)
                self.episodes_per_update = data.get("episodes_per_update", self.episodes_per_update)
                print("EPSILON: ", self.epsilon)
                print("EPISODE COUNTER: ", self.episode_counter)
        except FileNotFoundError:
            print("Configuration file not found. Using default values.")
