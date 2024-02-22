from pygame.sprite import Sprite
import pygame
from random import randint

class Pipe(Sprite):
    """Класс для управления колонной"""
    def __init__(self, fb_game):
        """Инициализирует пару колонн - верхнюю и нижнюю"""
        super().__init__()
        self.fb_game = fb_game
        self.settings = fb_game.settings
        self.screen = fb_game.screen
        self.screen_rect = fb_game.screen.get_rect()

        self.image = pygame.image.load('images/pipe.bmp')
        self.rect = self.image.get_rect()

        #Загружаем перевернутое изображение
        self.reversed_image = pygame.image.load('images/pipe_reversed.bmp')
        self.reversed_image_rect = self.reversed_image.get_rect()
    
        #Задаем случайную высоту колонны и ровняем по земле
        self.rect.left = self.screen_rect.right  
        self.rect.bottom = self.screen_rect.bottom
        self._reset_top()

        #Флаг прохождения
        self.passed = False

    def draw(self):
        """Рисует одну колонну"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """Обновляет позицию колонны"""
        self.x -= self.settings.world_velocity

        #Обновляем rect 
        self.rect.x = self.x
        self.reversed_image_rect.x = self.x

    def _reset_top(self):
        """Обновляет высоту колонны и атрибут х"""
        self.rect.top = randint(self.settings.floor_y, self.settings.upper_y)

        #Храним координату колонны в вещественном формате 
        self.x = float(self.rect.x)

    def check_end(self):
        """Возвращает True, если колонна покинула экран"""
        return self.rect.right <= 0

    def _center(self):
        """Центрует вторую колонну по первой"""
        self.reversed_image_rect.bottom =  self.rect.top - self.settings.interval_y

    def draw_reversed_part(self):
        '''Рисует вторую часть колонны'''
        self._center()
        self.screen.blit(self.reversed_image, self.reversed_image_rect)

    def check_of_passing(self):
        """Определяет, пройденна ли колонна птичкой"""
        return not self.passed and self.rect.x < self.fb_game.bird.rect.x
            