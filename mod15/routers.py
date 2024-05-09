import datetime

from flask import Flask, request, Response, jsonify

from models import init_db, Room, add_room_to_db, get_rooms, Order, add_order_to_db, check_order

app: Flask = Flask(__name__)


@app.route('/add-room', methods=['POST'])
def add_room():
    if request.method == "POST":
        result = add_room_to_db(request.get_json())
        return result


@app.route('/room', methods=['GET'])
def get_room():
    rooms = get_rooms(request.args.get('checkIn'), request.args.get('checkOut'))
    return rooms


@app.route('/booking', methods=['POST'])
def booking():
    if request.method == "POST":
        result = add_order_to_db(request.get_json())
        return result


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
