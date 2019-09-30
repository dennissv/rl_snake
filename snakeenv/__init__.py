#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:25:45 2018

@author: dennis
"""

from gym.envs.registration import register

register(
    id='SnakeEnv-v0',
    entry_point='snakeenv.snakeenv:SnakeEnv',
)

register(
    id='SnakeEnvSimple-v0',
    entry_point='snakeenv.snakeenvsimple:SnakeEnvSimple',
)

register(
    id='SnakeMover-v0',
    entry_point='snakeenv.snakemover:SnakeMover',
)

register(
    id='SnakeDQN-v0',
    entry_point='snakeenv.dqnsnake:SnakeDQNEnv',
)
