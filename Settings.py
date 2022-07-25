import math

class Settings:

    def __init__(self):
        
        self.screen_size = (500, 500)
        self.framerate = 30

        self.cells_in_row = 10
        self.cell_size = int(self.screen_size[1] / self.cells_in_row)

        self.black_col = (0,0,0)
        self.yellow_col = (0, 255, 255)
        self.red_col = (255, 0, 0)
        self.white_col = (255, 255, 255)
        self.gray_col =  (200, 200, 200)
        self.light_blue_col = (173, 216, 230)
        self.orange = (218, 161, 134)
        
        self.FOV = (120 * math.pi) / 180
        self.number_of_lines = 120
        self.step = 5
        self.angle_step = self.FOV / self.number_of_lines

        self.player_position = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        self.player_rad = 5
        self.rotation_speed = 0.1
        self.player_speed = 2
