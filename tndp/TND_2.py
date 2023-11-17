# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 16:22:40 2021

@author: nicolas.rincon
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import csv
import numpy as np
from datetime import datetime


def copya1(Acopy):
    Rcopya1=[]
    for i in range(len(Acopy)):
        Rcopya1.append(Acopy[i])
    return Rcopya1

Nodos=pd.read_csv('nodos.txt')
nNodos=Nodos.shape[0]

# file1 = open('OD.csv', 'r')
# Lines = file1.readlines()
# MOD=[]
# for line in Lines:
#     li=line.split(',')
#     MODx=[]
#     for e in li:
#         e.replace('\n','')
#         print(e)
#         MODx.append(int(e))
#     MOD.append(MODx)

#     #print(li)
#     #print(li)
MOD = [
    [0, 400, 200, 60, 80, 150, 75, 75, 30, 160, 30, 25, 35, 0, 0],
    [400, 0, 50, 120, 20, 180, 90, 90, 15, 130, 20, 10, 10, 5, 0],
    [200, 50, 0, 40, 60, 180, 90, 90, 15, 45, 20, 10, 10, 5, 0],
    [60, 120, 40, 0, 50, 100, 50, 50, 15, 240, 40, 25, 10, 5, 0],
    [80, 20, 60, 50, 0, 50, 25, 25, 10, 120, 20, 15, 5, 0, 0],
    [150, 180, 180, 100, 50, 0, 100, 100, 30, 880, 60, 15, 15, 10, 0],
    [75, 90, 90, 50, 25, 100, 0, 50, 150, 440, 35, 10, 10, 5, 0],
    [75, 90, 90, 50, 25, 100, 50, 0, 15, 440, 35, 10, 10, 5, 0],
    [30, 15, 15, 15, 10, 30, 150, 15, 0, 140, 20, 5, 0, 0, 0],
    [160, 130, 45, 240, 120, 880, 440, 440, 140, 0, 600, 250, 500, 200, 0],
    [30, 20, 20, 40, 20, 60, 35, 35, 20, 600, 0, 75, 95, 15, 0],
    [25, 10, 10, 25, 15, 15, 10, 10, 5, 250, 75, 0, 70, 0, 0],
    [35, 10, 10, 10, 5, 15, 10, 10, 0, 500, 95, 70, 0, 45, 0],
    [0, 5, 5, 5, 0, 10, 5, 5, 0, 200, 15, 0, 45, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
] 


#Se cargan sin direccion
Arcos=pd.read_csv('arcos.txt')

ANodo1=[]
ANodo2=[]
ADistancia=[]
for i in range(Arcos.shape[0]):
    ANodo1.append(Arcos.at[i,'Nodo1'])
    ANodo1.append(Arcos.at[i,'Nodo2'])
    ANodo2.append(Arcos.at[i,'Nodo2'])
    ANodo2.append(Arcos.at[i,'Nodo1'])
    ADistancia.append(Arcos.at[i,'distancia'])
    ADistancia.append(Arcos.at[i,'distancia'])
ArcosD=pd.DataFrame({'Nodo1':ANodo1,'Nodo2':ANodo2,'distancia':ADistancia})




def Graficar(RutasGr):
    #https://matplotlib.org/stable/gallery/color/named_colors.html
    Colors=['lightcoral','darkorange','yellow','lime','darkgreen','navy','blue','hotpink']
    
    CX=Nodos['cx']
    CY=Nodos['cy']
    plt.plot(CX, CY, 'o', color='black')
    
    for i in range(Arcos.shape[0]):
        Nodo1=Arcos.at[i,'Nodo1']
        Nodo2=Arcos.at[i,'Nodo2']
        CX1=Nodos.at[Nodo1,'cx']
        CY1=Nodos.at[Nodo1,'cy']
        CX2=Nodos.at[Nodo2,'cx']
        CY2=Nodos.at[Nodo2,'cy']
        #plt.plot([0,20], [0,20])
        plt.plot([CX1,CX2],[CY1,CY2],color="whitesmoke")
    for i in range(Nodos.shape[0]):
        CX=Nodos.at[i,'cx']
        CY=Nodos.at[i,'cy']
        NodoID=str(Nodos.at[i,'Nodo'])
        plt.text(CX+0.5,CY+0.5,NodoID,fontsize=12)
    #print(getList(RutasGr),'haber')
    print("xxxx xxxx")
    Lkeys=list(RutasGr.keys())
    for i in range(len(Lkeys)):
        Ractual=RutasGr[Lkeys[i]]
        AGCX=[]
        AGCY=[]
        for j in range(len(Ractual)):
            NG=Ractual[j]
            AGCX.append(Nodos.at[NG,'cx'])
            AGCY.append(Nodos.at[NG,'cy'])
        plt.plot(AGCX,AGCY,color=Colors[i])
    #plt.figure(figsize=(40, 20))
    plt.show(20,10)
    
    
    OD=[]
    f = open('OD.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        line=row[0].split(";")
        OD.append(line)
    print(OD[1][2])
    
Aindice=[]
ArcosDI=ArcosD.copy()
for i in range(ArcosD.shape[0]):
    Aindice=str(ArcosDI.at[i,'Nodo1'])+'-'+str(ArcosDI.at[i,'Nodo2'])
print(ArcosDI)

def rutacorta(NodoIncial,NodoFinal):
    # al iterar el algoritmo en la posicion n de EstadoNodos se almacena la evaluacion del nodo n, obtiene la menor distancia desde el inicial a todos los nodos
    #[evaluado, distancia desde el nodo inicial, nodo visitado anteriormente]
    ValorM=10000
    EstadoNodos=[]
    for i in range (len(Nodos)):
        if NodoIncial==i:
            EstadoNodos.append([1,0,-1]) 
        else:
            EstadoNodos.append([0,ValorM,-1]) #[Evaluado 0:no, 1:si, distancia= valor muy grande, -1 (NodoVisitadoAnterior)]
    terminar=0
    NodoActual=NodoIncial
    while (terminar==0):
        #El nodo actual se marca como evaluado dado que al final de esta iteracion estara evaluado
        EstadoNodos[NodoActual][0]=1
        Iteracion=[]
        #Se buscan todos los nodos adyacentes al nodo actual y se almacenan en el vector iteracion
        ArcosAdyacentes=ArcosD.loc[ArcosD['Nodo1']==NodoActual].copy()
        #ArcosAdyacentes.sort_values(by='distancia', ascending=False,inplace=True)
        #ArcosAdyacentes.reset_index(inplace=True)
        for i in range(ArcosAdyacentes.shape[0]):
            ND=ArcosAdyacentes.at[i,'Nodo2']
            if EstadoNodos[ND][0]==0:
                distancia=ArcosAdyacentes.at[i,'distancia']+EstadoNodos[NodoActual][1]
                Iteracion.append([ND,distancia])
        # si los nodos en iteracion no han sido evaluados y tienen una distancia menor se actualiza la distancia
        for i in range(0,len(Iteracion)):
            NodoIteracion=Iteracion[i][0]
            DistanciaIteracion=Iteracion[i][1]
            if ((EstadoNodos[NodoIteracion][0]==0)and(EstadoNodos[NodoIteracion][1]>DistanciaIteracion)):
                EstadoNodos[NodoIteracion][1]=DistanciaIteracion
                EstadoNodos[NodoIteracion][2]=NodoActual
        minimo_index=-1
        ValorComparacion=ValorM
        #Se selecciona el nodo adyacente no visitado con menor distancia como siguiente nodo actual
        for i in range(len(EstadoNodos)):
            if(EstadoNodos[i][1]<ValorComparacion and EstadoNodos[i][0]==0):
                minimo_index=i
                ValorComparacion=EstadoNodos[i][1]
        if (minimo_index==-1):
            terminar=1
        else:
            NodoActual=minimo_index   
    print(EstadoNodos)    
    Resultado=[]
    Resultado.append(NodoFinal)
    NodoAnterior=EstadoNodos[NodoFinal][2]
    Resultado.append(NodoAnterior)
    while (NodoIncial!=NodoAnterior):
        NodoAnterior=EstadoNodos[NodoAnterior][2]
        Resultado.append(NodoAnterior)
    Resultado.reverse()   
    print('hello',Resultado)


#rutacorta(0,2)

R={'R0':[0,1,2,5,7,9,12,13],'R1':[4,3,5,14,8],'R2':[1,3,11,10,9,6]}
R={'R0':[0,1,2,5,7,9,10,12,13],'R1':[4,3,5,14,6],'R2':[11,3,5,14,8],'R3':[12,13,9]}
#R={}

#Graficar(R)

Aindice=[]
ArcosDI=ArcosD.copy()
for i in range(ArcosD.shape[0]):
    Aindice.append(str(ArcosDI.at[i,'Nodo1'])+'-'+str(ArcosDI.at[i,'Nodo2']))
ArcosDI.index=Aindice
    
#  .set_index('indice',inplace=True)

class clsRutaMasCorta:
    def __init__(self, Nodos, Arcos):
        self.Nodos = Nodos
        self.Arcos = Arcos
    def rutacorta(self,NodoIncial,NodoFinal):
        EstadoNodos=[]
        ValorM=10000
        for i in range (len(self.Nodos)):
            if NodoIncial==i:
                EstadoNodos.append([1,0,-1]) 
            else:
                EstadoNodos.append([0,ValorM,-1]) #[Evaluado 0:no, 1:si, distancia= valor muy grande, -1 (NodoVisitadoAnterior)]
        terminar=0
        NodoActual=NodoIncial
        while (terminar==0):
            #El nodo actual se marca como evaluado dado que al final de esta iteracion estara evaluado
            EstadoNodos[NodoActual][0]=1
            Iteracion=[]
            #Se buscan todos los nodos adyacentes al nodo actual y se almacenan en el vector iteracion
            ArcosAdyacentes=self.Arcos.loc[self.Arcos['Nodo1']==NodoActual].copy()
            ArcosAdyacentes.reset_index(inplace=True)
            
            #"""
            for i in range(ArcosAdyacentes.shape[0]):
                ND=ArcosAdyacentes.at[i,'Nodo2']
                if EstadoNodos[ND][0]==0:
                    distancia=ArcosAdyacentes.at[i,'distancia']+EstadoNodos[NodoActual][1]
                    Iteracion.append([ND,distancia])
            # si los nodos en iteracion no han sido evaluados y tienen una distancia menor se actualiza la distancia
            for i in range(0,len(Iteracion)):
                NodoIteracion=Iteracion[i][0]
                DistanciaIteracion=Iteracion[i][1]
                if ((EstadoNodos[NodoIteracion][0]==0)and(EstadoNodos[NodoIteracion][1]>DistanciaIteracion)):
                    EstadoNodos[NodoIteracion][1]=DistanciaIteracion
                    EstadoNodos[NodoIteracion][2]=NodoActual
            minimo_index=-1
            ValorComparacion=ValorM
            #Se selecciona el nodo adyacente no visitado con menor distancia como siguiente nodo actual
            for i in range(len(EstadoNodos)):
                if(EstadoNodos[i][1]<ValorComparacion and EstadoNodos[i][0]==0):
                    minimo_index=i
                    ValorComparacion=EstadoNodos[i][1]
            # NodoActual==NodoFinal reduce el numero de iteraciones pero tan solo trae el menor entre nodoinicial y nodofinal
            if (minimo_index==-1) or (NodoActual==NodoFinal):
                terminar=1
            else:
                NodoActual=minimo_index   
        Resultado=[]
        Resultado.append(NodoFinal)
        NodoAnterior=EstadoNodos[NodoFinal][2]
        Resultado.append(NodoAnterior)
        while (NodoIncial!=NodoAnterior):
            NodoAnterior=EstadoNodos[NodoAnterior][2]
            Resultado.append(NodoAnterior)
        Resultado.reverse()   
        return[Resultado,EstadoNodos[NodoFinal][1]]
            #"""
#Instancia=clsRutaMasCorta(Nodos,ArcosD)
#b=Instancia.rutacorta(0,2)
#print(b)

def GenerarArcosDeSolucion(Solucion):
    LK=list(Solucion.keys())
    ANodo1=[]
    ANodo2=[]
    ADistancia=[]
    Aindice=[]
    for e in LK:
        print (len(Solucion[e]))
        for i in range(1,len(Solucion[e])):
            ANodo1.append(Solucion[e][i-1])
            ANodo2.append(Solucion[e][i])   
            ind=str(Solucion[e][i-1])+'-'+str(Solucion[e][i])
            Aindice.append(ind)
            ADistancia.append(ArcosDI.at[ind,'distancia'])
            ANodo2.append(Solucion[e][i-1])
            ANodo1.append(Solucion[e][i])   
            ind=str(Solucion[e][i])+'-'+str(Solucion[e][i-1])
            ADistancia.append(ArcosDI.at[ind,'distancia'])
            Aindice.append(ind)
    ArcosGenerarArcosDeSolucion=pd.DataFrame({'Nodo1':ANodo1,'Nodo2':ANodo2,'distancia':ADistancia})  
    ArcosGenerarArcosDeSolucion.index=Aindice
    return ArcosGenerarArcosDeSolucion

#"""

VOD=[]
Instancia=clsRutaMasCorta(Nodos,GenerarArcosDeSolucion(R))
for i in range(nNodos):
    VODx=[]
    for j in range(nNodos):
        if i!=j:
            b=Instancia.rutacorta(i,j)
            VODx.append(b[0])
        else:
            VODx.append([0])
    VOD.append(VODx)
#print(VOD)


def EvaluarMaximaCapacidadRuta(Solucion):
    CargaArcos=[]
    for i in range(nNodos):
        CargaArcosx=[]
        for j in range(nNodos):
            CargaArcosx.append(0)
        CargaArcos.append(CargaArcosx)
    for i in range(nNodos):
        for j in range(nNodos):
            ar=VOD[i][j]
            for k in range(1,len(ar)):
                n1=ar[k-1]
                n2=ar[k]
                Demanda=MOD[i][j]
                CargaArcos[n1][n2]=CargaArcos[n1][n2]+Demanda
    #print(CargaArcos)
    LK=list(Solucion.keys())
    for e in LK:
        Cap=0
        auxr=Solucion[e]
        for i in range(len(auxr)):
            n1=auxr[i-1]
            n2=auxr[i]
            #print(n1,n2)
            if CargaArcos[n1][n2]>Cap:
                Cap=CargaArcos[n1][n2]
        print(Cap)
            
    
#EvaluarMaximaCapacidadRuta(R)   

def GenerarRutasOD(SolGR):
    #NodosTrasbordo
    
    RutasOD=[]
    for i in range(nNodos):
        RutasODl=[]
        for j in range(nNodos):
            RutasODl.append([1])
        RutasOD.append(RutasODl)
    
    LK=list(SolGR.keys())
    for e in LK:
        Re=SolGR[e]
        for i in range(0,len(Re)-1):
          C=[]
          Cr=[]
          distancia=0
          for j in range(1+i,len(Re)):
              if i!=j:
                  ind=str(Re[i])+'-'+str(Re[j])
                  C.append(str(Re[j-1])+'-'+str(Re[j]))
                  Cr.insert(0,str(Re[j])+'-'+str(Re[j-1]))
                  #calculo para distancia simetrica y codigo optimizado
                  distancia=distancia+ArcosDI.at[C[len(C)-1],'distancia']
                  AuxC=copya1(C)
                  AuxCr=copya1(Cr)
                  DesRuta={'Ruta':[e],'Distancia':distancia,'Secuencia':[AuxC],'Tipo':'Directo'}
                  DesRutar={'Ruta':[e],'Distancia':distancia,'Secuencia':[AuxCr],'Tipo':'Directo'}
                  auxp=ind.split('-')
                  px=int(auxp[0])
                  py=int(auxp[1])
                  RutasOD[px][py][0]=0   
                  RutasOD[py][px][0]=0 
                  RutasOD[px][py].append(DesRuta)
                  RutasOD[py][px].append(DesRutar)
        
    
    for i in range(nNodos):
        for j in range(nNodos):
            if (i!=j) and len(RutasOD[i][j])==0:
                AiestaenR=[]
                AjestaenR=[]
                for e in LK:
                    if i in R[e]:
                        AiestaenR.append(e)
                    if j in R[e]:
                        AjestaenR.append(e)
    
    Conexiones=[]
    if len(LK)>1:
        for i in range(len(LK)-1):
            for j in  range(i+1,len(LK)):
                #print(LK[i],LK[j])
                for el in SolGR[LK[i]]:
                    if el in SolGR[LK[j]]:
                        Conexiones.append([LK[i],LK[j],el])
                        Conexiones.append([LK[j],LK[i],el])
    print('Conexiones')
    print(Conexiones)
    
    NodosEnRutas=[]
    for i in range(nNodos):
        NodosEnRutas.append([])
    
    for i in range(nNodos):
        for e in LK:
            if i in SolGR[e]:
               NodosEnRutas[i].append(e)
    #print(NodosEnRutas)

    vacios=0
    for i in range(nNodos):
        for j in range(nNodos):
            if (i!=j) and len(RutasOD[i][j])==0:
                vacios=vacios+1
                #print(i,j)
    #print(vacios)
    #print('aca vamos')
    
    """
    i=1
    j=3
    for ei in NodosEnRutas[i]:
        for ej in NodosEnRutas[j]:
            for g in range(len(Conexiones)):
                if ei==Conexiones[g][0] and ej==Conexiones[g][1]:
                    #print(Conexiones[g][0],Conexiones[g][1],Conexiones[g][2])
                    nodoconeccion=Conexiones[g][2]
                    print(nodoconeccion,ei,ej,'pruebas')
                    print(RutasOD[i][nodoconeccion][1]['Secuencia'][0])
                    print(RutasOD[nodoconeccion][j][1]['Secuencia'][0])
                    #gh1=RutasOD[i][nodoconeccion][0][1]
                    #gh2=RutasOD[nodoconeccion][j][0][1]
    """
    #"""
    #print('homero',RutasOD[0][2][1])


    for i in range(nNodos):
        for j in range(nNodos):
            if i!=j and RutasOD[i][j][0]==1:
                #print(i,j)
                for ei in NodosEnRutas[i]:
                    for ej in NodosEnRutas[j]:
                        for g in range(len(Conexiones)):
                            if ei==Conexiones[g][0] and ej==Conexiones[g][1]:
                                #print(Conexiones[g][0],Conexiones[g][1],Conexiones[g][2])
                                nodoconeccion=Conexiones[g][2]
                                AuxRutaParcial1=[]
                                AuxRutaParcial2=[]
                                distancia=0
                                for auxe in RutasOD[i][nodoconeccion][1]['Secuencia'][0]:
                                    AuxRutaParcial1.append(auxe)
                                    distancia=distancia+ArcosDI.at[auxe,'distancia']
                                for auxe in RutasOD[nodoconeccion][j][1]['Secuencia'][0]:
                                    AuxRutaParcial2.append(auxe)
                                    distancia=distancia+ArcosDI.at[auxe,'distancia']
                                AuxRutaN=[AuxRutaParcial1,AuxRutaParcial2]
                                DesRuta={'Ruta':[Conexiones[g][0],Conexiones[g][1]],'Distancia':distancia,'Secuencia':AuxRutaN,'Tipo':'Trasbordo'}
                                RutasOD[i][j].append(DesRuta)
    
    for i in range(nNodos):
        for j in range(nNodos):
            if len(RutasOD[i][j])==1 and i!=j:
                print('igual a 1 ',i,j)

    return RutasOD

print(datetime.now())
SRutasOD=GenerarRutasOD(R)
print(datetime.now())

def EvaluarCargasArcos(SolGR,RutasOD):
    LK=list(SolGR.keys())
    Aindex=[]
    ACargaPasajeros=[]
    for er in LK:
        for i in range(1,len(SolGR[er])):
            ei=str(SolGR[er][i-1])
            ej=str(SolGR[er][i])
            auxindij=er+'-'+ei+'-'+ej
            auxindji=er+'-'+ej+'-'+ei
            Aindex.append(auxindij)
            Aindex.append(auxindji)
            ACargaPasajeros.append(0)
            ACargaPasajeros.append(0)
    DCargaPasajeros=pd.DataFrame({'CargaPasajeros':ACargaPasajeros})
    DCargaPasajeros.index=Aindex
    
    
    
    
    #DCargaPasajeros.at['R0-0-1','CargaPasajeros']=DCargaPasajeros.at['R0-0-1','CargaPasajeros']+100
    #DCargaPasajeros.at['R0-0-1','CargaPasajeros']=DCargaPasajeros.at['R0-0-1','CargaPasajeros']+100
    
    
    
    i=0
    j=4
    """
    s=0
    for er in RutasOD[i][j][1]['Ruta']:
        for en in RutasOD[i][j][1]['Secuencia'][s]:
            auxind=er+'-'+en
            DCargaPasajeros.at[auxind,'CargaPasajeros']=DCargaPasajeros.at[auxind,'CargaPasajeros']+MOD[1][0]
        s=s+1
    """
    #print(RutasOD[i][j])
    #print(MOD[1][0])
    for i in range(nNodos):
        for j in range(nNodos):
            if i!=j:
                s=0
                for er in RutasOD[i][j][1]['Ruta']:
                    for en in RutasOD[i][j][1]['Secuencia'][s]:
                        auxind=er+'-'+en
                        DCargaPasajeros.at[auxind,'CargaPasajeros']=DCargaPasajeros.at[auxind,'CargaPasajeros']+MOD[i][j]
                    s=s+1
    
    print(DCargaPasajeros)
    #print(RutasOD[1][2])
    #print(RutasOD[2][1])
    #print(RutasOD[0][13])
    
    """
    carga=0
    for i in range(nNodos):
        for j in range(nNodos):
            if i!=j:
                for ef in RutasOD[i][j][1]['Secuencia']:
                    if '3-5' in ef:
                        carga=MOD[i][j]+carga
                        print(RutasOD[i][j][1]['Ruta'],'homi ',i,j,MOD[i][j])
    print(carga)
    """
    #R={'R0':[0,1,2,5,7,9,10,12,13],'R1':[4,3,5,14,6],'R2':[11,3,5,14,8],'R3':[12,13,9]}    
    i=0
    j=4  
    print(RutasOD[0][13])
    print()
    print(RutasOD[4][6])
    print(RutasOD[11][8])
    
    #for i in range(nNodos):
    #    for j in range(nNodos):
    #        if i!=j:
    #            s=0
    #            if len(RutasOD[i][j])>2:
    #                #print(RutasOD[i][j])

        
EvaluarCargasArcos(R,SRutasOD)
#Label=[]
#CX=[]
#CY=[]

#plt.plot(CX, CY, 'o', color='black')
#plt.plot([0,20], [0,20])
#plt.plot([20,30], [20,30])
#plt.show()

