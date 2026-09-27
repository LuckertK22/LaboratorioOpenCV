# LabCG3 – Eigenfaces: redimensionar, normalizar, proyección y PCA con OpenCV

| Archivo | Qué es |
|---|---|
| `Informe_LabCG3_Eigenfaces.docx` | Informe con gráficos, tablas, análisis de tareas, comparación y conclusiones |
| `LabCG3_Eigenfaces.ipynb` | Notebook con las partes 1 a 5 y las tareas (componentes y ruido), ya ejecutado |
| `datos/att_faces/` | Dataset AT&T / ORL Database of Faces (40 personas × 10 imágenes, 92×112) |
| `modelos/face_detection_yunet_2023mar.onnx` | Detector de rostros YuNet usado en el análisis de la parte 5 |
| `resultados/` | Figuras, capturas de la cámara, `datos_labcg3.json` y `modelo_eigenfaces.npz` |

```bash
pip install opencv-python numpy scikit-learn matplotlib jupyter
jupyter notebook LabCG3_Eigenfaces.ipynb
```

Dataset: The ORL Database of Faces, Olivetti Research Laboratory (AT&T Laboratories Cambridge).
