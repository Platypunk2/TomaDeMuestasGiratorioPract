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
usage: IntentiPractGiratorio1.py [-h] Grados Vueltas Carpeta

Script preparado para utilizar el brazoGiratorio. Se toman mediciones mientras el brazo este girando X grados,
se empieza a adquirir los datos y despues se envia la instruccion de mover. Se detiene la adquisicion, cuando
el aruduino retorna el termino de recorrer los X grados y se Plotea un grafico con "Matplotlib". Se repiten 
X numero de vueltas indicadas en parametros, y se plotean ensima de la anterior.
Para aprovechar la obligatoria vuelta en sentido antihoraria para desenrollar los cables, se aprovecha de adquirir
muestras OBLIGACION de controlar en processing esto, ya que hay que invertir el arreglo. Se envian los caracteres 
N/O para enviar al brazoGiratorio X grados a mover (obtenidos en parametros) en un sentido o en otro.
'./[NombreCarpetaParametro]/vuelta_###.csv'

Example: "IntentiPractGiratorio1.py 360 250 ./Mediciones_exterior"

positional arguments:
  Grados      Grados a mover el brazoGiratorio con las instrucciones N/O del arduino.
  Vueltas     Numero de vueltas que se quieren hacer, recomendacion siempre utilizar
              un numero par, esto debido a que asi los cables no se enrollan entre una
              tanda de medicion y otra inmediatamente continua.
  Carpeta     Nombre o ruta de la carpeta donde se guardaran los archivos.
              En caso de no existir la carpeta se crea automaticamente.

optional arguments:
  -h, --help  show this help message and exit

```

## Elementos extras

* Power Meter

![image](https://user-images.githubusercontent.com/90724923/180317810-1f942937-644c-408d-a36d-47d258273130.png)

* Arduino

![image](https://user-images.githubusercontent.com/90724923/181277746-ffa97a9c-0b40-44a6-a352-9bde4f12fa30.png)

