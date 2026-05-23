#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:44:15 2026

@author: asullivan
"""

from artificial_pulsar import artificial_pulsar
from space import space
from receiver import receiver
from parser import *
import os
from apta_baseline_engine import apta_baseline_engine
import numpy as np

class apta_engine(object):
    
    def __init__(self, P_pulse, x_satellite, x_receiver):
        # start by initializing the object variables
        self.params  = None
        self.N_artificial_pulsar= None
        self.satellite_error_list = None
        self.space_delay_list = None
        self.receiver_error_list = None
        self.h0 = None
        self.monochromatic = None
        self.f_GW  = None
        self.theta_src = None
        self.phi_src = None
        #------------------------------------------#

        
        
    def read_inputs(self, input_file):
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Parameter file {input_file} not found")
        else:
            params = parse_params(input_file)
        
        self.params = params
            
        self.N_artificial_pulsar = params["general"]["N"]
        
        self.satellite_error_list = params["general"]["satellite_error_list"]
        
        self.space_delay_list = params["general"]["space_delay_list"]
        
        self.receiver_error_list = params["general"]["receiver_error_list"]
        

        
        
        self.h0 = params["GW"]["h0"]
        
        self.monochromatic = params["GW"]["monochromatic"]
        
        self.f_GW = params["GW"]["f_GW"]
        
        self.theta_src = params["GW"]["theta_src"]
        
        self.phi_src = params["GW"]["phi_src"]

                                              
                                                
    def compue_allbaselines_deltat(self): 
        deltat_allbaselines = np.empty(self.N_artificial_pulsar)
        for n in range(0, self.N_artificial_pulsar):
            baseline_header = "baseline"+str(n+1)
            
            baseline_params = self.params[baseline_header]
            
            if baseline_params["readin_receiver_position_error"]:
                deltax_r1 = baseline_params["deltax_r1_fixed"]
                deltax_r2 = baseline_params["deltax_r2_fixed"] # read these from file only if readin receiver position error is turned on. This decides whether we will have a fixed error in the receiver position or whether it will be randomly generated for each baseline in the space module
            else:
                deltax_r1=0.0
                deltax_r2=0.0
            
            baseline_deltat = self.compute_baseline_deltat(baseline_params["P_pulse"], baseline_params["x_satellite"], baseline_params["x_receiver"], xi=baseline_params["xi"], deltax_s_sigma=baseline_params["deltax_s_sigma"], deltax_r_sigma=baseline_params["deltax_r_sigma"], manual=baseline_params["readin_receiver_error"], fixed_deltax_r1=deltax_r1, fixed_deltax_r2=deltax_r2)                             
            
            deltat_allbaselines[n] = baseline_deltat
        return deltat_allbaselines
    
        
    def compute_baseline_deltat(self, P_pulse, x_satellite, x_receiver, xi=0.0, deltax_s_sigma=0.0, deltax_r_sigma=0.0,  manual=False, fixed_deltax_r1=0.0, fixed_deltax_r2=0.0):
        
        baseline = apta_baseline_engine(P_pulse, x_satellite, x_receiver)
        
        baseline.init_baseline(xi=xi, satellite_error_list=self.satellite_error_list,  h0=self.h0, f_GW=self.f_GW, theta_src=self.theta_src, phi_src=self.phi_src, deltax_s_sigma=deltax_s_sigma, deltax_r_sigma=deltax_r_sigma, monochromatic = self.monochromatic, delay_list=self.space_delay_list, manual=manual, fixed_deltax_r1=fixed_deltax_r1, fixed_deltax_r2=fixed_deltax_r2, receiver_error_list=self.receiver_error_list)
        
        deltat = baseline.run_baseline()  
        
        return deltat
        
       
        