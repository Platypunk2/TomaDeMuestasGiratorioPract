<br />
<div align="center">

  <h3 align="center">Toma de Muestras de Antena Girando para Hacer Diagrama de Radiación</h3>

  <p align="center">
    con Python
  </p>
</div>

## Descripción

En este trabajo se busca la caracterización de una antena mediante la realizacion de diagramas de radiación, para ello se implemento un sistema que va a ir rotando con una antena receptora. Se registraran los datos correspondientes de las mediciones y se procede a realizar los diagramas de radiación.

### 🛠 Construído con:

* [Arduino](https://arduino.cl)
* [Python](https://www.python.org)

## Sobre el código

El código fue creado para lograr hacer mediciones de una antena rotando en su propio eje para lograr caracterizar el diagrama de radiación de la antena. Para realizar esto se implementaron tres codigos, de los cuales se explicaran dos, el del arduino y el de la toma de muestras junto con la vista del diagrama de radiación.

### Arduino

El código arduino es simple, se implementaron 6 casos dependiendo del input del usuario:

* **G**: Permite hacer girar a 360° en sentido horario.
* **H**: Permite hacer girar a 360° en sentido antihorario.
* **Nn\r**: Permite hacer girar a n° en sentido horario, siendo n un grado entre 1.8 a 360.
* **On\r**: Permite hacer girar a n° en sentido antihorario, siendo n un grado entre 1.8 a 360.
* **E**: Permite girar en sentido horario un solo grado.
* **F**: Permite girar en sentido antihorario un solo grado.

Se implemento una funcion de la cual, entregando una cantidad de grados y una velocidad, pemite hacer funcionar el motor para que la antena logre rotar la cantidad de grados insertada.

### Código toma de muestras

El código, a diferencia del arduino, es complicado y funciona derrepente, me explico. Como se habia visto en el repositorio [Toma de Muestras PM002](https://github.com/Platypunk2/TomaMuestrasRFPowerMeter002), para que funcione la antena se tiene que dejar un tiempo para que el buffer logre prender y funcionar correctamente, en este caso no fue la excepeción y, ademas, se tuvo que añadir ciertos time.sleep() porque el buffer fallaba muy seguido al insertar datos muy rápido. Pese a implementar esto ultimo, no se logro hacer que el código funcionara en el 100% de las muestras, pero que si detecatara cuando una vuelta estuviera mala y no tomar esta en cuenta para el diagrama de radiación, junto con catalogar el .csv de sus datos con una "R", significando esta raro, se realizo con el objetivo de, cuando se terminen de realizar todas las muestras, revisar esos datos y encontrar porque estos no funcionan para el analizis de la antena.

El código posee tres clases, las cuales son Controlador, Arduino y Archivo:

* **Controlador**: En esta se crearon los metodos necesarios para capturar los datos de la antena y poder manipular lo que se escribe y lee del buffer por parte del PowerMeter002.
* **Arduino**: El arduino posee los metodos correspondientes a las rotaciones posibles que puede realizar la antena, esto incluye los comandos dichos en la sección Arduino de este repositorio.
* **Archivo**: En esta clase se provee de los aspectos necesarios para crear los csv junto con el guardado de estos en la carpeta dada como parametro de inicio al ejecutar el código.

Aparte de poseer estas clases existe una funcion llamada **initvalues()** que lo unico que hace es inicializar unos valores que se ocupan constantemente en cada vuelta de medición que se hace.

Con respecto a la vueltas, se toma como una vuelta dos iteraciones, un giro horario y otro giro antihorario, esto se hace para que los cables ocupado no se enreden. En cada rotacion que haga la antena, horario o antihorario, se toman medidas para realizar el diagrama de radiación, el cual se va a ir graficando a medido que se logren rotaciones utiles que pasen por los filtros puestas para certificar la integridad de los datos. Los diagrmas generados no se deben de cerrar hasta que terminen todas las vueltas solicitadas, además de que cada rotacion lograda se va a solapar sobre la medicion anterior, sin borrarla claramente, esto se hace para poder ver un promedio de comportamiento de la antena con respecto a las medidas.

Al finalizar el código se deberian de haber creado una cantidad de .csv igual a la cantidad de vueltas solicitadas x2.

Si se quiere saber mas sobre el código, tambien se pueden leer los comentarios dejados en este mismo, donde se explican algunas secciones o lineas de código.


## :shipit: Instalación

Para lograr ejecutar el codigo se necesitan tener en consideracion los siguientes elementos:

### Pre-Requisitos

Tener Python instalado junto a las siguientes librerias
* [Installation Guide Python](https://www.python.org/downloads/)
* [Installation Guide Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
* [Installation Guide Pyserial](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)
* [Installation Guide Numpy](https://numpy.org/install/)

se utilizo la version actual de python (v3.8.10) para este proyecto, junto con matplotlib v3.5.2, pyserail v3.5 y numpy v1.23.1

### Ejecución

Para ejecutar el código se debe ir por medio de la terminal a la carpeta donde esta el código python y realizar los chmod 666 correspondientes a los puertos seriales que se quieren ocupar. En el caso de mi computador fueron el ttyUB0 (Identificando al PowerMeter002) y el ttyACM0, tambien puede ejecutar con el comando sudo, pero esto implicaria haber realizado las instalaciones anteriores con pip tambien aplicando el super usuario. Al ya estar en la carpeta del código se recomienda aplicar el siguiente comando:}

```curl
python3 IntentiPractGiratorio1.py -h
```

Este despliegara el siguiente texto donde se explican las variables para realizar la ejecución y algunos datos importantes a considerar con respecto al código y el proceso que realiza este mismo.

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
Al ya haber entendido solo faltaria ejecutar el código correctamente, esto implica:

```curl
python 3 IntentiPractGiratorio1.py <cantidad de grados de rotacion por vuelta> <cantidad de vueltas que se quieren relaizar> <./nombre de la carpeta donde se quiere guardar los .csv>
```

Y listo, el código deberia ya estar ejecutandose, y recuerda que si se demora al iniciar estimadamente unos 6 segunos, es por los time.sleep() implementados para abrir el buffer del Arduino y del PowerMeter002.


## Elementos extras

* Power Meter

![image](https://user-images.githubusercontent.com/90724923/180317810-1f942937-644c-408d-a36d-47d258273130.png)

* Arduino

![image](https://user-images.githubusercontent.com/90724923/181277746-ffa97a9c-0b40-44a6-a352-9bde4f12fa30.png)

