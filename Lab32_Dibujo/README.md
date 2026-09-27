# Laboratorio 32 (Práctica 32) – Drawing on Live Camera

Ejecutado en Windows 11, Python 3.12, OpenCV 5.0, con la webcam integrada del portátil (640x480).

| Archivo | Qué es |
|---|---|
| `Informe_Lab32_Dibujo_Camara_OpenCV.docx` | Informe con tablas, capturas, respuestas y conclusiones |
| `Lab32_Dibujo_Camara_OpenCV.ipynb` | Notebook con todas las secciones de la guía (4.1 a 4.9, integradora y reto), ya ejecutado |
| `anotador_camara.py` | Sistema de anotación de ROI de la actividad integradora |
| `modelos/face_detection_yunet_2023mar.onnx` | Detector de rostros YuNet (OpenCV Zoo) usado en el reto |
| `resultados/` | Capturas del dibujo fijo e interactivo, anotaciones, reto y `datos_lab32.json` |

```bash
pip install opencv-python matplotlib numpy jupyter
python anotador_camara.py      # clic-clic: ROI | r: reiniciar | s: guardar | q: salir
```
