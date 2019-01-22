# -*- coding: utf-8 -*-
"""
Implementation of the Oslo model.

@author mjm416
@date 16.01.19
"""

import numpy as np
from matplotlib import pyplot as plt

class Oslo:
    """Oslo model class, implementing four states of the algorithm
    and collecting data.
    """
    
    def __init__(self, L_size):
        self.state = np.zeros(L_size,dtype='uint') # state is array of slopes
        self.thresholds = np.random.randint(1, 3, size=L_size) # random slopes0
    
    def drive(self):
        """Drive the system at the left boundary"""
        self.state[0] = self.state[0] + 1
    
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
        if site > 0 and site < len(self.state)-1: #bulk site
            self.state[site-1] = self.state[site-1] + 1
            self.state[site] = self.state[site] - 2
            self.state[site+1] = self.state[site+1] + 1
        if site == len(self.state)-1: #right site site
            self.state[site-1] = self.state[site-1] + 1
            self.state[site] = self.state[site] - 1 # different here
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
            if start_site < len(self.state)-1:
                relaxations = relaxations + self._relax_recursively(start_site + 1)    
        return relaxations
    
    def height(self, site):
        """Returns height of a site"""
        return np.sum(self.state[site:])
    
    def heights_arr(self):
        """Return array of heights"""
        return np.array([self.height(site) for site in range(len(self.state))])
    
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
    T_total = 5000
    iterator = iter(model)
    avalanche_size_arr = list()
    height_time = list()
    for i in range(T_total):
        avalanche_size = next(iterator)
        avalanche_size_arr.append(avalanche_size)
        height_time.append(iterator.height(0))
        
    histogram = np.histogram(avalanche_size_arr, bins = range(0,max(avalanche_size_arr)))
    avalanche_size_bins = histogram[1][:-1]
    avalanche_size_histogram = histogram[0]
    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax1, ax2 = axes
    
    ax1.loglog(avalanche_size_bins, avalanche_size_histogram, '.')
    ax1.set_xlabel("avalanche size s")
    ax1.set_ylabel("frequency")
    
    ax2.plot(height_time)
    ax2.hlines(53.9,0,T_total)
    ax2.set_xlabel("number of grains added")
    ax2.set_ylabel("height of the pile")
    
    fig.tight_layout()