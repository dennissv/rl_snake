#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:00:09 2018

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

#black, red, green, yellow = [0,0,0], [255,0,0], [0,255,0], [255,255,0]
black, red, yellow, green = 0, 0.33, 0.66, 1
head = np.rot90(np.load('snakeenv/head.npy'), 2)
straight = np.load('snakeenv/straight.npy')
bend = np.load('snakeenv/bend.npy')

def transform(image, scale=8):
    new_image = []
    for row in image:
        for j in range(scale):
            new_row = []
            for element in row:
                for i in range(scale):
                    new_row.append(element)
            new_image.append(new_row)
    return np.float32(new_image)

class SnakeEnv(gym.Env):

    def __init__(self):
        self.steps_beyond_done = None
        self.screen = None
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(0, 1, [1, 80, 80])

    def create_state(self):
        self.state = np.zeros((80,80), dtype=(np.float32))

        p0, p1 = self.pos[0]*8, self.pos[1]*8
        self.state[p0:p0+8, p1:p1+8] = np.rot90(head, self.direction)
        
        o = self.occupied
        for c, pos in enumerate(o[:-1]):
            p0, p1 = pos[0]*8, pos[1]*8
            if c == 0:
                if o[1][0] == pos[0]: self.state[p0:p0+8, p1:p1+8] = np.rot90(straight)
                else: self.state[p0:p0+8, p1:p1+8] = straight
            else:
                right, up, left, down = False, False, False, False
                if (o[c-1][0] > pos[0]) or (o[c+1][0] > pos[0]): down = True
                if (o[c-1][0] < pos[0]) or (o[c+1][0] < pos[0]): up = True
                if (o[c-1][1] > pos[1]) or (o[c+1][1] > pos[1]): right = True
                if (o[c-1][1] < pos[1]) or (o[c+1][1] < pos[1]): left = True
                if up and down: self.state[p0:p0+8, p1:p1+8] = straight
                elif left and right: self.state[p0:p0+8, p1:p1+8] = np.rot90(straight)
                elif left and down: self.state[p0:p0+8, p1:p1+8] = np.rot90(bend, 3)
                elif left and up: self.state[p0:p0+8, p1:p1+8] = np.rot90(bend, 2)
                elif right and down: self.state[p0:p0+8, p1:p1+8] = bend
                elif right and up: self.state[p0:p0+8, p1:p1+8] = np.rot90(bend, 1)

        for target in self.targets:
            self.state[target[0]*8:target[0]*8+8,target[1]*8:target[1]*8+8] = np.ones((8,8))
        
    def step(self, action):
        y, x = self.pos
        if action == 0: self.direction += 1
        elif action == 2: self.direction -= 1
        self.direction = self.direction % 4
        if self.direction == 0: y += 1
        elif self.direction == 1: x += 1
        elif self.direction == 2: y -= 1
        elif self.direction == 3: x -= 1
        self.pos = (y, x)

        if self.pos in self.targets:
            reward = 1.0
            self.occupied += [(self.pos[0], self.pos[1])]
            self.targets.remove(self.pos)
            
            if len(self.occupied) < 100:
                target = (np.random.randint(0,10), np.random.randint(0,10))
                while (target in self.occupied) or (target == self.pos) or (target in self.targets):
                    target = (np.random.randint(0,10), np.random.randint(0,10))
                self.targets.append(target)
        else:
            self.occupied = self.occupied[1:] + [(self.pos[0], self.pos[1])]
            reward = 0.0
            
        done =  (x < 0) or (x > 9) or (y < 0) or (y > 9) \
                or (self.pos in self.occupied[:-1]) or len(self.occupied) == 100
        done = bool(done)
        
        if not done:
            self.create_state()
        
        self.score += reward
        self.episode_nr += 1

        return (self.state.reshape(1,80,80), reward, done, {'ale.lives': 0})

    def reset(self):
        self.steps_beyond_done = None
        self.direction = 1
        self.score = 0
        self.episode_nr = 1
        self.pos = (np.random.randint(5,7), np.random.randint(5,7)) # [y][x] because idk
        self.occupied = [(self.pos[0], self.pos[1]+i) for i in range(-4, 0)]
        self.occupied += [(self.pos[0], self.pos[1])]
        self.targets = []
        for i in range(1):
            target = (np.random.randint(0,10), np.random.randint(0,10))
            while (target in self.occupied) or (target == self.pos) or (target in self.targets):
                target = (np.random.randint(0,10), np.random.randint(0,10))
            self.targets.append(target)
        self.create_state()
        return self.state.reshape(1,80,80)
    
    def seed(self, rank):
        np.random.seed(rank)

    def render(self, mode='human', close=False, probs=[0,0,0]):
        if mode == 'rgb_array':
            return self.last_image
        elif mode == 'human':
            import pygame
            if close:
                pygame.quit()
            else:
                if self.screen is None:
                    pygame.init()
                    self.screen = pygame.display.set_mode((800, 800))
                    self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
                img = pygame.surfarray.make_surface(transform(self.state,10).swapaxes(0, 1)*255)
                self.screen.blit(img, (0, 0))
                
                textsurface1 = self.myfont.render(str(self.score), False, (255,255,255))
                self.screen.blit(textsurface1, (10, 10))
                textsurface2 = self.myfont.render(str(self.episode_nr), False, (255,255,255))
                self.screen.blit(textsurface2, (10, 40))

                pygame.display.update()
