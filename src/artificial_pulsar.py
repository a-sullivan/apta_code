#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:55:20 2026

@author: asullivan
"""

import numpy as np

class artificial_pulsar(object):
    
    def __init__(self, xi, P, error_list=[1]):
        
        xi_clock= xi /np.sqrt(P) # xi (average timing error for 1 s) averaged to pulse period which could be smaller
        
        P_pulse = P # pulse period
        
        clock_error_include = error_list[0]
        
    def emit(self):
        
        deltat=0
        if clock_error_include:
            deltat += self.clock_error()
        
        t_emit = deltat
        
        return t_emit
    
    def clock_error(self):
        return np.random.random(std=xi_clock)*P_pulse
    
    
    
        
        