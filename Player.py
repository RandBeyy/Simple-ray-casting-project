from re import S
import pygame
import math
from copy import deepcopy

class Player:

    def __init__(self, b_game):
        
        self.screen = b_game.screen
        self.settings = b_game.settings
        
        self.angle_direction = True
        self.player_direction = 'forward'
        self.angle = math.pi
        self.angle_update = False
        self.position_update = False
        self.player_x, self.player_y = self.settings.player_position
        self.position = ((self.player_x), self.player_y)

    def check_movement(self):
        if self.angle_update: self.update_angle()
        if self.position_update: self.update_position()

    def draw_player(self):
        pygame.draw.circle(self.screen, self.settings.yellow_col, (self.player_x, self.player_y), self.settings.player_rad)

    def update_angle(self):
        if self.angle_direction:
            if self.angle <= 0: self.angle = 2 * math.pi - self.angle
            self.angle -= self.settings.rotation_speed
        else:
            if self.angle >= 2 * math.pi: self.angle = 0 + (2 * math.pi - self.angle)
            self.angle += self.settings.rotation_speed

    def update_position(self):
        if self.player_direction == 'forward':
            self.player_x += math.sin(self.angle) * self.settings.player_speed
            self.player_y += math.cos(self.angle) * self.settings.player_speed
        elif self.player_direction == 'backward':
            self.player_x -= math.sin(self.angle) * self.settings.player_speed
            self.player_y -= math.cos(self.angle) * self.settings.player_speed
        elif self.player_direction == 'left':
            self.player_x += math.sin(self.angle - math.pi / 2) * self.settings.player_speed
            self.player_y += math.cos(self.angle - math.pi / 2) * self.settings.player_speed
        else:
            self.player_x += math.sin(self.angle + math.pi / 2) * self.settings.player_speed
            self.player_y += math.cos(self.angle + math.pi / 2) * self.settings.player_speed
        
