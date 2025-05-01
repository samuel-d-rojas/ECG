# Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet   
 LABORATORIO - 5 PROCESAMIENTO DIGITAL DE SEÑALES

## Requisitos
- Python 3.12
- STM32 CubeMX Y CubeIDE
- MATLAB
## Bibliotecas necesarias Python:
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
La variabilidad de la frecuencia cardíaca (HRV) es un parámetro fisiológico de gran relevancia en la evaluación no invasiva de la función del sistema nervioso autónomo. A través del análisis de las fluctuaciones en los intervalos entre latidos consecutivos del corazón (intervalos R-R), es posible inferir la influencia relativa de las ramas simpática y parasimpática sobre la actividad cardíaca. 

En el presente laboratorio, se realiza un estudio detallado de la HRV empleando la transformada wavelet, una técnica que permite observar cómo varían las componentes frecuenciales de la señal en función del tiempo. La práctica se estructura en varias etapas planteadas en el siguiente diagrama de flujo:

<p align="center">
    <img src="Blank board.png" alt="imagen" width="400">
</p>

## a. Fundamento teórico
La variabilidad de la frecuencia cardíaca (HRV) es una medida del intervalo de tiempo entre latidos consecutivos del corazón, conocidos como intervalos R-R. Esta métrica refleja la influencia del sistema nervioso autónomo (SNA) sobre el corazón y se utiliza como un indicador de la regulación autonómica y el equilibrio entre los sistemas simpático y parasimpático.
## - Sistema Nervioso Autónomo: Actividad Simpática y Parasimpática
El sistema nervioso simpático se asocia con respuestas de "lucha o huida", aumentando la frecuencia cardíaca y reduciendo la HRV. Por el contrario, el sistema nervioso parasimpático promueve estados de "reposo y digestión", disminuyendo la frecuencia cardíaca y aumentando la HRV. La HRV, por tanto, sirve como un marcador del tono autonómico y del estado fisiológico del individuo.
## - Variabilidad de la Frecuencia Cardíaca (HRV)
La HRV se evalúa midiendo las fluctuaciones en los intervalos R-R del electrocardiograma (ECG). El análisis puede realizarse en el dominio del tiempo que calcula parámetros estadísticos como la media y la desviación estándar de los intervalos R-R. Y tambien el el dominio de la frecuencia donde se estudian componentes de baja frecuencia (LF: 0.04–0.15 Hz) relacionadas con ambas ramas del SNA, y de alta frecuencia (HF: 0.15–0.4 Hz), vinculadas principalmente al tono parasimpático.
## - Transformada Wavelet
La Transformada Wavelet es una herramienta matemática que permite analizar señales no estacionarias, como el ECG, descomponiéndolas en componentes de tiempo y frecuencia simultáneamente. A diferencia de la transformada de Fourier, que proporciona una visión global del espectro de frecuencia, la wavelet permite localizar cambios específicos en el tiempo.

Wavelet continua (CWT): ideal para análisis detallado y visualización de espectrogramas.

Wavelet discreta (DWT): adecuada para descomposición jerárquica multirresolución.

Al extraer los intervalos R-R y analizarlos con la transformada wavelet, se puede observar cómo las bandas LF y HF evolucionan en el tiempo. Esto permite detectar de forma precisa transiciones fisiológicas, como cambios de postura, respiración controlada o respuesta al estrés. El uso de wavelets en el análisis de HRV proporciona una caracterización rica y detallada del comportamiento autonómico, permitiendo la evaluación de la dinámica simpático-parasimpática en condiciones fisiológicas o patológicas.
_ _ _
## b. Adquisición de la señal ECG

  ```MATLAB
  sp = serialport("COM5",115200);
    sp.Timeout = 1;
    flush(sp);
    fid = fopen("ecg.txt","w");
   T = 300;     
    t0 = tic;
    buf = zeros(1,500,"uint8");
```
Para la adquisicion de la señal se utilizo el microcontrolador stm32f103c8t6 el cual se le pogramo la comunicacion serial y el ADC atravez de STM32 CubeIde y Cube MX , en el cual se planteo el Timer (Frecuencia de muestreo (400Hz)),y Baud Rate (115200 bps) el cual es favorece en la calidad de los datos capturados es importante "Es importante configurar la misma cantidad de Baudios en CubeMX y en MATLAB".Despues de esto ya puede pogrmar la captura de la señal en MATLAB atravez de la comunicacion serial

  ```MATLAB
    while toc(t0)<T
% Leer,filtrar y guadar los datos
        n = sp.NumBytesAvailable;
        if n>0
            datos = read(sp,n,"uint8");
            fprintf(fid,"%u\n",datos);
            buf = [buf(length(datos)+1:end), datos];
            filt = movmean(buf,5);
        end
        % Graficar Señal Suavizada
        set(hRaw, "YData", buf);
        set(hFilt,"YData", filt);
        drawnow limitrate
    end
```
A través de este bucle realizamos la captura y visualización en tiempo real de la señal: cada vez que llegan nuevas muestras del ECG, se guardan en el archivo y se incorporan al buffer; luego las suavizamos con un promedio móvil (filtro que reemplaza cada punto por el promedio de él y sus próximos puntos) de cinco muestras para eliminar el ruido de alta frecuencia, y finalmente actualizamos la gráfica al instante para ver cómo evoluciona la señal.


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

