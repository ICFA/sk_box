from flask import Flask, jsonify, make_response
import os

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'application')
SERVICE_NAME = "It doesn't say what service name is needed. Oh, I haven't copied the answer from other students"


@app.route("/hello/<user>")
def hola(user):
    return make_response(
        jsonify(
            {'message': f'Hello from {SERVICE_NAME}, {user}!'}
        ))
 

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
