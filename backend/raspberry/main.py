import os, cv2, requests, time
from datetime import datetime
import numpy as np

def take_photo(frame):
    # Definimos la ruta y el nombre del fichero 
    ruta = "screenshots"
    nombre_fichero = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg";
    ruta_fichero = os.path.join("../api/media", ruta, nombre_fichero)
    
    # Formatea el frame2 para que sea jpg y luego se crea el fichero con su nombre, se pasa a binario y le indicamos el tipo que es, en este caso jpeg
    res, buffer = cv2.imencode(".jpg", frame)
    print(res)
    file = { "file": (nombre_fichero, buffer.tobytes(), "image/jpeg")}
    
    insert = {
        "fichero": nombre_fichero,
        "fecha": datetime.now().strftime('%Y%m%d_%H%M%S'),
        "ruta": ruta_fichero,
    }
    
    return requests.post("http://localhost:5000/api/photo", files=file, data=insert)

# Abrimos la cámara (0 = cámara principal)
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()

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
    promedio = np.mean(gris)


    # Si el promedio supera un valor, consideramos que hay movimiento
    if promedio > 10:  # puedes ajustar este número según lo sensible que quieras
        print("¡Movimiento detectado! Valor:", promedio)
        take_photo(frame2)
    else:
        print("Sin movimiento... Valor:", promedio)

    # Actualizamos el frame anterior
    frame1 = frame2
    
    time.sleep(15)
