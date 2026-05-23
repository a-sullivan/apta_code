#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:55:20 2026

@author: asullivan
"""

import numpy as np

class artificial_pulsar(object):
    
    def __init__(self, xi, P, error_list=[1]):
        # start by initializing the object variables
        self.xi_clock = None
        self.P_pulse = None
        self.clock_error_include = None
        #---------------------------------------#
        
        # Now actually give them their values
        self.xi_clock= xi /np.sqrt(P) # xi (average timing error for 1 s) averaged to pulse period which could be smaller
        
        self.P_pulse = P # pulse period
        
        self.clock_error_include = error_list[0]
        
    def emit(self):
        
        deltat=0
        if self.clock_error_include:
            deltat += self.clock_error() # for first pulse emitted
            deltat += self.clock_error() # for second pulse emitted
        
        deltat_emit = deltat
        
        return deltat_emit
    
    def clock_error(self):
        return np.random.random(std=self.xi_clock)*self.P_pulse
    
    
    
        
        