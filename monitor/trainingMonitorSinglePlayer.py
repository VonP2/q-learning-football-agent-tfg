import matplotlib.pyplot as plt
import numpy as np

class TrainingMonitorL:
    def __init__(self):
        self.episode_count = []
        self.rewards_L = []
        self.total_mean_L = []

        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))

        self.line_rewards_L, = self.ax1.plot([], [], label='Recompensa Total L', color='blue')
        self.ax1.legend()
        self.ax1.set_xlim(0, 10)
        self.ax1.set_ylim(-10, 10)
        self.ax1.set_xlabel('Episodios')
        self.ax1.set_ylabel('Recompensa')

        self.line_mean_L, = self.ax2.plot([], [], label='Media Total L', color='blue')
        self.ax2.legend()
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(-10, 10)
        self.ax2.set_xlabel('Episodios')
        self.ax2.set_ylabel('Media')

    def update_plot(self, episode, total_reward_L, mean_L):
        self.episode_count.append(episode)
        self.rewards_L.append(total_reward_L)
        self.total_mean_L.append(mean_L)

        self.line_rewards_L.set_xdata(self.episode_count)
        self.line_rewards_L.set_ydata(self.rewards_L)

        self.line_mean_L.set_xdata(self.episode_count)
        self.line_mean_L.set_ydata(self.total_mean_L)

        self.ax1.set_xlim(0, max(self.episode_count) + 1)
        self.ax1.set_ylim(min(self.rewards_L) - 1, max(self.rewards_L) + 1)

        self.ax2.set_xlim(0, max(self.episode_count) + 1)
        self.ax2.set_ylim(min(self.total_mean_L) - 1, max(self.total_mean_L) + 1)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_plot(self, filename):
        plt.savefig(filename)


class TrainingMonitorR:
    def __init__(self):
        self.episode_count = []
        self.rewards_L = []
        self.total_mean_L = []

        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))

        self.line_rewards_L, = self.ax1.plot([], [], label='Recompensa Total R', color='blue')
        self.ax1.legend()
        self.ax1.set_xlim(0, 10)
        self.ax1.set_ylim(-10, 10)
        self.ax1.set_xlabel('Episodios')
        self.ax1.set_ylabel('Recompensa')

        self.line_mean_L, = self.ax2.plot([], [], label='Media Total R', color='blue')
        self.ax2.legend()
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(-10, 10)
        self.ax2.set_xlabel('Episodios')
        self.ax2.set_ylabel('Media')

    def update_plot(self, episode, total_reward_L, mean_L):
        self.episode_count.append(episode)
        self.rewards_L.append(total_reward_L)
        self.total_mean_L.append(mean_L)

        self.line_rewards_L.set_xdata(self.episode_count)
        self.line_rewards_L.set_ydata(self.rewards_L)

        self.line_mean_L.set_xdata(self.episode_count)
        self.line_mean_L.set_ydata(self.total_mean_L)

        self.ax1.set_xlim(0, max(self.episode_count) + 1)
        self.ax1.set_ylim(min(self.rewards_L) - 1, max(self.rewards_L) + 1)

        self.ax2.set_xlim(0, max(self.episode_count) + 1)
        self.ax2.set_ylim(min(self.total_mean_L) - 1, max(self.total_mean_L) + 1)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_plot(self, filename):
        plt.savefig(filename)
