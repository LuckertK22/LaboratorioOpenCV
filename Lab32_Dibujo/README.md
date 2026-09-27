# Laboratorio 32 (Práctica 32) – Drawing on Live Camera

| Archivo | Qué es |
|---|---|
| `Lab32_Dibujo_Camara_OpenCV.ipynb` | Notebook con todas las secciones de la guía (4.1 a 4.9, integradora y reto) |
| `anotador_camara.py` | Sistema de anotación de la actividad integradora (el mismo del notebook) |
| `modelos/face_detection_yunet_2023mar.onnx` | Detector de rostros YuNet (OpenCV Zoo) usado en el reto |

## Cómo correrlo

```bash
pip install opencv-python matplotlib numpy jupyter
jupyter notebook Lab32_Dibujo_Camara_OpenCV.ipynb
# o solo el anotador:
python anotador_camara.py
```

Hay que hacer clic en la ventana para que reciba el teclado y cerrar antes cualquier programa que use la cámara.
Todo lo que se genera queda en `resultados/` (capturas y `datos_lab32.json`).
