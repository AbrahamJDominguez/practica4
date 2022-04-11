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
        
    
    def mapaEstelar(self, ar, dec, indice="", colores=[], teff=[], guardar=False):
        
        self.ax.scatter(ar, dec, s=2, color="blue")
        
        self.ax.set_facecolor((0,0,0))
        
        if indice:
            
            for i in indice:
                if teff and colores:
                    self.ax.scatter(ar[i], dec[i], s=2, color=colores[round(teff[i]*0.01)*100])
                    continue
                self.ax.scatter(ar[i], dec[i], s=2, color='r')
            
        #self.ax.set_xlim(45,50)
        #self.ax.set_ylim(2,6)
            
        #self.ax.scatter(229.6375, 2.0811, s=20, color=(1,1,1))
        
        if guardar:
            self.fig.savefig("mapaEstelar.jpg")
            
        plt.show()
        
        self.reiniciarFigura()
        
    def radiacionCuerpoN(self, teff, guardar=False):
        import numpy as np
        
        def f(x):
            return (2*(c/x)**3)/(c**2)*h*1/(np.exp((h*(c/x))/(k*teff))-1)   
        
        x=np.linspace(0, 0.0001, 1000)
        
        self.ax.plot(x, f(x))
        
        if guardar:
            self.fig.savefig("radiacionCuerpoNegro.jpg")
            
        plt.show()
        
        self.limpiarFigura()
        
    def diagramaHR(self, bp_rp, phot_g_mean_mag, guardar=True, tempt=False):
        
        if tempt:
        
            mapeo=self.ax.scatter(bp_rp, phot_g_mean_mag, c=bp_rp, s=2, cmap="RdYlBu", vmin=35000, vmax=2000)
            
        else:
            mapeo=self.ax.scatter(bp_rp, phot_g_mean_mag, c=bp_rp, s=2, cmap="RdYlBu_r", vmin=-1, vmax=5)
            
            
        cax = self.fig.add_axes([self.ax.get_position().x0,self.ax.get_position().y0,self.ax.get_position().width,0.01])
            
        colb=self.fig.colorbar(mapeo, cax=cax, orientation="horizontal")
        
        colb.ax.invert_xaxis()
        
        self.ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
            
        #self.fig.patch.set_facecolor('dimgray')
        self.ax.set_facecolor((0,0,0))
        
        if tempt:
        
            self.ax.set_xlim(2000,35000)
        
            self.ax.invert_xaxis()
            
        else:
            self.ax.set_xlim(-1,5)
            
        self.ax.set_ylim(-10,20)
        self.ax.invert_yaxis()
        
        if guardar:
            self.fig.savefig("diagramaHR.jpg")
            
        plt.show()
        
        self.limpiarFigura()
        
    def limpiarFigura(self):
        self.ax.cla()
        self.fig.clf()
        
    def reiniciarFigura(self):
        self.fig, self.ax = plt.subplots()
        
if __name__=="__main__":
    grafica().radiacionCuerpoN(3000)
        