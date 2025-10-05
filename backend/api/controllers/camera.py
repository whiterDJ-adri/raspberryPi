import os
import cv2
from datetime import datetime

class CameraController:
    def __init__(self):
        self.directorio = "media\screenshots"
    
            
    def hacer_foto(self):
        # Se selecciona la camara, se hace la foto y se cierra la camara seleccionada una vez realizada la foto
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    "success": False,
                    "error": "No se pudo acceder a la cámara"
                }
                
            ret, foto = cap.read()
            cap.release()
            
            if not ret or foto is None:
                return {
                    "success": False,
                    "error": "No se pudo capturar la imagen"
                }
            
            # Se define el nombre del fichero junto a la ruta final de esta (la carpeta + nombre del fichero)
            nombre_fichero = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg";
            ruta_fichero = os.path.join(self.directorio, nombre_fichero)
            
            # Se guarda la foto en la ruta especificada
            cv2.imwrite(ruta_fichero, foto)
            
            return {
                "fichero": nombre_fichero,
                "fecha": datetime.now().strftime('%Y%m%d_%H%M%S'),
                "ruta": ruta_fichero
            }
        except:
            return{
                "success": False,
                    "error": "Error haciendo la foto"
            }
        
        
