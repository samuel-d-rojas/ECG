# Señales Electromiográficas EMG  
 LABORATORIO - 4 PROCESAMIENTO DIGITAL DE SEÑALES

## Requisitos
- Python 3.12
- Bibliotecas necesarias:
  - nidaqmx
  - numpy
  - matplotlib
  - scipy
 
 ```python
# Importamos las librerías necesarias
import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.stats import ttest_rel
```

 _ _ _
## Introducción
En este laboratorio, se realizó la adquisición y análisis de señales electromiográficas (EMG) con el objetivo de estudiar la fatiga muscular a través del procesamiento digital de señales. Para ello, se utilizaron electrodos de superficie y un sistema de adquisición de datos (DAQ), permitiendo registrar la actividad eléctrica de los músculos durante una contracción sostenida. Posteriormente, se aplicaron técnicas de filtrado y análisis espectral mediante la Transformada de Fourier (FFT) para identificar cambios en la frecuencia de la señal, lo que permitió evaluar la fatiga en el musculo estudiado.

_ _ _

## 1) Preparación del Sujeto
Se analizó el músculo flexor común de los dedos, encargado de la flexión de los dedos de la mano y fundamental en la prensión y manipulación de objetos. Desde el punto de vista de la fisiología muscular, su frecuencia de contracción se encuentra en un rango de 10 a 500 Hz, lo que indica la actividad eléctrica generada durante su activación. Para analizar esta actividad, se utilizó un sensor de electromiografía (EMG), específicamente el Muscle Sensor v3, junto con un sistema de adquisición de datos (DAQ). Este sistema permitió registrar y almacenar la señal electromiográfica, para posteriormente realizar su correspondiente procesamiento digital. 

<p align="center">
    <img src="https://github.com/user-attachments/assets/d0a7cfdc-6328-43ff-8884-5fc5ccb0735b" alt="imagen" width="200" height="200">
    <img src="https://github.com/user-attachments/assets/841d468d-fa1d-41aa-a9ed-9167ff048171" alt="imagen" width="350" height="200">
</p>

Se empleó una configuración diferencial, que consiste en colocar dos electrodos activos sobre el mismo músculo y un tercer electrodo en una zona de referencia. En este método, se contrasta la señal registrada por los dos electrodos activos para suprimir interferencias y ruidos comunes, como el ambiental o el generado por músculos adyacentes. El electrodo de referencia, ubicado en una región eléctricamente estable (por ejemplo, en un punto óseo), El electrodo de referencia se utiliza para establecer un potencial de base o cero contra el cual se comparan las señales de los electrodos activos. 

<p align="center">
    <img src="https://github.com/user-attachments/assets/fbf058b1-05ab-48ff-bd4d-951703bb5857" alt="imagen" width="200">
</p>

Para determinar la frecuencia de muestreo, se siguió el teorema de Nyquist. Dado que la frecuencia máxima en este caso es de 500 Hz, la frecuencia de muestreo debe ser mayor o igual a 100 Hz para garantizar una correcta reconstrucción de la señal. Para esta caso se utilizo 1000 Hz de frecuencia.

$$
f_s \geq 2f_{\text{max}}
$$

$$
100 \geq 2(500)
$$


_ _ _

## 2) Adquisición de la Señal EMG:

La adquisición de la señal se realizó en Python, tomando como referencia un repositorio de GitHub [2].

```python
# Importamos las librerías necesarias
import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np
```
El código comienza importando las librerías necesarias para la adquisición de datos y el procesamiento numérico. Se importa nidaqmx, que permite la comunicación con el sistema de adquisición de datos (DAQ) de National Instruments

```python
sample_rate = 1000         
duration_minutes = 2      
duration_seconds = duration_minutes * 60  
num_samples = int(sample_rate * duration_seconds)
```
En esta sección se definen algunos parametros. Se establece la frecuencia de muestreo en 1000 Hz (sample_rate = 1000), lo que significa que se capturarán 1000 muestras por segundo. La duración de la adquisición se define en minutos (duration_minutes = 2), y se convierte a segundos (duration_seconds = duration_minutes * 60). Luego, se determina el número total de muestras a capturar (num_samples = int(sample_rate * duration_seconds)).

