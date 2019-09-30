#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:21:02 2018

@author: dennis
"""

from matplotlib import pyplot as plt
import numpy as np

data = []
with open('logs/snake_log_221', 'r') as f:
    for line in f.readlines()[20:]:
        data.append(float(line.split(' ')[9].strip(',')))
        
steps = 100
means = [np.mean(data[i:i+steps]) for i in range(len(data)-steps)]
plt.plot(means)