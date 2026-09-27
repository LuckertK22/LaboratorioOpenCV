# Miniaplicación de la actividad integradora (Lab 30 - cámara)
#
# Teclas (con la ventana seleccionada):
#   1 gris | 2 Canny | 3 desenfoque | 4 umbral adaptativo
#   s guardar captura | r empezar/parar grabación | q salir
#
# Uso desde terminal:  python camara_app.py            (cámara 0)
#                      python camara_app.py 1          (otra cámara)
#
# Hay que darle clic a la ventana para que reciba las teclas.

import os
import sys
import time

import cv2

MODOS = {ord('1'): 'gris', ord('2'): 'canny', ord('3'): 'desenfoque', ord('4'): 'umbral'}

# orden de códecs a probar para grabar: (fourcc, extensión)
CODECS = [('mp4v', '.mp4'), ('XVID', '.avi'), ('MJPG', '.avi')]


def procesar(frame, modo):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if modo == 'gris':
        return gray
    if modo == 'canny':
        # un poquito de blur antes para que no salga tanto ruido del sensor
        return cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    if modo == 'desenfoque':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    if modo == 'umbral':
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    return frame


def a_bgr(img):
    # VideoWriter y hconcat necesitan 3 canales
    return img if img.ndim == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def abrir_writer(base, fps, tam):
    for fcc, ext in CODECS:
        ruta = base + ext
        w = cv2.VideoWriter(ruta, cv2.VideoWriter_fourcc(*fcc), fps, tam)
        if w.isOpened():
            return w, ruta, fcc
        w.release()
    return None, None, None


def app(fuente=0, limite_seg=None, carpeta='resultados/app'):
    os.makedirs(carpeta, exist_ok=True)
    eventos = []

    def log(msg):
        t = time.strftime('%H:%M:%S')
        eventos.append(f'{t} {msg}')
        print(f'[{t}] {msg}')

    # 1. conectar y verificar
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        log(f'no se pudo abrir la cámara {fuente} (revisar permisos o si otro programa la está usando)')
        return {'error': 'sin cámara', 'eventos': eventos}
    ok, frame = cap.read()
    if not ok:
        log('la cámara abrió pero no entrega frames')
        cap.release()
        return {'error': 'sin frames', 'eventos': eventos}

    # 2. resolución (la saco del frame, que es lo que de verdad llega)
    h, w = frame.shape[:2]
    log(f'fuente {fuente} conectada, resolución {w}x{h}, backend {cap.getBackendName()}')

    # FPS: la propiedad muchas veces sale 0 o 30 fijo en webcams, así que también lo mido
    fps_prop = cap.get(cv2.CAP_PROP_FPS)
    t0 = time.time()
    for _ in range(20):
        cap.read()
    fps_med = 20 / (time.time() - t0)
    if 5 <= fps_med <= 60:
        fps_grab = fps_med
    else:
        fps_grab = fps_prop if fps_prop > 0 else 20
    log(f'FPS propiedad={fps_prop:.1f}, medidos={fps_med:.1f}, para grabar uso {fps_grab:.1f}')

    modo = 'gris'
    writer, ruta_video, frames_rec = None, None, 0
    capturas, videos = [], []
    n = 0
    fps_vis = 0.0
    t_ant = time.time()
    t_ini = time.time()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                log('read() devolvió False (se desconectó la cámara)')
                break
            n += 1

            procesado = procesar(frame, modo)

            if writer is not None:
                writer.write(a_bgr(procesado))
                frames_rec += 1

            # fps de la visualización (suavizado)
            ahora = time.time()
            fps_inst = 1 / max(ahora - t_ant, 1e-6)
            fps_vis = fps_inst if fps_vis == 0 else 0.9 * fps_vis + 0.1 * fps_inst
            t_ant = ahora

            vista = frame.copy()
            cv2.putText(vista, f'{w}x{h}  {fps_vis:4.1f} fps  modo: {modo}', (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(vista, '1 gris 2 canny 3 blur 4 umbral | s foto | r grabar | q salir',
                        (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            if writer is not None:
                cv2.circle(vista, (w - 25, 22), 9, (0, 0, 255), -1)
                cv2.putText(vista, 'REC', (w - 75, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.imshow('Original', vista)
            cv2.imshow('Procesado', procesado)
            k = cv2.waitKey(1) & 0xFF   # una sola lectura del teclado por ciclo

            if k == ord('q'):
                log('q presionada, saliendo')
                break
            elif k in MODOS:
                modo = MODOS[k]
                log(f'modo -> {modo}')
            elif k == ord('s'):
                i = len(capturas) + 1
                r1 = f'{carpeta}/captura_{i}_original.jpg'
                r2 = f'{carpeta}/captura_{i}_{modo}.jpg'
                r3 = f'{carpeta}/pantalla_{i}.jpg'   # como se veían las dos ventanas
                cv2.imwrite(r1, frame)
                cv2.imwrite(r2, procesado)
                cv2.imwrite(r3, cv2.hconcat([vista, a_bgr(procesado)]))
                capturas.append({'original': r1, 'procesada': r2, 'pantalla': r3, 'modo': modo})
                log(f'captura guardada: {r1}, {r2}')
            elif k == ord('r'):
                if writer is None:
                    base = f'{carpeta}/grabacion_{len(videos) + 1}'
                    writer, ruta_video, fcc = abrir_writer(base, fps_grab, (w, h))
                    if writer is None:
                        log('no se pudo abrir ningún códec para grabar')
                    else:
                        frames_rec = 0
                        t_rec = time.time()
                        log(f'grabando en {ruta_video} con {fcc} a {fps_grab:.1f} fps')
                else:
                    writer.release()
                    dur = time.time() - t_rec
                    videos.append({'ruta': ruta_video, 'frames': frames_rec,
                                   'duracion_real_s': round(dur, 2),
                                   'duracion_archivo_s': round(frames_rec / fps_grab, 2)})
                    log(f'grabación detenida: {frames_rec} frames en {dur:.1f} s')
                    writer = None

            if limite_seg and time.time() - t_ini > limite_seg:
                log(f'se alcanzó el límite de {limite_seg} s')
                break
    finally:
        # 7. liberar todo pase lo que pase
        if writer is not None:
            writer.release()
            dur = time.time() - t_rec
            videos.append({'ruta': ruta_video, 'frames': frames_rec,
                           'duracion_real_s': round(dur, 2),
                           'duracion_archivo_s': round(frames_rec / fps_grab, 2)})
            log('se cerró la grabación que seguía abierta')
        cap.release()
        cv2.destroyAllWindows()
        for _ in range(5):
            cv2.waitKey(1)   # a veces las ventanas se quedan pegadas si no se hace esto
        log(f'recursos liberados (cap.isOpened() = {cap.isOpened()})')

    return {'fuente': str(fuente), 'resolucion': [w, h], 'fps_propiedad': fps_prop,
            'fps_medidos': round(fps_med, 2), 'fps_grabacion': round(fps_grab, 2),
            'frames_mostrados': n, 'fps_visualizacion': round(fps_vis, 1),
            'capturas': capturas, 'videos': videos, 'eventos': eventos}


if __name__ == '__main__':
    fuente = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    resumen = app(fuente=fuente)
    print()
    print('Capturas:', len(resumen.get('capturas', [])))
    for v in resumen.get('videos', []):
        print('Video:', v)
