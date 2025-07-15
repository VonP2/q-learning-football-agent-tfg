import random
import pygame, time

class Ball(pygame.sprite.Sprite):
	"""
	CONSTRUCTOR
	"""
	def __init__(self, groups, obstacles, players, goal_L, goal_R, ball_radius, ball_color, ball_max_speed, ball_pos_x, ball_pos_y, deceleration, game):
		
		#Position, size and color
		super().__init__(groups)
		self.radius = ball_radius
		self.color = ball_color
		self.original_x = ball_pos_x
		self.original_y = ball_pos_y
		self.game = game
		
		#Sprites and rectangles
		self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
		self.rect = self.image.get_rect(center=(self.original_x, self.original_y))
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.old_rect = self.rect.copy()
		
		#Speeds
		self.max_x_speed = ball_max_speed
		self.max_y_speed = ball_max_speed
		self.x_speed = 0
		self.y_speed = 0
		self.deceleration = deceleration/5
		
		
		
		#Obstacles
		self.obstacles = obstacles
		self.players = players
		self.goal_L = goal_L
		self.goal_R = goal_R

		self.cooldownTimer = 0
		
	"""
	COLLISION HANDLER
	"""
	def collision(self,direction):
		from .game import Game
		from .player import Player
		from .obstacle import Obstacle
		collision_sprites = pygame.sprite.spritecollide(self,self.obstacles,False)
		actual_time = pygame.time.get_ticks()
		
		for player in self.players:
			if self.rect.colliderect(player.rect):
				collision_sprites.append(player)
		if self.rect.colliderect(self.goal_L.rect):
			collision_sprites.append(self.goal_L)
		if self.rect.colliderect(self.goal_R.rect):
			collision_sprites.append(self.goal_R)
		
		if collision_sprites:
		
			"""
			HORIZONTAL COLLISION
			"""

			if direction == 'horizontal':
				for sprite in collision_sprites:
					
					"""
					HORIZONTAL-RIGHT COLLISION
					"""
					
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left
						self.pos.x = self.rect.x

						if isinstance(sprite, Player):
							self.rect.right = sprite.rect.left
							self.pos.x = self.rect.x
							self.x_speed = min(sprite.x_speed*1.25, self.x_speed *(-1))
							self.y_speed += sprite.y_speed*0.5
							self.game.ball_hit(sprite.team)						
								
						elif self.goal_L in collision_sprites:
							self.game.goalScored("left")

						elif self.goal_R in collision_sprites:
							self.game.goalScored("right")

						else:
							self.rect.right = sprite.rect.left
							self.pos.x = self.rect.x
							self.x_speed = self.x_speed * (-1)

					"""
					HORIZONTAL-LEFT COLLISION
					"""

					if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
						self.rect.left = sprite.rect.right
						self.pos.x = self.rect.x

						if isinstance(sprite, Player): 
							self.rect.left = sprite.rect.right
							self.pos.x = self.rect.x
							self.x_speed = max(sprite.x_speed*1.25, self.x_speed *(-1))
							self.y_speed += sprite.y_speed*0.5
							self.game.ball_hit(sprite.team)

						elif self.goal_L in collision_sprites:
							self.game.goalScored("left")

						elif self.goal_R in collision_sprites:
							self.game.goalScored("right")

						else:
							self.rect.left = sprite.rect.right
							self.pos.x = self.rect.x
							self.x_speed = self.x_speed * (-1)

			"""
			VERTICAL COLLISION
			"""		
		
			if direction == 'vertical':
				for sprite in collision_sprites:
				
					"""
					VERTICAL_BOTTOM COLLISION
					"""
					
					if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top
						self.pos.y = self.rect.y
						
						if isinstance(sprite, Player):
							self.rect.bottom = sprite.rect.top
							self.pos.y = self.rect.y
							self.y_speed = min(sprite.y_speed*1.25, self.y_speed * (-1) )
							self.x_speed += sprite.x_speed*0.5
							self.game.ball_hit(sprite.team)

						elif self.goal_L in collision_sprites:
							self.game.goalScored("left")

						elif self.goal_R in collision_sprites:
							self.game.goalScored("right")

						else:
							self.rect.bottom = sprite.rect.top
							self.pos.y = self.rect.y
							self.y_speed = self.y_speed * (-1)
		
					"""
					VERTICAL_TOP COLLISION
					"""

					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom
						self.pos.y = self.rect.y

						if isinstance(sprite, Player):
							self.rect.top = sprite.rect.bottom
							self.pos.y = self.rect.y
							self.y_speed = max(sprite.y_speed*1.25, self.y_speed * (-1) )
							self.x_speed += sprite.x_speed*0.5
							self.game.ball_hit(sprite.team)

						elif self.goal_L in collision_sprites:
							self.game.goalScored("left")

						elif self.goal_R in collision_sprites:
							self.game.goalScored("right")
							
						else:
							self.rect.top = sprite.rect.bottom
							self.pos.y = self.rect.y
							self.y_speed = self.y_speed * (-1)

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
	RESET
	"""
	def reset(self):
		possible_x = self.game.possible_x
		possible_y = self.game.possible_y

		while True:
			self.pos.x = random.choice(possible_x)
			self.pos.y = random.choice(possible_y)
			if not ((self.pos.x == 340 and self.pos.y == 240) or (self.pos.x == 520 and self.pos.y == 240) or (self.pos.x == 160 and self.pos.y == 240) ):
				break  
		self.x_speed = 0
		self.y_speed = 0

		
	def update(self):
	
		
		if self.x_speed > 0:
			self.x_speed -= self.deceleration

		elif self.x_speed < 0:
			self.x_speed += self.deceleration
			
		else:
			self.x_speed = 0

		if self.y_speed > 0:
			self.y_speed -= self.deceleration

		elif self.y_speed < 0:
			self.y_speed += self.deceleration	 
			
		else:
			self.y_speed = 0
	
		self.old_rect = self.rect.copy()
		self.pos.x += self.x_speed 
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')
		self.pos.y += self.y_speed 
		self.rect.y = round(self.pos.y)
		self.collision('vertical')