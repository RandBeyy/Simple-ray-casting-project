import pygame
import sys
from Player import Player
from Settings import Settings
import math

class ShooterGame:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        
        self.max_depth = math.sqrt(pow(self.settings.screen_size[0],2) + pow(self.settings.screen_size[1],2))
        
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        self.map = (
            '##########',
            '#   #    #',
            '# #    # #',
            '#        #',
            '#        #',
            '# #    # #',
            '#        #',
            '#####    #',
            '#        #',
            '##########'
        )
        self.screen.fill(self.settings.black_col)
        self.player = Player(self)
        self.lines = []
        self.depths = []
        self.ray_angles = []

    def run_game(self):
        while True:
            self.clock.tick(self.settings.framerate)
            self._check_events()
            self._cast_rays()
            self._check_for_bound()
            self.player.check_movement()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_LEFT:
            self.player.angle_direction = True
            self.player.angle_update = True
        elif event.key == pygame.K_RIGHT:
            self.player.angle_direction = False
            self.player.angle_update = True
        elif event.key == pygame.K_w:
            self.player.position_update = True
            self.player.player_direction = 'forward'
        elif event.key == pygame.K_s:
            self.player.position_update = True
            self.player.player_direction = 'backward'
        elif event.key == pygame.K_a:
            self.player.position_update = True
            self.player.player_direction = 'left'
        elif event.key == pygame.K_d:
            self.player.position_update = True
            self.player.player_direction = 'right'
            
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.player.angle_update = False
        elif event.key == pygame.K_RIGHT:
            self.player.angle_update = False
        elif event.key == pygame.K_w:
            self.player.position_update = False
        elif event.key == pygame.K_s:
            self.player.position_update = False
        elif event.key == pygame.K_a:
            self.player.position_update = False
        elif event.key == pygame.K_d:
            self.player.position_update = False

    def _cast_rays(self):
        self.lines = []
        self.depths = []
        self.ray_angles = []
        x, y = self.player.player_x, self.player.player_y
        target_x = 0
        target_y = 0
        angle = self.player.angle - (self.settings.FOV / 2)
        for ray in range(self.settings.number_of_lines):
            for depth in range(int(self.max_depth)):
                target_x = x + math.sin(angle) * depth
                target_y = y + math.cos(angle) * depth

                i = int(target_y / self.settings.cell_size)
                j = int(target_x / self.settings.cell_size)
                if self.map[i][j] == '#':
                    self.depths.append(depth)
                    self.ray_angles.append(angle)
                    break
            angle += self.settings.angle_step
            self.lines.append((x, y))
            self.lines.append((target_x, target_y))

    def _update_screen(self):
        self.screen.fill(self.settings.white_col)
        #self._update_map()
        #pygame.draw.lines(self.screen, self.settings.red_col, True, self.lines)
        #self.player.draw_player()
        self.draw_3D()
        pygame.display.flip()

    def _check_for_bound(self):
        i1 = int((self.player.player_y + self.settings.player_rad) / self.settings.cell_size)
        i2 = int((self.player.player_y - self.settings.player_rad) / self.settings.cell_size)
        j1 = int((self.player.player_x + self.settings.player_rad) / self.settings.cell_size)
        j2 = int((self.player.player_x - self.settings.player_rad) / self.settings.cell_size)
        
        opposite_side = {'forward' : 'backward',
                         'backward' : 'forward',
                         'left': 'right',
                         'right': 'left'}

        if self.map[i1][j1] == '#' or self.map[i1][j2] == '#' or self.map[i2][j1] == '#' or self.map[i2][j2] == '#':
            self.player.position_update = True
            self.player.player_direction = opposite_side[self.player.player_direction]
            self.player.update_position()
            self.player.position_update = False

    def draw_3D(self):
        render_y1 = 0
        render_y2 = 0
        render_x = 0
        pygame.draw.rect(self.screen, self.settings.light_blue_col,pygame.Rect(0,0, 500, 250))
        pygame.draw.rect(self.screen, self.settings.orange,pygame.Rect(0,250, 500, 250))
        for i in range(0, len(self.depths)):
            depth = self.depths[i] * math.cos(self.player.angle - self.ray_angles[i])
            portion = 20 / depth
            length = self.settings.screen_size[1] * portion
            if length > 500: length = 500
            render_y1 = (self.settings.screen_size[1] - length) / 2
            render_y2 = render_y1 + length
            rgb = int(200 * portion)
            if rgb > 255: rgb = 255
            elif rgb < 0: rgb = 0
            color = (rgb, rgb, rgb)
            pygame.draw.line(self.screen, color, (render_x, render_y1), (render_x, render_y2), 5)
            render_x += self.settings.step



    def _update_map(self):
        cell_size = self.settings.screen_size[0]/10
        x = 0
        y = 0
        for row in self.map:
            x = 0
            for tile in row:
                if tile == '#': 
                    pygame.draw.rect(self.screen, self.settings.gray_col, pygame.Rect(x,y, cell_size, cell_size))
                else:
                    pygame.draw.rect(self.screen, self.settings.white_col, pygame.Rect(x,y, cell_size, cell_size))
                x+=cell_size
            y+=cell_size

if __name__ == '__main__':
    sg = ShooterGame()
    sg.run_game()