```python
with nidaqmx.Task() as task:
    
    task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
    
    task.timing.cfg_samp_clk_timing(
        sample_rate,
        sample_mode=AcquisitionType.FINITE,
        samps_per_chan=num_samples
    )
    
    task.start()

    task.wait_until_done(timeout=duration_seconds + 10)

    data = task.read(number_of_samples_per_channel=num_samples)
```
Para llevar a cabo la adquisición de datos, se utiliza un bloque with nidaqmx.Task() as task:, que crea una tarea en el DAQ. Dentro de esta tarea, se agrega un canal de entrada analógica con task.ai_channels.add_ai_voltage_chan("Dev3/ai0"), configurado para medir voltaje en el canal Dev3/ai0.

Una vez configurada la tarea, la adquisición de datos comienza con task.start(). Al finalizar, los datos se leen con task.read(number_of_samples_per_channel=num_samples), lo que devuelve una lista de valores de voltaje adquiridos.

```python
time_axis = np.linspace(0, duration_seconds, num_samples, endpoint=False)
with open("datos_adquiridos.txt", "w") as archivo_txt:
    archivo_txt.write("Tiempo (s)\tVoltaje (V)\n")
    for t, v in zip(time_axis, data):
        archivo_txt.write(f"{t:.6f}\t{v:.6f}\n")
```
Para representar los datos correctamente, se genera un eje de tiempo. La función np.linspace(0, duration_seconds, num_samples, endpoint=False) crea un arreglo de valores que representa el tiempo de cada muestra, comenzando en 0 segundos y extendiéndose hasta la duración total de la adquisición. Finalmente, los datos adquiridos se guardan en un archivo de texto llamado datos_adquiridos.txt.


```python
señal = np.loadtxt("datos_adquiridos.txt", skiprows=1)        
tiempo = señal[:, 0]  
voltaje = señal[:, 1] 

plt.figure(figsize=(10, 5))
plt.plot(tiempo, voltaje,color="b", label="Señal")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Gráfica de la Señal Adquirida")
plt.grid()
plt.show()
```
Posteriormente la señal obtenida y guardada en "datos_adquiridos.txt", se importa en otro Programa de python para realizar su correspondiente procesamiento digital.
Se muestra la señal Obtenida.
<p align="center">
    <img src="https://github.com/user-attachments/assets/d488e8e3-0482-4c9f-bbf5-d13a0767a985" alt="imagen" width="500">
</p>


_ _ _ 
## 3) Filtrado de la Señal:
### Filtro Pasa Banda
El siguiente código implementa un filtro pasa-banda digital utilizando un filtro Butterworth. Primero, establece un filtro pasa-bajos con una frecuencia de corte de 400 Hz y un filtro pasa-altos con una frecuencia de corte de 10 Hz, ambos de orden 10. Luego, la señal se filtra primero con el filtro pasa-bajos y posteriormente con el pasa-altos, eliminando frecuencias fuera del rango deseado. Finalmente, la señal filtrada se devuelve como salida.
```python
def filtro(s,fs):
    orden = 10
    corte1 = 400
    corte2 = 20
    nyquist = 0.5 * fs
    corte_normalizada1 = corte1 / nyquist
    corte_normalizada2 = corte2 / nyquist
    b, a = butter(orden, corte_normalizada1, btype='low', analog=False)
    b2, a2 = butter(orden, corte_normalizada2, btype='high', analog=False)
    señal_f1 = lfilter(b, a, s)
    return lfilter(b2, a2, señal_f1)    
sf = filtro(voltaje,fs)
```
Después de aplicar el filtro pasa-altos, la señal, que inicialmente era positiva, adquirió valores negativos. Esto puede deberse a la eliminación del componente de corriente directa (DC), lo que hizo que la señal comenzara a oscilar alrededor de cero. Esto ocurre porque un filtro pasa-altos elimina las frecuencias bajas, incluyendo cualquier desplazamiento positivo presente en la señal original.





