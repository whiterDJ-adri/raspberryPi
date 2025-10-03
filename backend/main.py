import os
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
import cv2

URL_MONGO = os.getenv("URL_MONGO")

app = Flask(__name__)


app.config["MONGO_URI"] = URL_MONGO

mongo = PyMongo(app)

@app.route("/add", methods=["POST"])
def bd():
    if request.method == 'POST':
        insert = {
            "Nombre": "holaMundo" 
        }
        
        mongo.db["record_camera"].insert_one(insert)
        return jsonify({
            "status": "ok"
        })

@app.route("/photo", methods=["GET"])
def take_photo():
    cap = cv2.VideoCapture(0)  # 0 = primera cámara USB o integrada
    if not cap.isOpened():
        return jsonify({"status": "error", "message": "No se pudo acceder a la cámara"}), 500

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"status": "error", "message": "No se pudo capturar la imagen"}), 500

    # Convertimos la imagen a JPEG
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        return jsonify({"status": "error", "message": "Error al codificar la imagen"}), 500

    # Devolvemos los bytes como respuesta HTTP
    return Response(jpeg.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':
   app.run(debug=True)