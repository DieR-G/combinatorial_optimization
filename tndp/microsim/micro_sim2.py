# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:10:03 2024

@author: nicolas.rincon
"""

from datetime import datetime
class Passenger:
    def __init__(self,tiempoLlegadaEstacionInicio,estacionInicio,estacionFin):
        self.active = False
        self.tiempoLlegadaEstacionInicio = tiempoLlegadaEstacionInicio
        self.estacionInicio=estacionInicio
        self.estacionFin=estacionFin
        self.busActual=-1
        self.estacionActual=-1
        
class Bus:
    def __init__(self, ruta, estacionInicio, estacionFin, capacidad, pasajerosAbordo):
        self.active = False
        self.ruta = ruta
        self.capacidad=capacidad
        self.pasajerosAbordo=pasajerosAbordo
        self.posx=-1
        self.posy=-1
        
        
matrizhoraAperturaArco=[[0, 8, 10, 17, 21, 13, 19, 15, 24, 23, 28, 27, 33, 31, 16], 
                        [8, 0, 2, 9, 13, 5, 11, 7, 16, 15, 20, 19, 25, 23, 8], 
                        [10, 2, 0, 7, 11, 3, 9, 5, 14, 13, 18, 17, 23, 21, 6], 
                        [17, 9, 7, 0, 4, 4, 10, 6, 15, 14, 19, 10, 24, 22, 7], 
                        [21, 13, 11, 4, 0, 8, 14, 10, 19, 18, 23, 14, 28, 26, 12], 
                        [13, 5, 3, 4, 8, 0, 6, 2, 11, 10, 15, 14, 20, 18, 3], 
                        [19, 11, 9, 10, 14, 6, 0, 4, 10, 12, 17, 19, 22, 20, 2], 
                        [15, 7, 5, 6, 10, 2, 4, 0, 10, 8, 13, 16, 18, 16, 2], 
                        [24, 16, 14, 15, 19, 11, 10, 10, 0, 21, 26, 25, 31, 29, 8], 
                        [23, 15, 13, 14, 18, 10, 12, 8, 21, 0, 5, 24, 10, 8, 10], 
                        [28, 20, 18, 19, 23, 15, 17, 13, 26, 5, 0, 29, 5, 7, 15], 
                        [27, 19, 17, 10, 14, 14, 19, 16, 25, 24, 29, 0, 34, 32, 17], 
                        [33, 25, 23, 24, 28, 20, 22, 18, 31, 10, 5, 34, 0, 2, 20], 
                        [31, 23, 21, 22, 26, 18, 20, 16, 29, 8, 7, 32, 2, 0, 18], 
                        [16, 8, 6, 7, 12, 3, 2, 2, 8, 10, 15, 17, 20, 18, 0]]

matriz_demanda = [[0, 400, 200, 60, 80, 150, 75, 75, 30, 160, 30, 25, 35, 0, 0],
                [400, 0, 50, 120, 20, 180, 90, 90, 15, 130, 20, 10, 10, 5, 0],
                [200, 50, 0, 40, 60, 180, 90, 90, 15, 45, 20, 10, 10, 5, 0],
                [60, 120, 40, 0, 50, 100, 50, 50, 15, 240, 40, 25, 10, 5, 0],
                [80, 20, 60, 50, 0, 50, 25, 25, 10, 120, 20, 15, 5, 0, 0],
                [150, 180, 180, 100, 50, 0, 100, 100, 30, 880, 60, 15, 15, 10, 0],
                [75, 90, 90, 50, 25, 100, 0, 50, 15, 440, 35, 10, 10, 5, 0],
                [75, 90, 90, 50, 25, 100, 50, 0, 15, 440, 35, 10, 10, 5, 0],
                [30, 15, 15, 15, 10, 30, 15, 15, 0, 140, 20, 5, 0, 0, 0],
                [160, 130, 45, 240, 120, 880, 440, 440, 140, 0, 600, 250, 500, 200, 0],
                [30, 20, 20, 40, 20, 60, 35, 35, 20, 600, 0, 75, 95, 15, 0],
                [25, 10, 10, 25, 15, 15, 10, 10, 5, 250, 75, 0, 70, 0, 0],
                [35, 10, 10, 10, 5, 15, 10, 10, 0, 500, 95, 70, 0, 45, 0],
                [0, 5, 5, 5, 0, 10, 5, 5, 0, 200, 15, 0, 45, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

station_coordinates = [[-46.449444, -25.874734], [-46.350297, -25.973882], [-46.216734, -25.977159], [-46.349477, -26.083682], [-46.506802, -26.083682], [-46.217553, -26.08614], [-45.884057, -26.218064], [-46.09956, -26.218883], [-45.836531, -26.08532], [-45.978288, -26.376208], [-46.04466, -26.461426], [-46.38635, -26.331961], [-45.936499, -26.504035], [-45.855378, -26.439302], [-45.9873, -26.084501]] 

timeInicio = datetime.now()
tiempoFaltanteporSimular=1980 
vPasajeros=[]
for i in range(len(matriz_demanda)):
    for j in range(len(matriz_demanda[i])):
        if matriz_demanda[i][j] == 0: continue
        numero_usuarios=matriz_demanda[i][j]
        intervaloLLegada=3600/numero_usuarios #Segundos por pasajero
        tiempoLlegada=0 #Se asume que empiezan a llegar hasta que el primer bus aparece
        for k in range(numero_usuarios):
            tiempoLlegada+=intervaloLLegada
            if tiempoLlegada >= matrizhoraAperturaArco[i][j]*60:
                vPasajeros.append(Passenger(tiempoLlegada,i,j))
        usuariosFaltantes=int(tiempoFaltanteporSimular/intervaloLLegada)
        for k in range(usuariosFaltantes):
            tiempoLlegada+=intervaloLLegada
            vPasajeros.append(Passenger(tiempoLlegada,i,j))

pasajeros_primera_hora = list(filter(lambda x: x.tiempoLlegadaEstacionInicio <= 3600, vPasajeros))

print("Pasajeros primera hora: ", len(pasajeros_primera_hora))
print("Pasajeros totales: ", len(vPasajeros))