# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 19:55:23 2019

@author: mjm416
"""

import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.style.use("plotstyle.mplstyle")
fig, axes = plt.subplots(nrows=1, ncols=1)
ax1 = axes

## L = 16
L_size = 16
T_total = 2000
crit_height = 26.5
filename = "./data/" + str(L_size) + "-" + str(T_total) + ".dat"

with open(filename, 'rb') as file:
    avalanche_size_arr, height_time_arr, overflow_reached = pickle.load(file)
    
ax1.plot(height_time_arr, 'r-', label="L=16")
ax1.hlines(crit_height, 0, T_total, colors='darkred', linestyle='dashed')
ax1.vlines(overflow_reached, 0, 100, colors='darkred', linestyle='dashed')
ax1.set_xlabel("number of grains added")
ax1.set_ylabel("height of the pile")
ax1.grid()
ax1.set_xlim([0, T_total])
ax1.set_ylim([0, 1.1*crit_height])

## L = 32
L_size = 32
T_total = 2000
crit_height = 53.9
filename = "./data/" + str(L_size) + "-" + str(T_total) + ".dat"

with open(filename, 'rb') as file:
    avalanche_size_arr, height_time_arr, overflow_reached = pickle.load(file)
    
ax1.plot(height_time_arr, 'b-', label="L=32")
ax1.hlines(crit_height, 0, T_total, colors='darkblue', linestyle='dashed')
ax1.vlines(overflow_reached, 0, 100, colors='darkblue', linestyle='dashed')
ax1.set_xlabel("number of grains added")
ax1.set_ylabel("height of the pile")
ax1.grid()
ax1.set_xlim([0, T_total])
ax1.set_ylim([0, 1.1*crit_height])
ax1.grid()
plt.legend(loc='lower right')
fig.tight_layout()