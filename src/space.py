#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:30:00 2026

@author: asullivan
"""

import numpy as np
import scipy 
from scipy import quad

class space(object): 
    
    def __init__(self, x_satellite, x_receiver,  h0, f_GW, theta_src, phi_src, P, deltax_s_sigma =0.0, deltax_r_sigma=0.0, monochromatic=True, delay_list=[1,1]):
        
        # Start by initializing all the object variables
        self.h0 =None # amplitude of GW strain
        
        self.f_GW = None # gravitational wave frequency in Hz
        self.omega_GW = None # gravitational wave angular frequency
        
        self.monochromatic = None # if gravutational wave is monochromatic plane wave, set True
        
        self.x_satellite = None # position in 3D space of satellite
        
        self.x_receiver = None # position in 3D space of receiving station
        
        self.baseline = None # computes the baseline from satellite to receiever
        
        self.baseline_norm = None # norm of baseline (length)
        
        self.baseline_unit = None
        
        self.n_vec = None # propagation vector of gravitational wave
        
        self.deltax_s_sigma = None # this is standard deviation of the position error of the satellite
        
        self.deltax_r_sigma = None # this is the standard deviation of the position error of the receiver
        
        self. P_pulse = None # period of artificial pulsar pulse
        
        self.include_GW = None
        
        self.include_position_error = None
        # ---------------------------------------------------------#
        
        # now actually set the valyes of all the variables
        self.h0 =h0 # amplitude of GW strain
        
        self.f_GW = f_GW # gravitational wave frequency in Hz
        self.omega_GW = 2.*np.pi*f_GW # gravitational wave angular frequency
        
        self.monochromatic = monochromatic # if gravutational wave is monochromatic plane wave, set True
        
        self.x_satellite = x_satellite # position in 3D space of satellite
        
        self.x_receiver = x_receiver # position in 3D space of receiving station
        
        self.baseline = self.x_receiver - self.satellite # computes the baseline from satellite to receiever
        
        self.baseline_norm = np.sqrt(np.sum(self.baseline**2)) # norm of baseline (length)
        
        self.baseline_unit = self.baseline/self.baseline_norm
        
        self.n_vec = np.array([np.sin(theta_src)*np.cos(phi_src), np.sin(theta_src)*np.sin(phi_src), np.cos(theta_src)]) # propagation vector of gravitational wave
        
        self.deltax_s_sigma = deltax_s_sigma # this is standard deviation of the position error of the satellite
        
        self.deltax_r_sigma = deltax_r_sigma # this is the standard deviation of the position error of the receiver
        
        self. P_pulse = P # period of artificial pulsar pulse
        
        self.include_GW = delay_list[0] 
        
        self.include_position_error = delay_list[1]
        
    
    def propagate(self):
        # computes total time delay
        deltat = 0.0
        deltax_s1=0.0
        deltax_s2=0.0
        deltax_r1=0.0
        deltax_r2=0.0
        if self.include_position_error:
            
            if self.manual is None:
                self.readin_receiver_position()
                
            
            deltax_s1, deltax_s2, deltax_s, deltax_r1, deltax_r2, deltax_r, deltax_s =  self.compute_distance_error( self.manual, fixed_deltax_r1=self.fixed_deltax_r1, fixed_deltax_r2=self.fixed_deltax_r2)
            
            deltat += deltax_r
            deltat += deltax_s

        if self.include_GW:
            deltat_GW = self.propagate_GW(deltax_s1, deltax_s2, deltax_r1, deltax_r2)
            deltat += deltat_GW
        
        deltat_space = deltat
        
        return deltat_space
        
        
    def readin_receiver_position(self, read_in = False, deltax_r1=0.0, deltax_r2=0.0):
        # reads in position of the receiver, assuming that is set external to this space module
        
        self.manual = None
        self.fixed_deltax_r1= None
        self.fixed_deltax_r2 =None
        self.manual = read_in
        
        self.fixed_deltax_r1 = deltax_r1
        
        self.fixed_deltax_r2 = deltax_r2
    
    
    
    def compute_distance_error(self, manual, fixed_deltax_r1=0.0, fixed_deltax_r2=0.0):
        #calculate uncertainty in the satellite position
        deltax_s1 = self.satellite_position_error()
        deltax_s2 = self.satellite_position_error()
        
        deltax_s = deltax_s2-deltax_s1
        
        # calculate contribution from uncertainty in receiver position
        deltax_r1 = self.receiver_position_error(manual, fixed_deltax_r1)
        deltax_r2 = self.receiver_position_error(manual, fixed_deltax_r2)
        
        deltax_r=deltax_r2-deltax_r1
        
        return deltax_s1, deltax_s2, deltax_s, deltax_r1, deltax_r2, deltax_r, deltax_s
    
     
    
    
    
    
    def propagate_GW(self, deltax_s1, deltax_s2, deltax_r1, deltax_r2):
        # propagates the timing residual from the GW alone given small deviations in satellite position and receiver position at pulse 1 and pulse 2 emission and arrival times
        
        
        # the time of a pulse being detected at the receiving station
        t_o_1 = self.baseline_norm+deltax_s1+deltax_r1
        t_o_2 = self.baseline_norm+deltax_s2+deltax_r2
        
        def proj_h1(t):
            
            return self.h_projected(t, t_o_1)
        
        def proj_h2(t):
            
            
            return self.h_projected(t, t_o_2+self.P_pulse)
        
        h1_int = quad(proj_h1, 0, t_o_1)
        h2_int = quad(proj_h2, 0, t_o_2)
        
        return 0.5*(h2_int-h1_int)*self.h0
            
            
            
            
    def h_projected(self, t, t_o):
        x_t=(t_o-t)*self.baseline_unit+self.x_receiver
        
        h_ij=np.zeros(3, 3)
        
        if self.monochromatic:
            h_ij = self.h_ij_plus_monochromatic(t,  x_t)
        
        h = np.dot( self.baseline_unit, np.einsum("i,ij->j", self.baseline_unit , h_ij)) 
        
        return h
        
        
        
    
    def satellite_position_error(self):
        return np.random.random(std=self.deltax_s_sigma)
    
    
        
    def receiver_position_error(self, manual=False, fixed_deltax_r=0.0):
        #activate manual if we want to override the random draw of a deltax_r and set fixed_deltax_r  (which might be a global receiver error across many baselines, drawn earlier)
        if manual:
            return fixed_deltax_r
        else:
            return np.random.random(std=self.deltax_r_sigma)

    
    def h_ij_plus_monochromatic(self, t, x ): # gravitational wave of monchromatic plane wave
        # x is the three vector postion
        
        R = transformation_matrix(self.theta_src, self.phi_src)
        
        R_T = R.transpose()
        
        # start in coordinate system where GW is propagating along z direction
        A_ij = np.zeros(3, 3)
        A_ij[0, 0] = 1
        A_ij[1, 1] = -1
        
        #Rotate A_ij so that GW propagates in direction defined by theta_src, phi_src
        
        A_ij_rot=np.einsum("ij,jk->ik", R_T, np.einsum("ij,jk->ik", A_ij, R))
        
        h_ij = np.cos(self.omega_GW*(t-np.dot(self.n_vec, x)))*A_ij_rot
        return h_ij
        
        
        
        
        
    
        
    
def transformation_matrix(theta, phi):
    # Function for calculating transformation matrix to a coordinate system rotated by angles theta and phi
    # theta is the angle off of z
    # phi is the azimuthal angle 
    R=np.empty(3, 3)
    R[0, 0] = np.cos(theta)*np.cos(phi)
    R[0, 1] = np.cos(theta)*np.sin(phi)
    R[0, 2] = -np.sin(theta)
    
    R[1, 0] = -np.cos(theta)*np.sin(phi)
    R[1, 1] = np.cos(theta)*np.cos(phi)
    R[1, 2] = 0.0
    
    R[2, 0] = np.sin(theta)*np.cos(phi)
    R[2, 1] = np.sin(theta)*np.sin(phi)
    R[3, 3] = np.cos(theta)
    
    return R
    
    