import pygame


class Bullet1(pygame.sprite.Sprite):
	"""普通子弹"""
	def __init__(self, position):
		super().__init__()
		self.image = pygame.image.load("images/bullet1.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.speed = 12
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		self.rect.top -= self.speed
		if self.rect.top < 0:
			self.active = False

	def reset(self, position):
		self.rect.left, self.rect.top = position
		self.active = True


class Bullet2(pygame.sprite.Sprite):
	"""超级子弹"""
	def __init__(self, position):
		super().__init__()
		self.image = pygame.image.load("images/bullet2.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.speed = 18
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		self.rect.top -= self.speed
		if self.rect.top < 0:
			self.active = False

	def reset(self, position):
		self.rect.left, self.rect.top = position
		self.active = True


class Bullet3(pygame.sprite.Sprite):
	"""超级子弹"""
	def __init__(self, position):
		super().__init__()
		self.image = pygame.image.load("images/bullet2.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.speed = 18
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		self.rect.top -= self.speed
		if self.rect.top < 0:
			self.active = False

	def reset(self, position):
		self.rect.left, self.rect.top = position
		self.active = True


class EnemyBullet(pygame.sprite.Sprite):
	"""敌机子弹"""
	def __init__(self, speed, position):
		super().__init__()
		self.image = pygame.image.load("images/bullet1.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.speed = speed
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)


class BigEnemyBullet(EnemyBullet):
	"""大型敌机三种子弹"""
	def __init__(self, speed, position):
		super().__init__(speed, position)

	def move1(self):
		self.rect.left -= self.speed
		self.rect.top += self.speed
		if self.rect.left < 0 or self.rect.left > 480 or self.rect.top > 700:
			self.active = False

	def move2(self):
		self.rect.top += self.speed
		if self.rect.left < 0 or self.rect.left > 480 or self.rect.top > 700:
			self.active = False

	def move3(self):
		self.rect.left += self.speed
		self.rect.top += self.speed
		if self.rect.left < 0 or self.rect.left > 480 or self.rect.top > 700:
			self.active = False

	def reset(self, position):
		self.rect.left, self.rect.top = position
		self.active = True


class CommonEnemyBullet(EnemyBullet):
	"""中型敌机二种子弹"""
	def __init__(self, speed, position):
		super().__init__(speed, position)

	def move1(self):
		self.rect.left -= self.speed
		self.rect.top += self.speed
		if self.rect.left < 0 or self.rect.left > 480 or self.rect.top > 700:
			self.active = False

	def move2(self):
		self.rect.left += self.speed
		self.rect.top += self.speed
		if self.rect.left < 0 or self.rect.left > 480 or self.rect.top > 700:
			self.active = False

	def reset(self, position):
		self.rect.left, self.rect.top = position
		self.active = True


