import time
import pygame
from enviroment.game_right_Q import GamerightQ as Gameright
from monitor.trainingMonitorSinglePlayer import TrainingMonitorR
from agent.qLearningAgent import QLearningAgent
import pickle
import sys

width, height = 680, 480
window = pygame.display.set_mode((width, height))

class FootballGameRQ:
    def __init__(self, window, width, height):
        self.game = Gameright(window, width, height)
        self.right_team_players = self.game.right_team_players
        self.right_team_player_1 = self.right_team_players[0]
        self.ball = self.game.ball
        self.num_resets = 0
        self.total_reward_R = 0
        self.agent = None
        self.last_save_time = pygame.time.get_ticks()
        self.last_save_time_g = pygame.time.get_ticks()

        self.save_interval_seconds = 150000

    def train_ai_single_agent(self, agent, done):
        state = self.right_team_player_1.get_state(self.ball)

        action = agent.act(state)
        self.game.player2_team_right.input(action)

        reward = self.calculate_rewardR()
        next_state = self.right_team_player_1.get_state(self.ball)

        agent.update_q_table(state, action, reward, next_state)
        agent.log_episode_result( reward, done)

        current_time = pygame.time.get_ticks()
        if (current_time - self.last_save_time) > self.save_interval_seconds:
            agent.save("agent/q_learning_agent_right")
            self.last_save_time = current_time

        if agent.done():
            state = self.right_team_player_1.get_state(self.ball)

            self.num_resets += 1
            self.total_reward_R += agent.rewards
            if self.num_resets %100 == 0:
                mean = self.total_reward_R / self.num_resets                
                monitor.update_plot(self.num_resets, agent.rewards, mean)

                if self.num_resets%1000==0:
                    monitor.save_plot("graphs/graficaR.png")

            if self.num_resets > 100000:
                print("Training completed. 100,000 episodes reached.")
                agent.save("agent/q_learning_agent_right")
                monitor.save_plot("graphs/graficaR.png")
                sys.exit()

            agent.reset_rewards()
            agent.reset_done()
            agent.decay_epsilon()

    def play_ai_single_agent(self, agent):
        state = self.right_team_player_1.get_state(self.ball)
        agent.epsilon = 0.0
        action = agent.act(state)
        self.game.player2_team_right.input(action)
        reward = self.calculate_rewardR()
        agent.log_episode_result( reward, self.game.done)

        if agent.done():
            self.num_resets += 1
            self.total_reward_R += agent.rewards
            mean = self.total_reward_R / self.num_resets
            print(f"Mean reward: {mean}")
            monitor.update_plot(self.num_resets, agent.rewards, mean)
            monitor.save_plot("graphs/graficaRResultado.png")
            agent.reset_rewards()
            agent.reset_done()
    
    def test_agent(self, agent):
        total_goals = 0
        state = self.right_team_player_1.get_state(self.ball)
        action = agent.act(state)
        self.game.player2_team_right.input(action)
        reward = self.calculate_rewardR()
        agent.log_episode_result( reward, self.game.done)

        if agent.done():
            self.num_resets += 1
            self.total_reward_R += agent.rewards
            mean = self.total_reward_R / self.num_resets
            print(f"Mean reward: {mean}")
            monitor.update_plot(self.num_resets, agent.rewards, mean)
            monitor.save_plot("graphs/graficaRResultado.png")
            agent.reset_rewards()
            agent.reset_done()

            total_goals = self.game.right_team_score
            print(f"Goal scoring rate: {total_goals/self.num_resets:.2%}")

    def calculate_rewardR(self):
        rewardR = self.game.reward_R
        self.game.reward_R = 0
        return rewardR

if __name__ == "__main__":
    football_game = FootballGameRQ(window, width, height)
    
    agentR = QLearningAgent(324, 4)

    monitor = TrainingMonitorR()

    agentR.load("agent/q_learning_agent_right")

    football_game.game.loop(agentR, football_game)
