import pygame
import sys
from pygame.locals import *
import hero_plane
import enemy_plane
import bullet
import supply
from random import *


class PlaneGame(object):

	def __variate__define(self):
		"""变量定义"""
		# 屏幕背景
		self.bg_size = self.width, self.height = (480, 700)
		# 用于英雄图片切换
		self.switch_image = True
		self.delay = 100
		# 设置中弹图片索引
		self.small_destroy_index = 0
		self.mid_destroy_index = 0
		self.big_destroy_index = 0
		self.hero_destroy_index = 0
		# 定义血条颜色
		self.BLACK = (0, 0, 0)
		self.GREEN = (0, 255, 0)
		self.RED = (255, 0, 0)
		self.WHILE = (255, 255, 255)
		# 定义分数
		self.score = 0
		# 定义暂停按钮
		self.paused = False
		# 设置游戏难度级别
		self.level = 1
		# 设置全屏炸弹数量
		self.bomb_num = 3
		# 超级子弹定时器
		self.DOUBLE_BULLET_TIME = USEREVENT + 1
		# 标志是否使用了超级子弹
		self.is_double_bullet = False
		# 标志是否使用三发超级子弹
		self.is_triple_bullet = False
		# 生成子弹容器
		self.bullets = []
		# 解除我方无敌状态计时器
		self.INVINCIBLE_TIME = USEREVENT + 2
		# 阻止重复打开文件
		self.recorded = False

	def __init__(self):
		# 1.变量定义
		self.__variate__define()
		# 2.pygame和音乐初始化
		pygame.init()
		pygame.mixer.init()
		# 3.创建游戏窗口
		self.screen = pygame.display.set_mode(self.bg_size)
		pygame.display.set_caption("飞机大战")
		# 4.获取背景图片
		self.background = pygame.image.load("images/background.png").convert()
		# 5.创建游戏时钟
		self.clock = pygame.time.Clock()
		# 6.载入音乐模块
		pygame.mixer.music.load("sound/game_music.ogg")
		pygame.mixer.music.set_volume(0.2)  # 设置音量
		self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
		self.bullet_sound.set_volume(0.2)
		self.bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
		self.bomb_sound.set_volume(0.2)
		self.supply_sound = pygame.mixer.Sound("sound/supply.wav")
		self.supply_sound.set_volume(0.2)
		self.get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
		self.get_bomb_sound.set_volume(0.2)
		self.get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
		self.get_bullet_sound.set_volume(0.2)
		self.upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
		self.upgrade_sound.set_volume(0.2)
		self.enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
		self.enemy3_fly_sound.set_volume(0.1)
		self.enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
		self.enemy1_down_sound.set_volume(0.2)
		self.enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
		self.enemy2_down_sound.set_volume(0.5)
		self.enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
		self.enemy3_down_sound.set_volume(0.9)
		self.me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
		self.me_down_sound.set_volume(0.2)

	def start__game(self):
		"""游戏开始"""
		# 播放背景音乐，这里的记录需要重新设置（因为重新调用start__game（）时，需要将成绩清零，并且需要重新打开record.txt读取记录）
		pygame.mixer.music.play(-1)
		self.score = 0
		self.recorded = False
		self.bomb_num = 3
		# 生成英雄飞机
		self.__create_hero()
		# 生成子弹
		self.__create_bullet()
		# 生成敌机
		self.__create_enemy()
		# 生成暂停按钮
		self.__create_stop()
		# 生成全屏炸弹
		self.__create_bomb()
		# 生成补给
		self.__create_supply()
		# 生成英雄生命数量
		self.__create_hero_num()
		# 生成敌机子弹
		self.__create_enemy_bullet()
		# 生成游戏结束画面
		self.__create_game_over()
		# 生成游戏开始界面
		self.__create_start_image()
		while True:
			# 1.设置刷新帧率
			self.clock.tick(60)
			self.screen.blit(self.background, (0, 0))
			self.__draw_start_image()
			# 如果没有点击暂停并且飞机还有生命
			if self.start and self.life_num and not self.paused:
				# 2.碰撞检测
				self.__check_collide()
				# 5.事件监听
				self.__keypress_hanlder()
				# 3.设置游戏级别
				self.add_enemy_level()
				# 4.更新画布
				self.screen.blit(self.background, (0, 0))
				self.__draw_score()
				self.__draw_hero()
				self.__draw_bullet()
				self.__draw_enemy()
				self.__draw_supply()
				self.__draw_hero_num()
				self.__draw_bomb()
			elif self.paused:
				self.screen.blit(self.background, (0, 0))
			elif self.life_num == 0:
				self.__draw_game_over()
			self.__draw_stop()
			# 5.事件监听
			self.__event_hanlder()
			# 6.屏幕刷新
			pygame.display.flip()

	def __event_hanlder(self):
		"""事件监听"""
		for event in pygame.event.get():
			# 1.检测关闭事件
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# 2.检测鼠标左键是否按下，并且是否在暂停图片上按下
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and self.paused_rect.collidepoint(event.pos):
					self.paused = not self.paused
					# 暂停时停止供给以及各种音效
					if self.paused:
						pygame.time.set_timer(self.SUPPLY_TIME, 0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					if not self.paused:
						pygame.time.set_timer(self.SUPPLY_TIME, 30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()
			# 3.检测鼠标是否经过暂停图片,显示不同状态
			elif event.type == MOUSEMOTION:
				if self.paused_rect.collidepoint(event.pos):
					if self.paused:
						self.paused_image = self.resume_pressed_image
					else:
						self.paused_image = self.pause_pressed_image
				if not self.paused_rect.collidepoint(event.pos):
					if self.paused:
						self.paused_image = self.resume_nor_image
					else:
						self.paused_image = self.pause_nor_image
				# 开始界面字体颜色切换
				if self.start_text_rect.collidepoint(event.pos):
					self.start_text = self.start_font.render("Start Game", True, self.BLACK)
				if not self.start_text_rect.collidepoint(event.pos):
					self.start_text = self.start_font.render("Start Game", True, self.WHILE)
			# 4.空格键释放炸弹
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if self.bomb_num > 0:
						self.bomb_num -= 1
						self.bomb_sound.play()
						for each in self.enemys:
							if each.rect.bottom > 0:
								each.active = False
			# 5.检测用户自定义事件（空投）
			elif event.type == self.SUPPLY_TIME:
				self.supply_sound.play()
				if choice([1, 2, 3]) == 1:
					self.bullet_supply.reset()
				elif choice([1, 2, 3]) == 2:
					self.bomb_supply.reset()
				else:
					self.life_supply.reset()
			# 6.关闭双发子弹定时器
			elif event.type == self.DOUBLE_BULLET_TIME:
				self.is_double_bullet = False
				self.is_triple_bullet = False
				pygame.time.set_timer(self.DOUBLE_BULLET_TIME, 0)
			# 7.三秒钟后关闭英雄无敌状态
			elif event.type == self.INVINCIBLE_TIME:
				self.hero.invincible = False
				pygame.time.set_timer(self.INVINCIBLE_TIME, 0)

	def __keypress_hanlder(self):
		"""检测用户的键盘操作，控制英雄飞机"""
		key_pressed = pygame.key.get_pressed()
		if key_pressed[K_w] or key_pressed[K_UP]:
			self.hero.moveUp()
		if key_pressed[K_s] or key_pressed[K_DOWN]:
			self.hero.moveDown()
		if key_pressed[K_a] or key_pressed[K_LEFT]:
			self.hero.moveLeft()
		if key_pressed[K_d] or key_pressed[K_RIGHT]:
			self.hero.moveRight()

	def __check_collide(self):
		# 英雄与敌机相撞--返回与英雄相撞的敌机列表(最后一个参数是使英雄为除空白区域外的图像)
		self.enemy_down = pygame.sprite.spritecollide(self.hero, self.enemys, False, pygame.sprite.collide_mask)
		# 如果英雄与敌机相撞并且不是处于无敌状态则摧毁
		if self.enemy_down and not self.hero.invincible:
			self.hero.active = False
			for each in self.enemy_down:
				each.active = False

	def add_small_enemy(self, group1, group2, num):
		"""创建小型敌机对象，num为对象个数，将其添加到精灵组中"""
		for i in range(num):
			e1 = enemy_plane.SmallEnemy(self.bg_size)
			group1.add(e1)
			group2.add(e1)

	def add_mid_enemy(self, group1, group2, num):
		"""创建中型敌机对象"""
		for i in range(num):
			e1 = enemy_plane.MidEnemy(self.bg_size)
			group1.add(e1)
			group2.add(e1)

	def add_big_enemy(self, group1, group2, num):
		"""创建大型敌机对象"""
		for i in range(num):
			e1 = enemy_plane.BigEnemy(self.bg_size)
			group1.add(e1)
			group2.add(e1)

	def add_enemy_speed(self, target, num):
		"""增加敌机速度"""
		for each in target:
			each.speed += num

	def add_enemy_level(self):
		if self.level == 1 and self.score > 50000:
			self.level = 2
			self.upgrade_sound.play()
			# 增加3架小型敌机，2架中型敌机，1架大型敌机
			self.add_small_enemy(self.small_enemys, self.enemys, 3)
			self.add_mid_enemy(self.mid_enemys, self.enemys, 2)
			self.add_big_enemy(self.big_enemys, self.enemys, 1)
			# 提升小型敌机的速度
			self.add_enemy_speed(self.small_enemys, 1)

		elif self.level == 2 and self.score > 300000:
			self.level = 3
			self.upgrade_sound.play()
			# 增加5架小型敌机，3架中型敌机，2架大型敌机
			self.add_small_enemy(self.small_enemys, self.enemys, 5)
			self.add_mid_enemy(self.mid_enemys, self.enemys, 3)
			self.add_big_enemy(self.big_enemys, self.enemys, 2)
			# 提升小型敌机的速度
			self.add_enemy_speed(self.small_enemys, 1)
			self.add_enemy_speed(self.mid_enemys, 1)

		elif self.level == 3 and self.score > 600000:
			self.level = 4
			self.upgrade_sound.play()
			# 增加7架小型敌机，5架中型敌机，4架大型敌机
			self.add_small_enemy(self.small_enemys, self.enemys, 7)
			self.add_mid_enemy(self.mid_enemys, self.enemys, 5)
			self.add_big_enemy(self.big_enemys, self.enemys, 4)
			# 提升小型敌机的速度
			self.add_enemy_speed(self.small_enemys, 1)
			self.add_enemy_speed(self.mid_enemys, 1)
			self.add_enemy_speed(self.big_enemys, 1)

		elif self.level == 4 and self.score > 1000000:
			self.level = 5
			self.upgrade_sound.play()
			# 增加9架小型敌机，7架中型敌机，6架大型敌机
			self.add_small_enemy(self.small_enemys, self.enemys, 9)
			self.add_mid_enemy(self.mid_enemys, self.enemys, 7)
			self.add_big_enemy(self.big_enemys, self.enemys, 6)
			# 提升小型敌机的速度
			self.add_enemy_speed(self.small_enemys, 1)
			self.add_enemy_speed(self.mid_enemys, 1)
			self.add_enemy_speed(self.big_enemys, 1)

	def __create_enemy(self):
		"""生成敌机"""
		# 建立全体敌机精灵组
		self.enemys = pygame.sprite.Group()
		# 生成敌方小型飞机
		self.small_enemys = pygame.sprite.Group()
		self.add_small_enemy(self.small_enemys, self.enemys, 15)
		# 生成敌方中型飞机
		self.mid_enemys = pygame.sprite.Group()
		self.add_mid_enemy(self.mid_enemys, self.enemys, 5)
		# 生成敌方大型飞机
		self.big_enemys = pygame.sprite.Group()
		self.add_big_enemy(self.big_enemys, self.enemys, 2)

	def __create_hero(self):
		self.hero = hero_plane.MyPlane(self.bg_size)

	def __create_bullet(self):
		# 生成普通子弹
		self.bullet1 = []
		self.bullet1_index = 0
		self.BULLET_NUM = 4
		for i in range(self.BULLET_NUM):
			self.bullet1.append(bullet.Bullet1(self.hero.rect.midtop))
		# 生成超级子弹
		self.bullet2 = []
		self.bullet2_index = 0
		self.BULLET2_NUM = 8
		for i in range(self.BULLET2_NUM // 2):
			self.bullet2.append(bullet.Bullet2((self.hero.rect.centerx - 33, self.hero.rect.centery)))
			self.bullet2.append(bullet.Bullet2((self.hero.rect.centerx + 30, self.hero.rect.centery)))
		# 生成三发超级子弹
		self.bullet3 = []
		self.bullet3_index = 0
		self.BULLET3_NUM = 12
		for i in range(self.BULLET3_NUM // 3):
			self.bullet3.append(bullet.Bullet3((self.hero.rect.centerx - 33, self.hero.rect.centery)))
			self.bullet3.append(bullet.Bullet3((self.hero.rect.centerx + 30, self.hero.rect.centery)))
			self.bullet3.append(bullet.Bullet3(self.hero.rect.midtop))

	def __create_enemy_bullet(self):
		"""生成大型敌机子弹"""
		self.enemy_big_bullet = []
		self.enemy_big_bullet_index = 0
		self.BIG_BULLET_NUM = 12
		for i in range(self.BIG_BULLET_NUM // 3):
			self.enemy_big_bullet.append(bullet.BigEnemyBullet(2, (0, 0)))
			self.enemy_big_bullet.append(bullet.BigEnemyBullet(2, (0, 0)))
			self.enemy_big_bullet.append(bullet.BigEnemyBullet(2, (0, 0)))

		self.enemy_common_bullet = []
		self.enemy_common_bullet_index = 0
		self.COMMON_BULLET_NUM = 8
		for i in range(self.COMMON_BULLET_NUM // 2):
			self.enemy_common_bullet.append(bullet.CommonEnemyBullet(2, (0, 0)))
			self.enemy_common_bullet.append(bullet.CommonEnemyBullet(2, (0, 0)))

	def __draw_big_enemy_bullet(self, big_enemy):
		""" 发射大型敌机子弹"""
		if not (self.delay % 100):
			self.enemy_big_bullet[self.enemy_big_bullet_index].reset((big_enemy.rect.left, big_enemy.rect.top + 251))
			self.enemy_big_bullet[self.enemy_big_bullet_index + 1].reset((big_enemy.rect.left + 82,
																		 big_enemy.rect.top + 251))
			self.enemy_big_bullet[self.enemy_big_bullet_index + 2].reset((big_enemy.rect.left + 164,
																		  big_enemy.rect.top + 251))
			self.enemy_big_bullet_index = (self.enemy_big_bullet_index + 3) % self.BIG_BULLET_NUM
		# 检测子弹是否击中英雄
		i = 0
		while i < len(self.enemy_big_bullet):
			# 三种发射子弹的方式
			if self.enemy_big_bullet[i].active:
				if i % 2:
					self.enemy_big_bullet[i].move2()
				elif i % 3:
					self.enemy_big_bullet[i].move1()
				else:
					self.enemy_big_bullet[i].move3()

				self.screen.blit(self.enemy_big_bullet[i].image, self.enemy_big_bullet[i].rect)
				# 碰撞检测
				enemy_hit = pygame.sprite.spritecollide(self.hero, self.enemy_big_bullet, False,
														pygame.sprite.collide_mask)
				if enemy_hit and not self.hero.invincible:
					self.enemy_big_bullet[i].active = False
					self.hero.active = False
			i += 1

	def __draw_common_enemy_bullet(self, common_enemy):
		""" 发射中型敌机子弹"""
		if not (self.delay % 100):
			self.enemy_common_bullet[self.enemy_common_bullet_index].reset((common_enemy.rect.left,
																			common_enemy.rect.top + 99))
			self.enemy_common_bullet[self.enemy_common_bullet_index + 1].reset((common_enemy.rect.left + 69,
																				common_enemy.rect.top + 99))
			self.enemy_common_bullet_index = (self.enemy_common_bullet_index + 2) % self.COMMON_BULLET_NUM
		# 检测子弹是否击中英雄
		i = 0
		while i < len(self.enemy_common_bullet):
			# 三种发射子弹的方式
			if self.enemy_common_bullet[i].active:
				if i % 2:
					self.enemy_common_bullet[i].move2()
				else:
					self.enemy_common_bullet[i].move1()

				self.screen.blit(self.enemy_common_bullet[i].image, self.enemy_common_bullet[i].rect)
				# 碰撞检测
				enemy_hit = pygame.sprite.spritecollide(self.hero, self.enemy_common_bullet, False,
														pygame.sprite.collide_mask)
				if enemy_hit and not self.hero.invincible:
					self.enemy_common_bullet[i].active = False
					self.hero.active = False
			i += 1

	def __create_stop(self):
		"""暂停设置(四张图片切换显示)"""
		self.pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
		self.pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
		self.resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
		self.resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
		self.paused_rect = self.pause_nor_image.get_rect()
		self.paused_rect.left, self.paused_rect.top = self.width - self.paused_rect.width - 10, 10
		self.paused_image = self.pause_nor_image

	def __create_bomb(self):
		"""炸弹定义"""
		self.bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
		self.bomb_rect = self.bomb_image.get_rect()
		self.bomb_font = pygame.font.Font("font/font.ttf", 48)

	def __create_supply(self):
		"""设置每十-三十秒发放一个补给包"""
		self.bullet_supply = supply.BulletSupply(self.bg_size)
		self.bomb_supply = supply.BombSupply(self.bg_size)
		self.life_supply = supply.LifeSupply(self.bg_size)
		self.SUPPLY_TIME = USEREVENT
		pygame.time.set_timer(self.SUPPLY_TIME, randint(10, 30) * 1000)

	def __create_hero_num(self):
		"""飞机生命数量显示"""
		self.life_image = pygame.image.load("images/life.png").convert_alpha()
		self.life_rect = self.life_image.get_rect()
		self.life_num = 3

	def __create_game_over(self):
		"""游戏结束画面"""
		self.gameover_font = pygame.font.Font("font/font.TTF", 48)
		self.again_image = pygame.image.load("images/again.png").convert_alpha()
		self.again_rect = self.again_image.get_rect()
		self.gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
		self.gameover_rect = self.gameover_image.get_rect()

	def __draw_hero(self):
		"""英雄飞机动态效果实现"""
		# 英雄生存
		if self.hero.active:
			if self.switch_image:
				self.screen.blit(self.hero.image1, self.hero.rect)
			else:
				self.screen.blit(self.hero.image2, self.hero.rect)
		# 英雄死亡
		else:
			if not (self.delay % 3):
				if self.hero_destroy_index == 0:
					self.me_down_sound.play()
				self.screen.blit(self.hero.destroy_images[self.hero_destroy_index], self.hero.rect)
				self.hero_destroy_index = (self.hero_destroy_index + 1) % 4
				# 毁灭图片播放完毕，重新回到初始位置
				if self.hero_destroy_index == 0:
					self.life_num -= 1
					self.hero.reset()
					# 设置无敌时间三秒钟
					pygame.time.set_timer(self.INVINCIBLE_TIME, 3 * 1000)

		# 延时切换
		if not (self.delay % 5):
			self.switch_image = not self.switch_image
		self.delay -= 1
		if not self.delay:
			self.delay = 100

	def __draw_enemy(self):
		"""绘制敌机"""
		# 绘制敌方大型飞机（动态效果实现）
		for each in self.big_enemys:
			# 如果敌机是生存状态
			if each.active:
				each.move()
				# 子弹击中敌机时切换敌机图片
				if each.hit:
					self.screen.blit(each.image_hit, each.rect)
					each.hit = False
				else:
					# 动态效果切换
					if self.switch_image:
						self.screen.blit(each.image, each.rect)
					else:
						self.screen.blit(each.image2, each.rect)
					# 血槽绘制
					# ---绘制总长度，黑色血条
					pygame.draw.line(self.screen, self.BLACK, (each.rect.left, each.rect.top - 5),
									 (each.rect.right, each.rect.top - 5))
					# ---绘制红，绿色血条，大于20%显示绿色，小于显示红色
					enemy_remain = each.energy / enemy_plane.BigEnemy.energy
					if enemy_remain > 0.2:
						enemy_color = self.GREEN
					else:
						enemy_color = self.RED
					pygame.draw.line(self.screen, enemy_color, (each.rect.left, each.rect.top - 5),
									 (each.rect.left + each.rect.width * enemy_remain, each.rect.top - 5))
				if (each.rect.bottom > -50) and (each.rect.bottom < 961):
					# 声音问题没解决
					self.enemy3_fly_sound.play(-1)
					# 敌机发射子弹
					if not self.easy and not self.common and self.difficult:
						self.__draw_big_enemy_bullet(each)

			# 如果敌机是毁灭状态
			else:
				if not (self.delay % 3):
					# 音效播放设置
					if self.big_destroy_index == 0:
						self.enemy3_down_sound.play()
					self.screen.blit(each.destroy_images[self.big_destroy_index], each.rect)
					self.big_destroy_index = (self.big_destroy_index + 1) % 6
					# 毁灭图片播放完毕，重新回到初始位置
					if self.big_destroy_index == 0:
						self.enemy3_fly_sound.stop()
						each.reset()
						# 分数加10000
						self.score += 10000

		# 绘制中型飞机
		for each in self.mid_enemys:
			# 如果敌机是生存状态
			if each.active:
				each.move()
				# 子弹击中敌机时切换敌机图片
				if each.hit:
					self.screen.blit(each.image_hit, each.rect)
					each.hit = False
				else:
					self.screen.blit(each.image, each.rect)
				# 血槽绘制
				# ---绘制总长度，黑色血条
				pygame.draw.line(self.screen, self.BLACK, (each.rect.left, each.rect.top - 5),
								 (each.rect.right, each.rect.top - 5))
				# ---绘制红，绿色血条，大于20%显示绿色，小于显示红色
				enemy_remain = each.energy / enemy_plane.MidEnemy.energy
				if enemy_remain > 0.2:
					enemy_color = self.GREEN
				else:
					enemy_color = self.RED
				pygame.draw.line(self.screen, enemy_color, (each.rect.left, each.rect.top - 5),
								 (each.rect.left + each.rect.width * enemy_remain, each.rect.top - 5))
				if (each.rect.bottom > -50) and (each.rect.bottom < 961):
					if self.common or self.difficult:
						self.__draw_common_enemy_bullet(each)
			# 如果敌机是毁灭状态
			else:
				if not (self.delay % 3):
					if self.mid_destroy_index == 0:
						self.enemy2_down_sound.play()
					self.screen.blit(each.destroy_images[self.mid_destroy_index], each.rect)
					self.mid_destroy_index = (self.mid_destroy_index + 1) % 4
					# 毁灭图片播放完毕，重新回到初始位置
					if self.mid_destroy_index == 0:
						each.reset()
						# 分数加5000
						self.score += 5000

		# 绘制小型飞机
		for each in self.small_enemys:
			# 如果敌机是生存状态
			if each.active:
				each.move()
				self.screen.blit(each.image, each.rect)
			# 如果敌机是毁灭状态
			else:
				if not (self.delay % 3):
					if self.small_destroy_index == 0:
						self.enemy1_down_sound.play()
					self.screen.blit(each.destroy_images[self.small_destroy_index], each.rect)
					self.small_destroy_index = (self.small_destroy_index + 1) % 4
					# 毁灭图片播放完毕，重新回到初始位置
					if self.small_destroy_index == 0:
						each.reset()
						# 分数加1000
						self.score += 1000

	def __draw_bullet(self):
		# 发射子弹
		if not (self.delay % 10):
			self.bullet_sound.play()
			# 判断是否是双发子弹
			if self.is_double_bullet and not self.is_triple_bullet:
				self.bullets = self.bullet2
				self.bullets[self.bullet2_index].reset((self.hero.rect.centerx - 33, self.hero.rect.centery))
				self.bullets[self.bullet2_index + 1].reset((self.hero.rect.centerx + 30, self.hero.rect.centery))
				self.bullet2_index = (self.bullet2_index + 2) % self.BULLET2_NUM
			# 判断是否是单发子弹
			elif not self.is_double_bullet and not self.is_triple_bullet:
				self.bullets = self.bullet1
				self.bullets[self.bullet1_index].reset(self.hero.rect.midtop)
				self.bullet1_index = (self.bullet1_index + 1) % self.BULLET_NUM
			# 判断是否是三发子弹
			elif self.is_double_bullet and self.is_triple_bullet:
				self.bullets = self.bullet3
				self.bullets[self.bullet3_index].reset((self.hero.rect.centerx - 33, self.hero.rect.centery))
				self.bullets[self.bullet3_index + 1].reset((self.hero.rect.centerx + 30, self.hero.rect.centery))
				self.bullets[self.bullet3_index + 2].reset(self.hero.rect.midtop)
				self.bullet3_index = (self.bullet3_index + 3) % self.BULLET3_NUM

		# 检测子弹是否击中敌机
		for b in self.bullets:
			if b.active:
				b.move()
				self.screen.blit(b.image, b.rect)
				# 碰撞检测
				enemy_hit = pygame.sprite.spritecollide(b, self.enemys, False, pygame.sprite.collide_mask)
				if enemy_hit:
					b.active = False
					for e in enemy_hit:
						# 判断子弹击中的是否为大中型敌机,若是则当energy为0时，飞机摧毁
						if e in self.mid_enemys or e in self.big_enemys:
							e.hit = True
							e.energy -= 1
							if e.energy == 0:
								e.active = False
						# 若不是则直接摧毁
						else:
							e.active = False

	def __draw_score(self):
		"""分数显示字体颜色设置"""
		self.score_font = pygame.font.Font("font/font.ttf", 36)
		self.score_text = self.score_font.render("Score : %s" % str(self.score), True, self.WHILE)
		self.screen.blit(self.score_text, (10, 5))

	def __draw_stop(self):
		self.screen.blit(self.paused_image, self.paused_rect)

	def __draw_bomb(self):
		"""绘制炸弹数量"""
		self.bomb_text = self.bomb_font.render("× %d" % self.bomb_num, True,  self.WHILE)
		self.text_rect = self.bomb_text.get_rect()
		self.screen.blit(self.bomb_image, (10, self.height - 10 - self.bomb_rect.height))
		self.screen.blit(self.bomb_text, (20 + self.bomb_rect.width, self.height - 5 - self.text_rect.height))

	def __draw_supply(self):
		 # 绘制全屏炸弹补给，并检测是否获得
		if self.bomb_supply.active:
			self.bomb_supply.move()
			self.screen.blit(self.bomb_supply.image, self.bomb_supply.rect)
			if pygame.sprite.collide_mask(self.bomb_supply, self.hero):
				if self.bomb_num < 3:
					self.get_bomb_sound.play()
					self.bomb_num += 1
					self.bomb_supply.active = False
		# 绘制超级子弹补给，并检测是否获得
		if self.bullet_supply.active:
			self.bullet_supply.move()
			self.screen.blit(self.bullet_supply.image, self.bullet_supply.rect)
			if pygame.sprite.collide_mask(self.bullet_supply, self.hero):
				self.get_bullet_sound.play()
				# 两发子弹：
				if not self.is_double_bullet:
					self.is_double_bullet = True
				# 三发子弹（在两发子弹的基础上增加第三发）
				elif self.is_double_bullet:
					self.is_triple_bullet = True
				pygame.time.set_timer(self.DOUBLE_BULLET_TIME, 18 * 1000)
				self.bullet_supply.active = False
		# 绘制生命补给
		if self.life_supply.active:
			self.life_supply.move()
			self.screen.blit(self.life_supply.image, self.life_supply.rect)
			if pygame.sprite.collide_mask(self.life_supply, self.hero):
				if self.life_num < 3:
					self.get_bullet_sound.play()
					self.life_num += 1
					self.life_supply.active = False

	def __draw_hero_num(self):
		"""绘制剩余生命数量"""
		if self.life_num:
			for i in range(self.life_num):
				self.screen.blit(self.life_image, (self.width - 10 - (i + 1) * self.life_rect.width,
												   self.height - 10 - self.life_rect.height))

	def __draw_game_over(self):
		"""游戏结束画面"""
		# 1.背景音乐和音效停止
		pygame.mixer.music.stop()
		pygame.mixer.stop()
		# 2.停止发放补给
		pygame.time.set_timer(self.SUPPLY_TIME, 0)
		# 3.打开记录
		if not self.recorded:
			self.recorded = True
			# 读取历史最高分
			with open("record.txt", "r") as f:
				self.record_score = int(f.read())
			# 如果现在的分数大于历史最高分，则将其写入
			if self.score > self.record_score:
				with open("record.txt", "w") as f:
					f.write(str(self.score))

		# 4.绘制结束画面
		self.screen.blit(self.background, (0, 0))
		self.record_score_text = self.score_font.render("Best : %d" % self.record_score, True, (255, 255, 255))
		self.screen.blit(self.record_score_text, (50, 50))

		self.gameover_text1 = self.gameover_font.render("Your Score", True, (255, 255, 255))
		self.gameover_text1_rect = self.gameover_text1.get_rect()
		self.gameover_text1_rect.left, self.gameover_text1_rect.top = \
			(self.width - self.gameover_text1_rect.width) // 2, self.height // 3
		self.screen.blit(self.gameover_text1, self.gameover_text1_rect)

		self.gameover_text2 = self.gameover_font.render(str(self.score), True, (255, 255, 255))
		self.gameover_text2_rect = self.gameover_text2.get_rect()
		self.gameover_text2_rect.left, self.gameover_text2_rect.top = \
			(self.width - self.gameover_text2_rect.width) // 2, \
			self.gameover_text1_rect.bottom + 10
		self.screen.blit(self.gameover_text2, self.gameover_text2_rect)

		self.again_rect.left, self.again_rect.top = \
			(self.width - self.again_rect.width) // 2, \
			self.gameover_text2_rect.bottom + 50
		self.screen.blit(self.again_image, self.again_rect)

		self.gameover_rect.left, self.gameover_rect.top = \
			(self.width - self.again_rect.width) // 2, \
			self.again_rect.bottom + 10
		self.screen.blit(self.gameover_image, self.gameover_rect)

		# 检测用户的鼠标操作
		# 如果用户按下鼠标左键
		if pygame.mouse.get_pressed()[0]:
			# 获取鼠标坐标
			self.pos = pygame.mouse.get_pos()
			# 如果用户点击“重新开始”
			if self.again_rect.left < self.pos[0] < self.again_rect.right and \
					self.again_rect.top < self.pos[1] < self.again_rect.bottom:
				# 调用start__game()函数，重新开始游戏
				self.start__game()
			# 如果用户点击“结束游戏”
			elif self.gameover_rect.left < self.pos[0] < self.gameover_rect.right and \
					self.gameover_rect.top < self.pos[1] < self.gameover_rect.bottom:
				# 退出游戏
				pygame.quit()
				sys.exit()

	def __create_start_image(self):
		# 定义难度属性
		self.easy = True
		self.common = False
		self.difficult = False
		# 飞机大战主题
		self.start = False
		self.theme_font = pygame.font.Font("font/font.ttf", 50)
		self.theme_text = self.theme_font.render("Plane   War", True, self.WHILE)
		self.theme_text_rect = self.theme_text.get_rect()
		self.theme_text_rect.left, self.theme_text_rect.top = (120, 40)
		# 游戏开始字体
		self.start_font = pygame.font.Font("font/font.ttf", 40)
		self.start_text = self.start_font.render("Start Game", True, self.WHILE)
		self.start_text_rect = self.start_text.get_rect()
		self.start_text_rect.left, self.start_text_rect.top = (150, 200)
		# 简单字体
		self.easy_font = pygame.font.Font("font/font.ttf", 40)
		self.easy_text = self.easy_font.render("easy", True,  self.BLACK)
		self.easy_text_rect = self.easy_text.get_rect()
		self.easy_text_rect.left, self.easy_text_rect.top = (200, 400)
		# 一般字体
		self.common_font = pygame.font.Font("font/font.ttf", 40)
		self.common_text = self.common_font.render("common", True,  self.WHILE)
		self.common_text_rect = self.common_text.get_rect()
		self.common_text_rect.left, self.common_text_rect.top = (180, 450)
		# 困难字体
		self.difficult_font = pygame.font.Font("font/font.ttf", 40)
		self.difficult_text = self.difficult_font.render("difficult", True, self.WHILE)
		self.difficult_text_rect = self.difficult_text.get_rect()
		self.difficult_text_rect.left, self.difficult_text_rect.top = (180, 510)
		# 左右两个小飞机图标
		self.small_hero1_image = pygame.image.load("images/life.png").convert_alpha()
		self.small_hero1_rect = self.small_hero1_image.get_rect()
		self.small_hero1_rect.left, self.small_hero1_rect.top = (0, 650)
		self.small_hero2_rect = self.small_hero1_image.get_rect()
		self.small_hero2_rect.left, self.small_hero2_rect.top = (435, 650)
		# 中间大飞机图标
		self.big_hero_image = pygame.image.load("images/me1.png").convert_alpha()
		self.big_hero_rect = self.big_hero_image.get_rect()
		self.big_hero_rect.left, self.big_hero_rect.top = (190, 250)

	def __draw_start_image(self):
		self.screen.blit(self.theme_text, self.theme_text_rect)
		self.screen.blit(self.start_text, self.start_text_rect)
		self.screen.blit(self.small_hero1_image, self.small_hero1_rect)
		self.screen.blit(self.small_hero1_image, self.small_hero2_rect)
		self.screen.blit(self.big_hero_image, self.big_hero_rect)
		# 难度选择
		if pygame.mouse.get_pressed()[0]:
			# 获取鼠标坐标
			self.pos = pygame.mouse.get_pos()
			if self.start_text_rect.left < self.pos[0] < self.start_text_rect.right and \
					self.start_text_rect.top < self.pos[1] < self.start_text_rect.bottom:
				self.start = True
			if self.easy_text_rect.left < self.pos[0] < self.easy_text_rect.right and \
					self.easy_text_rect.top < self.pos[1] < self.easy_text_rect.bottom:
				self.easy_text = self.easy_font.render("easy", True, self.BLACK)
				self.common_text = self.common_font.render("common", True, self.WHILE)
				self.difficult_text = self.difficult_font.render("difficult", True, self.WHILE)
				self.easy = True
				self.common = False
				self.difficult = False
			if self.common_text_rect.left < self.pos[0] < self.common_text_rect.right and \
					self.common_text_rect.top < self.pos[1] < self.common_text_rect.bottom:
				self.easy_text = self.easy_font.render("easy", True, self.WHILE)
				self.common_text = self.common_font.render("common", True, self.BLACK)
				self.difficult_text = self.difficult_font.render("difficult", True, self.WHILE)
				self.easy = False
				self.common = True
				self.difficult = False
			if self.difficult_text_rect.left < self.pos[0] < self.difficult_text_rect.right and \
					self.difficult_text_rect.top < self.pos[1] < self.difficult_text_rect.bottom:
				self.easy_text = self.easy_font.render("easy", True, self.WHILE)
				self.common_text = self.common_font.render("common", True, self.WHILE)
				self.difficult_text = self.difficult_font.render("difficult", True, self.BLACK)
				self.easy = False
				self.common = False
				self.difficult = True

		self.screen.blit(self.easy_text, self.easy_text_rect)
		self.screen.blit(self.common_text, self.common_text_rect)
		self.screen.blit(self.difficult_text, self.difficult_text_rect)


if __name__ == '__main__':
	game = PlaneGame()
	game.start__game()
