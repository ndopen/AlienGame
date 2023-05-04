import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # 实例化游戏统计信息
        self.stats = GameStats(self)

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 全屏幕运行
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

        # 调用pygame group
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)
    
    def run_game(self):
        """游戏主循环🔄🔄🔄
        """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_alien()
                self._update_bullets()

            self._update_screen()

    def _check_events(self):
        """事件管理辅组方法"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            """向右移动飞船"""
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            """向左移动"""
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # 发射子弹
            self._fire_bullet()
        elif event.key == pygame.K_q:
            # 推出游戏
            sys.exit()

    def _check_play_button(self, mouse_pos):
        """在单击paly是game_active = True
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置所有游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空屏幕
            self.aliens.empty()
            self.bullets.empty()

            # 重置游戏速度设置
            self.settings.initialize_dynamic_settings()
            
            # 创新新的外星人并且居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标
            pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建新的子弹， 并且加入到group中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # 更新子弹位置
        self.bullets.update()
        # 清楚消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        # 如果bullets与alien叠加，就删除两个元素并存入字典中
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # 删除aliens并创建新的fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提升等级
            self.stats.level += 1
            self.sb.prep_level()

        # 计算游戏得分
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _create_fleet(self):
        """创建外星人集群
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算屏幕可容纳的行数
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人放置到当前行
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_alien(self):
        """更新alien位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应alien与ship碰撞后的事件 👽 👊 ✈️
        """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空所有alien bullets 👽👽👽 🔪🔪🔪
            self.aliens.empty()
            self.bullets.empty()
            # 创建新的alien 并将ship放置到屏幕居中为之 👽👽👽 ✈️✈️✈️
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查外星人是否到达了屏幕底部,如果触碰底部就调用_ship_hit方法
        💻💻💻💻💻💻💻💻💻💻💻💻
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _check_fleet_edges(self):
        """外星人抵达边缘时的动作"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        """下移并改变方向
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """屏幕更新辅助方法"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # 循环bullet group中的sprites
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # 显示得分信息
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
                
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
