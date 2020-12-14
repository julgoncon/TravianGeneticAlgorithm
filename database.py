from bs4 import BeautifulSoup
import re
import urllib.request
import sqlite3 
import os

def loadURL(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("iso8859-1")
    fp.close()

    return mystr
def getListaRecursos(ID):
    html = loadURL(f"http://www.traviantoolbox.com/en/batiments.php?batiment="+str(ID)+"&type=&batp=1")
    soup = BeautifulSoup(html, 'html.parser')
    tabla = soup.find('table', class_="tab")
    tr=tabla.find_all('tr')
    listarecursos=list()
    for i in range(1,len(tr)):
        td=tr[i].find_all('td')
        for j in range(0,5):
            listarecursos.append(re.search("\d{1,10}", str(td[j])).group())
    return listarecursos

def getListaCosteTotal(ID):
    listarecursos=getListaRecursos(ID)
    listaCosteTotal=list()
    cont=0
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                listaCosteTotal.append(cont)
            cont=0
            if i!=95:
                continue
        cont=cont+int(listarecursos[i])
        if i==99:
            listaCosteTotal.append(cont-20)
    return listaCosteTotal

def getListaCosteTotalBONO(ID):
    listarecursos=getListaRecursos(ID)
    listaCosteTotal=list()
    cont=0
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                listaCosteTotal.append(cont)
            cont=0
            if i!=20:
                continue
        cont=cont+int(listarecursos[i])
        if i==24:
            listaCosteTotal.append(cont-20)
    return listaCosteTotal

def getListaCosteTotalEscondite(ID):
    listarecursos=getListaRecursos(ID)
    listaCosteTotal=list()
    cont=0
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                listaCosteTotal.append(cont)
            cont=0
            if i!=45:
                continue
        cont=cont+int(listarecursos[i])
        if i==49:
            listaCosteTotal.append(cont-20)
    return listaCosteTotal

def getListaRecursosSeparadosEscondite(ID):
    listarecursos=getListaRecursos(ID)
    recursosSeparados=[]
    lista=[]
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                recursosSeparados.append(lista)
            lista=[]
            continue
        lista.append(listarecursos[i])
        if i==49:
            recursosSeparados.append(lista)
    return recursosSeparados


def getListaRecursosSeparados(ID):
    listarecursos=getListaRecursos(ID)
    recursosSeparados=[]
    lista=[]
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                recursosSeparados.append(lista)
            lista=[]
            continue
        lista.append(listarecursos[i])
        if i==99:
            recursosSeparados.append(lista)
    return recursosSeparados

def getListaRecursosSeparadosBONO(ID):
    listarecursos=getListaRecursos(ID)
    recursosSeparados=[]
    lista=[]
    for i in range(len(listarecursos)):
        if i%5==0:
            if i!=0:
                recursosSeparados.append(lista)
            lista=[]
            continue
        lista.append(listarecursos[i])
        if i==24:
            recursosSeparados.append(lista)
    return recursosSeparados

def getCultura(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        lista.append(lista1[9])
    fileobj.close()
    return lista

def getHabis(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        lista.append(lista1[6])
    fileobj.close()
    return lista


def getProduccion(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        lista.append(lista1[11])
    fileobj.close()
    return lista

def getBonoEdifP(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        valor=lista1[11]
        valor=valor.replace('%','')
        lista.append(int(valor)/100)
    fileobj.close()
    return lista

def getAlmacenamiento(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        valor=lista1[11]
        lista.append(int(valor))
    fileobj.close()
    return lista

def getTiempoResi(ID):
    lista=[]
    fileobj=open("text\\text"+str(ID)+".txt", "r")
    for line in fileobj.readlines():
        lista1=line.split()
        valor=lista1[10]
        valor=valor.split(':')
        valor1=int(valor[0])
        valor2=int(valor[1])
        valor3=int(valor[2])
        valor=round(valor1+(valor2/60)+((valor3)*(1/3600)),3)
        lista.append(valor)
    fileobj.close()
    return lista


def populatePRO(ID,tabla,i):
    tuplas=[]
    cultura=getCultura(ID)
    habis=getHabis(ID)
    produccion=getProduccion(ID)
    recursosSeparados=getListaRecursosSeparados(ID)
    listaCosteTotal=getListaCosteTotal(ID)
    for i in range(len(listaCosteTotal)):
        tupla=(recursosSeparados[i][0],recursosSeparados[i][1],recursosSeparados[i][2],recursosSeparados[i][3],listaCosteTotal[i],habis[i],cultura[i],produccion[i])
        tuplas.append(tupla)
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE '%s'(id integer PRIMARY KEY AUTOINCREMENT, madera int, barro int,hierro int,cereal int,coste int,habis int, pc int, produccion int)" % tabla)
    cursor.executemany("INSERT INTO '%s' (madera,barro,hierro,cereal,coste,habis, pc, produccion) VALUES (?,?,?,?,?,?,?,?)" % tabla, tuplas)
    con.commit()
    con.close()

def populateGENERAL(ID,tabla,i):    
    if (i>3 and i<=8) or i==11 or (i>12 and i<=21) or (i>23 and i<=27):#FALTAN LOS ESPECIALES
        tuplas=[]
        cultura=getCultura(ID)
        habis=getHabis(ID)
        if i>3 and i<=8:
            recursosSeparados=getListaRecursosSeparadosBONO(ID)
            listaCosteTotal=getListaCosteTotalBONO(ID)
        if i==20:
            recursosSeparados=getListaRecursosSeparadosEscondite(ID)
            listaCosteTotal=getListaCosteTotalEscondite(ID)

        else:
            recursosSeparados=getListaRecursosSeparados(ID)
            listaCosteTotal=getListaCosteTotal(ID)
            if tabla=='escondite' or tabla=='plaza':
                print(len(listaCosteTotal))
        for i in range(len(listaCosteTotal)):
            tupla=(recursosSeparados[i][0],recursosSeparados[i][1],recursosSeparados[i][2],recursosSeparados[i][3],listaCosteTotal[i],habis[i],cultura[i])
            tuplas.append(tupla)
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        if tabla=='escondite' or tabla=='plaza':
            print(len(tuplas))
        cursor.execute("CREATE TABLE '%s'(id integer PRIMARY KEY AUTOINCREMENT, madera int, barro int,hierro int,cereal int,coste int,habis int, pc int)" % tabla)
        cursor.executemany("INSERT INTO '%s' (madera,barro,hierro,cereal,coste,habis,pc) VALUES (?,?,?,?,?,?,?)" % tabla, tuplas)
        con.commit()
        con.close()
        

def populateALMACENAJE(ID,tabla,i):    
    if i==9 or i==10:#FALTAN LOS ESPECIALES
        tuplas=[]
        cultura=getCultura(ID)
        habis=getHabis(ID)
        recursosSeparados=getListaRecursosSeparados(ID)
        listaCosteTotal=getListaCosteTotal(ID)
        almacenaje=getAlmacenamiento(ID)
        for i in range(len(listaCosteTotal)):
            tupla=(recursosSeparados[i][0],recursosSeparados[i][1],recursosSeparados[i][2],recursosSeparados[i][3],listaCosteTotal[i],habis[i],cultura[i],almacenaje[i])
            tuplas.append(tupla)
        
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("CREATE TABLE '%s'(id integer PRIMARY KEY AUTOINCREMENT, madera int, barro int,hierro int,cereal int,coste int,habis int, pc int,almacenaje int)" % tabla)
        cursor.executemany("INSERT INTO '%s' (madera,barro,hierro,cereal,coste, habis,pc,almacenaje) VALUES (?,?,?,?,?,?,?,?)" % tabla, tuplas)
        con.commit()
        con.close()
       

def populateRESI(ID,tabla,i):    
    tuplas=[]
    cultura=getCultura(ID)
    habis=getHabis(ID)
    recursosSeparados=getListaRecursosSeparados(ID)
    listaCosteTotal=getListaCosteTotal(ID)
    tiempo=getTiempoResi(ID)
    for i in range(len(listaCosteTotal)):
        tupla=(recursosSeparados[i][0],recursosSeparados[i][1],recursosSeparados[i][2],recursosSeparados[i][3],listaCosteTotal[i],habis[i],cultura[i],tiempo[i])
        tuplas.append(tupla)        
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE '%s'(id integer PRIMARY KEY AUTOINCREMENT, madera int, barro int,hierro int,cereal int,coste int,habis int, pc int,tiempo int)" % tabla)
    cursor.executemany("INSERT INTO '%s' (madera,barro,hierro,cereal,coste,habis, pc,tiempo) VALUES (?,?,?,?,?,?,?,?)" % tabla, tuplas)
    con.commit()
    con.close()
  
def populateEDIFPRIN(ID,tabla,i):    
    tuplas=[]
    cultura=getCultura(ID)
    habis=getHabis(ID)
    recursosSeparados=getListaRecursosSeparados(ID)
    listaCosteTotal=getListaCosteTotal(ID)
    bono=getBonoEdifP(ID)
    for i in range(len(listaCosteTotal)):
        tupla=(recursosSeparados[i][0],recursosSeparados[i][1],recursosSeparados[i][2],recursosSeparados[i][3],listaCosteTotal[i],habis[i],cultura[i],bono[i])
        tuplas.append(tupla)        
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE '%s'(id integer PRIMARY KEY AUTOINCREMENT, madera int, barro int,hierro int,cereal int,coste int,habis int, pc int,bono int)" % tabla)
    cursor.executemany("INSERT INTO '%s' (madera,barro,hierro,cereal,coste,habis, pc,bono) VALUES (?,?,?,?,?,?,?,?)" % tabla, tuplas)
    con.commit()
  

