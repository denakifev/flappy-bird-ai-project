import pygame
from pygame.sprite import Sprite

class Base(Sprite):
    """Класс для создания платформы"""
    def __init__(self, fb_game):
        """Инициализирует начальные атрибуты платформы"""
        super().__init__()
        self.screen = fb_game.screen
        self.screen_rect = fb_game.screen.get_rect()
        self.settings = fb_game.settings
    
        self.image = pygame.image.load('images/base.bmp')
        self.rect = self.image.get_rect()

        #Задаем начальное расположение
        self.rect.bottom = self.screen_rect.bottom
        self.rect.left = 0

        # х координату платформы будем хранить в вещественном формате 
        self.x = float(self.rect.x)

    def update(self):
        """Обновляет позицию платформы"""
        self.x -= self.settings.world_velocity

        #Обновляем rect.x 
        self.rect.x = self.x

    def draw(self):
        """Рисует платформу"""
        self.screen.blit(self.image, self.rect)

    def change_pos(self):
        """Обновляет позицию платформы, вышедшей за границы экрана"""
        if self.rect.right <= 0:
            self.rect.right += (self.rect.width * 2) 
            self.x = float(self.rect.x)

    

        
