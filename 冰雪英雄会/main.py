import pygame
import random
from os import path
import sys
from pygame.locals import *
import math
from datetime import datetime, date, time
import pygame_menu



WIDTH,HEIGHT = 800,600
NEW_ENEMY_GENERATE_INTERVAL = 500
NEW_SPACESHIP_GENERATE_INTERVAL = 500
NEW_XUEHUA_GENERATE_INTERVAL = 500
NEW_SPACESHIP_BULLET_INTERVAL = 5000

MISSILE_LIFETIME = 10000
MISSILE_INTERVAL = 400

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("冰雪英雄会")
clock = pygame.time.Clock()

# last_enemy_generate_time = 0
# last_spaceship_generate_time = 0



class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
#		self.image = pygame.Surface((50,50))
		self.image = pygame.transform.flip(player_img,False,False)
		self.image = pygame.transform.scale(self.image,(70,60))
		self.image.set_colorkey((0,0,0))
#		self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT
		self.radius = 20
		self.score = 0


		self.hp = 100
		self.lives =3
		self.huihui = 0
		self.hidden = False
		self.hide_time = 0

		self.is_missile_firing = False
		self.start_missile_time = 0
		self.last_missile_time = 0




	def update(self):
		key_state = pygame.key.get_pressed()
		if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
			self.rect.x -= 5
		if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
			self.rect.x += 5
		if key_state[pygame.K_UP] or key_state[pygame.K_w]:
			self.rect.y -= 5
		if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
			self.rect.y += 5
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.y < 0:
			self.rect.y = 0
		if self.rect.y > HEIGHT:
			self.rect.y = HEIGHT

	
		now = pygame.time.get_ticks()
		if self.hidden and now - self.hide_time > 1000:
			self.hidden = False
			self.rect.bottom = HEIGHT
			self.hp = 100
			if self.hp < 50:
				pygame.draw.rect(screen,(255,0,0),(10,10,player.hp,15))


		if self.is_missile_firing:
			if now - self.start_missile_time <= MISSILE_LIFETIME:
				if now - self.last_missile_time > MISSILE_INTERVAL:
					missile = Missile(self.rect.center)
					missiles.add(missile)
					self.last_missile_time = now
			else:
				self.is_missile_firing = False



	def shoot(self):
		bullet = Bullet(self.rect.centerx,self.rect.centery)
		bullets.add(bullet)
		shoot_sound.play()

	def fire_missile(self):
		self.is_missile_firing = True
		self.start_missile_time = pygame.time.get_ticks()

	def hide(self):
		self.hidden = True
		self.rect.y = HEIGHT
		self.hide_time = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		img_width = random.randint(20,60)
		self.image = pygame.transform.scale(enemy_img,(img_width,img_width))
		self.image.set_colorkey((0,0,0))
		self.image_origin = self.image.copy()
#		self.image = pygame.Surface((30,30))
#		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.radius = img_width // 2
#		pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
		self.rect.x = random.randint(0,WIDTH-self.rect.w)
		self.rect.bottom = 0

		self.vx = random.randint(-2,2)
		self.vy = random.randint(2,6)

		self.last_time = pygame.time.get_ticks()
		self.rotate_speed = random.randint(-5,5)
		self.rotate_angle = 0

		self.hidden = False
		self.hide_time = 0

		now = pygame.time.get_ticks()
		if self.hidden and now - self.hide_time > 10000:
			self.hidden = False


	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 30:
			self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
			old_center = self.rect.center
			self.image = pygame.transform.rotate(self.image_origin,self.rotate_angle)
			self.rect = self.image.get_rect()
			self.rect.center = old_center
			self.last_time = now

 
	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
		self.rotate()

	def hide(self):
		self.hidden = True
		self.hide_time = pygame.time.get_ticks()


