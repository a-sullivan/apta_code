#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:44:15 2026

@author: asullivan
"""

from artificial_pulsar import artificial_pulsar
from space import space
from receiver import receiver


class apta_baseline_engine(object):
    
    def __init__(self, P_pulse, x_satellite, x_receiver):
        # start by initializing the object variables
        self.artificial_pulsar = None
        self.space = None
        self.receiver = None
        self.P_pulse = None
        self.x_satellite = None
        self.x_receiver = None
        #------------------------------------------#
        
        self.P_pulse = P_pulse # period of the pulse of the artificial pulsar
        
        self.x_satellite=x_satellite # position of the satellite
        
        self.x_receiver = x_receiver # position of the receiver
        
        
        
        
    def init_satellite(self, xi=0.0, satellite_error_list=[1]):
        
        self.artificial_pulsar = artificial_pulsar(xi, self.P_pulse, error_list=satellite_error_list)
        
    
    
    def init_space(self, h0=0.0, f_GW=10, theta_src=0.0, phi_src=0.0, deltax_s_sigma=0.0, deltax_r_sigma=0.0, monochromatic = True, delay_list=[1,1], manual=False, fixed_deltax_r1=0.0, fixed_deltax_r2=0.0): 
        self.space = space(self.x_satellite, self.x_receiver,  h0, f_GW, theta_src, phi_src, self.P_pulse, deltax_s_sigma = deltax_s_sigma, deltax_r_sigma=deltax_r_sigma, monochromatic=monochromatic, delay_list=delay_list)
        
        self.space.readin_receiver_position(read_in=manual, deltax_r1=fixed_deltax_r1, deltax_r2=fixed_deltax_r2)
        
   
    def init_receiver(self, receiver_error_list=[0]):
        
        self.reveiver = receiver(error_list=receiver_error_list)
        
        
        
    def init_baseline(self, xi=0.0, satellite_error_list=[1],  h0=0.0, f_GW=10, theta_src=0.0, phi_src=0.0, deltax_s_sigma=0.0, deltax_r_sigma=0.0, monochromatic = True, delay_list=[1,1], manual=False, fixed_deltax_r1=0.0, fixed_deltax_r2=0.0, receiver_error_list=[0]):    
        
        self.init_receiver(xi=xi, satellite_error_list=satellite_error_list)
        
        self.init_space(h0=h0, f_GW = f_GW, theta_src = theta_src, phi_src = phi_src, deltax_s_sigma=deltax_s_sigma, deltax_r_sigma=deltax_r_sigma, monochromatic = monochromatic, delay_list=delay_list, manual=manual, fixed_deltax_r1=fixed_deltax_r1, fixed_deltax_r2=fixed_deltax_r2)
        
        self.init_receiver(receiver_error_list=receiver_error_list)
        
    def run_baseline(self):
        
        deltat_satellite = self.artificial_pulsar.emit()

        deltat_space = self.space.propagate()
        
        deltat_receiver = self.receiver.readout()
        
        deltat_baseline = deltat_satellite + deltat_space + deltat_receiver
        
        return deltat_baseline
        
        
        