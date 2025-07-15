import time
import pygame
from enviroment.game_left_Q import GameleftQ as Gameleft
from monitor.testMonitorSingle import TrainingMonitorL
from agent.qLearningAgent import QLearningAgent
import pickle
import sys

width, height = 680, 480
window = pygame.display.set_mode((width, height))

class FootballGameLQ:
    def __init__(self, window, width, height):
        self.game = Gameleft(window, width, height)
        self.left_team_players = self.game.left_team_players
        self.left_team_player_1 = self.left_team_players[0]
        self.ball = self.game.ball
        self.num_resets = 0
        self.total_reward_L = 0
        self.agent = None
        self.last_save_time = pygame.time.get_ticks()
        self.last_save_time_g = pygame.time.get_ticks()
        self.final_step = 0
        self.save_interval_seconds = 150000

    def train_ai_single_agent(self, agent, done):
        state = self.left_team_player_1.get_state(self.ball)

        action = agent.act(state)
        self.game.player1_team_left.input(action)

        reward = self.calculate_rewardL()
        next_state = self.left_team_player_1.get_state(self.ball)

        agent.update_q_table(state, action, reward, next_state)
        agent.log_episode_result( reward, done)

        current_time = pygame.time.get_ticks()
        if (current_time - self.last_save_time) > self.save_interval_seconds:
            agent.save("agent/q_learning_agent_left")
            self.last_save_time = current_time

        if agent.done():
            state = self.left_team_player_1.get_state(self.ball)

            self.num_resets += 1
            self.total_reward_L += agent.rewards
            if self.num_resets %100 == 0:
                mean = self.total_reward_L / self.num_resets
                
                monitor.update_plot(self.num_resets, agent.rewards, mean)

                if self.num_resets%1000==0:
                    monitor.save_plot("graficaL.png")

            if self.num_resets > 100000:
                print("Training completed. 100,000 episodes reached.")
                agent.save("agent/q_learning_agent_left")
                monitor.save_plot("graphs/graficaL.png")
                sys.exit()

            agent.reset_rewards()
            agent.reset_done()
            agent.decay_epsilon()

    def play_ai_single_agent(self, agent):
        state = self.left_team_player_1.get_state(self.ball)
        agent.epsilon = 0.0
        action = agent.act(state) 
        self.game.player1_team_left.input(action)

        reward = self.calculate_rewardL()
        agent.log_episode_result(reward, self.game.done)

        if agent.done():
            self.num_resets += 1
            self.total_reward_L += agent.rewards
            mean = self.total_reward_L / self.num_resets
            print(f"Mean reward: {mean}")
            monitor.update_plot(self.num_resets, agent.rewards, mean)
            monitor.save_plot("graphs/graficaLResultado.png")
            agent.reset_rewards()
            agent.reset_done()
    
    def test_agent(self, agent,steps):
        total_goals = 0
        state = self.left_team_player_1.get_state(self.ball)
        action = agent.act(state)
        self.game.player1_team_left.input(action)
        reward = self.calculate_rewardL()
        agent.log_episode_result( reward, self.game.done)

        if not agent.done():
            self.final_step = steps

        if agent.done():
            self.num_resets += 1
            self.total_reward_L += agent.rewards
            mean = self.total_reward_L / self.num_resets
            print(f"Mean reward: {mean}")
            agent.reset_rewards()
            agent.reset_done()

            total_goals = self.game.left_team_score
            print(f"Goal scoring rate: {total_goals/self.num_resets:.2%}")

            if self.num_resets ==100:
                sys.exit()

    def calculate_rewardL(self):
        rewardL = self.game.reward_L
        self.game.reward_L = 0
        return rewardL

if __name__ == "__main__":
    football_game = FootballGameLQ(window, width, height)
    
    agentL = QLearningAgent(324, 4)
    monitor = TrainingMonitorL()

    agentL.load("agent/q_learning_agent_left")

    football_game.game.loop(agentL, football_game)
