import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        # 初始化飞船并设置起始位置
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # 移动位置默认参数参数
        self.x = float(self.rect.x)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
 
    def update(self):
        # 更新飞船移动位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 更新rect属性
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让ship居中于屏幕底部💻
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


