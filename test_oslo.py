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
        self.assertTrue(not self.model8.state.any())
        
    def test_drive(self):
        self.model3.drive()
        self.assertTrue(np.allclose([self.model3.state],[1.0,0.0,0.0]))
        
    def test_relax_site_left(self):
        model = oslo.Oslo(3)
        model.state = np.array([1,1,1])
        model.thresholds = np.array([1,1,1])
        model.drive()
        model.relax_site(0)
        self.assertTrue(np.allclose(model.state,np.array([0, 2, 1])))
    def test_relax_site_right(self):
        model = oslo.Oslo(3)
        model.state = np.array([1,1,2])
        model.thresholds = np.array([1,1,1])
        model.relax_site(2)
        self.assertTrue(np.allclose(model.state,np.array([1, 2, 1])))
        
    def test_relax_site_bulk(self):
        model = oslo.Oslo(3)
        model.state = np.array([1,2,1])
        model.thresholds = np.array([1,1,1])
        model.relax_site(1)
        self.assertTrue(np.allclose(model.state,np.array([2, 0, 2])))
        
if __name__ == '__main__':
    unittest.main()