import matplotlib.pyplot as plt

class TrainingMonitorL:
    def __init__(self):
        self.episodes = []
        self.results = []
        self.goal_percentages = []
        self.actions_per_episode = []
        self.mean_actions = []

        self.total_goals = 0

        plt.ion()
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 10))

        self.line_result, = self.ax1.plot([], [], label='Resultado del Episodio (Gol=1/Propia=-1/Nada=0)', color='green')
        self.ax1.set_ylabel('Resultado')
        self.ax1.set_xlabel('Episodio')
        self.ax1.set_ylim(-1.5, 1.5)
        self.ax1.legend()

        self.line_goal_pct, = self.ax2.plot([], [], label='Tasa de Éxito (%)', color='blue')
        self.ax2.set_ylabel('% Goles')
        self.ax2.set_xlabel('Episodio')
        self.ax2.set_ylim(0, 100)
        self.ax2.legend()

        self.line_actions, = self.ax3.plot([], [], label='Acciones por Episodio', color='orange')
        self.line_mean_actions, = self.ax3.plot([], [], label='Media de Acciones', color='red')
        self.ax3.set_ylabel('Acciones')
        self.ax3.set_xlabel('Episodio')
        self.ax3.legend()

    def update_plot(self, episode, total_reward, num_actions):
        if total_reward >= 40:
            result = 1
            self.total_goals += 1
        elif total_reward <= -30:
            result = -1
        else:
            result = 0

        self.episodes.append(episode)
        self.results.append(result)
        self.goal_percentages.append((self.total_goals / len(self.episodes)) * 100)
        self.actions_per_episode.append(num_actions)
        self.mean_actions.append(sum(self.actions_per_episode) / len(self.actions_per_episode))

        self.line_result.set_xdata(self.episodes)
        self.line_result.set_ydata(self.results)

        self.line_goal_pct.set_xdata(self.episodes)
        self.line_goal_pct.set_ydata(self.goal_percentages)

        self.line_actions.set_xdata(self.episodes)
        self.line_actions.set_ydata(self.actions_per_episode)

        self.line_mean_actions.set_xdata(self.episodes)
        self.line_mean_actions.set_ydata(self.mean_actions)

        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_xlim(0, max(self.episodes) + 1)

        if self.actions_per_episode:
            self.ax3.set_ylim(0, max(self.actions_per_episode) + 5)

        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_plot(self, filename):
        self.fig.savefig(filename)
