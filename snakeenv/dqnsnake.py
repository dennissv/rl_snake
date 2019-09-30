#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 13:58:18 2018

@author: dennis


Implements a simple snake environment.

State is Atari standard (210,160,3) numpy array. Different colors for empty,
snake body, snake head and apple

There's three possible actions each step; turn left (0), go straight (1)
or turn right (2).

Reward is 1 if an apple is eaten, else 0.

Game is over if head collides with wall or body.
"""

import gym
import numpy as np
from gym import spaces

black, red, green, yellow = [0,0,0], [255,0,0], [0,255,0], [255,255,0]
#black, red, yellow, green = 0, 0.33, 0.66, 1

def transform(image):
    new_image = []
    for row in image:
        for j in range(6):
            new_row = []
            for element in row:
                for i in range(6):
                    new_row.append(element)
            new_image.append(new_row)
    return np.uint8(new_image)

class SnakeDQNEnv(gym.Env):

    def __init__(self):
        self.steps_beyond_done = None
        self.screen = None
        self.action_space = spaces.Discrete(3)

    def step(self, action):
        old_pos = self.pos
        y, x = self.pos
        if action == 0: self.direction += 1
        elif action == 2: self.direction -= 1
        self.direction = self.direction % 4
        # 0 = up, 1 = right, 2 = down, 3 = left
        if self.direction == 0: y += 1
        elif self.direction == 1: x += 1
        elif self.direction == 2: y -= 1
        elif self.direction == 3: x -= 1
        self.pos = (y, x)

        if self.pos == self.target:
            reward = 1.0
            self.occupied += [old_pos]
            while (self.target in self.occupied) or (self.target == self.pos):
                self.target = (np.random.randint(0,13), np.random.randint(0,13))
        else:
            self.occupied = self.occupied[1:] + [old_pos]
            reward = 0.0
        if self.pos in self.occupied:
            reward = -1.0
            
        done =  (x < 0) or (x > 13) or (y < 0) or (y > 13)
#                or (self.pos in self.occupied)
#        done = bool(done)
        if done:
            reward = -1.0
        
        self.state = np.uint8([[black for x in range(14)] for y in range(14)])
#        self.state = np.float64([[black for x in range(16)] for y in range(21)])
        if not done:
            self.state[self.pos[0]][self.pos[1]] = yellow
        self.state[self.target[0]][self.target[1]] = green
        for y, x in self.occupied:
            self.state[y][x] = red
        self.state = transform(self.state)
            
        return self.state.flatten(), reward, done, {}

    def reset(self):
        self.steps_beyond_done = None
        self.direction = 1
        self.pos = (np.random.randint(4,10), np.random.randint(4,10)) # [y][x] because idk
        y, x = self.pos
        self.occupied = [(y, x+i) for i in range(-4, 0)]
        self.target = (np.random.randint(0,13), np.random.randint(0,13))
        while (self.target in self.occupied) or (self.target == self.pos):
            self.target = (np.random.randint(0,13), np.random.randint(0,13))
        self.state = np.uint8([[black for x in range(14)] for y in range(14)])
#        self.state = np.float64([[black for x in range(16)] for y in range(21)])
        self.state[self.target[0]][self.target[1]] = green
        self.state[self.pos[0]][self.pos[1]] = yellow
        for y, x in self.occupied:
            self.state[y][x] = red
        self.state = transform(self.state)
        return self.state.flatten()
    
    def seed(self):
        pass

    def render(self, mode='human', close=False):
        if mode == 'rgb_array':
            return self.last_image
        elif mode == 'human':
            import pygame
            if close:
                pygame.quit()
            else:
                if self.screen is None:
                    pygame.init()
                    self.screen = pygame.display.set_mode((160, 210))
                img = pygame.surfarray.make_surface(self.state.swapaxes(0, 1))
                self.screen.blit(img, (0, 0))
                pygame.display.update()