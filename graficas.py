# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 08:17:58 2022

@author: estudiantes
"""
import matplotlib.pyplot as plt
#import random as rd

c=3*10**8
h=6.63*10**-34
k=1.38*10**-23

class grafica:
    
    def __init__(self):
        
        self.fig, self.ax = plt.subplots()
        
    
    def mapaEstelar(self, ar, dec, indice, colores=[], teff=[], guardar=False):
        
        self.ax.scatter(ar, dec, s=2, color="blue")
        
        self.ax.set_facecolor((0,0,0))
        for i in indice:
            if teff and colores:
                self.ax.scatter(ar[i], dec[i], s=2, color=colores[round(teff[i]*0.01)*100])
                continue
            self.ax.scatter(ar[i], dec[i], s=2, color='r')
            
        self.ax.set_xlim(102.5,103.7)
        self.ax.set_ylim(56.25,56.8)
            
        #self.ax.scatter(229.6375, 2.0811, s=20, color=(1,1,1))
        
        if guardar:
            self.fig.savefig("mapaEstelar.jpg")
            
        plt.show()
        
    def radiacionCuerpoN(self, teff, guardar=False):
        import numpy as np
        
        def f(x):
            return (2*(c/x)**3)/(c**2)*h*1/(np.exp((h*(c/x))/(k*teff))-1)   
        
        x=np.linspace(0, 0.0001, 1000)
        
        self.ax.plot(x, f(x))
        
        if guardar:
            self.fig.savefig("radiacionCuerpoNegro.jpg")
            
        plt.show()
        
if __name__=="__main__":
    grafica().radiacionCuerpoN(3000)
        