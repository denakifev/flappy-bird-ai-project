#!/usr/bin/env python3
import sys
import os
import pygame
import neat
from settings import Settings
from base import Base
from pipe import Pipe
from bird import Bird
from text import TextBorder

generation = 0
class FlappyBird:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.set_bg()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption('Flappy bird')
        self.clock = pygame.time.Clock()

        #Инициализируем игровые объекты
        self.bases = pygame.sprite.Group()
        self._create_bases()
        self._init_pipes()
        self.birds = []
        self.ge = []
        self.nets = []
        self.tb = TextBorder(self)

    def make_decision(self):
        """Принимает решение - прыгать или нет"""
        # Определяем индекс ближайшей к нам колонны
        pipe_ind = 0
        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].rect.x > self.pipes[0].rect.x + self.pipes[0].rect.width: 
                pipe_ind = 1   
        
        for i, bird in enumerate(self.birds):
            output = self.nets[i].activate((bird.rect.y, abs(bird.rect.y - self.pipes[pipe_ind].rect.top), \
                abs(bird.rect.y - self.pipes[pipe_ind].reversed_image_rect.bottom)))
            if output[0] > 0.5:
                bird.do_jump()
   
    def _check_events(self):
        """Отслеживает нажатия клавиш и события мыши """
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_event(event)

    def _update_screen(self):
        """Обновляет экран и отрисовывает новый"""
        #Отрисовываем обновленные объекты
        for pipe in self.pipes:
            pipe.draw()
        self.bases.draw(self.screen)
        for bird in self.birds:
            bird.draw_bird()
        self.tb.draw_score()
        self.tb.show_msg()
 
        #Отображаем последний отрисованный кадр
        pygame.display.flip()
    
    def _check_keydown_event(self, event):
        """Отслеживает события нажатия клавиши"""
        if event.key == pygame.K_q:
            sys.exit()
            

    def set_bg(self):
        """Создает задний фон"""
        self.bg_image = pygame.image.load('images/background.bmp')
        self.bg_rect = self.bg_image.get_rect()
        
        #Записываем размеры окна на основе размеров заднего фона в настройки
        self.settings.width, self.settings.height = self.bg_rect.size
    
    def blit_bg(self):
        """Отрисовывает фон"""
        self.screen.blit(self.bg_image, self.bg_rect)

    def _create_bases(self):
        """Создает 2 платформы"""
        for base_number in range(2):
            base = Base(self)
            base.rect.left = base.rect.width * base_number
            base.x = float(base.rect.x)
            self.bases.add(base)

    def _update_bases(self):
        """Обновляет позиции каждой платформы"""
        self.bases.update()
        
        #Перемещаем платформы, вышедшие за границу экрана
        for base in self.bases:
            base.change_pos()

    def _create_pipe(self):
        """Создает кoлонну с интервалом в self.settings.interval пиксела"""
        pipe = Pipe(self)
        pipe.rect.left = self.pipes[-1].rect.right + self.settings.interval_x
        pipe.x = float(pipe.rect.x)
        self.pipes.append(pipe)
    
    def _update_pipes(self):
        """Обновляет позицию колонн, удаляет и добавляет колонны"""
        # Проходимся по копии группы, обновляем счет, добавляем и удаляем колонны
        add_score = False
        for pipe in self.pipes.copy():
            pipe.update()
            for i, bird in enumerate(self.birds):
                if bird.check_edges():
                    self.rm_form_lists(i)
                if pipe.check_collision(bird):
                    self.ge[i].fitness -= 1
                    self.rm_form_lists(i)
                
                if pipe.check_of_passing(bird):
                    add_score = True
                    pipe.passed = True
                
            if pipe.check_end():
                self._create_pipe()
                self.pipes.remove(pipe)
        
        if add_score:
            self.score += 1
            for genome in self.ge:
                genome.fitness += 5
    
    def _init_pipes(self):
        """Инициализирует группу колонн"""
        self.pipes = []
        #Заполняем группу первой колонной вручную, второй c помощью метода 
        self.pipes.append(Pipe(self))
        self._create_pipe()
    
    def rm_form_lists(self, index):
        """Удаляет объект из всех списков"""
        self.birds.pop(index)
        self.ge.pop(index)
        self.nets.pop(index)
    
    def update_birds(self):
        """Обновляет позицию птичек"""
        for i, bird in enumerate(self.birds):
            bird.update()
            self.ge[i].fitness += 0.1

    
def eval_genomes(genomes, config):
    """Запускает одну игру для поколения"""
    global generation
    fb = FlappyBird()
    generation += 1
    fb.score = 0
    #Заполняем списки объектами
    for _ , genome in genomes:
        fb.birds.append(Bird(fb))
        fb.ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        fb.nets.append(net)
        genome.fitness = 0
    
    while True and len(fb.birds) > 0:
        fb._check_events()
        pygame.mouse.set_visible(False)
        fb.blit_bg()
        fb._update_bases()
        fb._update_pipes()
        fb.make_decision()
        fb.update_birds()
        fb.tb.prep_score()
        fb.tb.prep_msg(generation, len(fb.birds))
    
        fb._update_screen()
        if len(fb.birds) == 0:
            break
        fb.clock.tick(fb.settings.fps)



def run(config_path):
    """Инициализирует NEAT"""
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
