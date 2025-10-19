import cv2
import requests
import time
import numpy as np
from datetime import datetime


# FALTA: Control de errores en la función take_photo
# - Verificar que el frame no esté vacío antes de procesarlo
# - Manejar errores de conexión de red cuando haga el POST al servidor
# - Validar que la codificación del frame a JPG sea exitosa
# - Manejar timeouts en las peticiones HTTP
def take_photo(frame):
    try:
        # Verificar que el frame no esté vacío
        if frame is None or frame.size == 0:
            print("Error: Frame vacío o inválido")
            return None

        # Definimos el nombre del fichero
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

        # Formatea el frame2 para que sea jpg y luego se crea el fichero con su nombre, se pasa a binario y le indicamos el tipo que es, en este caso jpeg
        res, buffer = cv2.imencode(".jpg", frame)

        # Verificar que la codificación fue exitosa
        if not res:
            print("Error: No se pudo codificar el frame a JPG")
            return None

        file = {"file": (filename, buffer.tobytes(), "image/jpeg")}

        insert = {
            "filename": filename,
            "date": datetime.now().strftime("%Y%m%d_%H%M%S"),
        }

        # Manejar errores de conexión y timeout
        try:
            response = requests.post(
                "http://localhost:5000/api/photo", files=file, data=insert, timeout=10
            )  # Timeout de 10 segundos
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            return response
        except requests.exceptions.Timeout:
            print("Error: Timeout al enviar la foto al servidor")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al servidor")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            return None

    except Exception as e:
        print(f"Error inesperado en take_photo: {e}")
        return None


# FALTA: Control de errores en el bucle principal
# - Verificar que la cámara se abra correctamente
# - Manejar errores si no se puede leer frames de la cámara
# - Liberar recursos de la cámara al finalizar (usar try/finally)
# - Manejar interrupciones del usuario (Ctrl+C)

# Abrimos la cámara (0 = cámara principal)
cap = cv2.VideoCapture(0)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit(1)

try:
    ret, frame1 = cap.read()
    if not ret:
        print("Error: No se pudo leer el primer frame de la cámara")
        exit(1)

    count = 1
    max_photos = 5

    while True:
        try:
            # Leemos el siguiente frame
            ret, frame2 = cap.read()
            if not ret:
                print("Error: No se pudo leer frame de la cámara")
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

                # Intentar tomar la foto y manejar posibles errores
                result = take_photo(frame2)
                if result is not None:
                    print(f"Foto enviada exitosamente: {result.status_code}")
                    count += 1
                else:
                    print("No se pudo enviar la foto")
            else:
                print("Sin movimiento... Valor:", average)

            # Actualizamos el frame anterior
            frame1 = frame2
            time.sleep(2)

        except KeyboardInterrupt:
            print("\nInterrupción del usuario. Cerrando programa...")
            break
        except Exception as e:
            print(f"Error en el bucle principal: {e}")
            # Continuar el bucle en caso de error no crítico
            time.sleep(1)

finally:
    # Liberar recursos de la cámara
    if cap.isOpened():
        cap.release()
        print("Cámara liberada correctamente")
