# -*- coding: utf-8 -*-
"""
Implementation of the Oslo model.

@author mjm416
@date 16.01.19
"""

import numpy as np
from matplotlib import pyplot as plt
import pickle
import os

class Oslo:
    """Oslo model class, implementing four states of the algorithm
    and collecting data.
    """
    
    def __init__(self, L_size):
        self.L_size = L_size
        self.state = np.zeros(L_size,dtype='uint') # state is array of slopes
        self.thresholds = np.random.randint(1, 3, size=L_size) # random slopes
        self.total_height = 0 # height of the pile
        self.overflow = False # flag whether the system is saturated
    
    def drive(self):
        """Drive the system at the left boundary"""
        self.state[0] = self.state[0] + 1
        self.total_height += 1
    
    def relax_site(self, site):
        """Relax site labelled as (integer) 0 <= 'site' < L_size. Returns True
        if a relaxation was needed once it completes, False if it was not
        required."""
        if self.state[site] <= self.thresholds[site]:
            return False # already stable
        
        if site == 0: # left boundary
            # not updating to the left
            self.state[site] = self.state[site] - 2
            self.state[site+1] = self.state[site+1] + 1
            self.total_height -= 1
        if site > 0 and site < self.L_size-1: #bulk site
            self.state[site-1] = self.state[site-1] + 1
            self.state[site] = self.state[site] - 2
            self.state[site+1] = self.state[site+1] + 1
        if site == self.L_size-1: #right site site
            self.state[site-1] = self.state[site-1] + 1
            self.state[site] = self.state[site] - 1 # different here
            self.overflow = True # set the overflow flag that we reached the right site
            # no right site to the rightmost
            
        # choose new threshold for relaxed site
        self.thresholds[site] = np.random.randint(1, 3) # uniform for now
        
        return True # relaxed that site
    
    def relax_system(self):
        """Relax the whole system; this is a function that hides the relaxation 
        implementation under the hood"""
        return self._relax_recursively(0)
    
    def _relax_recursively(self, start_site):
        """Recursive relaxation: if a site relaxes, it relaxes the 
        neighbouring sites in the same manner. Counts up number of 
        relaxations too. It is the simplest guarantee to make fewer scans 
        than a sweep, because it relaxes all sites that need it and checks 
        all the ones that could be relaxed but did not, covering all 
        possibilities without excessive checks."""
        relaxations = 0
        if self.relax_site(start_site):
            relaxations = 1
            if start_site > 0:
                relaxations = relaxations + self._relax_recursively(start_site - 1)
            if start_site < self.L_size-1:
                relaxations = relaxations + self._relax_recursively(start_site + 1)    
        return relaxations
    
    def height(self, site):
        """Returns height of a site. For zero site, we track it with total_heigth
        variable"""
        if site == 0:
            return self.total_height
        else:
            return np.sum(self.state[site:])
    
    def heights_arr(self):
        """Return array of heights"""
        return np.array([self.height(site) for site in range(self.L_size)])
    
    def __next__(self):
        """Make an iteration of Olso model algorithm"""
        self.drive()
        return self.relax_system()
    
    def __str__(self):
        return str(self.state)
    
    def __iter__(self):
        return self
    
if __name__ == "__main__":
    L_size = 32
    model = Oslo(L_size)
    T_total = 2000
    iterator = iter(model)
    avalanche_size_arr = list()
    height_time_arr = list()
    overflow_reached = 0
    for i in range(T_total):
        avalanche_size = next(iterator)
        avalanche_size_arr.append(avalanche_size)
        height_time_arr.append(iterator.height(0))
        if iterator.overflow and overflow_reached == 0:
            overflow_reached = i
    
    filename = "./data/" + str(L_size) + "-" + str(T_total) + ".dat"
    if os.path.exists(filename):
        if input("file with the name exists; overwrite? y/n").lower() == 'y':
            with open(filename, 'wb+') as file:
                pickle.dump([avalanche_size_arr, height_time_arr, overflow_reached], file)            
    else:
        with open(filename, 'wb+') as file:
            pickle.dump([avalanche_size_arr, height_time_arr, overflow_reached], file)
    