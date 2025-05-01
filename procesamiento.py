import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import find_peaks 
import pywt

fs = 400
s = np.loadtxt("ecg.txt")
señal = (s*3.3*1000)/4095 #conversion a mv
tiempo = (np.arange(len(señal)) / fs)

plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal[:],color="r")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (mv)")
plt.title("ECG, Señal Original")
plt.grid()


# Pre-procesamiento de la señal 
def filtro(fs, señal):
    b, a = butter(1, [1 / (fs / 2), 160 / (fs / 2)], btype='band')
    eq = f"y[n] = ({b[0]:.3f} * x[n] + {b[1]:.2f} * x[n-1] - {a[1]:.3f} * y[n-1])"
    
    print("Ecuación en diferencias:", eq)
    return lfilter(b, a, señal)

señal_filtrada = filtro(fs, señal)
plt.figure(figsize=(15, 8))
plt.plot(tiempo[:], señal_filtrada[:], color="b")
plt.title('ECG, Señal Filtrada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (mv)')
plt.grid()


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

t = t_picos[1:]

plt.figure(figsize=(15, 8))
plt.plot(t[:-1], intervalo, marker='o', linestyle='-', color='k')
plt.title('Señal Basada en Intervalos R-R')
plt.xlabel('Tiempo en el que Sucede Cada Pico R (s)')
plt.ylabel('Intervalo R-R (s)')
plt.grid()


# Análisis de la HRV en el dominio del tiempo


diffs = np.diff(intervalo)
squared_diffs = diffs ** 2
mean_squared_diffs = np.mean(squared_diffs)
rmssd = np.sqrt(mean_squared_diffs)
media = np.mean(intervalo)
desviacion = np.std(intervalo, ddof=1)

print()
print('Media de los Intervalos R-R:', round(media, 4) , "segundos")
print('Desviación Estandar de los Intervalos R-R:', round(desviacion, 4), "segundos")
print("RMSSD:", round(rmssd, 4), "segundos")
print()

# transformada Wavelet

avg_RR = np.mean(np.diff(t))  
fs = 1/avg_RR  

wavelet_morl = 'morl'
escalas_morl = np.arange(1, 128)
coef_morl, freqs_morl = pywt.cwt(intervalo, escalas_morl, wavelet_morl, sampling_period=avg_RR)
freqs_morl = pywt.scale2frequency(wavelet_morl, escalas_morl) / avg_RR

wavelet_mexh = 'mexh'
escalas_mexh = np.linspace(1, 40, 100)  # Rango diferente para mejor visualización
coef_mexh, freqs_mexh = pywt.cwt(intervalo, escalas_mexh, wavelet_mexh, sampling_period=avg_RR)
freqs_mexh = pywt.scale2frequency(wavelet_mexh, escalas_mexh) / avg_RR

# Crear figura con subplots
plt.figure(figsize=(15, 10))

# Primer subplot - Morlet
plt.subplot(2, 1, 1)
img1 = plt.imshow(np.abs(coef_morl), extent=[t[0], t[-1], freqs_morl[-1], freqs_morl[0]],
                 cmap='jet', aspect='auto', vmax=np.abs(coef_morl).max()*0.5)
plt.title('Espectrograma HRV - Wavelet Morlet')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.axhline(0.04, color='k', linestyle='--')
plt.axhline(0.15, color='k', linestyle='--', label='LF (0.04-0.15 Hz)')
plt.axhline(0.4, color='w', linestyle='--', label='HF (0.15-0.4 Hz)')
plt.legend()

# Segundo subplot - Mexican Hat
plt.subplot(2, 1, 2)
img2 = plt.imshow(np.abs(coef_mexh), extent=[t[0], t[-1], freqs_mexh[-1], freqs_mexh[0]],
                 cmap='jet', aspect='auto', vmax=np.abs(coef_mexh).max()*0.5)
plt.title('Espectrograma HRV - Wavelet Mexican Hat')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.axhline(0.04, color='k', linestyle='--')
plt.axhline(0.15, color='k', linestyle='--', label='LF (0.04-0.15 Hz)')
plt.axhline(0.4, color='w', linestyle='--', label='HF (0.15-0.4 Hz)')
plt.legend()

plt.show()
