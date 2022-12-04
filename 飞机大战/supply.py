import pygame
from random import *


class BulletSupply(pygame.sprite.Sprite):
	def __init__(self, bgsize):
		super().__init__()
		self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = bgsize[0], bgsize[1]
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class BombSupply(pygame.sprite.Sprite):
	def __init__(self, bgsize):
		super().__init__()
		self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = bgsize[0], bgsize[1]
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class LifeSupply(pygame.sprite.Sprite):
	def __init__(self, bgsize):
		super().__init__()
		self.image = pygame.image.load("images/life.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = bgsize[0], bgsize[1]
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
		self.speed = 2
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100

