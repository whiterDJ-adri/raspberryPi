import cv2


# FALTA: Control de errores más robusto en la función de video streaming
# - Verificar disponibilidad de la cámara antes de usarla
# - Manejar desconexiones de cámara durante streaming
# - Liberar recursos de cámara adecuadamente
# - Timeouts para evitar bloqueos indefinidos
def make_video():
    video = None
    try:
        video = cv2.VideoCapture(0)
        if not video.isOpened():
            print("❌ No se pudo abrir la cámara")
            return

        print("✅ Cámara abierta correctamente")

        while True:
            try:
                ret, frame = video.read()
                if not ret:
                    print("⚠️ No se pudo leer un frame")
                    break

                # Verificar que el frame no esté vacío
                if frame is None or frame.size == 0:
                    print("⚠️ Frame vacío recibido")
                    continue

                # print("📸 Frame capturado")  # Puedes dejarlo activo para ver en la terminal

                ret, buffer = cv2.imencode(".jpg", frame)
                if not ret:
                    print("⚠️ Error al codificar frame")
                    continue

                frame = buffer.tobytes()

                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

            except Exception as e:
                print(f"Error durante streaming: {e}")
                break

    except Exception as e:
        print(f"Error al inicializar streaming: {e}")
    finally:
        # Asegurar que la cámara se libera siempre
        if video is not None and video.isOpened():
            video.release()
            print("🔓 Cámara liberada correctamente")
