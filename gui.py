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
        
        self.modelframe = ModelFrame(self)
        self.modelframe.pack(side="top")
        
        #self.refresh = tk.Button(self, text="Refresh", command=self.plotframe.refreshFigure)
        #self.refresh.pack(side="bottom")
        
        self.drive = tk.Button(self, text="Drive", command=self.modelframe.drive)
        self.drive.pack(side="bottom")
        
        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        self.pack()

class ModelFrame(tk.Frame):
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
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()