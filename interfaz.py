# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 20:00:46 2022

@author: Abrah
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from proyecto import Archivo
from graficas import grafica as graf
from manejoDatos import datosMapaEstelarRadCN, datosDiagramaHR, coloresCuerpoNegro

colores=coloresCuerpoNegro()

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

def conversion(ascension):
    ascension=ascension.split("/")
    ascension[1]=float(ascension[1])/60
    ascension[2]=float(ascension[2])/3600
    ar=(float(ascension[0])+ascension[1]+ascension[2])*15
    
    return ar

class Ventana(tk.Tk):
    ANCHO_CANVAS=800
    ALTURA_CANVAS=600
    COLOR_CANVAS="white"
    #graficas=[graf(), graf(), graf()]
    figs={"mapa":Figure(figsize=(5,4), dpi=100),"mapao":Figure(figsize=(5,4), dpi=100),
          "HRT":Figure(figsize=(5,4), dpi=100), "HRB":Figure(figsize=(5,4), dpi=100),
          "CNG":Figure(figsize=(5,4), dpi=100), "CNO":Figure(figsize=(5,4), dpi=100)}
    
    datos={}

    FONDO="#0b0b0b"
    mg=[False,False]
    mo=[False,False]
    hrt=[False,False]
    hrb=[False,False]
    cng=[False,False]
    cno=[False,False]
    yahay=[mg,mo,hrt,hrb,cng,cno]
    cont=0
    
    def __init__(self, tam_min=(1200,600)):
        super().__init__()
        self.cambio=True
        self._iniciar_ventana("Gaia Archive", tam_min)
        self._cuadro_plots()
        self._opciones_archivo()
        self._iniciarWid()
        self.archivo=""
        self.protocol("WM_DELETE_WINDOW",self.__cerrar)
        
    def __cerrar(self):
        self.quit()
        self.destroy()
        
    def _iniciar_ventana(self, titulo, tam):
        self.title(titulo)
        self.minsize(*tam)
        self["bg"]=self.FONDO
        
    def _cuadro_plots(self):
        self._cuadro=tk.Frame(self, bg=self.FONDO)
        self._cuadro.place(relx=0.3, relheight=1, relwidth=0.9)
        self._canvasm= tk.Canvas(self._cuadro)
        self._canvasm.place(rely=0,relheight=0.333, relwidth=1)
        self._canvasHR= tk.Canvas(self._cuadro)
        self._canvasHR.place(rely=0.33, relheight=0.333, relwidth=1)
        self._canvasCN= tk.Canvas(self._cuadro)
        self._canvasCN.place(rely=0.66, relheight=0.333, relwidth=1)
        
    def _barra_menu(self):
        self._barra_opciones=tk.Menu(self)
        
    def _opciones_archivo(self):
        self._barra_menu()
        self.menu_archivos=tk.Menu(self._barra_opciones, tearoff=0)
        self.menu_archivos.add_command(label="Abrir archivo", command=self._seleccionar_archivo)
        self._barra_opciones.add_cascade(label="Archivo", menu=self.menu_archivos)
        self.config(menu=self._barra_opciones)
        
    def _seleccionar_archivo(self):
        self.archivo=filedialog.askopenfilename()
        if self.archivo:
            self._leer_archivo(self.archivo)
            
    def _leer_archivo(self, evento):
        try:
            self.datos=Archivo().leerArchivo(evento)
            self._obtenerDatos()
            print("datos obtenidos exitosamente")
            for i in self.yahay:
                i[0]=False
                i[1]=False
            
            if self.datos:
                self.graficas=[graf(interfaz=True), graf(interfaz=True), [graf(interfaz=True), graf(interfaz=True)]] 
            
        except:
            print("El archivo no fue leido exitosamente")
        
    def _radiacionCN(self):
        try:
            if self.objeto:
                self._obtenerDatos()
                teff_o=self.MEO[5]
                tempMax=self.MEO[6]
                if not self.cno[0] and self.cambio:
                    self.figs["CNO"]=self.graficas[1].radiacionCuerpoN(teff_o,tempMax,colores=colores)
                    self.cno[0]=True
                    self.cont+=1
                    if self.cont>=2:
                        self.cambio=False
                        self.cont=0
                    
                self._canvasFiguras("CNO")
                self.cno[1]=True
            
        except:
            "Falle :("
        if self.funcion3.get()==1:
            teff_o=self.ME[5]
            tempMax=self.ME[6]
            if not self.cng[0]: 
                self.figs["CNG"]=self.graficas[1].radiacionCuerpoN(teff_o,tempMax,colores=colores)
                self.cng[0]=True
            self._canvasFiguras("CNG")
            self.cng[1]=True
            
        
    def _mapaEstelar(self, boton=False):
        
        if self.funcion1.get() == 1 and not self.mg[1] and not boton:
        
            x=self.ME[1]
            y=self.ME[2]
            objeto=self.ME[0]
            teffval=self.ME[4]
            lista=self.ME[3]
            
            if not self.mg[0]:
                self.figs["mapa"]=self.graficas[0].mapaEstelar(x, y, objeto, indice=lista, teff=teffval, colores=colores, guardar=False)
                self.mg[0]=True
            print("Figura creada, se imprimira en un momento")
            self._canvasFiguras("mapa")
            self.mg[1]=True
            
        elif self.funcion1.get() == 1 and not self.mo[1] and boton:
            x=self.MEO[-2]
            y=self.MEO[-1]
            objeto=self.MEO[0]
            teffval=self.MEO[5]
            lista=self.MEO[3]
            
            if not self.mo[0] and self.cambio:
                self.figs["mapao"]=self.graficas[0].mapaEstelar(x, y, objeto, indice=lista, teff=teffval, colores=colores, ob=True, guardar=False)
                self.mo[0]=True
                self.cont+=1
                if self.cont>=2:
                    self.cambio=False
                    self.cont=0
            print("Figura creada, se imprimira en un momento")
            self._canvasFiguras("mapao")
            self.mo[1]=True
        
    def _diagramaHR(self):
        
        if self.funcion2.get() == 1 and self.DHRtemp.get() == 1:
        
            teff=self.HRt[1]
            g_abs1=self.HRt[2]
            radius1=self.HRt[0]
            
            if not self.hrt[0]:
                self.figs["HRT"]=self.graficas[2][0].diagramaHR(teff, g_abs1, radius1, tempt=True, zoom=True)
                self.hrt[0]=True
                
            self._canvasFiguras("HRT")
            self.hrt[1]=True
            
        if self.funcion2.get() == 1 and self.DHRbp_rp.get() == 1:
            
            bp_rp=self.HRb[1]
            g_abs1=self.HRb[2]
            radius1=self.HRb[0]
            
            if not self.hrb[0]:
                self.figs["HRB"]=self.graficas[2][1].diagramaHR(bp_rp, g_abs1, radius1, zoom=True)
                self.hrb[0]=True
                
            self._canvasFiguras("HRB")
            self.hrt[1]=True
        
    def _cambio(self):
        self.cambio=True
        
    def _canvasFiguras(self, tipo):

        graph=self.figs[tipo]
        if tipo == "mapa" or tipo == "mapao":
            canvasFig = FigureCanvasTkAgg(graph, master=self._canvasm)
            
        elif tipo == "HRT" or tipo == "HRB":
            canvasFig = FigureCanvasTkAgg(graph, master=self._canvasHR)
            
        elif tipo == "CNG" or tipo == "CNO":
            canvasFig = FigureCanvasTkAgg(graph, master=self._canvasCN)
            
        canvasFig.draw()
        
        if tipo == "mapao" or tipo =="HRB" or tipo == "CNO":
            canvasFig.get_tk_widget().place(relx=0.4,relheight=1, relwidth=0.4)
            
        else:
            canvasFig.get_tk_widget().place(relheight=1, relwidth=0.4)
            
    def _iniciarWid(self):
        self._cuadro_checks()
        self.check1()
        self._opcionesMapa()
        self.check2()
        self._opcionesDiagramaHR()
        self.check3()
        self._obtenerRCN()
    
    def _cuadro_checks(self):
        self._cuadrocks=tk.Frame(self, bg=_from_rgb((50,122,122)))
        self._cuadrocks.place(relx=0, rely=0, relheight=1, relwidth=0.3)
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.0500, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.3800, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.7100, relwidth=0.2, anchor="ne")
        
    def check1(self):
        self.funcion1=tk.IntVar()
        opfuncion1=tk.Checkbutton(self._cuadrocks, text="Mapa Estelar", variable=self.funcion1, command=self._mapaEstelar, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        opfuncion1.place(relx=0, rely=0, relwidth=1)
        
    def _opcionesMapa(self):
        label=tk.Label(self._cuadrocks, text="¿Desea senalar un objeto estelar?",bg=_from_rgb((50,122,130)))
        label.place(relx=0, rely=0.06)
        self.opcion = tk.IntVar() 
        self.opcion.set(2)

        tk.Radiobutton(self._cuadrocks, text="Si", variable=self.opcion, 
                    value=1,bg=_from_rgb((50,122,130))).place(relx=0.53, rely=0.06)
        tk.Radiobutton(self._cuadrocks, text="No", variable=self.opcion,
                    value=2,bg=_from_rgb((50,122,130))).place(relx=0.7, rely=0.06)
        
        label2=tk.Label(self._cuadrocks, text="Seleccione el tipo de coordenadas",bg=_from_rgb((50,122,130)))
        label2.place(relx=0, rely=0.1)
        self.opcion2 = tk.IntVar() 
        self.opcion2.set(2)

        tk.Radiobutton(self._cuadrocks, text="h/m/s", variable=self.opcion2, 
                    value=1,bg=_from_rgb((50,122,130))).place(relx=0.53, rely=0.1)
        tk.Radiobutton(self._cuadrocks, text="Grados", variable=self.opcion2,
                    value=2,bg=_from_rgb((50,122,130))).place(relx=0.7, rely=0.1)
        
        label3=tk.Label(self._cuadrocks, text="Ascencion Recta: ",bg=_from_rgb((50,122,130)))
        label3.place(relx=0, rely=0.16)
        
        self.entrada_ar=tk.Entry(self._cuadrocks)
        self.entrada_ar.place(relx=0.54,rely=0.16)
        
        label4=tk.Label(self._cuadrocks, text="Declinacion: ",bg=_from_rgb((50,122,130)))
        label4.place(relx=0, rely=0.2)
        
        self.entrada_dec=tk.Entry(self._cuadrocks)
        self.entrada_dec.place(relx=0.54,rely=0.2)
        
        label5=tk.Label(self._cuadrocks, text="Radio de busqueda(grados): ",bg=_from_rgb((50,122,130)))
        label5.place(relx=0, rely=0.24)
        
        self.entrada_rad=tk.Entry(self._cuadrocks)
        self.entrada_rad.place(relx=0.54,rely=0.24)
        
        boton=ttk.Button(self._cuadrocks, text="Senalar", command=self._obtenerEntradaME)
        boton.place(relx=0.75,rely=0.282)
        
    def _obtenerEntradaME(self):
        if self.opcion2.get() == 1 and self.opcion.get() ==1:
            try:
                ar=conversion(self.entrada_ar.get())
                dec=conversion(self.entrada_dec.get())
                rad=float(self.entrada_rad.get())
                
                print("Datos obtenidos con exito")
                
            except:
                print("Un cuadro no fue llenado correctamente, horas/minutos/segundos")
            
        elif self.opcion2.get() == 2 and self.opcion.get() ==1:
            try:
                ar=float(self.entrada_ar.get())
                dec=float(self.entrada_dec.get())
                rad=float(self.entrada_rad.get())
                
                print("Datos obtenidos con exito")
                
            except:
                print("Un cuadro no fue llenado correctamente")
                
        if self.opcion.get() ==1 and self.funcion1.get() == 1:
                    
            #try:
            self.objeto=[ar, dec, rad]
            self._obtenerDatos()
            self._cambio()
            self._mapaEstelar(boton=True)
                
            # except:
            #     print("Los datos no fueron recuperados de manera exitosa")
        
    def check2(self):
        self.funcion2=tk.IntVar()
        opfuncion2=tk.Checkbutton(self._cuadrocks, text="Diagrama H-R", command=self._diagramaHR,variable=self.funcion2, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        opfuncion2.place(relx=0, rely=0.33, relwidth=1)
        
    def _opcionesDiagramaHR(self):
        self.DHRbp_rp=tk.IntVar()
        opfuncion3=tk.Checkbutton(self._cuadrocks, text="H-R con el color BP-RP", command=self._diagramaHR,variable=self.DHRbp_rp, onvalue=1, offvalue=0,bg=_from_rgb((50,122,130)))
        opfuncion3.place(relx=0, rely=0.40)
        
        self.DHRtemp=tk.IntVar()
        opfuncion4=tk.Checkbutton(self._cuadrocks, text="H-R de las estrellas con temperatura", command=self._diagramaHR,variable=self.DHRtemp, onvalue=1, offvalue=0,bg=_from_rgb((50,122,130)))
        opfuncion4.place(relx=0, rely=0.44)
        
    def check3(self):
        self.funcion3=tk.IntVar()
        opfuncion3=tk.Checkbutton(self._cuadrocks, text="Radiacion Cuerpo Negro", variable=self.funcion3, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        opfuncion3.place(relx=0, rely=0.66, relwidth=1)
        
    def _obtenerRCN(self):
        boton2=tk.Button(self._cuadrocks, text="Generar grafica radiacion cuerpo negro", command=self._radiacionCN)
        boton2.place(relx=0, rely=0.75)
        
    def _obtenerDatos(self):
        try:
            self.MEO=datosMapaEstelarRadCN(self.datos, ob=True, objeto=self.objeto)
        except:
            self.ME=datosMapaEstelarRadCN(self.datos)
            
        self.HRt=datosDiagramaHR(self.datos)
        self.HRb=datosDiagramaHR(self.datos,op="bp_rp")
            
        
    def dibujar(self):
        pass
               
        
if __name__=="__main__":
    prin=Ventana()
    
    tk.mainloop()