import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

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

if __name__ == '__main__':
   app.run(debug=True)