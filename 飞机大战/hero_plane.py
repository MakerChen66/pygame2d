import pygame


class MyPlane(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super().__init__()
        # 获取英雄图片（两幅图片实现动态效果）
        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        # 英雄毁灭图片切换
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/me_destroy_1.png").convert_alpha(),
                                    pygame.image.load("images/me_destroy_2.png").convert_alpha(),
                                    pygame.image.load("images/me_destroy_3.png").convert_alpha(),
                                    pygame.image.load("images/me_destroy_4.png").convert_alpha()])
        # 获取英雄大小，宽度和高度
        self.rect = self.image1.get_rect()
        # 设置英雄位置
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        # 设置英雄速度
        self.speed = 10
        # 设置英雄生存状态
        self.active = True
        # 设置飞机无敌
        self.invincible = False
        # 返回英雄除了空白区域的部分
        self.mask = pygame.mask.from_surface(self.image1)

    def moveUp(self):
        """英雄方向控制"""
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    # 飞机一条命结束之后调用该方法开始下一命
    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.active = True
        self.invincible = True

