import sqlite3

class Aldea:

    def __init__(self):
        self.edificios = [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2,2,2],0,0,0,0,0,7,3,0,5,1,1,1,0,0,0,0,[1],0,1,0,0,0,0,0]
        self.tiempo=2400
        self.habis=69
        self.recursos=11000
        self.pc=600
        self.traza=[]
        
    def produccionTotal(self,bono):
        edificios=self.edificios
        tiempo=self.tiempo
        habis=self.habis
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cont=0
        for i in range(len(edificios[0])):
            ID=edificios[0][i]
            if ID==0:
                continue
            cursor.execute("SELECT produccion FROM leñador WHERE id='%s'" % ID )
            pro=cursor.fetchone()
            cont +=pro[0]
            ID=edificios[1][i]
            if ID==0:
                continue
            cursor.execute("SELECT produccion FROM barrera WHERE id='%s'" % ID )
            pro=cursor.fetchone()
            cont +=pro[0]
            ID=edificios[2][i]
            if ID==0:
                continue
            cursor.execute("SELECT produccion FROM hierro WHERE id='%s'" % ID )
            pro=cursor.fetchone()
            cont +=pro[0]
        for i in range(len(edificios[3])):
            ID=edificios[3][i]
            if ID==0:
                continue
            cursor.execute("SELECT produccion FROM cereal WHERE id='%s'" % ID )
            pro=cursor.fetchone()
            cont +=pro[0]
        
        if tiempo<=14400:
            cont+=144
        if tiempo>14400 and tiempo <=172800:
            cont+=252
        if tiempo>172800 and tiempo <=345600:
            cont+=396
        if tiempo>345600 and tiempo <=777600:
            cont+=540
        if bono:
            cont=cont*1.25
        cont-=habis+3
        cont=int(cont)
        
        con.commit()
        con.close()
        return cont/3600
    
    def balanceCereal(self):
        edificios=self.edificios
        habis=self.habis
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cont=0
        for i in range(len(edificios[3])):
            ID=edificios[3][i]
            if ID==0:
                continue
            cursor.execute("SELECT produccion FROM cereal WHERE id='%s'" % ID )
            pro=cursor.fetchone()
            cont +=pro[0]
        cont-=habis
        cont=int(cont)
        
        con.commit()
        con.close()
        return cont

    def getPc(self,edificios):
        casillas=self.edificios
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cont=0
        for i in range(len(edificios)):
            if i<=3 or i==20:
                tabla=edificios[i][1]
                for j in range(len(casillas[i])):
                    lvl=casillas[i][j]
                    cursor.execute("SELECT pc FROM %s WHERE id=%s;" % (tabla, lvl)) 
                    pc=cursor.fetchone()                    
                    cont +=pc[0]
            
            else:
                tabla=edificios[i][1]
                lvl=casillas[i]
                if lvl==0:
                    continue
                cursor.execute("SELECT pc FROM %s WHERE id=%s;" % (tabla, lvl)) 
                pc=cursor.fetchone()
                cont +=pc[0]
        con.commit()
        con.close()
        return cont/86400

    def almacenaje(self):
        l1=[]
        almacen=self.edificios[9]
        granero=self.edificios[10]
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("SELECT almacenaje FROM almacen WHERE id=%s;" % almacen)
        capAlma=cursor.fetchone()[0]
        l1.append(capAlma)
        cursor.execute("SELECT almacenaje FROM granero WHERE id=%s;" % granero)
        capGran=cursor.fetchone()[0]
        l1.append(capGran)
        con.commit()
        con.close()
        return l1


