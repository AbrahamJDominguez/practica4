import graficas as graf
import proyecto as p
import math

tabla="E:/practica4_copia/1649354370049O-result.csv"
tabla1="E:/practica4_copia/GaiaSource-1000172165251650944-1000424567594791808.csv"
tabla2="E:/practica4_copia/GaiaSource-1000424601954531200-1000677322125743488.csv"
tabla3="E:/practica4_copia/GaiaSource-1000677386549270528-1000959999693425920.csv"
colr="E:/practica4_copia/coloresCuerpoNegro.txt"

archivo = p.Archivo()
colores = p.Archivo().obtenerColoresCuerpoN()
dic = archivo.leerArchivos()

graficas = graf.grafica()   

def estrella_teff():
    
    teff=dic["teff_val"]
    lista=[]
    
    for temp in teff:
        
        if temp:
            lista.append(teff.index(temp))
            
    return lista

def densidadFlujo():
    
    CBoltz=5.67*10**-8
    F=[]
    teff=dic["teff_val"]
    
    for i in lista:
        F.append(CBoltz*float(teff[i]))
    
    return F

def crearDiagramaHR():
    
    global dic
    
    bp_rp=dic["bp_rp"]
    
    
    phot_g_mean_mag=dic["phot_g_mean_mag"]
    
    
    while "" in bp_rp:
        cont=0
        
        for val in bp_rp:
            
            if not val:
                bp_rp.pop(cont)
                phot_g_mean_mag.pop(cont)
                
            cont+=1
    
    graficas.diagramaHR(bp_rp, phot_g_mean_mag)
    
def crearDiagramaHR2():
    
    global dic
    
    bp_rp=dic["teff_val"]
    
    parallax=dic["parallax"]
    phot_g_mean_mag=dic["phot_g_mean_mag"]
    g_abs=[]
    #g_abs=dic["g_abs"]
    
    while "" in parallax:
        cont=0
        
        for val in parallax:
            
            if not val:
                parallax.pop(cont)
                phot_g_mean_mag.pop(cont)
                bp_rp.pop(cont)
                
            cont+=1
            
    for i in range(len(parallax)):
        g_abs.append(phot_g_mean_mag[i] + 5 + 5*math.log10(abs(parallax[i])/1000))
    
    
    while "" in bp_rp:
        cont=0
        
        for val in bp_rp:
            
            if not val:
                bp_rp.pop(cont)
                #phot_g_mean_mag.pop(cont)
                g_abs.pop(cont)
                
            cont+=1
    
    #graficas.diagramaHR(bp_rp, phot_g_mean_mag, tempt=True)
    graficas.diagramaHR(bp_rp, g_abs, tempt=True)

def crearMapaEstelar():
    
    global colores
    
    x=dic["ra"]
    y=dic["dec"]
    teffval=dic["teff_val"]
    
    graficas.mapaEstelar(x, y, indice=lista, teff=teffval, colores=colores, guardar=False)
    
lista = estrella_teff()
F = densidadFlujo()

crearMapaEstelar()

crearDiagramaHR2()