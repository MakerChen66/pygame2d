import pygame
from random import *


class Enemy(pygame.sprite.Sprite):
	"""敌机父类"""
	def __init__(self, image, speed, bg_size):
		super().__init__()
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.width, self.height = bg_size[0], bg_size[1]

	# 设置敌机飞行动作，所有的敌机都是从上往下飞行，敌机的位置随机出现
	def move(self, first, two):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			# 敌机飞出屏幕回到原始位置（该位置是一个范围）
			self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
											randint(first * self.height, two * self.height)

	# 使敌机恢复原始位置
	def reset(self, first, two):
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
										randint(first * self.height, two * self.height)


class SmallEnemy(Enemy):
	def __init__(self, bg_size):
		super().__init__("images/enemy1.png", 2, bg_size)
		# 小型敌机毁灭图片切换
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy1_down1.png").convert_alpha(),
									pygame.image.load("images/enemy1_down2.png").convert_alpha(),
									pygame.image.load("images/enemy1_down3.png").convert_alpha(),
									pygame.image.load("images/enemy1_down4.png").convert_alpha()])
		# 设置敌机原始位置
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)
		# 表明敌机目前的状态（为True表明敌机生存，反之为碰撞时毁灭，之后播放毁灭画面，重新调用reset方法，将敌机设置到初始位置）
		self.active = True
		# 返回英雄除了空白区域的部分
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		super().move(-5, 0)

	def reset(self):
		# 将敌机生存状态重新设置为True
		self.active = True
		super().reset(-5, 0)


class MidEnemy(Enemy):
	# 中型敌机打击次数
	energy = 8

	def __init__(self, bg_size):
		super().__init__("images/enemy2.png", 1, bg_size)
		# 中型敌机毁灭图片切换
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy2_down1.png").convert_alpha(),
									pygame.image.load("images/enemy2_down2.png").convert_alpha(),
									pygame.image.load("images/enemy2_down3.png").convert_alpha(),
									pygame.image.load("images/enemy2_down4.png").convert_alpha()])
		# 子弹打击时效果图片
		self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
		# 设置敌机原始位置
		# self.width, self.height = bg_size[0], bg_size[1]
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10 * self.height,
																						  -self.height)
		self.active = True
		# 返回英雄除了空白区域的部分
		self.mask = pygame.mask.from_surface(self.image)
		# 击打次数属性
		self.energy = MidEnemy.energy
		# 是否击中属性
		self.hit = False

	def move(self):
		super().move(-10, -5)

	def reset(self):
		# 将敌机生存状态重新设置为True
		self.active = True
		# 将击打次数重新设置为8
		self.energy = MidEnemy.energy
		super().reset(-10, -5)


class BigEnemy(Enemy):
	# 大型敌机打击次数
	energy = 20

	def __init__(self, bg_size):
		super().__init__("images/enemy3_n1.png", 1, bg_size)
		self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
		# 大型敌机毁灭图片切换
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy3_down1.png").convert_alpha(),
									pygame.image.load("images/enemy3_down2.png").convert_alpha(),
									pygame.image.load("images/enemy3_down3.png").convert_alpha(),
									pygame.image.load("images/enemy3_down4.png").convert_alpha(),
									pygame.image.load("images/enemy3_down5.png").convert_alpha(),
									pygame.image.load("images/enemy3_down6.png").convert_alpha()])
		# 子弹打击时效果图片
		self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
		# 设置敌机原始位置
		# self.width, self.height = bg_size[0], bg_size[1]
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-15 * self.height,
																						  -10 * self.height)
		self.active = True
		# 返回英雄除了空白区域的部分
		self.mask = pygame.mask.from_surface(self.image)
		# 击打次数属性
		self.energy = BigEnemy.energy
		# 是否击中属性
		self.hit = False

	def move(self):
		super().move(-15, -10)

	def reset(self):
		# 将敌机生存状态重新设置为True
		self.active = True
		# 将击打次数重新设置为20
		self.energy = BigEnemy.energy
		super().reset(-15, 10)
