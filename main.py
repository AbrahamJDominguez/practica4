import graficas as graf
import proyecto as p

tabla="E:/practica4_copia/1649354370049O-result.csv"
colr="E:/practica4_copia/coloresCuerpoNegro.txt"

archivo = p.Archivo()
colores=p.Archivo().obtenerColoresCuerpoN(colr)
dic=archivo.leerArchivo()

graficas = graf.grafica()
    
def estrella_teff():
    
    teff=dic["teff_val"]
    lista=[]
    
    for temp in teff:
        
        if temp:
            lista.append(teff.index(temp))
            
    return lista

def crearMapaEstelar():
    
    global colores
    
    x=dic["ra"]
    y=dic["dec"]
    teffval=dic["teff_val"]
    
    graficas.mapaEstelar(x, y, lista, colores, teff=teffval, guardar=False)
    
lista = estrella_teff()
crearMapaEstelar()