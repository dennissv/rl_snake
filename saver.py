#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 22:43:04 2018

@author: dennis
"""

import time
import subprocess

c = 1
while True:
    bashCommand = 'aws s3 cp trained_models/snake.dat s3://sds-ec2-container/snake_'+str(c)+'.dat'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    bashCommand = 'aws s3 cp logs/snake_log s3://sds-ec2-container/snake_log_'+str(c)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print('Saved file nr ' + str(c))
    time.sleep(600)
    c += 1