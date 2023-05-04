import pygame.font

class Button:
    """绘制play按扭
    """
    def __init__(self, ai_game, msg):
        """初始化按扭属性

        Args:
            msg (_type_): 按扭文字信息
            ai_game (_type_): 调用主要函数，获取屏幕信息
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # 设置按扭所需要的参数
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按扭rect对象，使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg文字参数渲染为图像

        Args:
            msg (_type_): msg渲染的参数
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按扭
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)