# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:15:27 2019

@author: mjm416
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import oslo

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.modelframe = ModelFrame(self)
        self.modelframe.pack(side="top")
        
        self.drive = tk.Button(self, text="Drive", command=self.drive_event)
        self.drive.pack(side="bottom")
        
        self.grains_count = tk.IntVar()
        self.grains_count_display = tk.Entry(self, textvariable=self.grains_count)
        self.grains_count_display.pack(side="top")
        
        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        self.pack()
    
    def drive_event(self):
        self.modelframe.drive()
        self.grains_count.set(self.grains_count.get() + 1)
        return

class ModelFrame(tk.Frame):
    def __init__(self, master=None, L_size=8, mode="heights"):
        """mode = {heights, slopes}"""
        super().__init__(master)
        self.model = oslo.Oslo(L_size)
        self.mode = mode
        
        #plotting facilities
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.subplot = self.fig.add_subplot(111)
        self.contents, = self.subplot.plot(range(self.model.L_size), \
                                           np.zeros(self.model.L_size))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
    def drive(self):
        x = range(self.model.L_size)
        if self.mode == "heights":
            y = self.model.heights_arr()
        elif self.mode == "slopes":
            y = self.model.state
        else:
            raise Exception("inappropriate visualisation mode; only 'heights' \
                            or 'slopes' are allowed")
        print(next(self.model))
        self.contents.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(0, self.model.L_size)
        ax.set_ylim(0, max(y))
        self.canvas.draw()
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()