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
        """Called every time before all tests"""
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
        self.model8.state = np.array([2,1,2,0,0,1,0,2]) # slopes
        self.model8.total_height = 8 # this is tracked in a different way than bulk
        self.assertTrue(np.allclose(self.model8.heights_arr(),np.array([8,6,5,3,3,3,2,2])))
    
    def test_heights_from_script_L16(self):
        """According to the script, in the long term, the average height of the
        pile for system of size L=16 should be about 26.5"""
        avg = self.height_testing_meta(16, test_time=3000)
        self.assertTrue(np.abs(avg - 26.5) < 1)
        
    def test_heights_from_script_L32(self):
        """According to the script, in the long term, the average height of the
        pile for system of size L=32 should be about 53.9"""
        avg = self.height_testing_meta(32, test_time=3000)
        self.assertTrue(np.abs(avg - 53.9) < 1)
    
    def height_testing_meta(self, L_size, test_time=5000):
        """According to the script, in the long term, the average height of the
        pile for system of size L=16 should be about 26.5, whereas for L=32, 
        it should be 53.9.
        'test_time' specifies how many time units the model should run for."""
        if test_time < 2000:
            raise Exception("Too short test time. \
                            I suggest test_time > 3000 for small systems.")
        model = iter(oslo.Oslo(L_size))
        height_time_arr = list()
        for i in range(test_time):
            next(model)
            height_time_arr.append(model.height(0))
        mean1 = np.mean(height_time_arr[-2000:-1000])
        mean2 = np.mean(height_time_arr[-1000:])
        if np.abs(mean1 - mean2) < 0.05* mean1 \
        and np.abs(mean1 - mean2) < 0.05*mean2:
            # difference is smaller than 5% of either; converged
            print("height test converged with height", mean2)
            return mean2
if __name__ == '__main__':
    unittest.main()