import pygame
from itertools import cycle


class Bird:
    """Реализует объект птички"""
    def __init__(self, fb_game):
        """Инициализирует начальные атрибуты птички"""
        self.fb_game = fb_game
        self.screen = fb_game.screen
        self.screen_rect = fb_game.screen.get_rect()
        self.settings = fb_game.settings

        # Получаем изображение птички
        self.image = pygame.image.load("images/bird.bmp")
        self.rect = self.image.get_rect()

        # Получаем дополнительные изображения
        self.image_downflip = pygame.image.load("images/bird-downflap.bmp")
        self.image_upflip = pygame.image.load("images/bird-upflap.bmp")

        # Собираем изображения в список 
        # и записываем в атрибут генератор изображения
        self.images = [self.image_downflip, self.image, self.image_upflip]
        self.image_generator = self._ch_image()

        # Выравниваем птичку по центру экрана и записываем координату у в атрибут self.y
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)

        # Количество пройденных колонн
        self.passed_pipes = 0

    def update(self):
        """Обновляет позицию птички"""
        self.y += (2 ** 0.5 * self.settings.world_velocity + self.settings.bird_gravity) / 2

        # Обновляем атрибут rect.y
        self.rect.y = self.y

    def draw_bird(self):
        """Отрисовывает птичку на экране"""
        self.screen.blit(next(self.image_generator), self.rect)
        
    def do_jump(self):
        """Cовершает прыжок"""
        self.y -= self.settings.bird_jump_speed 

        # Обновляем атрибут rect.y
        self.rect.y = self.y

    def _check_edges(self):
        """Проверяет, достигла ли птичка краев экрана"""
        return self.rect.top <= 0 or self.rect.bottom >= self.settings.height - 112

    def _check_collisions(self):
        """Проверят была ли коллизия с какой-либо колонной"""
        for pipe in self.fb_game.pipes:
            if  (pipe.reversed_image_rect.bottom - 5 >= self.rect.top or pipe.rect.top + 5 <= self.rect.bottom) \
                and pipe.rect.left <= self.rect.centerx <= pipe.rect.right:
                return True

    def check_pos(self):
        """Проверяет надо ли закончить игру"""
        return (self._check_edges() or self._check_collisions())

    def _ch_image(self):
        """Генератор новоого изображения птички"""
        for image in cycle(self.images):
            yield image 



            
    

    

                
                
