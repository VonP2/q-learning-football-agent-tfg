import pygame
import math
from .ball import Ball

class Playeruser(pygame.sprite.Sprite):

    """
	CONSTRUCTOR
	"""
    def __init__(self,groups,obstacles, controls, color, width, height, original_x, original_y, team_tag, max_speed, acceleration, deceleration,game):
        super().__init__(groups)
        
        #CONFIG
        self.color = color
        self.width = width
        self.height = height
        self.original_x = original_x
        self.original_y = original_y
        self.team = team_tag
        self.game = game

        self.GRID_SIZE_X = 5
        self.GRID_SIZE_Y = 5
        self.FIELD_WIDTH = 680
        self.FIELD_HEIGHT = 480
        self.CELL_WIDTH = self.FIELD_WIDTH / self.GRID_SIZE_X
        self.CELL_HEIGHT = self.FIELD_HEIGHT / self.GRID_SIZE_Y

        self.GOAL_R_POS_X = 673
        self.GOAL_R_POS_Y = 150
        self.GOAL_L_POS_X = 0
        self.GOAL_L_POS_Y = 150
        self.GOAL_L_HEIGHT, self.GOAL_R_HEIGHT = 200,200
        self.GOAL_L_WIDTH, self.GOAL_R_WIDTH = 7.8,7.8
        

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        
        # INITIAL POSITION
        self.rect = self.image.get_rect(topleft = (self.original_x, self.original_y))
        self.old_rect = self.rect.copy()
        
        # MOVEMENT
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.x_speed = 0
        self.y_speed = 0
        self.max_x_speed = max_speed
        self.max_y_speed = max_speed
        self.deceleration = deceleration / 5
        self.acceleration = acceleration 
        
        self.obstacles = obstacles
        self.opponent = None
        self.controls = controls
        
        self.otherplayers = []
        
        self.ball = None

        # Q-LEARNING
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.reward = 0
        self.cooldownTimer_L = 0
        self.cooldownTimer_R = 0

    """
	INPUTS
	"""
    
    def input(self, action = None):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:  # UP
            self.y_speed -= self.acceleration
        if keys[pygame.K_DOWN]:  # DOWN
            self.y_speed += self.acceleration
        if keys[pygame.K_LEFT]:  # LEFT
            self.x_speed -= self.acceleration
        if keys[pygame.K_RIGHT]:  # RIGHT
            self.x_speed += self.acceleration
    
    def move(self, y_102, x_102):
        #Arriba
        if y_102 == 1:
            self.y_speed -= self.acceleration
        #Abajo
        if y_102 == 0:
            self.y_speed += self.acceleration
        # Derecha
        if x_102 == 1:
            self.x_speed += self.acceleration
        #izquierda
        if x_102 == 0:
            self.x_speed -= self.acceleration
    
    """
	COLLISION
	"""
    def collision(self):
        from .game import Game
        from .obstacle import Obstacle

        collision_sprites = pygame.sprite.spritecollide(self,self.obstacles,False)
        collision_sprites_with_players = pygame.sprite.spritecollide(self,self.obstacles,False)
        actual_time = pygame.time.get_ticks()

        for player in self.otherplayers:
            if self.rect.colliderect(player.rect):
                collision_sprites_with_players.append(player)
                
        if collision_sprites_with_players:

            """
            HORIZONTAL
            """
            if self.x_speed != 0:
                for sprite in collision_sprites_with_players:
                    """
	                HORI RIGHT
	                """
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        
                    """
	                HORI LEFT
	                """
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x

            """
            VERTICAL
            """
            if self.y_speed != 0:
                for sprite in collision_sprites_with_players:
                
                    """
	                VERTI BOTTOM
	                """
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        
                    """
	                VERTI TOP
	                """
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
        """
        WINDOW COLLISION
        """
        if self.x_speed != 0:
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.x_speed *= -1
            if self.rect.right > Game.SCREEN_WIDTH:
                self.rect.right = Game.SCREEN_WIDTH
                self.pos.x = self.rect.x
                self.x_speed *= -1
                
        if self.y_speed != 0:
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.y_speed *= -1
            if self.rect.bottom > Game.SCREEN_HEIGHT:
                self.rect.bottom = Game.SCREEN_HEIGHT
                self.pos.y = self.rect.y
                self.y_speed *= -1

    """
	UPDATE
	"""
    def update(self):
        if self.x_speed > 0:
            if self.x_speed > self.max_x_speed:
                self.x_speed = self.max_x_speed
            self.x_speed -= self.deceleration

        elif self.x_speed < 0:
            if self.x_speed < -self.max_x_speed:
                self.x_speed = -self.max_x_speed
            self.x_speed += self.deceleration
            
        else:
            self.x_speed = 0

        if self.y_speed > 0:
            if self.y_speed > self.max_y_speed:
                self.y_speed = self.max_y_speed
            self.y_speed -= self.deceleration

        elif self.y_speed < 0:
            if self.y_speed < -self.max_y_speed:
                self.y_speed = -self.max_y_speed
            self.y_speed += self.deceleration    
            
        else:
            self.y_speed = 0
    
        self.old_rect = self.rect.copy()
        self.input()

        self.pos.x += self.x_speed 
        self.rect.x = round(self.pos.x)
        self.pos.y += self.y_speed 
        self.rect.y = round(self.pos.y)
        self.collision()


    def distance_to_enemy_goal(self, goal_position_x, goal_position_y):
        distance = math.sqrt((goal_position_x - self.pos.x) ** 2 + 
                             (goal_position_y - self.pos.y) ** 2)
        return distance
    
    def distance_to_ball(self, ball_position_x, ball_position_y):
        distance = math.sqrt((ball_position_x - self.pos.x) ** 2 + 
                             (ball_position_y - self.pos.y) ** 2)
        return distance

    def discretize_relative_position_3(self, relative_position, axis, grid_size=3):
        max_distance_x = 680
        max_distance_y = 480

        if axis == "x":
            normalized_position = relative_position / max_distance_x
        elif axis == "y":
            normalized_position = relative_position / max_distance_y
        else:
            raise ValueError("axis needs to be 'x' or 'y'")

        if grid_size == 3:
            if normalized_position < -0.05:
                return -1
            elif normalized_position > 0.05:
                return 1
            else:
                return 0
        else:
            raise ValueError("grid_size must be 3")
        
    
    def discretize_relative_position_5(self, relative_position, axis, grid_size=5):
        max_distance_x = 680  
        max_distance_y = 480   

        if axis == "x":
            normalized_position = relative_position / max_distance_x
        elif axis == "y":
            normalized_position = relative_position / max_distance_y
        else:
            raise ValueError("axis must be 'x' or 'y'")

        if grid_size == 5:
            if normalized_position < -0.5:
                return -2
            elif normalized_position < -0.05:
                return -1
            elif normalized_position < 0.05:
                return 0
            elif normalized_position < 0.5:
                return 1
            else:
                return 2
        else:
            raise ValueError("grid_size must be 5")


    def discretize_direction(self, x_speed, y_speed):
        angle = math.atan2(y_speed, x_speed)

        # Discretize angle in 4 directions
        if -math.pi / 4 <= angle < math.pi / 4:
            return 3  # RIGHT
        elif math.pi / 4 <= angle < 3 * math.pi / 4:
            return 0  # UP
        elif -3 * math.pi / 4 <= angle < -math.pi / 4:
            return 2  # LEFT
        else:
            return 1  # DOWN
        
    def discretize_relative_position_x(self, relative_position_x):
        max_distance_x = 680
        normalized_position = abs(relative_position_x) / max_distance_x

        # Discretize position based on the goal
        if normalized_position < 0.25:
            return 3  # REALLY CLOSE
        elif normalized_position < 0.5:
            return 2  # CLOSE
        elif normalized_position < 0.75:
            return 1  # MID
        else:
            return 0  # FAR
        
    def distance_to(self, ball):
        dx = self.pos.x - ball.pos.x
        dy = self.pos.y - ball.pos.y
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def get_shot_alignment(self, ball):
        if self.team == "left":
            goal_x = self.GOAL_R_POS_X
            goal_y = self.GOAL_R_POS_Y + self.GOAL_R_HEIGHT / 2
        else:
            goal_x = self.GOAL_L_POS_X
            goal_y = self.GOAL_L_POS_Y + self.GOAL_L_HEIGHT / 2

        to_ball = (ball.pos.x - self.pos.x, ball.pos.y - self.pos.y)
        to_goal = (goal_x - ball.pos.x, goal_y - ball.pos.y)

        dot = to_ball[0]*to_goal[0] + to_ball[1]*to_goal[1]
        mag1 = (to_ball[0]**2 + to_ball[1]**2)**0.5
        mag2 = (to_goal[0]**2 + to_goal[1]**2)**0.5

        if mag1 == 0 or mag2 == 0:
            return 0

        cos_theta = dot / (mag1 * mag2)

        if cos_theta > 0.9:
            return 1    # GOOD
        elif cos_theta < 0.3:
            return -1   # BAD
        else:
            return 0    # OK

    def is_near_goal(self, ball):
        goal_x = self.GOAL_R_POS_X if self.team == "left" else self.GOAL_L_POS_X
        distance_x = abs(ball.pos.x - goal_x)
        return 1 if distance_x < 150 else 0

    """
	RESET
	"""

    def reset(self):
        self.pos.x = self.original_x
        self.pos.y = self.original_y
        self.x_speed = 0
        self.y_speed = 0

    def get_state(self, ball, etapa=2):
        relative_ball_x = ball.pos.x - self.pos.x
        relative_ball_y = ball.pos.y - self.pos.y
        discrete_relative_ball_x = self.discretize_relative_position_3(relative_ball_x, axis="x", grid_size=3)  # -1, 0, 1
        discrete_relative_ball_y = self.discretize_relative_position_3(relative_ball_y, axis="y", grid_size=3)  # -1, 0, 1

        if self.team == "left":
            discrete_goal_x = 1
        elif self.team == "right":
            discrete_goal_x = -1


        discrete_angle = self.get_shot_alignment(ball)
        
        distance = self.distance_to(ball)

        if distance > 200:
            distance_ball = 2
        elif distance > 80:
            distance_ball = 1
        else:
            distance_ball = 0

        near_goal = self.is_near_goal(ball)
        
        state = [
            discrete_relative_ball_x, discrete_relative_ball_y,
            discrete_goal_x,
            discrete_angle,  
            distance_ball,
            near_goal
            ]
        return tuple(state)