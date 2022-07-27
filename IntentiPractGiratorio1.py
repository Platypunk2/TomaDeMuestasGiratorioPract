from __future__ import division
import time
import sys
import serial
import os
import math
import datetime as dt
from threading import Timer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
#--------------------------- HELP MENU------------
import argparse

parser = argparse.ArgumentParser(description='Script preparado para utilizar el brazoGiratorio. Se toman mediciones mientras el brazo este girando X grados,\nse empieza a adquirir los datos y despues se envia la instruccion de mover. Se detiene la adquisicion, cuando\nel aruduino retorna el termino de recorrer los X grados y se Plotea un grafico con \"Matplotlib\". Se repiten \nX numero de vueltas indicadas en parametros, y se plotean ensima de la anterior.\nPara aprovechar la obligatoria vuelta en sentido antihoraria para desenrollar los cables, se aprovecha de adquirir\nmuestras OBLIGACION de controlar en processing esto, ya que hay que invertir el arreglo. Se envian los caracteres \nN/O para enviar al brazoGiratorio X grados a mover (obtenidos en parametros) en un sentido o en otro.\n\'./[NombreCarpetaParametro]/vuelta_###.csv\'\n\nExample: \"rfpm002-cp_us_Giratorio_Cont_graph.py 360 250 ./Mediciones_exterior\"', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("Grados", help="Grados a mover el brazoGiratorio con las instrucciones N/O del arduino.")
parser.add_argument("Vueltas", help="Numero de vueltas que se quieren hacer, recomendacion siempre utilizar\nun numero par, esto debido a que asi los cables no se enrollan entre una\ntanda de medicion y otra inmediatamente continua.")
parser.add_argument("Carpeta", help="Nombre o ruta de la carpeta donde se guardaran los archivos.\nEn caso de no existir la carpeta se crea automaticamente.")

args = parser.parse_args()
#---------------------------------------------------

class Controlador():
    def __init__(self):
        #caso linux
        puerto = [x for x in os.listdir('/dev') if x[:6]=='ttyUSB'][0]
        puerto = "/dev/"+puerto
        #caso windows
        #puerto = 'COM4'
        try:
            #En esta primera parte se dictan los parametros necesarios para abrir el puerto y se pueda leer y escribir en el Power Meter
            self.ser = serial.Serial(
            port=puerto,
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            )
            if(not self.ser.isOpen()):
                self.ser.open()

            time.sleep(3) #ESTE TIME ES LA PIEZA MAS FUNDAMENTAL DE ESTE CODIGO, SI LO QUITAN NO COMPILA
        except Exception as e:
            raise Exception("Error al incializar puerto: " + str(e))

        #self.ser.flushInput()

    
    #Estos 4 metodos son comandos basicos para pyserial que permiten la escritura, lectura, contar elementos del buffer y cerrar el puerto.
    def Escribir(self,instr):
        self.ser.write(instr.encode())
        
    def ContInput(self):
        return self.ser.inWaiting()

    def ContRead(self):
        return self.ser.readline()

    def Flush(self):
        self.ser.flush()

    def FlushInput(self):
        self.ser.flushInput()

    def End(self):
        self.ser.close()

#Esta clase fue creada con el proposito de crear el archivo .csv lo mas simple y ordenadamente como se era posible

class Arduino():
    def __init__(self):
        #caso linux
        puerto=[x for x in os.listdir('/dev') if x[:6]=='ttyACM'][0]
        puerto = '/dev/'+puerto
        #caso windows
        try:
            self.arduino= serial.Serial(puerto,
            baudrate=115200
            )
            if(not self.arduino.isOpen()):
                self.arduino.open()

            time.sleep(3)
        except Exception as e:
            raise Exception("Error al incializar puerto: " + str(e))

    def Escribir(self,instr):
        self.arduino.write(instr.encode())
    
    def ContRead(self):
        return str(self.arduino.readline())

    def ContInput(self):
        return self.arduino.inWaiting()

    def FlushInput(self):
        self.arduino.flushInput()

    def Vuelta360A(self):
        self.Escribir('H')

    def Vuelta360H(self):
        self.Escribir('G')

    def XgradosH(self, grados):
        self.Escribir('N'+grados+'\r')

    def XgradosA(self, grados):
        self.Escribir('O'+grados+'\r')

    def UnGradoH(self):
        self.Escribir('E')

    def UnGradoA(self):
        self.Escribir('F')

    def Flush(self):
        self.arduino.flush()

    def End(self):
        self.arduino.close()
        

class Archivo():
    def __init__(self, carpeta, narch):
        self.save = open(carpeta + narch, 'w')
    
    #Consta de dos clases que son solo para escribir y cerrar el archivo.
    def Escribir(self,tiempo,potencia):
        self.save.write(str(tiempo)+','+str(potencia)+'\n')


    def Cerrar(self):
        self.save.close()
    
    def Renombrar(self):
        return



def initvalues(Pw):
    global meanpotencia, maxPeak, potenciaold, muestras, oldtiempo, valid, verificador, VueltaTerminada, VecPotencia, vale
    meanpotencia = 0
    maxPeak = 0
    potenciaold=-100
    muestras = 0
    oldtiempo = 0
    valid = False
    verificador = 0
    VueltaTerminada = ""
    Pw.FlushInput()
    VecPotencia = []
    vale = False

Pw = Controlador()
Ardu = Arduino()
novueltas = 0
fallos = []
foldername = "./"+sys.argv[3]+"/"
if(not os.path.exists(foldername)):
    os.mkdir(foldername)
for i in range(int(sys.argv[2])):
    initvalues(Pw)
    filename="vuelta"+str(i).zfill(3)+"Horario.csv"
    file = Archivo(foldername,filename)
    for j in ("c"+'\r'):
        time.sleep(1.5)
        Pw.Escribir(str(j))
    EscrBuffer = 0
    while(not EscrBuffer):
        EscrBuffer = Pw.ContInput()
        #Este while esta puesto solo por seguridad

    Ardu.Vuelta360H()
    Pw.ContRead() #Este se amplica para que no lea la instruccion.
    print("vuelta ",i," a")
    while(Pw.ContInput()>0 and verificador != 13):
        #aquí se realiza la lectura del buffer, los datos se limpian antes de ser verificado
    
        out = str(Pw.ContRead())
        data = out.split(',')
        verificador = len(str(data))
        try:
            tiempo = str(data[0])[2:12]
            potencia = str(data[1])[0:6]
        except:
            print("Se termino una vuelta")
            file.Cerrar()
        try:
            if((int(tiempo) == 0 or vale) and int(oldtiempo)<=int(tiempo)):
                tiempo = int(tiempo)
                potencia = float(potencia)
                VecPotencia.append(potencia)
                oldtiempo = tiempo
                file.Escribir(tiempo, potencia)
                vale = True
            else:
                file.Escribir(tiempo, potencia)
        except:
            print("Se descarta dato o ya no hay datos")
        if(Ardu.ContInput() and not valid):
            print("SE CUMPLIO LA CONDICION")
            valid = True
            Pw.Escribir('\r')
    try:
        VectorPotencias_array=np.asarray(VecPotencia)
        theta=np.arange(0,2*np.pi, (2*np.pi)/len(VectorPotencias_array))
        ax1 = plt.subplot(111, polar = True, facecolor="lightgoldenrodyellow")
        plt.ion()
        plt.rcParams["figure.autolayout"] = True
        r=np.asarray(VecPotencia)
        ax1.plot(theta[0:len(VectorPotencias_array)], r,  color='r', linewidth=3, alpha = 0.150)
        ax1.set_rmin(-70)
        ax1.set_rmax(-15)
        plt.pause(0.01)
        plt.show(block = False)
        plt.draw()
    except: 
        fallos.append(str(i).zfill(3)+"Horario")
        novueltas+=1
    initvalues(Pw)
    filename="vuelta"+str(i).zfill(3)+"Antihorario.csv"
    file = Archivo(foldername,filename)
    print("vuelta ",i," b")
    VueltaTerminada = str(Ardu.ContRead())[2:4]

    for j in ("c"+'\r'):
        time.sleep(1.5)
        Pw.Escribir(str(j))
    Ardu.Vuelta360A()
    Pw.ContRead() #Este se amplica para que no lea la instruccion.
    while(Pw.ContInput()>0 and verificador != 13):
        #aquí se realiza la lectura del buffer, los datos se limpian antes de ser verificado
        out = str(Pw.ContRead())
        data = out.split(',')
        verificador = len(str(data))
        try:
            tiempo = str(data[0])[2:12]
            potencia = str(data[1])[0:6]
        except:
            print("Se termino una vuelta")
            file.Cerrar()
        try:
            if((int(tiempo) == 0 or vale) and int(oldtiempo)<=int(tiempo)):
                tiempo = int(tiempo)
                potencia = float(potencia)
                VecPotencia.append(potencia)
                file.Escribir(tiempo, potencia)
                oldtiempo = tiempo
                vale = True
            else:
                file.Escribir(tiempo, potencia)
        except:
            print("Se descarta dato o ya no hay datos")
        if(Ardu.ContInput() and not valid):
            print("SE CUMPLIO LA CONDICION")
            Pw.Escribir('\r')
            valid = True
    Ardu.ContRead()
    try:
        VectorPotencias_array=np.asarray(VecPotencia)

        theta=np.arange(0,2*np.pi, (2*np.pi)/len(VectorPotencias_array))
        ax1 = plt.subplot(111, polar = True, facecolor="lightgoldenrodyellow")
        plt.ion()
        plt.rcParams["figure.autolayout"] = True
        r=np.asarray(VecPotencia)
        ax1.plot(theta[0:len(VectorPotencias_array)], r[::-1],  color='b', linewidth=3, alpha = 0.150)
        ax1.set_rmin(-70)
        ax1.set_rmax(-15)
        plt.pause(0.01)
        plt.show(block = False)
        plt.draw()
    except:
        fallos.append(str(i).zfill(3)+"AntiHorario")
        novueltas+=1

plt.show(block = True)
print("\nCantidad de vueltas realizadas horario y antihorario: ", int(sys.argv[2])*2 - novueltas)
print("Las vueltas que fallaron son: ", fallos)

for i in fallos:
    old_name = r""
    os.rename(old_name+(foldername+"vuelta"+str(i)+".csv"),old_name+(foldername+"vuelta"+str(i)+"R.csv"))
Pw.End()
Ardu.End()