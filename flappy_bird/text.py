import pygame 

class TextBorder:
    """Инициализирует сообщение, если игра неактивна, иначе - игровой счет"""
    def __init__(self, fb_game):
        """Инициализирует начальные атрибуты текста"""
        self.screen = fb_game.screen
        self.screen_rect = fb_game.screen.get_rect()
        self.fb_game = fb_game

        # Назначение размера и свойств текстового сообщения  
        self.text1 = "Для начала игры нажмите space,"
        self.text2 = "для выхода q"
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = (0, 230, 0)
        self.bg_color = (0,136,148)

        self._prep_msg()

    def _prep_msg(self):
        """Подготавливает сообщение"""
        self.msg_image1 = self.font.render(
            self.text1, True, self.text_color, self.bg_color
        )
        self.msg_image2 = self.font.render(
            self.text2, True, self.text_color, self.bg_color
        )
        
        #Построение атрибута rect и выравнивание по верхней стороне
        self.image_rect1 = self.msg_image1.get_rect()
        self.image_rect1.top = self.screen_rect.top

        self.image_rect2 = self.msg_image2.get_rect()
        self.image_rect2.top = self.image_rect1.bottom

    def show_msg(self):
        """Выводит сообщение на экран"""
        self.screen.blit(self.msg_image1, self.image_rect1)
        self.screen.blit(self.msg_image2, self.image_rect2)        

    def draw_score(self):
        """Отображает текущий счет"""
        for d_image, d_rect in self.d_images:
            self.screen.blit(d_image, d_rect)
        
    def prep_score(self):
        '''Подготавливает текущий счет для вывода'''
        self.score = str(self.fb_game.bird.passed_pipes)
        self.d_images = []
        # Выравниваем каждую цифру и добавляем в список 
        for number, digit in enumerate(self.score):
            digit_image = pygame.image.load(f'images/digits/{digit}.bmp')
            digit_rect = digit_image.get_rect()
            digit_rect.top = self.screen_rect.top + 10
            digit_rect.right = self.screen_rect.centerx + digit_rect.width * number
            self.d_images.append((digit_image, digit_rect))


