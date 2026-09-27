# Sistema sencillo de anotación sobre cámara en vivo (actividad integradora Lab 32)
#
# Mouse:  clic izquierdo = primera esquina, segundo clic = esquina opuesta
#         (mientras se mueve el mouse se ve una vista previa de la caja)
# Teclas: r reiniciar selección | s guardar captura | q salir
#
# Uso desde terminal:  python anotador_camara.py        (cámara 0)
#                      python anotador_camara.py 1      (otra cámara)

import os
import sys
import time

import cv2

VENTANA = 'Anotador'
ROJO, VERDE, AMARILLO, BLANCO, NEGRO = (0, 0, 255), (0, 255, 0), (0, 255, 255), (255, 255, 255), (0, 0, 0)

estado = {'p1': None, 'p2': None, 'mouse': None}


def al_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if estado['p1'] is None or estado['p2'] is not None:
            # primer clic (o clic después de tener una caja completa): empieza una nueva
            estado['p1'], estado['p2'] = (x, y), None
        else:
            estado['p2'] = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        estado['mouse'] = (x, y)


def normalizar(p1, p2, w, h):
    # que funcione sin importar en qué orden se hagan los clics, y sin salirse de la imagen
    x1, x2 = sorted((min(max(p1[0], 0), w - 1), min(max(p2[0], 0), w - 1)))
    y1, y2 = sorted((min(max(p1[1], 0), h - 1), min(max(p2[1], 0), h - 1)))
    return x1, y1, x2, y2


def texto_con_fondo(img, texto, org, color_fondo, escala=0.55, grosor=1):
    (tw, th), base = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, escala, grosor)
    x, y = org
    y = max(y, th + 4)          # que no se salga por arriba
    cv2.rectangle(img, (x, y - th - 4), (x + tw + 4, y + base), color_fondo, -1)
    cv2.putText(img, texto, (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, escala, NEGRO if color_fondo != NEGRO else BLANCO, grosor)


def anotador(fuente=0, etiqueta='ROI', limite_seg=None, carpeta='resultados/anotador'):
    os.makedirs(carpeta, exist_ok=True)
    estado.update(p1=None, p2=None, mouse=None)
    rois, capturas = [], []

    # 1. validar la cámara
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        print(f'No fue posible abrir la cámara {fuente}')
        return {'error': 'sin cámara'}
    ok, frame = cap.read()
    if not ok:
        print('La cámara abrió pero no entrega frames')
        cap.release()
        return {'error': 'sin frames'}

    # 2. resolución (del frame real)
    h, w = frame.shape[:2]
    print(f'Cámara {fuente} conectada: {w}x{h}')

    cv2.namedWindow(VENTANA)
    cv2.setMouseCallback(VENTANA, al_mouse)

    ultima_guardada = None
    t0 = time.time()
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print('read() devolvió False')
                break
            vista = frame.copy()

            texto_con_fondo(vista, f'Resolucion: {w}x{h}', (8, 22), BLANCO)
            cv2.putText(vista, 'clic: esquinas | r: reiniciar | s: guardar | q: salir', (8, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, BLANCO, 1)

            p1, p2 = estado['p1'], estado['p2']
            if p1 is not None:
                cv2.circle(vista, p1, 5, ROJO, -1)
                if p2 is None and estado['mouse'] is not None:
                    # vista previa mientras se busca la segunda esquina
                    cv2.rectangle(vista, p1, estado['mouse'], AMARILLO, 1)

            if p1 is not None and p2 is not None:
                x1, y1, x2, y2 = normalizar(p1, p2, w, h)
                bw, bh = x2 - x1, y2 - y1

                # 4. bounding box
                cv2.rectangle(vista, (x1, y1), (x2, y2), VERDE, 2)
                # 5. coordenadas de las dos esquinas
                cv2.circle(vista, (x1, y1), 4, ROJO, -1)
                cv2.circle(vista, (x2, y2), 4, ROJO, -1)
                cv2.putText(vista, f'({x1},{y1})', (x1 + 4, y1 + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, AMARILLO, 1)
                cv2.putText(vista, f'({x2},{y2})', (max(x2 - 85, 0), min(y2 + 16, h - 25)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, AMARILLO, 1)
                # 6 y 7. ancho, alto y etiqueta encima de la región
                texto_con_fondo(vista, f'{etiqueta}  {bw}x{bh} px', (x1, y1 - 4), VERDE)

                caja = (x1, y1, bw, bh)
                if not rois or rois[-1]['caja'] != caja:
                    rois.append({'esquina1': (x1, y1), 'esquina2': (x2, y2), 'caja': caja,
                                 'ancho': bw, 'alto': bh, 'area': bw * bh})
                    print(f'ROI: esquinas ({x1},{y1}) y ({x2},{y2}), ancho={bw}, alto={bh}')

            cv2.imshow(VENTANA, vista)
            k = cv2.waitKey(1) & 0xFF

            if k == ord('q'):
                break
            elif k == ord('r'):
                # 8. reiniciar
                estado.update(p1=None, p2=None)
                print('selección reiniciada')
            elif k == ord('s'):
                ruta = f'{carpeta}/anotacion_{len(capturas) + 1}.jpg'
                cv2.imwrite(ruta, vista)
                capturas.append(ruta)
                print('guardada', ruta)

            ultima_guardada = vista
            if limite_seg and time.time() - t0 > limite_seg:
                print(f'límite de {limite_seg} s')
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        for _ in range(5):
            cv2.waitKey(1)

    if ultima_guardada is not None:
        cv2.imwrite(f'{carpeta}/ultimo_frame.jpg', ultima_guardada)
    return {'resolucion': [w, h], 'rois': rois, 'capturas': capturas}


if __name__ == '__main__':
    fuente = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    resumen = anotador(fuente=fuente)
    print()
    for r in resumen.get('rois', []):
        print(r)