class Xuehua(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		img_width = random.randint(20,120)
		self.image = pygame.transform.scale(xuehua_img,(30,20))
		self.image.set_colorkey((0,0,0))
		self.image_origin = self.image.copy()
#		self.image = pygame.Surface((30,30))
#		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.radius = img_width // 2
#		pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
		self.rect.x = random.randint(0,WIDTH-self.rect.w)
		self.rect.bottom = 0

		self.vx = random.randint(-2,2)
		self.vy = random.randint(2,6)

		self.last_time = pygame.time.get_ticks()
		self.rotate_speed = random.randint(-5,5)
		self.rotate_angle = 0


	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 30:
			self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
			old_center = self.rect.center
			self.image = pygame.transform.rotate(self.image_origin,self.rotate_angle)
			self.rect = self.image.get_rect()
			self.rect.center = old_center
			self.last_time = now

 
	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
		self.rotate()

# class Spaceship_Boss_One(pygame.sprite.Sprite):

# 	def __init__(self):
# 		pygame.sprite.Sprite.__init__(self)
# 		self.image = pygame.transform.scale(ship_boss_one_img,ship_boss_one_img.get_size())
# 		self.rect = self.image.get_rect()
# 		self.image.set_colorkey((0,0,0))
# 		self.rect.centerx = WIDTH // 2
# 		self.rect.centery = -5
# 		self.vy = 10
		

# 	def update(self):
# 		self.rect.centery += self.vy


class Point(object):
	def __init__(self, x, y):
		self.__x = x
		self.__y = y

	def getx(self): return self.__x
	def setx(self, x): self.__x = x
	x = property(getx, setx)

	def gety(self): return self.__y
	def sety(self, y): self.__y = y
	y = property(gety, sety)

	def __str__(self):
		return "{X:" + "{:.0f}".format(self.__x) + \
			",Y:" + "{:.0f}".format(self.__y) + "}"

def wrap_angle(angle):
	return angle % 360

class Spaceship(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(spaceship_img,(60,110))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(0,WIDTH-self.rect.w)
		self.rect.bottom = 0

		self.vx = random.randint(-2,4)
		self.vy = random.randint(4,7)

		self.last_spaceship_bullet_generate_time = 0

		self.hidden = False
		self.hide_time = 0

		now = pygame.time.get_ticks()
		if self.hidden and now - self.hide_time > 10000:
			self.hidden = False
		

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy


		now = pygame.time.get_ticks()
		if now - self.last_spaceship_bullet_generate_time > NEW_SPACESHIP_BULLET_INTERVAL:
			spaceship_bullet = Spaceship_bullet(self.rect.center)
			spaceship_bullets.add(spaceship_bullet)
			self.last_spaceship_bullet_generate_time = now

	def hide(self):
		self.hidden = True
		self.hide_time = pygame.time.get_ticks()
		


class Spaceship_bullet(pygame.sprite.Sprite):

	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.flip(spaceship_bullet_img,False,False)
		self.image = pygame.transform.scale(self.image,(20,30))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.radius = 20 // 2


		

	def update(self):
		self.rect.y += 10

		
	# def fire_spaceship_bullet(self):
	# 	self.is_spaceship_bulllet_firing = True
	# 	self.start_spaceship_bulllet_time = pygame.time.get_ticks()



# class Spaceship_Boss_One_Bullet(pygame.sprite.Sprite):

# 	def __init__(self):
# 		pygame.sprite.Sprite.__init__(self)
# 		self.image = pygame.transform.flip(spaceship_bullet_img,False,True)
# 		self.image = pygame.transform.scale(self.image,(20,30))
# 		self.image.set_colorkey((0,0,0))
# 		self.rect = self.image.get_rect()
# 		# self.rect.center = scratch_ship_boss_one_img.get_width() // 2
# 		self.radius = 20 // 2 

# 	def update(self):
# 		self.rect.y += 15



class Bullet(pygame.sprite.Sprite):

	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(bullet_img,bullet_img.get_size())
		self.image.set_colorkey((0,0,0))
#		self.image = pygame.Surface((5,10))
#		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y



	def update(self):
		self.rect.y -= 10

class Missile(pygame.sprite.Sprite):

	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image = missile_img
		self.image.set_colorkey((0,0,0))
#		self.image = pygame.Surface((5,10))
#		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.rect.center = center
		missile_sound.play()
		


	def update(self):
		self.rect.y -= 10


class Explosion(pygame.sprite.Sprite):
	
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(explosion_animation[0],(80,80))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_time = pygame.time.get_ticks()
		explosion_sound.play()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 30:
			if self.frame<len(explosion_animation):
				self.image = pygame.transform.scale(explosion_animation[self.frame],(80,80))
				self.image.set_colorkey((0,0,0))
				self.frame += 1
				self.last_time = now
			else:
				self.kill()




class Powerup(pygame.sprite.Sprite):
	
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		random_num = random.random()
		if random_num <0.5:
			self.type = 'add_hp'
		elif random_num < 0.8:
			self.type = 'add_missile'
		else:
			self.type = 'add_life'

		self.image = powerup_imgs[self.type]
		self.rect = self.image.get_rect()
		self.image.set_colorkey((0,0,0))
		self.rect.center = center

	def update(self):
		self.rect.y += 3

class Huihui(pygame.sprite.Sprite):
	
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		random_num = random.random()
		# if random_num <0.5:
		# 	self.type = 'add_faguo'
		# elif random_num < 0.8:
		# 	self.type = 'add_ruishi'
		# else:
		# 	self.type = 'add_america'
		# self.image = huihui_images[self.type]
		# for i in range(1,25):
		# if random_num > 0.9:
		i = random.randint(0,23) 
		self.image = huihui_images[i]
		self.image = pygame.transform.scale(self.image,(85,65))
		self.rect = self.image.get_rect()
		self.image.set_colorkey((0,0,0))
		self.rect.center = center
		if player.huihui == 24:
			game_over == True
			show_success_menu()
 	
	def update(self):
		self.rect.y += 6


class Spaceship_zhan_shiwu(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(spaceship_zhan_animation[0],(150,50))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH-500
		self.rect.centery = HEIGHT-500
		self.frame = 0
		self.last_time = pygame.time.get_ticks()


	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 1000:
			if self.frame<len(spaceship_zhan_animation):
				self.image = pygame.transform.scale(spaceship_zhan_animation[self.frame],(150,50))
				self.image.set_colorkey((0,0,0))
				self.frame += 1
				self.last_time = now
				while self.frame == 2:
					self.frame = 0
					spaceship_zhan_shiwu.update()
			else:
				self.kill()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over == True
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.K_ESCAPE:
					game_over == True


"""
class Space_plant_entity(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(space_plant_animation[0],space_plant_animation[0].get_size())
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH-200
		self.rect.centery = HEIGHT-550
		self.frame = 0
		self.last_time = pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 1000:
			if self.frame < len(space_plant_animation):
				self.image = pygame.transform.scale(space_plant_animation[self.frame],(100,100))
				self.image.set_colorkey((0,0,0))
				self.frame += 1
				self.last_time = now
				while self.frame == 4:
					self.frame = 0
					space_plant_entity.update()
			else:
				self.kill()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over == True
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.K_ESCAPE:
					game_over == True
"""


class Dynamic_Background1(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.flip(background_img1,False,False)
		self.rect = self.image.get_rect()
		self.speed = 3
		self.last_time = pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 5:
			self.rect.y += self.speed
			self.last_time = now
			while self.rect.y >= HEIGHT:
				self.rect.y = -self.rect.height
				dynamic_background2.update()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over == True
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.K_ESCAPE:
					game_over == True


class Dynamic_Background2(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.flip(background_img2,False,False)
		self.rect = self.image.get_rect()
		self.rect.y = -self.rect.height
		self.speed = 3
		self.last_time = pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 5:
			self.rect.y += self.speed
			self.last_time = now
			while self.rect.y >= HEIGHT:
				self.rect.y = -self.rect.height
				dynamic_background1.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over == True
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.K_ESCAPE:
					game_over == True

class Yingxiong_bingdundun_img(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img_small,(120,100))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2-270
		self.rect.centery = HEIGHT/2-170                  



class Yingxiong_xuerongrong_img(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(missile_img_small,(120,100))
		# self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2+280
		self.rect.centery = HEIGHT/2-170

def draw_ui():
	pygame.draw.rect(screen,(0,255,0),(10,10,player.hp,15))
	if player.hp < 50:
		pygame.draw.rect(screen,(255,0,0),(10,10,player.hp,15)) 
	pygame.draw.rect(screen,(255,255,255),(10,10,100,15),2)
 
	# draw_text('scores:' + str(player.score),screen,(0,255,0),20,WIDTH/2,10)
	draw_text('会徽:' + str(player.huihui),screen,(0,255,0),20,WIDTH/2,10)

	img_rect = player_img_small.get_rect()
	img_rect.right = WIDTH - 10
	img_rect.top = 10
	for _ in range(player.lives):
		screen.blit(player_img_small,img_rect)
		img_rect.x -= img_rect.width + 10


def draw_text(text,surface,color,font_size,x,y):
	# font_name = pygame.font.Font('C:/Windows/Fonts/stxinwei.ttf',50)
	font = pygame.font.Font('C:/Windows/Fonts/stxinwei.ttf',font_size)
	text_surface = font.render(text,True,color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface,text_rect)


def show_menu():
	global game_state,screen
	font_name = pygame.font.match_font('arial')
	font = pygame.font.Font(font_name,40)
	screen.blit(background_img3,background_rect)
	screen.blit(yingxiong_bingdundun.image,yingxiong_bingdundun.rect)
	screen.blit(yingxiong_xuerongrong.image,yingxiong_xuerongrong.rect)

	# rect1 = pygame.draw.rect(screen,(255,255,255),(WIDTH/20,80, 550, 100), 10)
	# screen.blit(font.render('SPACE SHOOTER',True,(0,255,0)), (150, 100))
	draw_text('冰 雪 英 雄 会',screen,(255,255,255),70,WIDTH/2,100)
	font = pygame.font.Font('C:/Windows/Fonts/stxinwei.ttf',50)
	rect2 = pygame.draw.rect(screen,(187,255,255),(WIDTH/7 + 80,350, 400, 50), 10)
	screen.blit(font.render('按 Space 键开始',True,(187,255,255)), (220, 350))
	rect3 = pygame.draw.rect(screen,(152,245,255),(WIDTH/7 + 80,450, 400, 50), 10)
	screen.blit(font.render('按   ESC键    退出',True,(152,245,255)), (220, 450))
	# draw_text('Press Space key to start',screen,(255,255,255),20,WIDTH/2,300)
	# draw_text('Press Esc key to quit',screen,(255,255,255),20,WIDTH/2,350)

	event_list = pygame.event.get()
	for event in event_list:
		if event.type == pygame.QUIT:
			game_over = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_over = True 
			if event.key == pygame.K_SPACE:
				game_state = 1



	pygame.display.flip()



img_dir = path.join(path.dirname(__file__),'img')
background_dir = path.join(img_dir,'space.png')
background_img1 = pygame.image.load(background_dir).convert()
background_img2 = pygame.image.load(background_dir).convert()
background_img3 = pygame.image.load('img/lantian.jpg').convert()
background_rect = background_img1.get_rect()
player_dir = path.join(img_dir,'hero_bingdundun.jpg')
player_img = pygame.image.load(player_dir).convert()
player_img_small = pygame.transform.scale(player_img,(35,40))
player_img_small.set_colorkey((0,0,0))
enemy_dir = path.join(img_dir,'spaceMeteors_004.png')
enemy_img = pygame.image.load(enemy_dir).convert()
xuehua_dir = path.join(img_dir,'xuehua.png')
xuehua_img = pygame.image.load(xuehua_dir).convert()
xuehua_img.set_colorkey((0,0,0))
bullet_dir = path.join(img_dir,'xuerongrong.jpg')
bullet_img = pygame.image.load(bullet_dir).convert()
bullet_img = pygame.transform.scale(bullet_img,(30,20))
bullet_img.set_colorkey((0,0,0))
missile_dir = path.join(img_dir,'hero_xuerongrong.jpg')
missile_img = pygame.image.load(missile_dir).convert()
missile_img = pygame.transform.scale(missile_img,(65,95))
missile_img.set_colorkey((0,0,0))
missile_img_small = pygame.transform.scale(missile_img,(35,40))
missile_img_small.set_colorkey((0,0,0))
spaceship_dir = path.join(img_dir,'bingzhui.png')
spaceship_img = pygame.image.load(spaceship_dir).convert_alpha()
spaceship_img.set_colorkey((0,0,0))
spaceship_bullet_dir = path.join(img_dir,'bingzhui.png')
spaceship_bullet_img = pygame.image.load(spaceship_bullet_dir).convert()
spaceship_bullet_img = pygame.transform.scale(spaceship_bullet_img,(30,20))
# spaceship_boss_one = path.join(img_dir,'spaceShips_002.png')
# spaceship_boss_one_img = pygame.image.load(spaceship_boss_one).convert_alpha()
# width,height = spaceship_boss_one_img.get_size()
# ship_boss_one_img = pygame.transform.smoothscale(spaceship_boss_one_img, (width//2 + 150, height//2 + 150))


explosion_animation = []
for i in range(9):
	explosion_dir = path.join(img_dir,'regularExplosion0{}.png'.format(i))
	explosion_img = pygame.image.load(explosion_dir).convert()
	explosion_animation.append(explosion_img)

spaceship_zhan_animation = []
for i in range(14,16):
	spaceship_zhan_dir = path.join(img_dir,'spaceBuilding_0{}.png'.format(i))
	spaceship_zhan_img = pygame.image.load(spaceship_zhan_dir).convert()
	spaceship_zhan_animation.append(spaceship_zhan_img)

huihui_images = []
for i in range(1,25):
	huihui_images_dir = path.join(img_dir,'{}.jpg'.format(i))
	huihui_image = pygame.image.load(huihui_images_dir).convert()
	huihui_images.append(huihui_image)


# space_plant_animation = []
# for i in range(6,10):
# 	space_plant_dir = path.join(img_dir,'spaceBuilding_00{}.png'.format(i))
# 	space_plant_img = pygame.image.load(space_plant_dir).convert()
# 	space_plant_animation.append(space_plant_img)

powerup_imgs = {}
powerup_add_hp_dir = path.join(img_dir,'gem_red.png')
powerup_imgs['add_hp'] = pygame.image.load(powerup_add_hp_dir).convert()
powerup_add_life_dir = path.join(img_dir,'heartFull.png')
powerup_imgs['add_life'] = pygame.image.load(powerup_add_life_dir).convert()
powerup_add_missile_dir = path.join(img_dir,'gem_yellow.png')
powerup_imgs['add_missile'] = pygame.image.load(powerup_add_missile_dir).convert()


# huihui_images = {}
# faguo_dir = path.join(img_dir,'1.jpg')
# huihui_images['add_faguo'] = pygame.image.load(faguo_dir).convert()
# ruishi_dir = path.join(img_dir,'2.jpg')
# huihui_images['add_ruishi'] = pygame.image.load(ruishi_dir).convert()
# america_dir = path.join(img_dir,'3.jpg')
# huihui_images['add_america'] = pygame.image.load(america_dir).convert()


sound_dir = path.join(path.dirname(__file__),'sound')
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot14.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir,'Explosion7.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot5.wav'))
pygame.mixer.music.load(path.join(sound_dir,'background_01.wav'))


dynamic_background1 = Dynamic_Background1()
dynamic_background2 = Dynamic_Background2()
yingxiong_bingdundun = Yingxiong_bingdundun_img()
yingxiong_xuerongrong = Yingxiong_xuerongrong_img()
# space_plant_entity = Space_plant_entity()
# spaceship_boss_one =Spaceship_Boss_One()
player = Player()
spaceship_zhan_shiwu = Spaceship_zhan_shiwu()
enemys = pygame.sprite.Group()
for i in range(5):
	enemy = Enemy()
	enemys.add(enemy)
spaceships = pygame.sprite.Group()
for i in range(4):
	spaceship = Spaceship()
	spaceships.add(spaceship)
xuehuas = pygame.sprite.Group()
for i in range(5):
	xuehua = Xuehua()
	xuehuas.add(xuehua)
bullets = pygame.sprite.Group()
spaceship_bullets = pygame.sprite.Group()
# spaceship_boss_one_bullet = Spaceship_Boss_One_Bullet()
# spaceship_boss_one_bullets = pygame.sprite.Group()
#for i in range(1):
#	spaceship_bullet = Spaceship_bullet()
#	spaceship_bullets.add(spaceship_bullet)
missiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()
powerups = pygame.sprite.Group()
huihuis = pygame.sprite.Group()

# game_over = False
game_state = 0
boss_time = 0

last_spaceship_boss_one_bullet_generate_time = 0

radius = 200
angle = 0.0
pos = Point(0,0)
old_pos = Point(0,0)

pygame.mixer.music.play(loops = -1)

def main():
	game_over = False
	last_enemy_generate_time = 0
	last_spaceship_generate_time = 0
	last_xuehua_generate_time = 0
	while not game_over:
			clock.tick(60)
			if game_state == 0:
				show_menu()
			else:
				event_list = pygame.event.get()
				for event in event_list:
					if event.type == pygame.QUIT:
						game_over = True
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							game_over = True 
						if event.key == pygame.K_SPACE:
							player.shoot()

				now = pygame.time.get_ticks()
				if now - last_enemy_generate_time > NEW_ENEMY_GENERATE_INTERVAL:
					enemy = Enemy()
					enemys.add(enemy)
					last_enemy_generate_time = now	

				if now - last_spaceship_generate_time > NEW_SPACESHIP_GENERATE_INTERVAL:
					spaceship = Spaceship()
					spaceships.add(spaceship)
					last_spaceship_generate_time = now

				if now - last_xuehua_generate_time > NEW_XUEHUA_GENERATE_INTERVAL:
					xuehua = Xuehua()
					xuehuas.add(xuehua)
					last_xuehua_generate_time = now



				
				screen.fill((255,255,255)) 
			#	pygame.draw.rect(screen,(0,255,0),(100,100,50,80))
				
				dynamic_background1.update()
				dynamic_background2.update()
				player.update()
				enemys.update()
				xuehuas.update()
				bullets.update()
				missiles.update()
				explosions.update()
				powerups.update()
				huihuis.update()
				spaceships.update()
				spaceship_bullets.update()
				# spaceship_boss_one_bullets.update()
				spaceship_zhan_shiwu.update()
				# space_plant_entity.update()


			#	hits = pygame.sprite.spritecollide(player,enemys,False,pygame.sprite.collide_rect_ratio(0.7))
				hits = pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)
				for hit in hits:
					player.hp -= 40
					if player.hp<0:
						player.lives -= 1
						player.hp = 100 
						player.hide()
						if player.lives == 0:
							game_over = True
							show_game_over_menu()

				hits = pygame.sprite.spritecollide(player,spaceships,True,pygame.sprite.collide_circle)
				for hit in hits:
					player.hp -= 30
					if player.hp<0:
						player.lives -= 1
						player.hp = 100
						player.hide()
						if player.lives == 0:
							game_over = True
							show_game_over_menu()


				hits = pygame.sprite.spritecollide(player,spaceship_bullets,True,pygame.sprite.collide_circle)
				for hit in hits:
					player.hp -= 10  
					if player.hp<0:
						player.lives -= 1
						player.hp = 100
						player.hide()
						if player.lives == 0:
							game_over = True
							show_game_over_menu()

				hits_bullets = pygame.sprite .groupcollide(enemys,bullets,True,True)
				hits_missiles = pygame.sprite.groupcollide(enemys,missiles,True,True)
				hits_spaceships = pygame.sprite.groupcollide(spaceships,bullets,True,True)
				hits_spaceships_and_missiles = pygame.sprite.groupcollide(spaceships,missiles,True,False)  
				hits = {}
				hits.update(hits_bullets)
				hits.update(hits_missiles)
				hits.update(hits_spaceships)
				hits.update(hits_spaceships_and_missiles)
				for hit in hits:
					enemy = Enemy()
					enemys.add(enemy)
					explosion = Explosion(hit.rect.center)
					explosions.add(explosion)
					player.score += (100 - hit.radius)
					if random.random() > 0.9: 
						powerup = Powerup(hit.rect.center)
						powerups.add(powerup)
						huihui = Huihui(hit.rect.center) 
						huihuis.add(huihui)


				hits = pygame.sprite.spritecollide(player,powerups,True)
				for hit in hits:
					if hit.type == 'add_hp':
						player.hp += 50
						if player.hp > 100:
							player.hp = 100
					elif hit.type == 'add_life':
						player.lives += 1
						if player.lives > 3:
							player.lives = 3
					else:
						player.fire_missile()

				hits = pygame.sprite.spritecollide(player,huihuis,True)
				for hit in hits:
					player.huihui += 1
					if player.huihui == 24:
						game_over == True
						show_success_menu()
					# if hit.type == 'add_faguo':
					# 	player.huihui += 1
					# 	if player.huihui == 24:
					# 		game_over == True

					# elif hit.type == 'add_ruishi':
					# 	player.huihui += 1
					# 	if player.huihui == 24:
					# 		game_over == True
					# else:
					# 	player.huihui += 1
					# 	if player.huihui == 24:
					# 		game_over == True


				
				screen.blit(dynamic_background1.image,dynamic_background1.rect)
				screen.blit(dynamic_background2.image,dynamic_background2.rect)
				screen.blit(player.image,player.rect)
				screen.blit(spaceship_zhan_shiwu.image,spaceship_zhan_shiwu.rect)
				# screen.blit(space_plant_entity.image,space_plant_entity.rect)
				enemys.draw(screen)
				xuehuas.draw(screen)
				bullets.draw(screen)
				missiles.draw(screen)
				explosions.draw(screen)
				powerups.draw(screen)
				huihuis.draw(screen)
				spaceships.draw(screen)
				spaceship_bullets.draw(screen)
				# spaceship_boss_one_bullets.draw(screen)

				draw_ui()

				# if now - boss_time > 30000:
				# 	enemy.hide()
				# 	spaceship.hide()
				# 	# screen.blit(spaceship_boss_one.image,spaceship_boss_one.rect)
				# 	# spaceship_boss_one.update()
				# 	angle = wrap_angle(angle - 0.1)
				# 	pos.x = math.sin( math.radians(angle) ) * radius
				# 	pos.y = math.cos( math.radians(angle) ) * radius 

				# 	delta_x = ( pos.x - old_pos.x )
				# 	delta_y = ( pos.y - old_pos.y )
				# 	rangle = math.atan2(delta_y, delta_x)
				# 	scratch_ship_boss_one_img = pygame.transform.rotate(ship_boss_one_img,rangle)

				# 	width,height = scratch_ship_boss_one_img.get_size()
				# 	x = 400+pos.x-width//2
				# 	y = -pos.y + 100
				# 	screen.blit(scratch_ship_boss_one_img, (x,y))
				# 	now = pygame.time.get_ticks()
				# 	if now - last_spaceship_boss_one_bullet_generate_time > NEW_SPACESHIP_BULLET_INTERVAL:
				# 		spaceship_boss_one_bullet = Spaceship_Boss_One_Bullet()
				# 		spaceship_boss_one_bullets.add(spaceship_boss_one_bullet)
				# 		last_spaceship_boss_one_bullet_generate_time = now
		 

				pygame.display.flip()

				# old_pos.x = pos.x
				# old_pos.y = pos.y
				
			
def set_difficulty(value, difficulty):
	pass

def set_hero(value,num):
	pass

def show_beign_menu():
	menu = pygame_menu.Menu(600,
						800,
						'Welcome',
						theme=pygame_menu.themes.THEME_ORANGE)

	# menu.add_text_input('Player', default='John')
	menu.add_selector('Hero', [('Bing dundun', 1), ('Xue rongrong', 2)],
					  onchange=set_difficulty)
	menu.add_selector('Difficulty', [('Easy', 1), ('Hard', 2)],
					  onchange=set_difficulty)
	menu.add_button('Play', main)
	menu.add_button('Quit', pygame_menu.events.EXIT)
	menu.add_button('About')
	menu.mainloop(screen)

def show_game_over_menu():
	menu = pygame_menu.Menu(600,
						800,
						'GameOver!',
						theme=pygame_menu.themes.THEME_DARK)

	# menu.add_text_input('Player', default='John')
	# menu.add_button('Continue to Play', main)
	if menu.add_button('Replay', main):
		player.lives = 3
		player.huihui = 0
	menu.add_button('Quit', pygame_menu.events.EXIT)
	menu.mainloop(screen)

def show_success_menu():
	font = pygame.font.Font('C:/Windows/Fonts/stxinwei.ttf',50)
	menu = pygame_menu.Menu(600,
	                        800,
	                        'Successfully!',
	                        theme=pygame_menu.themes.THEME_BLUE)

	# menu.add_text_input('Player', default='John Doe')
	if menu.add_button('Replay', start_the_game):
		player.lives = 3
		player.huihui = 0
	menu.add_button('Quit', pygame_menu.events.EXIT)
	menu.mainloop(surface)



if __name__ == '__main__':
	# surface = pygame.display.set_mode((800, 600))
	show_beign_menu()