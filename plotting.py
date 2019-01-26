# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 19:55:23 2019

@author: mjm416
"""

import pickle
import numpy as np
from matplotlib import pyplot as plt

L_size = 32
T_total = 2000
filename = "./data/" + str(L_size) + "-" + str(T_total) + ".dat"

with open(filename, 'rb') as file:
    avalanche_size_arr, height_time_arr, overflow_reached = pickle.load(file)
    
histogram = np.histogram(avalanche_size_arr, bins = range(0,max(avalanche_size_arr)))
avalanche_size_bins = histogram[1][:-1]
avalanche_size_histogram = histogram[0]
fig, axes = plt.subplots(nrows=2, ncols=1)
ax1, ax2 = axes

ax1.loglog(avalanche_size_bins, avalanche_size_histogram, '.')
ax1.set_xlabel("avalanche size s")
ax1.set_ylabel("frequency")

crit = 53.9
ax2.plot(height_time_arr)
ax2.hlines(crit, 0, T_total)
ax2.vlines(overflow_reached, 0, 100)
ax2.set_xlabel("number of grains added")
ax2.set_ylabel("height of the pile")
ax2.grid()
ax2.set_xlim([0, T_total])
ax2.set_ylim([0, 1.1*crit])

fig.tight_layout()