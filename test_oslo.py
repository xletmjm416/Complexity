# -*- coding: utf-8 -*-
"""
Testing for the Oslo model

@author: mjm416
@ date 16.01.19
"""

import unittest
import numpy as np
import oslo

class TestOslo(unittest.TestCase):
    def setUp(self):
        self.model3 = oslo.Oslo(3)
        self.model8 = oslo.Oslo(8)
    
    def test_init(self):
        """All states are 0 at init. """
        self.assertTrue(not self.model8.state.any())
        
    def test_drive(self):
        """Make sure drive works as expected. """
        self.model3.drive()
        self.assertTrue(np.allclose([self.model3.state],[1.0,0.0,0.0]))
        
    def test_relax_site_left(self):
        """Check relaxing edge site on the left hand side where grains enter
        the system. """
        self.model3.state = np.array([1,1,1])
        self.model3.thresholds = np.array([1,1,1])
        self.model3.drive()
        self.model3.relax_site(0)
        self.assertTrue(np.allclose(self.model3.state,np.array( [0, 2, 1])))
    
    def test_relax_site_right(self):
        """Check relaxing edge site from which the grains leave the system. """
        self.model3.state = np.array([1,1,2])
        self.model3.thresholds = np.array([1,1,1])
        self.model3.relax_site(2)
        self.assertTrue(np.allclose(self.model3.state,np.array([1, 2, 1])))
    
    def test_relax_site_bulk(self):
        """Relaxing sites in the bulk of the system, far from any edges. """
        self.model3.state = np.array([1,2,1])
        self.model3.thresholds = np.array([1,1,1])
        self.model3.relax_site(1)
        self.assertTrue(np.allclose(self.model3.state,np.array([2, 0, 2])))
    
    def test_heights_arr(self):
        """The heights are correct with a hand-calculated example"""
        self.model8.state = np.array([2,1,2,0,0,1,0,2])
        self.assertTrue(np.allclose(self.model8.heights_arr(),np.array([8,6,5,3,3,3,2,2])))
        
if __name__ == '__main__':
    unittest.main()