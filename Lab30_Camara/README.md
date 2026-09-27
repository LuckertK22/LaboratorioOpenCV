# Laboratorio 30 (Práctica 31) – Conexión y captura desde cámara

| Archivo | Qué es |
|---|---|
| `Lab30_Conexion_Camara_OpenCV.ipynb` | Notebook con todas las secciones de la guía (4.1 a 4.8 e integradora) |
| `camara_app.py` | Miniaplicación de la actividad integradora (misma que en el notebook) |
| `DATA/camara_simulada.mp4` | Video de respaldo (vtest.avi de OpenCV a 640x480) por si no hay cámara |

## Cómo correrlo en el portátil

1. Cerrar Zoom/Teams/Meet o cualquier programa que use la cámara.
2. Instalar (la versión normal de OpenCV, **no** `opencv-python-headless`):
   ```bash
   pip install opencv-python matplotlib numpy jupyter
   ```
3. Desde esta carpeta (`Lab30_Camara/`):
   ```bash
   jupyter notebook Lab30_Conexion_Camara_OpenCV.ipynb
   ```
4. Ejecutar las celdas en orden (o *Kernel → Restart & Run All*). Cuando se abra una ventana de la cámara,
   **hacer clic sobre ella** y usar las teclas que dice la celda (`q` salir, `s` captura, etc.).
   Cada ciclo se corta solo a los ~20 s por si la ventana no recibe el teclado.
5. En la integradora: cambiar modos con 1-4, tomar 2-3 capturas con `s`, grabar ~5 s con `r` ... `r` y salir con `q`.

Al terminar, todo queda en `resultados/` (capturas, videos y `datos_lab30.json` con las medidas).

## Problemas comunes

- **No abre la cámara (isOpened False)**
  - Windows: Configuración → Privacidad y seguridad → Cámara → activar "Permitir que las aplicaciones de escritorio accedan a la cámara".
  - Mac: Configuración del Sistema → Privacidad y seguridad → Cámara → habilitar Terminal / VS Code / Anaconda (el programa desde donde se abrió Jupyter) y reiniciarlo.
  - Probar con `INDICE_CAMARA = 1` si hay cámara USB o virtual (OBS, etc.).
  - En Windows, si tarda mucho en abrir: `cv2.VideoCapture(0, cv2.CAP_DSHOW)`.
- **La ventana no responde a las teclas**: hacer clic en la ventana primero.
- **En Mac la ventana no se cierra**: ya está el `waitKey` extra después de `destroyAllWindows`; si sigue, reiniciar el kernel.
- **El video grabado no abre**: ver la tabla de códecs de la sección 4.6 para saber cuáles funcionan en el equipo.
