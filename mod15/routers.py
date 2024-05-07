import datetime

from flask import Flask, request, Response, jsonify

from models import init_db, Room, add_room_to_db, get_rooms, Order, add_order_to_db, check_order

app: Flask = Flask(__name__)


@app.route('/add-room', methods=['POST'])
def add_room():
    if request.method == "POST":
        data = request.get_json()
        room = Room(
            id=None,
            floor=data["floor"],
            beds=data["beds"],
            guestNum=data["guestNum"],
            price=data["price"]
        )
        add_room_to_db(room)
        return jsonify({"id": room.id}), 201


@app.route('/get-rooms', methods=['GET'])
def get_room():
    rooms = get_rooms(request.args.get('checkIn'), request.args.get('checkOut'))
    properties = {}
    properties["rooms"] = []
    for room in rooms:
        properties["rooms"].append({
            "roomId": room.id,
            "floor": room.floor,
            "beds": room.beds,
            "guestNum": room.guestNum,
            "price": room.price,
            "bookingParams": {
                "checkIn": request.args.get('checkIn'),
                "checkOut": request.args.get('checkOut'),
                "roomId": room.id
            }
        })
    return jsonify(properties)


@app.route('/book-room', methods=['POST'])
def booking():
    if request.method == "POST":
        data = request.get_json()
        checkIn = datetime.datetime.strptime(str(data["bookingDates"]["checkIn"]), "%Y%m%d")
        checkOut = datetime.datetime.strptime(str(data["bookingDates"]["checkOut"]), "%Y%m%d")
        order = Order(
            id=None,
            checkIn=checkIn,
            checkOut=checkOut,
            firstName=data["firstName"],
            lastName=data["lastName"],
            roomId=data["roomId"]
        )
        if check_order(order):
            return Response(status=409)
        order_id = add_order_to_db(order)
        return jsonify({"roomId": order_id}), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
