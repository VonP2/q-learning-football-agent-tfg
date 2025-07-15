import random
import numpy as np
import pygame, sys, time
from  .ball import Ball
from .goal import Goal
from .player import Player
from .obstacle import Obstacle
from agent.qLearningAgent import QLearningAgent
import threading
import math

pygame.init()

class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class GamerightQ:
    #SCREEN CONFIGURATION
    SCREEN_WIDTH, SCREEN_HEIGHT = 680, 480

    #TEAMS CONFIGURATION

    #TEAM LEFT
    TEAM_LEFT_TAG = "left"
    TEAM_LEFT_CONTROLS = [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a]
    TEAM_LEFT_WIDTH, TEAM_LEFT_HEIGHT = 42,42
    TEAM_LEFT_ORIGINAL_X, TEAM_LEFT_ORIGINAL_Y = 2*(SCREEN_WIDTH-TEAM_LEFT_WIDTH)//7,(SCREEN_HEIGHT - TEAM_LEFT_HEIGHT)//2
    TEAM_LEFT_MAX_SPEED = 5
    TEAM_LEFT_ACCELERATION = 0.5
    TEAM_LEFT_DECELERATION = 0.1
    TEAM_LEFT_COLOR = "blue"
    
    #TEAM RIGHT
    TEAM_RIGHT_TAG = "right"
    TEAM_RIGHT_CONTROLS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
    TEAM_RIGHT_WIDTH, TEAM_RIGHT_HEIGHT = 42,42
    TEAM_RIGHT_ORIGINAL_X, TEAM_RIGHT_ORIGINAL_Y = 5*(SCREEN_WIDTH-TEAM_RIGHT_WIDTH)//7,(SCREEN_HEIGHT - TEAM_LEFT_HEIGHT)//2
    TEAM_RIGHT_MAX_SPEED = 5
    TEAM_RIGHT_ACCELERATION = 0.5
    TEAM_RIGHT_DECELERATION = 0.1
    TEAM_RIGHT_COLOR = "red"
    
    #BALL CONFIGURATION
    BALL_DECELERATION = 0.1
    BALL_RADIUS = 15
    possible_x = [SCREEN_WIDTH / 2, (SCREEN_WIDTH / 2) - 180, (SCREEN_WIDTH / 2) + 180]
    possible_y = [SCREEN_HEIGHT / 2, (SCREEN_HEIGHT / 2) - 130, (SCREEN_HEIGHT / 2) + 130]

    while True:
        BALL_ORIGINAL_X = random.choice(possible_x)
        BALL_ORIGINAL_Y = random.choice(possible_y)
        if not ((BALL_ORIGINAL_X == SCREEN_WIDTH / 2 and BALL_ORIGINAL_Y == SCREEN_HEIGHT / 2) or ((BALL_ORIGINAL_X == (SCREEN_WIDTH / 2 + 180))and BALL_ORIGINAL_Y == SCREEN_HEIGHT / 2) 
                or ((BALL_ORIGINAL_X == (SCREEN_WIDTH / 2 - 180))and BALL_ORIGINAL_Y == SCREEN_HEIGHT / 2)):
            break
    BALL_MAX_SPEED = 0
    BALL_COLOR = "white"
    
    #GOALS CONFIGURATION
    GOAL_L_WIDTH,GOAL_L_HEIGHT = 7.8,480
    GOAL_R_WIDTH,GOAL_R_HEIGHT = 7.8,480
    GOAL_L_POS_X, GOAL_L_POS_Y = 0, 0
    GOAL_R_POS_X, GOAL_R_POS_Y = 673,0

    #SCORE CONFIGURATION
    SCORE_FONT = pygame.font.SysFont("comicsans",60)
    WINNING_SCORE = 5
    REWARD_LOOKUP = {0: 1, 1: 2, 2: 4, 3: 8}
    REWARD_LOOKDOWN = {0:8, 1:6, 2:4, 3:2}
    
    def __init__(self, window, window_width, window_height):
    
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        self.max_distance = math.sqrt(self.window_width ** 2 + self.window_height ** 2)
        
        self.left_team_score = 0
        self.right_team_score = 0
        self.left_hits = 0
        self.right_hits = 0
        
        self.left_score = 0
        self.right_score = 0
        
        #Q LEARNING
        self.reward_L = 0
        self.reward_R = 0

        self.ball_hited = False

        self.area_reward_ball = 300

        # GROUP SETUP
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # SPRITE SETUP
        goalL = Goal((self.GOAL_L_POS_X,self.GOAL_L_POS_Y),(self.GOAL_L_WIDTH,self.GOAL_L_HEIGHT),[self.all_sprites,self.collision_sprites], "A")
        goalR = Goal((self.GOAL_R_POS_X,self.GOAL_R_POS_Y),(self.GOAL_R_WIDTH,self.GOAL_R_HEIGHT),[self.all_sprites,self.collision_sprites], "B")
       
        self.obstacles = []

        self.player2_team_right = Player(self.all_sprites,self.collision_sprites, self.TEAM_RIGHT_CONTROLS, self.TEAM_RIGHT_COLOR, self.TEAM_RIGHT_WIDTH, self.TEAM_RIGHT_HEIGHT, self.TEAM_RIGHT_ORIGINAL_X, self.TEAM_RIGHT_ORIGINAL_Y, self.TEAM_RIGHT_TAG, self.TEAM_RIGHT_MAX_SPEED, self.TEAM_RIGHT_ACCELERATION, self.TEAM_RIGHT_DECELERATION,self)
        self.players = [self.player2_team_right]
        self.right_team_players = []

        self.start_time = time.time()
        self.ball_near_timer = time.time()
        self.test_ai_timer = time.time()
        self.done = False

        self.actions_limit = 1000
        self.reward_update = 15
        self.actions_counter = 0
        self.reward_scored = 0

        for player in self.players:
            if player.team == "right":
                self.right_team_players.append(player)
            for playerother in self.players:
                if playerother is not player:
                    player.otherplayers.append(playerother)
                    
        self.ball = Ball(self.all_sprites,self.collision_sprites,self.players,goalL, goalR, self.BALL_RADIUS, self.BALL_COLOR, self.BALL_MAX_SPEED, self.BALL_ORIGINAL_X+self.BALL_RADIUS, self.BALL_ORIGINAL_Y, self.BALL_DECELERATION, self)
        for player in self.players:
            player.ball = self.ball
        
        self.pos_ini = self.ball.pos.x
        self.area_ini = self.player2_team_right.discretize_relative_position_x(self.ball.pos.x - self.GOAL_R_POS_X)
        self._last_reward_frame = -1
        self.reward_a = 0
        self.reward_h = 0
        
        
        
        

    def ball_hit(self, team_tag):
        self.ball_hited = True
            
        
    def goalScored(self, side):
        self.ball.reset()
        self.pos_ini = self.ball.pos.x
        self.ball_hited = False

        for player in self.players:
            player.reset()

        if side == "left":
            self.right_team_score += 0.5
            self.reward_R += 20
        else:
            self.reward_R = -20
            self.left_team_score += 0.5

        
        self.actions_counter = 0
        self.done = True


    def notGoalScored(self):
        self.ball.reset()
        self.pos_ini = self.ball.pos.x
        self.ball_hited = False

        for player in self.players:
            player.reset()

        self.actions_counter = 0
        self.done = True

    def calculateReward(self):
        return  self.reward_R

    def distanceBallToGoals(self):
        distanceL = math.sqrt((self.GOAL_L_POS_X - self.ball.pos.x) ** 2 + 
                             (self.GOAL_L_POS_Y- self.ball.pos.y) ** 2)
        
        distanceR = math.sqrt((self.GOAL_R_POS_X - self.ball.pos.x) ** 2 + 
                             (self.GOAL_R_POS_Y- self.ball.pos.y) ** 2)
        
        return distanceL, distanceR


    def moveToBallReward(self, current_frame):
        if self._last_reward_frame == current_frame or self.done:
            return        

        state = self.player2_team_right.get_state(self.ball)
        ball_x, ball_y, discrete_goal_x, discrete_angle, distance_ball, near_goal = state[0], state[1], state[2], state[3], state[4], state[5]

        reward_direction = self._calculate_directional_reward(ball_x, ball_y, distance_ball)
        reward_ball_angle = self._calculate_alignment_reward(discrete_angle, distance_ball)
        reward_ball_shot = self._calculate_shot_reward(discrete_angle, distance_ball, discrete_goal_x, near_goal)
        reward_encouragment = self._encouragement_reward(distance_ball, discrete_goal_x)

        total_reward = reward_direction + reward_ball_angle + reward_ball_shot + reward_encouragment
        
        if total_reward >0:
            self.reward_R += total_reward

        self._last_reward_frame = current_frame

    def _calculate_directional_reward(self, ball_x, ball_y, distance_ball):
        if distance_ball == 0:
            return 0
        reward = 0
        moving_up = self.player2_team_right.y_speed < 0
        moving_down = self.player2_team_right.y_speed > 0
        moving_left = self.player2_team_right.x_speed < 0
        moving_right = self.player2_team_right.x_speed > 0
        
        if (ball_x == -1 and moving_left) or (ball_x == 1 and moving_right):
            reward += 1.5
        
        if (ball_y == -1 and moving_up) or (ball_y == 1 and moving_down):
            reward += 1.5
        
        if reward >= 3:
            reward += 1
        
        return reward
    

    def _calculate_shot_reward(self, alignment, distance_ball, discrete_goal_x, near_goal):

        if alignment != 1 or distance_ball != 0 or near_goal != 1:
            return 0

        reward = 0
        moving_left = self.ball.x_speed < 0
        moving_right = self.ball.x_speed > 0

        if (discrete_goal_x == -1 and moving_left) or (discrete_goal_x == 1 and moving_right):
            reward += 1.5
       
        return reward


    def _calculate_alignment_reward(self, alignment, distance_ball):

        if distance_ball == 2:
            return 0

        if alignment == 1: # PERFECT
            return 2.0
        elif alignment == 0: # OK
            return 0.3
        elif alignment == -1: # BAD
            return -1.0  
        return 0
    
    def _encouragement_reward(self, distance_ball, discrete_goal_x):
        if distance_ball == 0:
            moving_right = self.ball.x_speed > 0
            moving_left = self.ball.x_speed < 0

            if (discrete_goal_x == 1 and moving_right) or (discrete_goal_x == -1 and moving_left):
                return 1.5
        return 0



        
    def draw(self, screen,left_score, right_score):
        screen.fill("orange")

        left_score_text = self.SCORE_FONT.render(f"{int(self.left_team_score)}",1,"blue")
        right_score_text = self.SCORE_FONT.render(f"{int(self.right_team_score)}",1,"red")
        screen.blit(left_score_text,(self.SCREEN_WIDTH//4 - left_score_text.get_width()//2, 5))
        screen.blit(right_score_text,(self.SCREEN_WIDTH * (3/4) - right_score_text.get_width()//2, 5))

    def loop(self, agentR, footballGame):

        self.agentR = agentR

        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 10)

        while True:
                
                self.draw(self.window, self.left_score, self.right_score)
                
                #footballGame.train_ai_single_agent(self.agentR,self.done)
                #footballGame.play_ai_single_agent(self.agentR)
                footballGame.test_agent(self.agentR)

                self.moveToBallReward(self.actions_counter)

                self.done = False
                fps = clock.get_fps()
                fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
                self.window.blit(fps_text, (10, 10))

                self.all_sprites.update()
                self.all_sprites.draw(self.window)
            
                pygame.display.update()
                
                game_info = GameInformation(self.left_hits, self.right_hits, self.left_score, self.right_score)

                clock.tick(240)

                self.actions_counter +=1
                if self.actions_counter % self.actions_limit == 0:
                    self.notGoalScored()