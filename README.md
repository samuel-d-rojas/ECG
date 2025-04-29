# Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet   
 LABORATORIO - 5 PROCESAMIENTO DIGITAL DE SEÑALES

## Requisitos
- Python 3.12
- STM32 CubeMX Y CubeIDE
- MATLAB
 - Bibliotecas necesarias Python:
  - numpy
  - matplotlib
  - scipy

  ```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import find_peaks
from scipy.signal import cwt, ricker
```

 _ _ _
## Introducción
La variabilidad de la frecuencia cardíaca (HRV) representa una medida esencial para evaluar el estado de regulación del corazón por parte del sistema nervioso autónomo, en donde se equilibran las respuestas simpáticas y parasimpáticas. Analizar estas variaciones permite observar cómo el cuerpo responde a diferentes condiciones fisiológicas y detectar posibles disfunciones. En este laboratorio, se analizará el comportamiento de la HRV utilizando la transformada wavelet. Esta técnica permite descomponer la señal cardíaca y observar su evolución en el tiempo y en diferentes escalas de frecuencia.

La práctica incluirá la recolección de señales ECG en estado de reposo y condiciones controladas, su posterior limpieza mediante filtros digitales, la extracción de intervalos R-R y el análisis cuantitativo de los datos en el dominio del tiempo y tiempo-frecuencia.
_ _ _

## a. Fundamento teórico


_ _ _
## b. Adquisición de la señal ECG



_ _ _
## c. Pre-procesamiento de la señal

### Cargar Señal de ECG

 ```python
fs = 400
s = np.loadtxt("ecg.txt")
señal = (s*3.3*1000)/4095 #conversion a mv
tiempo = (np.arange(len(señal)) / fs)

plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal[:],color="r")
```
<p align="center">
    <img src="https://github.com/user-attachments/assets/e062d3cb-64a8-41b9-9579-fd5a4ab1fb72" alt="image" width="400">
</p>

Este fragmento de codigo carga y grafica una señal de electrocardiograma. Primero, se define la frecuencia de muestreo fs como 400 Hz. Luego, se lee el archivo ecg.txt que contiene los datos del ECG en formato numérico. La señal se convierte de valores digitales a milivoltios utilizando la fórmula (s * 3.3 * 1000) / 4095, donde 3.3V es el voltaje de referencia. Se crea un vector de tiempo que asigna un instante temporal a cada muestra en función de la frecuencia de muestreo. Finalmente, se grafica toda la señal.

 ```python
plt.figure(figsize=(15, 8))
plt.plot(tiempo[:2000], señal[:2000],color="r")
```
En el código anterior se realiza una modificación para mostrar en lugar de la señal completa, únicamente las primeras 2000 muestras de la señal. Esto permite apreciar mejor las primeras ondas del ECG.

<p align="center">
    <img src="https://github.com/user-attachments/assets/c47169de-8cbf-46f9-b85e-9a7aa3316ed3" alt="image" width="400">
</p>


___
### Filtros Digitales

 ```python
def filtro(fs, señal):
    b, a = butter(1, [1 / (fs / 2), 50 / (fs / 2)], btype='band')
    eq = f"y[n] = ({b[0]:.3f} * x[n] + {b[1]:.1f} * x[n-1] - {a[1]:.3f} * y[n-1])"
    
    print("Ecuación en diferencias:", eq)
    return lfilter(b, a, señal)

señal_filtrada = filtro(fs, señal)
plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal_filtrada[:], color="b")
```
$$
y[n] = 0.496 * x[n] + 0.00 * x[n-1] - 0.992 * y[n-1]
$$

<p align="center">
    <img src="https://github.com/user-attachments/assets/8371c896-1ab2-4246-989a-d33b9380647d" alt="image" width="400">
</p>

Este código aplica un filtro pasa banda de Butterworth de primer orden a la señal ECG, eliminando el ruido fuera del rango de 1 a 100 Hz. Se grafica la señal resultante en color azul, permitiendo visualizar la señal ya filtrada. Se seleccionó este rango de frecuencias porque abarca la actividad cardíaca más importante, incluyendo las ondas P, QRS y T, que son fundamentales para el análisis del ritmo cardíaco.
Se utilizó un filtro de primer orden debido a que la señal original no contenía demasiado ruido. Además, ya que que se trata de un filtro IIR, aumentar el orden podría provocar un comportamiento inestable, lo que afectaría significativamente la señal de salida.
Finalmente, se muestra la ecuación en diferencias del filtro. Al ser de primer orden la ecuación es relativamente sencilla, lo que facilita su implementación.


 ```python
señal_filtrada = filtro(fs, señal)
plt.figure(figsize=(15, 8))
plt.plot(tiempo[:2000], señal_filtrada[:2000], color="b")
```
Se muestran las primeras 2000 muestras de la señal filtrada.

<p align="center">
    <img src="https://github.com/user-attachments/assets/86dc153e-a8e9-49d8-baf6-4555f6455988" alt="image" width="400">
</p>

