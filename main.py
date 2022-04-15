import graficas as graf
import proyecto as p
import math
import copy

tabla="E:/practica4_copia/1649354370049O-result.csv"
tabla1="E:/practica4_copia/GaiaSource-1000172165251650944-1000424567594791808.csv"
tabla2="E:/practica4_copia/GaiaSource-1000424601954531200-1000677322125743488.csv"
tabla3="E:/practica4_copia/GaiaSource-1000677386549270528-1000959999693425920.csv"
colr="E:/practica4_copia/coloresCuerpoNegro.txt"

archivo = p.Archivo()
colores = p.Archivo().obtenerColoresCuerpoN(colr)
dic = archivo.leerArchivo()

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
    
    radius=dic["radius_val"]
    bp_rp=dic["bp_rp"]
    teff=dic["teff_val"]
    parallax=dic["parallax"]
    phot_g_mean_mag=dic["phot_g_mean_mag"]
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
    
    opcion=int(input("""¿Qué diagrama H-R desea generar?
    1. H-R de las estrellas con temperaturas efectivas conocidas.
    2. H-R con el color BP-RP.
    3. Ambos.
Selección: """))
    
    if opcion==1:
        
        teff1, g_abs1, radius1=depurar_teff(teff, g_abs, radius)
        graficas.diagramaHR(teff1, g_abs1, radius1, tempt=True, zoom=True)
        
    elif opcion==2:
        
        bp_rp2, g_abs2, radius2=depurar_bp_rp(bp_rp, g_abs, radius)
        graficas.diagramaHR(bp_rp2, g_abs2, radius2)
    
    else:
        bp_rp, g_abs2, radius2=depurar_bp_rp(bp_rp, g_abs, radius)
        graficas.diagramaHR(bp_rp, g_abs2, radius2)
        teff, g_abs1, radius1=depurar_teff(teff, g_abs, radius)
        graficas.diagramaHR(teff, g_abs1, radius1, tempt=True, zoom=True)
        
        
def depurar_teff(teff, g_abs, radius):
    
    g_abs1=copy.copy(g_abs)
    radius1=copy.copy(radius)
    
    while "" in teff:
        cont=0
        
        for val in teff:
            
            if not val:
                teff.pop(cont)
                g_abs1.pop(cont)
                radius1.pop(cont)
                
            cont+=1
    
    return teff, g_abs1, radius1

def depurar_bp_rp(bp_rp, g_abs, radius):
    
    g_abs2=copy.copy(g_abs)
    radius2=copy.copy(radius)

    while "" in bp_rp:
        cont=0
        
        for val in bp_rp:
            
            if not val:
                bp_rp.pop(cont)
                g_abs2.pop(cont)
                radius2.pop(cont)
                
            cont+=1
            
    return bp_rp, g_abs2, radius2

def crearMapaEstelar():
    
    global colores
    
    x=dic["ra"]
    y=dic["dec"]
    teffval=dic["teff_val"]
    
    graficas.mapaEstelar(x, y, indice=lista, teff=teffval, colores=colores, guardar=False)
    
lista = estrella_teff()
F = densidadFlujo()

crearMapaEstelar()

crearDiagramaHR()