En este codigo se carga y grafica una señal de electrocardiograma. Primero, se define la frecuencia de muestreo fs como 400 Hz. Luego, se lee el archivo ecg.txt que contiene los datos del ECG en formato numérico. La señal se convierte de valores digitales a milivoltios utilizando la fórmula (s * 3.3 * 1000) / 4095, donde 3.3V es el voltaje de referencia. Se crea un vector de tiempo que asigna un instante temporal a cada muestra en función de la frecuencia de muestreo. Finalmente, se grafica toda la señal.

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
    b, a = butter(1, [1 / (fs / 2), 160 / (fs / 2)], btype='band')
    eq = f"y[n] = ({b[0]:.3f} * x[n] + {b[1]:.1f} * x[n-1] - {a[1]:.3f} * y[n-1])"
    
    print("Ecuación en diferencias:", eq)
    return lfilter(b, a, señal)

señal_filtrada = filtro(fs, señal)
plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal_filtrada[:], color="b")
```
$$
y[n] = 0.750 * x[n] + 0.00 * x[n-1] - 0.477 * y[n-1]
$$

<p align="center">
    <img src="https://github.com/user-attachments/assets/8371c896-1ab2-4246-989a-d33b9380647d" alt="image" width="400">
</p>

Este código aplica un filtro pasa banda de Butterworth de primer orden a la señal ECG, eliminando el ruido fuera del rango de 1 a 160 Hz. Se grafica la señal resultante en color azul, permitiendo visualizar la señal ya filtrada. Se seleccionó este rango de frecuencias porque abarca la actividad cardíaca más importante, incluyendo las ondas P, QRS y T, que son fundamentales para el análisis del ritmo cardíaco.
Se utilizó un filtro de primer orden debido a que la señal original no contenía demasiado ruido. Además, debido a que se trata de un filtro IIR, aumentar el orden podría provocar un comportamiento inestable, lo que afectaría significativamente la señal de salida.
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
t = t_picos[1:]

plt.figure(figsize=(15, 8))
plt.plot(t[:-1], intervalo, marker='o', linestyle='-', color='k')
plt.title('Señal Basada en Intervalos R-R')
plt.xlabel('Tiempo en el que Sucede Cada Pico R (s)')
plt.ylabel('Intervalo R-R (s)')
plt.grid()
```
<p align="center">
    <img src="https://github.com/user-attachments/assets/bc6928f9-4b15-4049-9039-33ae1cca1643" alt="image" width="400">
</p>


Esta parte del código se encarga de graficar la señal basada en los intervalos R-R, que representan las diferencias de tiempo entre los picos R detectados en la señal ECG. La variable t se define como todos los tiempos de los picos R, excepto el primero (t_picos[1:]), ya que este primer pico no corresponde a un verdadero pico R, sino que posiblemente es un artefacto generado por la respuesta inicial del filtro IIR. A continuación, se genera una gráfica donde el eje X representa el instante de tiempo en el que ocurre cada pico R y el eje Y muestra la duración del intervalo R-R correspondiente. Esta visualización permite analizar la variabilidad del ritmo cardíaco a lo largo del tiempo.


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
Este fragmento de código realiza cálculos estadísticos sobre los intervalos R-R de la señal ECG, con el objetivo de analizar la variabilidad en los tiempos entre latidos. Para ello, se calcula la media y la desviación estándar de los intervalos R-R, proporcionando una visión general del valor promedio de los intervalos y de la dispersión de estos. Además, se incluyo el calculo del RMSSD (Root Mean Square of Successive Differences), una medida que evalúa los cambios rápidos en la variabilidad de los intervalos. Un valor mayor de RMSSD indica que el corazón es más capaz de adaptarse a cambios rápidos.

$$
\text{Media de los Intervalos R-R:} \ 0.793 \ \text{segundos}
$$

$$
\text{Desviación Estándar de los Intervalos R-R:} \ 0.1366 \ \text{segundos}
$$

$$
\text{RMSSD:} \ 0.106 \ \text{segundos}
$$


Esto indica que en promedio, hay aproximadamente 0.7358 segundos entre cada latido, lo que equivale a una frecuencia cardíaca promedio de aproximadamente 81.5 latidos por minuto (bpm), calculada como:

$$
\frac{60}{0.7358} = 81.5
$$

Este valor se encuentra dentro del rango normal en reposo (60–100 bpm), lo que sugiere un ritmo cardíaco saludable.

La desviación estándar obtenida refleja una variabilidad moderada en los intervalos entre latidos. Un valor más alto podría indicar un ritmo irregular dependiendo el contexto, aunque también puede interpretarse como una buena capacidad de adaptación del corazón a diferentes situaciones, como cambios posturales, respiración o estrés. Por otro lado, una desviación estándar muy baja podría sugerir rigidez en la respuesta del sistema nervioso autónomo. En este caso, el valor indica una variabilidad fisiológica razonable, lo que también es señal de una buena regulación del ritmo cardíaco [1].


_ _ _
## e. Aplicación de transformada Wavelet


_ _ _

## Bibliografias
[1] J. Ortiz y D. Mendoza, "Variabilidad de la frecuencia cardiaca, una herramienta útil," Revista Digital Buenos Aires, vol. 13, no. 121, pp. 35–56, 2008. [En línea]. Disponible en: https://www.efdeportes.com/efd121/variabilidad-de-la-frecuencia-cardiaca-una-herramienta-util.htm

_ _ _
