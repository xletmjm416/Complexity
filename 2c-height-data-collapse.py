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

## L = 16
L_size = np.array([8,16,32,64,128,256])
T_total = np.array((1000*(L_size/16)**2)).astype(int)

filenames = ["./data/" + str(L) + "-" + str(T) + ".dat" for L, T in zip(L_size, T_total)]

data = []
for L in L_size:
    data.append({"avalanche_size_arr":[],
                 "height_time_arr":[],
                 "crossing_time":[],
                 "twos_arr":[],
                 "ones_arr":[],
                 "zeros_arr":[],
                 "time":[]
                 })

for filename, i in zip(filenames, range(len(L_size))):
    with open(filename, 'rb') as file:
        data[i]["avalanche_size_arr"], data[i]["height_time_arr"],  \
        data[i]["crossing_time"], data[i]["twos_arr"], data[i]["ones_arr"],  \
        data[i]["zeros_arr"] = pickle.load(file)
        data[i]["time"] = np.arange(T_total[i])


fig, axes = plt.subplots(nrows=1, ncols=1)
ax1 = axes

for i in range(len(L_size)):
    lab = "L="+str(L_size[i])
    ax1.plot(data[i]["time"]/(L_size[i]**2),data[i]["height_time_arr"]/L_size[i], linewidth="1.0", label=lab)
    ax1.vlines(data[i]["crossing_time"], 0, 100, colors='darkred', linestyle='dashed')
    ax1.set_xlim([0, 2])
    print(data[i]["crossing_time"]/(L_size[i]**2))
ax1.set_xlabel("number of grains added")
ax1.set_ylabel("height of the pile")
ax1.grid()
ax1.set_ylim([0, 2])

plt.legend(loc='lower right')
fig.tight_layout()