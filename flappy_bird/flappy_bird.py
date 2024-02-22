import sys
import pygame
from time import sleep
from settings import Settings
from base import Base
from pipe import Pipe
from bird import Bird
from text import TextBorder

class FlappyBird:
    def __init__(self):
        
        pygame.init()
        self.settings = Settings()
        self.set_bg()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption('Flappy bird')
        self.clock = pygame.time.Clock()

        
        self.bases = pygame.sprite.Group()
        self._create_bases()
        self._init_pipes()
        self.bird = Bird(self)
        self.tb = TextBorder(self)

    def run_game(self):
       
        while True:
            self._check_events()
            
            
            if not self.settings.game_active:
                pygame.mouse.set_visible(True)
                self.blit_bg()
                self._update_bases()
            else: 
                pygame.mouse.set_visible(False)
                self.blit_bg()
                self._update_bases() 
                self._update_pipes()
                self.bird.update()
                self.tb.prep_score()
        
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
       
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_event(event)

    def _update_screen(self):
        
        if self.bird.check_pos():
            sleep(0.5)
            self.reset_game()
            self.settings.game_active = False

        
        if not self.settings.game_active:
            self.tb.show_msg()
            self.bases.draw(self.screen)
            self.bird.draw_bird()
        else:
            self.pipes.draw(self.screen)
            self.bases.draw(self.screen)
            self.bird.draw_bird()
            self.tb.draw_score()
 
        
        pygame.display.flip()
    
    def _check_keydown_event(self, event):
        
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.settings.game_active:
            self.bird.do_jump()
        elif event.key == pygame.K_SPACE and not self.settings.game_active:
            self.settings.game_active = True
            self.reset_game()

    def set_bg(self):
        
        self.bg_image = pygame.image.load('images/background.bmp')
        self.bg_rect = self.bg_image.get_rect()
        
        
        self.settings.width, self.settings.height = self.bg_rect.size
    
    def blit_bg(self):
        
        self.screen.blit(self.bg_image, self.bg_rect)

    def _create_bases(self):
        
        for base_number in range(2):
            base = Base(self)
            base.rect.left = base.rect.width * base_number
            base.x = float(base.rect.x)
            self.bases.add(base)

    def _update_bases(self):
        
        self.bases.update()
        
        
        for base in self.bases:
            base.change_pos()

    def _create_pipe(self):
       
        pipe = Pipe(self)
        pipe.rect.left = self.pipes.sprites()[-1].rect.right + self.settings.interval_x
        pipe.x = float(pipe.rect.x)
        self.pipes.add(pipe)
    
    def _update_pipes(self):
       
        self.pipes.update()

        
        for pipe in self.pipes.copy():
            if pipe.check_of_passing():
                self.bird.passed_pipes += 1
                pipe.passed = True
                self._create_pipe()
            if pipe.check_end():
                self.pipes.remove(pipe)
            pipe.draw_reversed_part()

    def _init_pipes(self):
       
        self.pipes = pygame.sprite.Group()
       
        self.pipes.add(Pipe(self))
        self._create_pipe()
    
    def reset_game(self):
       
        self.pipes.empty()
        
        
        self.bird.rect.center = self.screen.get_rect().center
        self.bird.y = float(self.bird.rect.y)
        
        
        self.bird.passed_pipes = 0

        
        self._init_pipes() 


if __name__ == '__main__':
    fb = FlappyBird()
    fb.run_game()
