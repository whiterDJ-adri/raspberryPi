import cv2
import requests
import time
import numpy as np
from datetime import datetime

def take_photo(frame):
    # Definimos el nombre del fichero
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    # Formatea el frame2 para que sea jpg y luego se crea el fichero con su nombre, se pasa a binario y le indicamos el tipo que es, en este caso jpeg
    res, buffer = cv2.imencode(".jpg", frame)

    file = {"file": (filename, buffer.tobytes(), "image/jpeg")}

    insert = {
        "filename": filename,
        "date": datetime.now().strftime("%Y%m%d_%H%M%S"),
    }

    return requests.post("http://localhost:5000/api/photo", files=file, data=insert)


# Abrimos la cámara (0 = cámara principal)
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()

count = 1
max_photos = 5

while True:
    # Leemos el siguiente frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Calculamos la diferencia entre las dos imagenes
    diferencia = cv2.absdiff(frame1, frame2)

    # Convertimos la diferencia a escala de grises (para analizarla mejor)
    gris = cv2.cvtColor(diferencia, cv2.COLOR_BGR2GRAY)

    # Calculamos el valor medio de la diferencia (cuanto a cambiado la iomagen)
    average = np.mean(gris)

    # Si el promedio supera un valor, consideramos que hay movimiento
    if average > 10:  # puedes ajustar este número según lo sensible que quieras
        print("¡Movimiento detectado! Valor:", average)
        if count == max_photos:
            count = 1
            time.sleep(60)
        take_photo(frame2)
        count+=1
    else:
        print("Sin movimiento... Valor:", average)

    # Actualizamos el frame anterior
    frame1 = frame2
    time.sleep(2)
