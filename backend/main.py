import os
from flask import Flask, request, jsonify, Response, render_template
from flask_pymongo import PyMongo

import cv2
from datetime import datetime

import requests

URL_MONGO = os.getenv("URL_MONGO")

app = Flask(__name__)


app.config["MONGO_URI"] = URL_MONGO

mongo = PyMongo(app)

# En la raiz, se carga el index.html
@app.route("/")
def main():
    return render_template("index.html")

# @app.route("/add", methods=["POST"])
# def bd():
#     if request.method == 'POST':
#         insert = {
#             "Nombre": "holaMundo" 
#         }
        
#         mongo.db["record_camera"].insert_one(insert)
#         return jsonify({
#             "status": "ok"
#         })

@app.route("/photo", methods=["POST"])
def take_photo():
    # Seleccionamos la camara 0, suele ser la que hay por defecot
    cap = cv2.VideoCapture(0)
    
    # Devuelve error en caso de que no se pueda acceder a la camara
    if not cap.isOpened():
        return jsonify({"status": "error", "message": "No se pudo acceder a la cámara"}), 500

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"status": "error", "message": "No se pudo capturar la imagen"}), 500
    
    # Definimos el nombre de la carpeta donde se van a guardar las imagenes
    ruta = "photos"
    # Para el nombre del fichero, se obtiene la fecha de hoy, se le da el formato a string que queremos y se le concatena .jgp
    nombre_fichero = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg";
    # Se define la ruta del fichero que es la que mas adelante se va a guardar en la bd
    ruta_fichero = os.path.join(ruta, nombre_fichero)
    
    # Se guarda el frame capturado anteriormente en la ruta especificada
    cv2.imwrite(ruta_fichero, frame)
    
    # Una vez guardado, hay que hacer el insert a la bd con la ruta, nombre hora...
    insert = {
        "fichero": nombre_fichero,
        "fecha": datetime.now().strftime('%Y%m%d_%H%M%S'),
        "ruta": ruta_fichero
    }
    
    mongo.db["record_camera"].insert_one(insert)
    n8n_webhook_url = "http://localhost:5678/webhook-test/http://127.0.0.1:5000/photo"
    payload = {
        "fichero": nombre_fichero,
        "ruta": ruta_fichero,
        "fecha": insert["fecha"]
    }

    files = {'file': (nombre_fichero, open(ruta_fichero, 'rb'), 'image/jpeg')}
    
    try:
        response = requests.post(n8n_webhook_url, files=files, data={'fecha': insert["fecha"]})

        print("Respuesta de n8n:", response.text)
    except Exception as e:
        print("Error enviando a n8n:", e)

    # Se devuelve un json con el estado y la ruta donde se encuentra el fichero
    # return jsonify({"status": "ok", "ruta": ruta_fichero})
    return render_template("fotos.html"), 200

if __name__ == '__main__':
   app.run(debug=True)