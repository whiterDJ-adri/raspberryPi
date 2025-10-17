import cv2

video = cv2.VideoCapture(0)

# def make_video():
#     while(True):
#         ret, frame = video.read()
#         if not ret:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpeg',frame)
#             frame = buffer.tobytes()
#             # yield, es como un return pero en vede devolver todo de golpe, lo va devolviendo poco a poco
#             # --frame\r\n --> Indica el inicio de un nuevo bloque
#             # Content-type: image/jpeg\r\n\r\n --> Indica el tipo de contenido que se va a enviar al navegador
#             # + frame + --> Se le pasa el frame
#             # \r\n --> final del bloque
#             yield (b'--frame\r\n'
#        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def make_video():
    if not video.isOpened():
        print("❌ No se pudo abrir la cámara")
        return

    print("✅ Cámara abierta correctamente")

    while True:
        ret, frame = video.read()
        if not ret:
            print("⚠️ No se pudo leer un frame")
            break

        # print("📸 Frame capturado")  # Puedes dejarlo activo para ver en la terminal

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("⚠️ Error al codificar frame")
            continue

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video.release()