_ _ _ 
## 4) Aventanamiento:
Se aplica la técnica de ventaneo a la señal filtrada sf utilizando la ventana de Hanning, que suaviza los bordes de cada segmento para minimizar efectos de discontinuidad en el análisis espectral.
### Primeras contracciones
```python
hanning = np.hanning(1000) 
ventana1 = sf[:1000] * hanning
ventana2 = sf[1000:2000] * hanning
ventana3 = sf[2000:2700] * hanning[:700]
ventana4 = sf[2700:3400] * hanning[:700]
ventana5 = sf[3400:4100] * hanning[:700]
ventana6 = sf[4100:4800] * hanning[:700]
señal_ventaneada = np.concatenate([ventana1, ventana2, ventana3, ventana4, ventana5, ventana6])
```
Primero se genera una ventana de Hanning de 1000 puntos, que se utiliza para multiplicar los primeros dos segmentos de la señal, cada uno de 1000 muestras. Luego, se extraen cuatro segmentos adicionales de 700 muestras cada uno, a los cuales se les aplica la parte correspondiente de la ventana de Hanning. Finalmente, todos los segmentos ventaneados se concatenan para formar una señal continua con transiciones más suaves entre las secciones.

<p align="center">
    <img src="https://github.com/user-attachments/assets/d6ab7258-2d25-46ff-bd9c-deb251aa3c95" alt="imagen" width="400">
    
</p>


### Ultimas Contracciones
```python
ventana7 = sf[82400:83000] * hanning[:600]
ventana8 = sf[83000:83660] * hanning[:660]
ventana9 = sf[83660:84560] * hanning[:900]
ventana10 = sf[84560:85100] * hanning[:540]
ventana11 = sf[85100:85570] * hanning[:470]
ventana12 = sf[85570:86400] * hanning[:830]
señal_ventaneadaf = np.concatenate([ventana7, ventana8, ventana9, ventana10, ventana11, ventana12])
```
Este código aplica ventanas de Hanning a seis segmentos específicos de la señal filtrada sf, pero en rangos de índices más altos. Cada segmento se extrae con una cantidad diferente de muestras y se multiplica por una porción de la ventana de Hanning correspondiente. Posteriormente, todos los segmentos ventaneados se concatenan para formar señal_ventaneadaf.

<p align="center">
    <img src="https://github.com/user-attachments/assets/2c2eaf4c-b0df-4d4a-9827-8033c4fea131" alt="imagen" width="400">
</p>

Se aplicó el venteado únicamente a algunas contracciones, específicamente a las primeras y últimas antes de la fatiga. Para ello, se utilizó una ventana de Hanning con el fin de dividir cada contracción en intervalos de tiempo. Esta ventana fue seleccionada porque ayuda a suavizar los extremos de la señal, evitando cambios bruscos que puedan distorsionar el análisis. Su forma es similar a una curva de coseno, lo que permite que los valores en los bordes de la señal se reduzcan gradualmente a cero, minimizando la discontinuidad en los límites de cada intervalo y mejorando la precisión del análisis espectral.

Para determinar el tamaño de cada ventana, se analizó la gráfica de la señal y se realizó una estimación de la duración de cada contracción, dado que la duración variaba entre ellas. Esto permitió ajustar el tamaño de la ventana de manera adecuada para cada caso, asegurando que el análisis se adaptara a estas diferencias

_ _ _
### trasformada de fourier
Luego, se aplica la transformada de Fourier a cada ventana para obtener su espectro de frecuencias.

```python
for i in range(1, 13):
    ventana = eval(f"ventana{i}")  
    N = len(ventana)
    
    fre = np.fft.fftfreq(N, 1/fs)
    frecuencias = fre[:N//2]
    espectro = np.fft.fft(ventana) / N
    magnitud = 2 * np.abs(espectro[:N//2])
```
<p align="center">
        <img src="https://github.com/user-attachments/assets/8e67297d-7d2f-43da-9c13-3b42da1f35e7" alt="imagen" width="400">
    <img src="https://github.com/user-attachments/assets/1e67d02b-2812-4f31-a341-c48baf78dcaa" alt="imagen" width="400">
