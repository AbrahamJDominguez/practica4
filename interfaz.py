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

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

class Ventana(tk.Tk):
    ANCHO_CANVAS=800
    ALTURA_CANVAS=600
    COLOR_CANVAS="white"
    graficas=[graf(), graf(), graf()]
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
        self.datos=Archivo().leerArchivo(evento)
        
    def _radiacionCN(self):
        self.graficas[1].radiacionCuerpoN()
        self._cambio()
        
    def _mapaEstelar(self):
        self.graficas[0].mapaEstelar()
        self._cambio()
        
    def _diagramaHR(self):
        self.graficas[2].diagramaHR()
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
        self.check2()
        self.check3()
    
    def _cuadro_checks(self):
        self._cuadrocks=tk.Frame(self, bg=_from_rgb((50,122,122)))
        self._cuadrocks.place(relx=0, rely=0,relheight=1, relwidth=0.3)
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.0500, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.3800, relwidth=0.2, anchor="ne")
        ttk.Separator(self._cuadrocks, orient="horizontal").place(relx=0.6, rely=0.7100, relwidth=0.2, anchor="ne")
        
    def check1(self):
        self.funcion1=tk.IntVar()
        self.opfuncion1=tk.Checkbutton(self._cuadrocks, text="Mapa Estelar", variable=self.funcion1, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        self.opfuncion1.place(relx=0, rely=0, relwidth=1)
        
    def check2(self):
        self.funcion2=tk.IntVar()
        self.opfuncion2=tk.Checkbutton(self._cuadrocks, text="Radiacion Cuerpo Negro", variable=self.funcion2, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        self.opfuncion2.place(relx=0, rely=0.33, relwidth=1)
        
    def check3(self):
        self.funcion3=tk.IntVar()
        self.opfuncion3=tk.Checkbutton(self._cuadrocks, text="Diagrama H-R", variable=self.funcion3, onvalue=1, offvalue=0,bg=_from_rgb((100,102,200)))
        self.opfuncion3.place(relx=0, rely=0.66, relwidth=1)
               
        
if __name__=="__main__":
    prin=Ventana()
    
    tk.mainloop()