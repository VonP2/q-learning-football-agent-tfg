import matplotlib.pyplot as plt

class TrainingMonitor:
    def __init__(self):
        self.episodes = []

        self.results_L = []
        self.results_R = []
        self.goal_pct_L = []
        self.goal_pct_R = []
        self.total_goals_L = 0
        self.total_goals_R = 0

        self.actions = []
        self.mean_actions = []

        plt.ion()
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 10))

        self.line_res_L, = self.ax1.plot([], [], label='Resultado L (Gol=1/Propia=-1/Nada=0)', color='blue')
        self.line_res_R, = self.ax1.plot([], [], label='Resultado R (Gol=1/Propia=-1/Nada=0)', color='red')
        self.ax1.set_ylabel('Resultado del Episodio')
        self.ax1.set_xlabel('Episodio')
        self.ax1.set_ylim(-1.5, 1.5)
        self.ax1.legend()

        self.line_pct_L, = self.ax2.plot([], [], label='% Goles L', color='blue')
        self.line_pct_R, = self.ax2.plot([], [], label='% Goles R', color='red')
        self.ax2.set_ylabel('Tasa de Éxito (%)')
        self.ax2.set_xlabel('Episodio')
        self.ax2.set_ylim(0, 100)
        self.ax2.legend()

        self.line_act, = self.ax3.plot([], [], label='Acciones Totales', color='purple')
        self.line_mean, = self.ax3.plot([], [], label='Media Acciones', linestyle='--', color='orange')
        self.ax3.set_ylabel('Acciones por Episodio')
        self.ax3.set_xlabel('Episodio')
        self.ax3.legend()

    def update_plot(self, episode, reward_L, reward_R, total_actions):
        self.episodes.append(episode)

        result_L = 1 if reward_L >= 40 else -1 if reward_L <= -30 else 0
        result_R = 1 if reward_R >= 40 else -1 if reward_R <= -30 else 0
        self.results_L.append(result_L)
        self.results_R.append(result_R)

        if result_L == 1:
            self.total_goals_L += 1
        if result_R == 1:
            self.total_goals_R += 1
        self.goal_pct_L.append((self.total_goals_L / len(self.episodes)) * 100)
        self.goal_pct_R.append((self.total_goals_R / len(self.episodes)) * 100)

        self.actions.append(total_actions)
        self.mean_actions.append(sum(self.actions) / len(self.actions))

        self.line_res_L.set_xdata(self.episodes)
        self.line_res_L.set_ydata(self.results_L)
        self.line_res_R.set_xdata(self.episodes)
        self.line_res_R.set_ydata(self.results_R)

        self.line_pct_L.set_xdata(self.episodes)
        self.line_pct_L.set_ydata(self.goal_pct_L)
        self.line_pct_R.set_xdata(self.episodes)
        self.line_pct_R.set_ydata(self.goal_pct_R)

        self.line_act.set_xdata(self.episodes)
        self.line_act.set_ydata(self.actions)
        self.line_mean.set_xdata(self.episodes)
        self.line_mean.set_ydata(self.mean_actions)

        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_xlim(0, max(self.episodes) + 1)

        max_actions = max(self.actions + [1])
        self.ax3.set_ylim(0, max_actions + 5)

        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_plot(self, filename):
        self.fig.savefig(filename)
