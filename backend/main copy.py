import os
from flask import Flask, request, jsonify

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
    
if __name__ == '__main__':
    app.run(debug=True, port = PORT_API)