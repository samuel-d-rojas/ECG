# Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet   
 LABORATORIO - 5 PROCESAMIENTO DIGITAL DE SEÑALES

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

_ _ _

## 1) Preparación del Sujeto


_ _ _
## b. Adquisición de la señal ECG



_ _ _
## c. Pre-procesamiento de la señal


_ _ _
## e. Aplicación de transformada Wavelet


_ _ _

## Bibliografias
[1] Pololu, "Muscle Sensor v3 User’s Manual," [Online]. Available: https://www.pololu.com/file/0J745/Muscle_Sensor_v3_users_manual.pdf. [Accessed: 24-Mar-2025].

[2] National Instruments, "NI-DAQmx Python API," GitHub repository, [Online]. Available: https://github.com/ni/nidaqmx-python. [Accessed: 24-Mar-2025].

[3] National Instruments, "Understanding FFTs and Windowing," NI, [Online]. Available: https://www.ni.com/es/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/understanding-ffts-and-windowing.html. [Accessed: 25-Mar-2025].

_ _ _
