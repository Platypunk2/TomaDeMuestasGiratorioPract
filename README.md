<br />
<div align="center">

  <h3 align="center">Toma de Muestras de Antena Girando para Hacer Diagrama de Radiación</h3>

  <p align="center">
    con Python
  </p>
</div>

## Descripción


### 🛠 Construído con:

* [Arduino](https://arduino.cl)
* [Python](https://www.python.org)

## Sobre el código


## :shipit: Instalación


### Pre-Requisitos

Tener Python instalado junto a las siguientes librerias
* [Installation Guide Python](https://www.python.org/downloads/)
* [Installation Guide Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
* [Installation Guide Pyserial](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)
* [Installation Guide Numpy](https://numpy.org/install/)

se utilizo la version actual de python (v3.8.10) para este proyecto, junto con matplotlib v3.5.2, pyserail v3.5 y numpy v1.23.1

### Primeros pasos

```curl
usage: RFPM002-cp_us.py [-h] [option] Number Carpeta Archivo

Script para Adquisicion de datos del Power Meter, donde se le pasa por parametro  el tiempo en minutos o el numero de muestras que se quieren tomar.
 Example: "RFPM002-cp_us.py s 1000 ./Mediciones_exterior Posicion1"
 Example: "RFPM002-cp_us.py t 10 ./Mediciones_exterior Posicion1"

positional arguments:
  [option]    s (samples), o 
              t (time).
  Number      for option=s ---> numero de muestras
              for option=t ---> tiempo en minutos.
  Carpeta     Nombre o ruta de la carpeta donde se guardaran los archivos.
              En caso de no existir la carpeta se crea automaticamente.
  Archivo     Nombre del archivo a guardar.

optional arguments:
  -h, --help  show this help message and exit

```

## Elementos extras

* Power Meter

![image](https://user-images.githubusercontent.com/90724923/180317810-1f942937-644c-408d-a36d-47d258273130.png)

* Arduino

![image](https://user-images.githubusercontent.com/90724923/181277746-ffa97a9c-0b40-44a6-a352-9bde4f12fa30.png)

