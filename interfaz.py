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
    figs=[]
    datos={}

    FONDO="#0b0b0b"
    
    def __init__(self, tam_min=(1200,600)):
        super().__init__()
        self.cambio=True
        self._iniciar_ventana("Gaia Archive", tam_min)
        self._cuadro_plots()
        self._opciones_archivo()
        self._iniciarWid()
        self.archivo=""
        self.protocol("WM_DELETE_WINDOW",self.__cerrar)
        if self.archivo:
            self.graficas=[graf(), graf(), [graf(), graf()]]          
        
    def __cerrar(self):
        self.quit()
        self.destroy()
        
    def _iniciar_ventana(self, titulo, tam):
        self.title(titulo)
        self.minsize(*tam)
        self["bg"]=self.FONDO
        
    def _cuadro_plots(self):
        self._cuadro=tk.Frame(self, bg=self.COLOR_CANVAS)
        self._cuadro.place(relx=0.3, rely=0,relheight=1, relwidth=0.9)
        
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
            #self._obtenerDatos()
            
        except:
            print("El archivo no fue leido exitosamente")
        
    def _radiacionCN(self):
        teff_o=self.ME[5]
        tempMax=self.ME[6]
        self.graficas[1].radiacionCuerpoN(teff_o,tempMax,colores=colores)
        self._cambio()
        
    def _mapaEstelar(self):
        
        x=self.ME[1]
        y=self.ME[2]
        objeto=self.ME[0]
        teffval=self.ME[4]
        lista=self.ME[3]
        
        self.graficas[0].mapaEstelar(x, y, objeto, indice=lista, teff=teffval, colores=colores, guardar=False)
        self._cambio()
        
    def _diagramaHR(self):
        
        teff=self.HR[1]
        g_abs1=self.HR[2]
        radius1=self.HR[0]
        
        self.graficas[2][0].diagramaHR(teff, g_abs1, radius1)
        self._cambio()
        
    def _cambio(self):
        self.cambio=True
        
    def _canvasFiguras(self):
        for graph in self.graficas:
            if graph:
                self.figs.append(graph[0])
                
    def _iniciarWid(self):
        self._cuadro_checks()
        self.check1()
        self._opcionesMapa()
        self.check2()
        self._opcionesDiagramaHR()
        self.check3()
    
    def _cuadro_checks(self):
        self._cuadrocks=tk.Frame(self, bg=_from_rgb((50,122,122)))
        self._cuadrocks.place(relx=0, rely=0, relheight=1, relwidth=0.3)
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.0500, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.3800, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.7100, relwidth=0.2, anchor="ne")
        
    def check1(self):
        self.funcion1=tk.IntVar()
        opfuncion1=tk.Checkbutton(self._cuadrocks, text="Mapa Estelar", variable=self.funcion1, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
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
        if self.opcion2.get() == 1:
            try:
                ar=conversion(self.entrada_ar.get())
                dec=conversion(self.entrada_dec.get())
                rad=float(self.entrada_rad.get())
                
            except:
                print("Un cuadro no fue llenado correctamente, horas/minutos/segundos")
            
        elif self.opcion2.get() == 2:
            try:
                ar=float(self.entrada_ar.get())
                dec=float(self.entrada_dec.get())
                rad=float(self.entrada_rad.get())
                
            except:
                print("Un cuadro no fue llenado correctamente")
                
        try:
            self.objeto=[ar, dec, rad]
            self._cambio()
            
        except:
            print("Los datos no fueron recuperados de manera exitosa")
        
    def check2(self):
        self.funcion2=tk.IntVar()
        opfuncion2=tk.Checkbutton(self._cuadrocks, text="Diagrama H-R", variable=self.funcion2, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        opfuncion2.place(relx=0, rely=0.33, relwidth=1)
        
    def _opcionesDiagramaHR(self):
        self.DHRbp_rp=tk.IntVar()
        opfuncion3=tk.Checkbutton(self._cuadrocks, text="H-R con el color BP-RP", variable=self.funcion2, onvalue=1, offvalue=0,bg=_from_rgb((50,122,130)))
        opfuncion3.place(relx=0, rely=0.40)
        
        self.DHRtemp=tk.IntVar()
        opfuncion4=tk.Checkbutton(self._cuadrocks, text="H-R de las estrellas con temperatura", variable=self.funcion2, onvalue=1, offvalue=0,bg=_from_rgb((50,122,130)))
        opfuncion4.place(relx=0, rely=0.44)
        
    def check3(self):
        self.funcion3=tk.IntVar()
        opfuncion3=tk.Checkbutton(self._cuadrocks, text="Radiacion Cuerpo Negro", variable=self.funcion3, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        opfuncion3.place(relx=0, rely=0.66, relwidth=1)
        
    def _obtenerDatos(self):
        try:
            self.ME=datosMapaEstelarRadCN(self.datos, ob=True, objeto=self.objeto)
        except:
            self.ME=datosMapaEstelarRadCN(self.datos)
            
        self.HR=datosDiagramaHR(self.datos)
            
        
    def dibujar(self):
        pass
               
        
if __name__=="__main__":
    prin=Ventana()
    
    tk.mainloop()