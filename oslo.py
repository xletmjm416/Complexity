# -*- coding: utf-8 -*-
"""
Implementation of the Oslo model.

@author mjm416
@date 16.01.19
"""

import numpy as np

class Oslo:
    """Oslo model class, implementing four states of the algorithm
    and collecting data.
    """
    
    def __init__(self, L_size):
        self.state = np.zeros(L_size,dtype='uint') # state is array of slopes
        self.thresholds = np.random.randint(1, 3, size=L_size) # random slopes
        self.counter = 0
    
    def drive(self):
        """Drive the system at the left boundary"""
        self.state[0] = self.state[0] + 1
    
    def relax_site(self, site):
        """Relax site labelled as (integer) 0 <= 'site' < L_size"""
        if self.state[site] <= self.thresholds[site]:
            print("no relaxation")
            return False # already stable
        
        print("relaxing " + str(site))
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
    
    def __iter__(self):
        return self
    
    def relax_recursively(self, start_site):
        relaxations = 0
        if self.relax_site(start_site):
            relaxations = 1
            if start_site > 0:
                relaxations = relaxations + self.relax_recursively(start_site - 1)
            if start_site < len(self.state)-1:
                relaxations = relaxations + self.relax_recursively(start_site + 1)    
        return relaxations
    
    def __next__(self):
        self.drive()
        print(self.relax_recursively(0))
    
    def __str__(self):
        return str(self.state)
    
if __name__ == "__main__":
    #tests
    model = Oslo(8)
    iterator = iter(model)
    for i in range(200):
        next(iterator)
        print("---------------------stable------------------------")
    