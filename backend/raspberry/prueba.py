import cv2

def listar_camaras(max_camaras=10):
    """
    Lista todas las cámaras disponibles, mostrando su índice y nombre.
    Compatible con Windows, Linux y Raspberry Pi.
    """
    camaras = []
    print("🔍 Buscando cámaras conectadas...")

    for index in range(max_camaras):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # CAP_DSHOW mejora compatibilidad en Windows
        if cap.isOpened():
            nombre = cap.getBackendName()
            camaras.append((index, nombre))
            print(f"✅ Cámara detectada en índice {index} (Backend: {nombre})")
            cap.release()
        else:
            cap.release()

    if not camaras:
        print("🚫 No se detectó ninguna cámara.")
    return camaras


def abrir_camara_por_indice(index, label):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"❌ No se pudo abrir la cámara {label} (índice {index})")
        return None
    print(f"🎥 Cámara {label} abierta (índice {index})")
    return cap


def main():
    camaras = listar_camaras()

    if len(camaras) == 0:
        return
    elif len(camaras) == 1:
        print("⚠️ Solo se detectó una cámara, se abrirá solo esa.")
        cam1 = abrir_camara_por_indice(camaras[0][0], "Cam1")
        cam2 = None
    else:
        cam1 = abrir_camara_por_indice(camaras[0][0], "Cam1")
        cam2 = abrir_camara_por_indice(camaras[1][0], "Cam2")

    print("📸 Mostrando video (presiona 'q' para salir)")

    while True:
        if cam1:
            ret1, frame1 = cam1.read()
            if ret1:
                cv2.imshow("Camara 1", frame1)
        if cam2:
            ret2, frame2 = cam2.read()
            if ret2:
                cv2.imshow("Camara 2", frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if cam1: cam1.release()
    if cam2: cam2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
