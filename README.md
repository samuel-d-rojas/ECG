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
    <img src="https://github.com/user-attachments/assets/e062d3cb-64a8-41b9-9579-fd5a4ab1fb72" alt="image" width="200">
</p>


<p align="center">
    <img src="https://github.com/user-attachments/assets/c47169de-8cbf-46f9-b85e-9a7aa3316ed3" alt="image" width="400">
</p>




### Filtros Digitales

### intervalos R-R

_ _ _
## d. Análisis de la HRV en el dominio del tiempo


_ _ _
## e. Aplicación de transformada Wavelet


_ _ _

## Bibliografias

_ _ _
