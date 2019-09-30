#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 03:17:37 2018

@author: dennis
"""

import numpy as np

def create_head():
    img = np.ones((8,8))*.66
    for i in range(8):
        for j in range(8):
            if ((j == 3) or (j == 4)) and (i > 2):
                img[i][j] = 0.5
    for i in range(8):
        for j in range(8):
            if ((1 <= j <= 2) or (5 <= j <= 6)) and (i == 1):
                img[i][j] = 0.5
    return img

def create_straight():
    img = np.ones((8,8))*.33
    for i in range(8):
        for j in range(8):
            if 3 <= j <= 4:
                img[i][j] = 0.18
    return img

def create_bend():
    img = np.ones((8,8))*.33
    for i in range(8):
        for j in range(8):
            if (3 <= j <= 4) and (i >= 3):
                img[i][j] = 0.18
            if (3 <= i <= 4) and (j >= 3):
                img[i][j] = 0.18
    return img

np.save('head.npy', create_head())
np.save('straight.npy', create_straight())
np.save('bend.npy', create_bend())