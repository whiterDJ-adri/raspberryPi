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

app.register_blueprint(record_cam_bp, url_prefix='/api/photo')

if __name__ == '__main__':
   app.run(debug=True)