</p>

Se presenta el espectro de frecuencias correspondiente a la primera contracción y a la última contracción en el inicio de la fatiga.
Al comparar ambas gráficas, se observa una disminución en las frecuencias presentes en el espectro de la señal a medida que se acerca la fatiga. Este cambio indica una reducción en la activación de componentes de alta frecuencia, lo que puede estar asociado a una disminución en la velocidad de conducción de las fibras musculares. Estos resultados sugieren que la fatiga muscular influye en la dinámica espectral de la señal, reflejando una disminución en la eficiencia neuromuscular conforme avanza el esfuerzo.






_ _ _
## 5) Análisis Espectral:

### Prueba de Hipotesis
Además de determinar el espectro de frecuencias, se calcula la frecuencia mediana en cada ventana con el fin de analizar la fatiga mediante una prueba de hipótesis.

```python
antes = []
despues = []        

for i in range(1, 13):
    ventana = eval(f"ventana{i}")  
    N = len(ventana)
    
    fre = np.fft.fftfreq(N, 1/fs)
    frecuencias = fre[:N//2]
    espectro = np.fft.fft(ventana) / N
    magnitud = 2 * np.abs(espectro[:N//2])
    
    psd = magnitud ** 2
    potencia_total = np.sum(psd)
    potencia_acumulada = np.cumsum(psd)
    
    fm_index = np.where(potencia_acumulada >= potencia_total / 2)[0][0]
    fm = frecuencias[fm_index]

    if 1<=i<=6:
        antes.append(fm)
    else:
        despues.append(fm)
```
<p align="center">
    <img src="https://github.com/user-attachments/assets/d24c997b-d753-4d09-bb3e-58d79be0d7e8" alt="imagen" width="400">
</p>

La mediana obtenida en cada ventana se guarda en una lista correspondiente. Primero, se registran las primeras 6 contracciones iniciales y luego las 6 ultimas, cuando el músculo entra en fatiga.
Finalmente se realiza la prueba de hipotesis haciendo uso de scipy.

 ```python
stat, p = ttest_rel(antes, despues)

print(f'P-valor: {p}')

if p < 0.05:
    print("Rechazamos la hipotesis H₀, La fatiga afecta significativamente la mediana de frecuencia.")
else:
    print("No se puede rechazar H₀, No hay evidencia suficiente de un cambio significativo.")

```

<p align="center">
    <img src="https://github.com/user-attachments/assets/0017a9a3-f2dd-44a5-b1b4-3982d2abc4fa" alt="imagen" width="500">
</p>

En el test de hipótesis realizado, se descartó la hipótesis nula (𝐻₀) al observar que la mediana de las frecuencias cerca de la fatiga disminuyó, indicando una diferencia significativa. Esto sugiere que, a medida que el músculo se fatiga, hay una reducción en las frecuencias características de la señal, lo que puede estar relacionado con una menor velocidad de conducción en las fibras musculares y una modificación en el reclutamiento de unidades motoras. La disminución de la velocidad de conducción se debe a cambios en la excitabilidad de la membrana, lo que ralentiza la propagación del potencial de acción y afecta la activación eficiente del músculo.







_ _ _

## Bibliografias
[1] Pololu, "Muscle Sensor v3 User’s Manual," [Online]. Available: https://www.pololu.com/file/0J745/Muscle_Sensor_v3_users_manual.pdf. [Accessed: 24-Mar-2025].

[2] National Instruments, "NI-DAQmx Python API," GitHub repository, [Online]. Available: https://github.com/ni/nidaqmx-python. [Accessed: 24-Mar-2025].

[3] National Instruments, "Understanding FFTs and Windowing," NI, [Online]. Available: https://www.ni.com/es/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/understanding-ffts-and-windowing.html. [Accessed: 25-Mar-2025].

_ _ _
