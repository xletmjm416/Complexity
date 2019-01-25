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
        #self.plotframe = PlotFrame(self)
        #self.plotframe.pack(side="top")
        
        self.modelframe = ModelFrameHeights(self)
        self.modelframe.pack(side="top")
        
        #self.refresh = tk.Button(self, text="Refresh", command=self.plotframe.refreshFigure)
        #self.refresh.pack(side="bottom")
        
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

class ModelFrameSlopes(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        L_size = 8
        self.model = oslo.Oslo(L_size)
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.subplot = self.fig.add_subplot(111)
        self.contents, = self.subplot.plot(range(len(self.model.state)), self.model.state)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.pack()
        
    def drive(self):
        x = range(len(self.model.state))
        y = self.model.state
        next(self.model)
        self.contents.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(0, len(self.model.state))
        ax.set_ylim(0, max(y))
        self.canvas.draw()
        
class ModelFrameHeights(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        L_size = 8
        self.model = oslo.Oslo(L_size)
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.subplot = self.fig.add_subplot(111)
        self.contents, = self.subplot.plot(range(len(self.model.state)), self.model.heights_arr())
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.pack()
        
    def drive(self):
        x = range(len(self.model.state))
        y = self.model.heights_arr()
        print(next(self.model))
        self.contents.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(0, len(self.model.state))
        ax.set_ylim(0, max(y))
        self.canvas.draw()
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()