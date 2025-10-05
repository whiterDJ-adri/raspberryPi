import os, cv2, requests
from datetime import datetime

def take_photo():
    # Inicia la camara y toma una foto
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    # Definimos la ruta y el nombre del fichero 
    ruta = "screenshots"
    nombre_fichero = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg";
    ruta_fichero = os.path.join("../api/media", ruta, nombre_fichero)
    
    # Guardamos la imagen
    cv2.imwrite(ruta_fichero, frame)
    
    insert = {
        "name": nombre_fichero,
        "date": datetime.now().strftime('%Y%m%d_%H%M%S'),
        "path_file": ruta_fichero
    }
    return requests.post("http://localhost:5000/api/photo", json=insert)

take_photo()