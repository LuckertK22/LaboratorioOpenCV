# Laboratorio 31 – Uso de archivos de video con OpenCV (Práctica 32)

Visión Computacional – Corporación Universitaria de la Costa.

| Archivo | Qué es |
|---|---|
| `Informe_Lab31_Video_OpenCV.docx` | Informe con tablas, capturas, respuestas a las preguntas, discusión y conclusiones |
| `Lab31_Archivos_Video_OpenCV.ipynb` | Notebook con el desarrollo de la práctica (ya ejecutado) |
| `reproductor_video.py` | Script de la sección 4.9 y del reto 4.9.6 (usa `cv2.imshow`, correr en local) |
| `video.mp4`, `DATA/video_capture.mp4` | Megamind.avi de las muestras de OpenCV, en MP4 |
| `DATA/peatones.mp4` | Primeros 300 frames de vtest.avi (muestras de OpenCV) |
| `resultados/` | Figuras y fotogramas extraídos |

Los videos reescalados del reto (`DATA/generados/`) los crea el notebook al ejecutarse.

```bash
pip install opencv-python matplotlib numpy
jupyter notebook Lab31_Archivos_Video_OpenCV.ipynb
python reproductor_video.py --auto      # reproducción con los FPS del archivo
```
