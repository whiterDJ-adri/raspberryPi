import os
from flask import Flask, request, jsonify
import cv2
from datetime import datetime


URL_MONGO = os.getenv("URL_MONGO")

PORT_API = os.getenv("PORT_API")

WEB_PORT = os.getenv("WEB_PORT")


print(PORT_API)
print(WEB_PORT)
print(URL_MONGO)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello country"}
        print(data["data"])
        return jsonify(data)

@app.route("/photo", methods=["GET"])
def take_photo():
    cap = cv2.VideoCapture(0)  # Abrir la cámara USB
    if not cap.isOpened():
        return jsonify({"status": "error", "message": "No se pudo acceder a la cámara"}), 500

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"status": "error", "message": "No se pudo capturar la imagen"}), 500

    # Crear nombre de archivo con fecha y hora
    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join("photos", filename)

    # Crear carpeta si no existe
    os.makedirs("photos", exist_ok=True)

    # Guardar la imagen
    cv2.imwrite(filepath, frame)

    return jsonify({"status": "ok", "file": filepath})
    
if __name__ == '__main__':
    app.run(debug=True, port = PORT_API)