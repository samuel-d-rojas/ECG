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
y[n] = 0.288\, x[n] + 0.00\, x[n-1] + 1.414\, y[n-1]
$$

<p align="center">
    <img src="https://github.com/user-attachments/assets/8371c896-1ab2-4246-989a-d33b9380647d" alt="image" width="400">
</p>


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
\text{Media de los Intervalos R-R:} \ 0.793 \ \text{segundos}
$$

$$
\text{Desviación Estándar de los Intervalos R-R:} \ 0.1367 \ \text{segundos}
$$

$$
\text{RMSSD:} \ 0.1065 \ \text{segundos}
$$



_ _ _
## e. Aplicación de transformada Wavelet


_ _ _

## Bibliografias

_ _ _
