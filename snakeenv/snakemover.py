#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 23:14:00 2018

@author: dennis
"""

import gym
import numpy as np
#from skimage import transform
from gym import spaces

black, green, yellow, red = 0, 0.33, 0.66, 1

class SnakeMover(gym.Env):

    def __init__(self):
        self.screen = None
        self.action_space = spaces.Discrete(3)
#        self.observation_space = spaces.Box(shape=(7,7))

    def step(self, action):
        # 0 up, 1 right, 2 down, 3 left
        y, x = self.pos
        self.state[self.pos[0]][self.pos[1]] = 0.0
        if x == 0 or x == 6 or y == 0 or y == 6:
            done = True
            reward = -1
            return self.state.flatten(), reward, done, {}
        if action == 0: y -= 1
        elif action == 1: x += 1
        elif action == 2: y += 1
        elif action == 3: x -= 1
        self.pos = (y, x)
        self.state[self.pos[0]][self.pos[1]] = 0.66
        
        done = False
        reward = 0
        if self.pos in self.reds:
            reward = -1
            done = True
        elif self.pos == self.target:
            reward = 1
            while self.target == self.pos or self.target in self.reds:
                self.target = (np.random.randint(1,6), np.random.randint(1,6))
            
        return self.state.flatten(), reward, done, {}

    def reset(self):
        self.pos = (np.random.randint(1,6), np.random.randint(1,6))
        self.reds = []
        for i in range(3):
            new_block = (np.random.randint(1,6), np.random.randint(1,6))
            while new_block == self.pos or new_block in self.reds:
                new_block = (np.random.randint(1,6), np.random.randint(1,6))
            self.reds.append(new_block)
        self.target = (np.random.randint(1,6), np.random.randint(1,6))
        while self.target == self.pos or self.target in self.reds:
            self.target = (np.random.randint(1,6), np.random.randint(1,6))
        self.state = np.zeros((7,7), dtype=np.float64)
        self.state[0] = 1.0
        self.state[6] = 1.0
        for i in range(1,6):
            self.state[i][0] = 1.0
            self.state[i][6] = 1.0
        self.state[self.pos[0]][self.pos[1]] = 0.66
        self.state[self.target[0]][self.target[1]] = 0.33
        for red in self.reds:
            self.state[red[0]][red[1]] = 1
        return self.state.flatten()

#    def seed(self):
#        pass

    def render(self, mode='human', close=False):
        if mode == 'array':
            return self.state
        elif mode == 'human':
            import pygame
            if close:
                pygame.quit()
            else:
                if self.screen is None:
                    pygame.init()
                    self.screen = pygame.display.set_mode((160, 210))
                img = pygame.surfarray.make_surface(transform.resize(self.state.swapaxes(0, 1), (160, 210)))
                self.screen.blit(img, (0, 0))
                pygame.display.update()