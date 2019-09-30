#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:30:26 2018

@author: dennis
"""

import gym
import pygame
import snakeenv
import numpy as np
env = gym.make('SnakeEnvSimple-v0')

pygame.init()
w = 160
h = 210
size=(h,w)
screen = pygame.display.set_mode(size) 
c = pygame.time.Clock() # create a clock object for timing

observations = []
for i_episode in range(20):
    observation = env.reset()
    for t in range(1000):
#        surf = pygame.surfarray.make_surface(observation)
#        screen.blit(surf,(0,0))
#        pygame.display.flip()
#        c.tick(5)
        env.render('human')
        observations.append(observation)
        observation, reward, done, info = env.step(np.random.randint(0,3))
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
        
env.render('human', True)