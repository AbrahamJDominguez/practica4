# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 08:11:49 2022

@author: estudiantes
"""

class estrella:
    def __init__(self, dec, ra, parallax, photo_g_mean, bp_rp, teff ):
        self.declinacion=dec
        self.ar=ra
        self.parallax=parallax
        self.photo_mean=photo_g_mean
        self.bp_rp=bp_rp
        self.teff=teff
        
    def __bool__(self):
        if self.teff:
            return True
        
        else:
            return False
        
        #__nonzero__="__bool__"
    