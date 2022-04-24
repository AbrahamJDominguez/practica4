# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 22:52:21 2022

@author: Abrah
"""

#import graficas as graf
import proyecto as p
import math
import copy

colr="coloresCuerpoNegro.txt"
colores = p.Archivo().obtenerColoresCuerpoN("clr")

def coloresCuerpoNegro(ruta=""):
    
    if not ruta:
        global colores
        
        return colores
    
    else:
        colores=p.Archivo().obtenerColoresCuerpoN(ruta)
        return colores

def depurar_lista(lista):
    
    lista=copy.deepcopy(lista)
    
    while "" in lista:
        cont=0
        
        for val in lista:
            
            if not val:
                lista.pop(cont)
                
            cont+=1
    
    return lista

def depurar(lista, g_abs, radius):
    
    g_abs1=copy.deepcopy(g_abs)
    radius1=copy.deepcopy(radius)
    
    while "" in lista:
        cont=0
        
        for val in lista:
            
            if not val:
                lista.pop(cont)
                g_abs1.pop(cont)
                radius1.pop(cont)
                
            cont+=1
    
    return lista, g_abs1, radius1

def estrella_teff(dic):    
    
    try:
        teff=copy.deepcopy(dic["teff_val"])
        lista=[]
        
        for temp in teff:
            
            if temp:
                lista.append(teff.index(temp))
                
        return lista
    except:
        return []
    
    
def datosDiagramaHR(dic, op="teff"):
    
    radius=copy.deepcopy(dic["radius_val"])
    bp_rp=copy.deepcopy(dic["bp_rp"])
    teff=copy.deepcopy(dic["teff_val"])
    parallax=copy.deepcopy(dic["parallax"])
    phot_g_mean_mag=copy.deepcopy(dic["phot_g_mean_mag"])
    g_abs=[]
    
    while "" in radius:
        cont=0
        
        for val in radius:
            if not val:
                radius[cont]=1
            cont+=1
    
    while "" in parallax:
        cont=0
        
        for val in parallax:
            
            if not val:
                parallax.pop(cont)
                phot_g_mean_mag.pop(cont)
                teff.pop(cont)
                bp_rp.pop(cont)
                radius.pop(cont)
                
            cont+=1
            
    for i in range(len(parallax)):
        g_abs.append(phot_g_mean_mag[i] + 5 + 5*math.log10(abs(parallax[i])/1000))
        
    if op== "bp_rp":  
        
        bp_rp, g_abs, radius=depurar(bp_rp, g_abs, radius)
        
        return radius, bp_rp, g_abs
        
    elif op == "teff":
        teff, g_abs, radius=depurar(teff, g_abs, radius)
        
        return radius, teff, g_abs
        
def datosMapaEstelarRadCN(dic, ob=False , objeto=[]):
    
    x=copy.deepcopy(dic["ra"])
    y=copy.deepcopy(dic["dec"])
    teffval=copy.deepcopy(dic["teff_val"])
    #print(teffval)
    teff_o=[]
    coord_ar=[]
    coord_dec=[]
    lista = estrella_teff(dic)
    
    if ob:
        for index in range(len(x)):
            if ((x[index]-objeto[0])**2 + (y[index]-objeto[1])**2) <= objeto[2]**2:
                if teffval[index]:    
                    teff_o.append(teffval[index])
                    coord_ar.append(round(x[index],13))
                    coord_dec.append(round(y[index],14))
        #print(teff_o)
        
        c=0
        for temp in teff_o:
            if c==0:
                tempMax=temp
            elif c>0 and not isinstance(temp,str):
                if(temp>tempMax):
                   tempMax=temp 
                else:
                    tempMax=tempMax
            c+=1
            
        return objeto, x, y, "", teffval, teff_o, tempMax, coord_ar, coord_dec
    
    else:
        c=0
        for temp in teffval:
            if c==0 and temp != "":
                tempMax=temp
                c+=1
                
            elif c>0 and not isinstance(temp,str):
                if(temp>tempMax):
                   tempMax=temp 
                else:
                    tempMax=tempMax
                    
        teff_o=depurar_lista(teffval)
        
        return objeto, x, y, lista, teffval, teff_o, tempMax, coord_ar, coord_dec
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        