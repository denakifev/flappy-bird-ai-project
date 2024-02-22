
class Settings:
    """Класс, содержащий игровые настройки Flappy bird"""
    def __init__(self):
        """Инициализирует игровые настройки"""
        self.width = 350
        self.height = 500
        self.fps = 60

        #Настройки скорости мира 
        self.world_velocity = 1.5

        #Настройки колонн
        #Интервал между колоннами
        self.interval_x = 150
        self.interval_y = 115

        #Диапазон разброса высоты(33 - высoта выступа у колонны, 112 - высота платформы)
        self.upper_y = self.height - 112 - 33
        self.floor_y = 33 + self.interval_y

        
        #Настройки птички
        self.bird_gravity = ( (2 * 200 * 200 - 2 * self.interval_x) * (self.world_velocity ** 2 / 2)) / self.interval_x ** 2
        self.bird_jump_speed = self.bird_gravity * 16

        #флажок состояния
        self.game_active = False
        