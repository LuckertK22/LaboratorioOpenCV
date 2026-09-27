# Laboratorio 30 (Práctica 31) – Conexión y captura desde cámara

Ejecutado en Windows 11, Python 3.12, OpenCV 5.0, con la webcam integrada del portátil (640x480, 30 fps).

| Archivo | Qué es |
|---|---|
| `Informe_Lab30_Camara_OpenCV.docx` | Informe con tablas, capturas, respuestas, problemas encontrados y conclusiones |
| `Lab30_Conexion_Camara_OpenCV.ipynb` | Notebook con todas las secciones de la guía (4.1 a 4.8 e integradora), ya ejecutado |
| `camara_app.py` | Miniaplicación de la actividad integradora (misma que en el notebook) |
| `resultados/` | Capturas, videos grabados (`student_capture.mp4`, `app/grabacion_1.mp4`), pruebas de códecs y `datos_lab30.json` |

## Cómo correrlo

```bash
pip install opencv-python matplotlib numpy jupyter
jupyter notebook Lab30_Conexion_Camara_OpenCV.ipynb
# o solo la app:
python camara_app.py
```

Teclas de la app: `1` gris, `2` Canny, `3` desenfoque, `4` umbral adaptativo, `s` captura, `r` grabar, `q` salir.
Hay que hacer clic en la ventana para que reciba las teclas y cerrar antes cualquier programa que use la cámara.
