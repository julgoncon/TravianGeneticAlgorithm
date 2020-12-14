import database as db
import os
import sqlite3
import aldea as aldea
import functions as f
import random as rnd

edificios=[[1,'leñador'],[2,'barrera'],[3,'hierro'],[4,'cereal'],[5,'serreria'],[6,'ladrillar'],[7,'fundicion'],[8,'molino'],[9,'panaderia'],[10,'almacen'],[11,'granero'],[13,'herreria'],[15,'edifprin'],[16,'plaza'],[17,'mercado'],[18,'embajada'],[19,'cuartel'],[20,'establo'],[21,'taller'],[22,'academia'],[23,'escondite'],[24,'ayuntamiento'],[25,'residencia'],[26,'palacio'],[27,'tesoro'],[28,'oficina'],[32,'terraplen'],[37,'hogar']]
populate=False
N=50
bono=True

if populate:
    if(os.path.exists("./database.db")):
                os.remove("database.db")
    for i in range(4):
        ID=str(edificios[i][0]).replace(',','')
        db.populatePRO(ID,edificios[i][1],i)
    for i in range(4,28):
        ID=str(edificios[i][0]).replace(',','')
        db.populateGENERAL(ID,edificios[i][1],i)
    for i in range(9,11):
        ID=str(edificios[i][0]).replace(',','')
        db.populateALMACENAJE(ID,edificios[i][1],i)
    for i in range(22,24):
        ID=str(edificios[i][0]).replace(',','')
        db.populateRESI(ID,edificios[i][1],i)
    db.populateEDIFPRIN(15,edificios[12][1],12)
    print('populated')


       
l=f.generadorAldeas(1)
for x in range(500):
    print(x)
    if l[0].produccionTotal(bono)==2500:
        break
    for i in range(len(l)):
        a1=l[i]
        casillas=l[i].edificios
        randon=rnd.random()
        rand=rnd.randrange(len(casillas))
        if rand==23:
            continue
        if randon<0.85:
            rand=rnd.choice((0,1,2,3))
        else:
            rand=rnd.choice((9,10))
        balance=a1.balanceCereal()
        if balance < 5:
            rand=3
        if rand<=3 or rand==20:
            if rand==3:
                rand1=rnd.randrange(6) 
            else:
                rand1=rnd.randrange(4)
            cont=0
            if rand==20:
                for i in range(4,28):
                    if i ==20:
                        for i in casillas[i]:
                            if i!=0:
                                cont+=1
                    else:
                        if casillas[i]!=0:
                           cont+=1
                randon=rnd.random()

                if cont>=21:
                    continue
               
                if randon<0.7:
                    a1.edificios[rand].append(0)
                    rand1=len(a1.edificios[rand])-1
                else:
                    rand1=0
            lvl=casillas[rand][rand1]
            tabla=edificios[rand][1]
            if lvl==10:
                continue
            con = sqlite3.connect('edificios.db')
            cursor = con.cursor()
            cursor.execute("SELECT madera,barro,hierro,cereal FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            recursosSeparado=cursor.fetchone()
            noCap=False
            almacenaje=a1.almacenaje()
            for i in range(3):
                if recursosSeparado[i]>almacenaje[0]:
                    noCap=True
                    break
            if noCap==True:
                continue
            if recursosSeparado[3]>almacenaje[1]:
                continue
            cursor.execute("SELECT coste FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            coste=cursor.fetchone()[0]
            cursor.execute("SELECT habis FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            habis=cursor.fetchone()[0]
            con.commit()
            con.close()
            a1.traza.append([tabla,lvl+1])
            a1.edificios[rand][rand1]+=1
            recursos=a1.recursos
            if recursos>=coste:
                a1.tiempo+=5
                a1.recursos+=a1.produccionTotal(bono)*5
                a1.recursos-=coste
                a1.habis+=habis
            else: 
                diff=coste-a1.recursos
                a1.tiempo+=diff/a1.produccionTotal(bono)
                tiempoHastaConstruir=diff/a1.produccionTotal(bono)
                a1.pc+=a1.getPc(edificios)*tiempoHastaConstruir
                a1.recursos=0
                a1.habis+=habis
        if rand>3 and rand!=20:
            lvl=casillas[rand]
            cont=0
            if lvl==0:
                for i in range(3,28):
                    if i ==20:
                        for i in casillas[i]:
                            if i!=0:
                                cont+=1
                    else:
                        if casillas[i]!=0:
                            cont+=1
            if cont>=21:
                continue
            if rand == 13 and lvl==9:
                continue
            if (rand <=8 and rand >3) and lvl==5:
                continue
            if (rand <=3 or rand ==20) and lvl==10:
                continue
            if lvl==20:
                continue

            tabla=edificios[rand][1]
            con = sqlite3.connect('edificios.db')
            cursor = con.cursor()
            cursor.execute("SELECT madera,barro,hierro,cereal FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            recursosSeparado=cursor.fetchone()
            noCap=False
            almacenaje=a1.almacenaje()
            for i in range(3):
                if recursosSeparado[i]>almacenaje[0]:
                    noCap=True
                    break
            if noCap==True:
                continue
            if recursosSeparado[3]>almacenaje[1]:
                continue
            cursor.execute("SELECT coste FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            coste=cursor.fetchone()[0]
            cursor.execute("SELECT habis FROM %s WHERE id=%s;" % (tabla, lvl+1)) 
            habis=cursor.fetchone()[0]
            con.commit()
            con.close()
            a1.traza.append([tabla,lvl+1])
            a1.edificios[rand]+=1
            recursos=a1.recursos
            if recursos>=coste:
                a1.tiempo+=5
                a1.recursos+=a1.produccionTotal(bono)*5
                a1.recursos-=coste
                a1.habis+=habis
            else: 
                diff=coste-a1.recursos
                a1.tiempo+=diff/a1.produccionTotal(bono)
                tiempoHastaConstruir=diff/a1.produccionTotal(bono)
                a1.pc+=a1.getPc(edificios)*tiempoHastaConstruir
                a1.recursos=0
                a1.habis+=habis
            if a1.pc>=2000:
                break

print('TIEMPO:  '+str(a1.tiempo/86400))
print('PC :  '+ str(a1.pc))
print('PRODUCCION:  '+ str(a1.produccionTotal(bono)*3600))
print('EDIFICIOS:  '+ str(a1.edificios))
            
  

"""print('TIEMPO:  '+str(a1.tiempo/86400))
            print('PC :  '+ str(a1.pc))
            print('PRODUCCION:  '+ str(a1.produccionTotal(bono)*3600))
""" 