___
### Intervalos R-R


 ```python
height = 84
distance = fs * 0.1
peaks, _ = find_peaks(señal_filtrada[:], height=height, distance=distance)
t_picos = peaks / fs
intervalo = np.diff(t_picos)
peaks = peaks[1:]
intervalo = intervalo[1:]

plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal_filtrada[:], label='ECG filtrado', color='b')
plt.title('ECG, Picos R')
plt.plot(tiempo[peaks], señal_filtrada[peaks], 'ro', label='Picos R detectados')
plt.legend()
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (mv)')
plt.grid()
```
<p align="center">
    <img src="https://github.com/user-attachments/assets/0bfd822f-2777-4e32-9b5a-dac5aa7d92e7" alt="image" width="400">
</p>

Este fragmento de código se utiliza para detectar y marcar los picos R en la señal ECG filtrada. Se definen dos parámetros clave: height, que establece el umbral mínimo de altura para que un valor sea considerado un pico (en este caso, 84 mV), y distance, que determina la distancia mínima entre picos, establecida en fs * 0.1 para asegurar que los picos estén suficientemente separados. Usando la función find_peaks, se identifican los índices de los picos R en la señal, y luego se calcula el tiempo de cada pico dividiendo estos índices por la frecuencia de muestreo fs. Además, se calculan los intervalos entre los picos en segundos. Finalmente, se grafica la señal ECG filtrada y se destacan los picos R detectados con puntos rojos.

 ```python
peaks, _ = find_peaks(señal_filtrada[:2000], height=height, distance=distance)

plt.figure(figsize=(15, 8))
plt.plot(tiempo[:2000], señal_filtrada[:2000], label='ECG filtrado', color='b')
```
Se muestran las primeras 2000 muestras de la señal filtrada con los picos R.

<p align="center">
    <img src="https://github.com/user-attachments/assets/61f85d40-4613-473f-8230-26d0bc8c8390" alt="image" width="400">
</p>

#### Señal Obtenida Apartir de los Intervalos R-R

 ```python
latidos = np.arange(1, len(intervalo)+1)

plt.figure(figsize=(15, 8))
plt.plot(latidos, intervalo, marker='o', linestyle='-', color='k')
plt.title('Señal Basada en Intervalos R-R')
plt.xlabel('Número de Latidos')
plt.ylabel('Intervalo R-R (s)')
plt.grid()
```
<p align="center">
    <img src="https://github.com/user-attachments/assets/334731dc-71aa-422c-b9dd-03f9fb394aac" alt="image" width="400">
</p>

Ahora se grafican los intervalos R-R, que representan el tiempo entre dos latidos sucesivos del corazón. Para ello, primero se genera un arreglo llamado latidos, que contiene una secuencia de números que corresponden al número de latidos, basado en el número de intervalos calculados. Luego, se crea una gráfica donde el eje x representa el número de latidos y el eje y muestra los intervalos R-R en segundos.


_ _ _
## d. Análisis de la HRV en el dominio del tiempo

 ```python
diffs = np.diff(intervalo)
squared_diffs = diffs ** 2
mean_squared_diffs = np.mean(squared_diffs)
rmssd = np.sqrt(mean_squared_diffs)
media = np.mean(intervalo)
desviacion = np.std(intervalo, ddof=1)

print('Media de los Intervalos R-R:', round(media, 4) , "segundos")
print('Desviación Estandar de los Intervalos R-R:', round(desviacion, 4), "segundos")
print("RMSSD:", round(rmssd, 4), "segundos")
```
$$
\text{Media de los Intervalos R-R:} \ 0.7358 \ \text{segundos}
$$

$$
\text{Desviación Estándar de los Intervalos R-R:} \ 0.0967 \ \text{segundos}
$$

$$
\text{RMSSD:} \ 0.1203 \ \text{segundos}
$$

Este fragmento de código realiza cálculos estadísticos sobre los intervalos R-R de la señal ECG, con el objetivo de analizar la variabilidad en los tiempos entre latidos. Para ello, se calcula la media y la desviación estándar de los intervalos R-R, proporcionando una visión general del valor promedio de los intervalos y de la dispersión de estos. Además, se calcula el RMSSD (Root Mean Square of Successive Differences), una medida que evalúa los cambios rápidos en la variabilidad de los intervalos. Un valor mayor de RMSSD indica que el corazón es más capaz de adaptarse a cambios rápidos.

Esto indica que, en promedio, hay aproximadamente 0.7358 segundos entre cada latido, lo que equivale a una frecuencia cardíaca promedio de aproximadamente 81.5 latidos por minuto (bpm), calculada como 
$$
60/0.7358
$$.
Este valor se encuentra dentro del rango normal en reposo (60–100 bpm), lo que sugiere un ritmo cardíaco saludable.

La desviación estándar obtenida refleja una variabilidad moderada en los intervalos entre latidos. Un valor más alto podría indicar un ritmo irregular, aunque también puede interpretarse como una buena capacidad de adaptación del corazón a diferentes situaciones, como cambios posturales, respiración o estrés. Por otro lado, una desviación estándar muy baja podría sugerir rigidez en la respuesta del sistema nervioso autónomo. En este caso, el valor indica una variabilidad fisiológica razonable, lo que también es señal de una buena regulación del ritmo cardíaco.


_ _ _
## e. Aplicación de transformada Wavelet


_ _ _

## Bibliografias

_ _ _
