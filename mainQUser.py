import pygame
from enviroment.game_user import Gameuser
from monitor.testMonitorSingle import TrainingMonitorL
from agent.qLearningAgent import QLearningAgent
import pickle
import sys

width, height = 680, 480
window = pygame.display.set_mode((width, height))

class FootballGameUser:
    def __init__(self, window, width, height):
        self.game = Gameuser(window, width, height)
        self.left_team_players = self.game.left_team_players
        self.left_team_player_1 = self.left_team_players[0]
        self.right_team_players = self.game.right_team_players
        self.right_team_player_1 = self.right_team_players[0]
        self.ball = self.game.ball
        self.num_resets = 0
        self.total_reward_L = 0
        self.total_reward_R = 0
        self.agentL = None
        self.agentR = None
        self.last_save_time = pygame.time.get_ticks()
        self.last_save_time_g = pygame.time.get_ticks()
        self.save_interval_seconds = 150000
        self.final_step = 0

    def train_ai(self, agentL, agentR, done):
        stateL = self.left_team_player_1.get_state(self.ball)
        stateR = self.right_team_player_1.get_state(self.ball)

        actionL = agentL.act(stateL)
        actionR = agentR.act(stateR)

        self.game.player1_team_left.input(actionL)
        self.game.player2_team_right.input(actionR)
        
        rewardL = self.calculate_rewardL()
        rewardR = self.calculate_rewardR()

        next_state_L = self.left_team_player_1.get_state(self.ball)
        next_state_R = self.right_team_player_1.get_state(self.ball)
        

        agentL.update_q_table(stateL, actionL, rewardL, next_state_L)
        agentR.update_q_table(stateR, actionR, rewardR, next_state_R)

        agentL.log_episode_result( rewardL, done)
        agentR.log_episode_result( rewardR, done)

        current_time = pygame.time.get_ticks()

        if (current_time - self.last_save_time) > self.save_interval_seconds:
            agentL.save("agent/q_learning_agent_left")
            agentR.save("agent/q_learning_agent_right")
            self.last_save_time = current_time

        if agentL.done() or agentR.done():
            stateL = self.left_team_player_1.get_state(self.ball)
            stateR = self.right_team_player_1.get_state(self.ball)
            
            self.num_resets += 1

            self.total_reward_L += agentL.rewards
            self.total_reward_R += agentR.rewards

            if self.num_resets %100 == 0:
                mean = (self.total_reward_L + self.total_reward_R) / self.num_resets
                meanL = self.total_reward_L / self.num_resets
                meanR = self.total_reward_R / self.num_resets
       
            agentL.reset_rewards()
            agentR.reset_rewards()

            agentL.reset_done()
            agentR.reset_done()

            agentL.decay_epsilon()
            agentR.decay_epsilon()

    
    def play_ai_single_agent(self, agentL, agentR):
        stateL = self.left_team_player_1.get_state(self.ball)
        stateR = self.right_team_player_1.get_state(self.ball)

        agentL.epsilon = 0.0
        agentR.epsilon = 0.0

        actionL = agentL.act(stateL)
        actionR = agentR.act(stateR)
        self.game.player1_team_left.input(actionL)
        self.game.player2_team_right.input(actionR)

        rewardL = self.calculate_rewardL()
        rewardR = self.calculate_rewardL()

        agentL.log_episode_result(rewardL, self.game.done)
        agentR.log_episode_result(rewardR, self.game.done)

        if agentL.done() or agentR.done():
            self.num_resets += 1

            self.total_reward_L += agentL.rewards
            self.total_reward_R += agentR.rewards

            mean = (self.total_reward_L + self.total_reward_R) / self.num_resets
            meanL = self.total_reward_L / self.num_resets
            meanR = self.total_reward_R / self.num_resets

            agentL.reset_rewards()
            agentR.reset_rewards()

            agentL.reset_done()
            agentR.reset_done()
    
    def test_agent(self, agentL, agentR, step, left_is_human=False):
        if not left_is_human:
            stateL = self.left_team_player_1.get_state(self.ball)
            actionL = agentL.act(stateL)
            self.game.player1_team_left.input(actionL)

        stateR = self.right_team_player_1.get_state(self.ball)
        actionR = agentR.act(stateR)
        self.game.player2_team_right.input(actionR)

        rewardR = self.calculate_rewardR()
        agentR.log_episode_result(rewardR, self.game.done)

        if not agentR.done():
            self.final_step = step

        if agentR.done():
            self.num_resets += 1
            self.total_reward_R += agentR.rewards
            meanR = self.total_reward_R / self.num_resets
            print(f"Mean reward Right Agent: {meanR}")
            monitor.update_plot(self.num_resets, agentR.rewards, self.final_step)
            monitor.save_plot("graphs/graficaJugadorResultado.png")
       
            agentR.reset_rewards()
            agentR.reset_done()

            total_goals_R = self.game.right_team_score
            print(f"Goal scoring rate Right Agent: {total_goals_R / self.num_resets:.2%}")

            if self.num_resets== 50: sys.exit()
  
    def calculate_rewardL(self):
        rewardL = self.game.reward_L
        self.game.reward_L = 0
        return rewardL
    
    def calculate_rewardR(self):
        rewardR = self.game.reward_R
        self.game.reward_R = 0
        return rewardR

if __name__ == "__main__":
    football_game = FootballGameUser(window, width, height)
    
    agentL = QLearningAgent(324, 4)
    agentR = QLearningAgent(324, 4)
    
    monitor = TrainingMonitorL()

    agentL.load("agent/q_learning_agent_left")
    agentR.load("agent/q_learning_agent_right")
    
    football_game.game.loop(agentL,agentR,football_game)
