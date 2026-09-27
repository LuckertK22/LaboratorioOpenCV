# Script de la seccion 4.9 (reproduccion respetando FPS) + el reto 4.9.6
# Este es para correrlo en local porque usa cv2.imshow (en Colab no sirve).
#
# Ejemplos:
#   python reproductor_video.py                      -> fps = 25 fijo, waitKey(25)
#   python reproductor_video.py --fps 10             -> experimento 2
#   python reproductor_video.py --sleep 0.1          -> experimento 3
#   python reproductor_video.py --wait 100           -> experimento 4
#   python reproductor_video.py --sin-sleep          -> experimento 5
#   python reproductor_video.py --auto               -> reto: fps leidos del archivo
#
# Al final imprime cuanto se demoro de verdad en mostrar todo, para poder
# comparar con la duracion real del video.

import argparse
import time

import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--video', default='DATA/video_capture.mp4')
parser.add_argument('--fps', type=float, default=25)
parser.add_argument('--sleep', type=float, default=None, help='pausa fija en segundos (reemplaza 1/fps)')
parser.add_argument('--wait', type=int, default=25, help='ms de cv2.waitKey')
parser.add_argument('--sin-sleep', action='store_true')
parser.add_argument('--auto', action='store_true', help='usar CAP_PROP_FPS del archivo')
args = parser.parse_args()

cap = cv2.VideoCapture(args.video)

if cap.isOpened() == False:
    print("Error opening the video file. Please double check your file path.")
    raise SystemExit(1)

fps = args.fps
if args.auto:
    # reto: sacar los fps del archivo en vez de ponerlos a mano
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS detectados:", fps)

if fps > 0:
    tiempo_frame = 1 / fps
else:
    tiempo_frame = 1 / 25

if args.sleep is not None:
    tiempo_frame = args.sleep

fps_archivo = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

mostrados = 0
inicio = time.time()

while cap.isOpened():
    ret, frame = cap.read()

    if ret == True:
        if not args.sin_sleep:
            time.sleep(tiempo_frame)

        cv2.putText(frame, f'fps prog: {fps:.2f}  pausa: {tiempo_frame:.3f}s  waitKey: {args.wait}',
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow('frame', frame)
        mostrados += 1

        # q para salir
        if cv2.waitKey(args.wait) & 0xFF == ord('q'):
            print('Se presiono q')
            break
    else:
        break

fin = time.time()
cap.release()
cv2.destroyAllWindows()

print('isOpened despues de release:', cap.isOpened())
print(f'Fotogramas mostrados: {mostrados} de {total}')
print(f'Tiempo real de reproduccion: {fin - inicio:.2f} s')
print(f'Duracion real del video: {total / fps_archivo:.2f} s')
