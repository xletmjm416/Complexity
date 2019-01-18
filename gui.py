# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:15:27 2019

@author: mjm416
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.plotframe = PlotFrame(self)
        self.plotframe.pack(side="top")
        
        self.refresh = tk.Button(self, text="Refresh", command=self.plotframe.refreshFigure)
        self.refresh.pack()
        
        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.pack()
        
        self.pack()

class PlotFrame(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.subplot = self.fig.add_subplot(111)
        self.contents, = self.subplot.plot([1,2,3,4,5], [1,2,3,2,1])
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.pack()
        
    def refreshFigure(self):
        x = [1,2,3,4,5,6]
        y = [1,4,3,2,1,7]
        self.contents.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))        
        self.canvas.draw()

root = tk.Tk()
app = Application(master=root)
app.mainloop()