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

if __name__ == '__main__':
    unittest.main()