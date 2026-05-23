#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 07:22:23 2026

@author: asullivan
"""

import numpy as np
import scipy 
from scipy import quad

class receiver(object):
    def __init__(self, error_list=[0]):
        # start by initializing the object variables
        self.include_read_arrival_error = None
        #---------------------------------------#
        
        self.include_read_arrival_error = error_list[0] # error in reading the arrival time of pulse by receiver
        
    def readout(self): 
        # function which calculates error introduced by receiving the pulses at the end of one baseline
        deltat=0.0
        if self.include_read_arrival_error:
            deltat += self.read_arrival_error() 
            
        deltat_receiver = deltat
        return deltat_receiver
    
    def read_arrival_error(self):
        # function which specifically computes error from misreading the arrival times
        return 0.0 # currently 0 because we have not implemented yet 