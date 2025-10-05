import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from routes.record_camera import record_cam_bp

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("URL_MONGO")
mongo = PyMongo(app)
app.mongo = mongo

@app.route("/")
def main():
    return render_template("index.html")

# Se registra el blueprint en la aplicación principal Flask.
# Todas las rutas definidas dentro de este blueprint estarán bajo el prefijo '/api/photo'.
# Por ejemplo: una ruta '/' dentro del blueprint pasará a ser '/api/photo/' en la app.
app.register_blueprint(record_cam_bp, url_prefix='/api/photo')

if __name__ == '__main__':
   app.run(debug=True)