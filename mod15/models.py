import datetime
import sqlite3
from typing import Optional, Any

from flask import jsonify, Response


class Room:
    def __init__(self, id: Optional[int], floor: int, beds: int, guestNum: int, price: int):
        self.id: int = id
        self.floor: int = floor
        self.beds: int = beds
        self.guestNum: int = guestNum
        self.price: int = price

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class Order:

    def __init__(self, id: Optional[int], checkIn: datetime, checkOut: datetime, firstName: str, lastName: str,
                 roomId: int):
        self.id = id
        self.checkIn: datetime = checkIn
        self.checkOut: datetime = checkOut
        self.firstName = firstName
        self.lastName = lastName
        self.roomId = roomId


def init_db() -> None:
    with sqlite3.connect('mod15.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS table_rooms 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, floor INTEGER, beds INTEGER, guestNum INTEGER, price INTEGER);
            """)
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS table_bookings 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, checkIn DATETIME, checkOut DATETIME,
            firstName VARCHAR(255), lastName VARCHAR(255), roomId INTEGER,
            FOREIGN KEY (roomId) REFERENCES table_rooms(id))""")


def get_rooms(checkIn: str = None, checkOut: str = None) -> Response:
    with sqlite3.connect('mod15.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from table_rooms")
        rooms = [Room(*row) for row in cursor.fetchall()]
        properties = {"rooms": []}
        for room in rooms:
            properties["rooms"].append({
                "roomId": room.id,
                "floor": room.floor,
                "beds": room.beds,
                "guestNum": room.guestNum,
                "price": room.price,
                "bookingDates": {
                    "checkIn": checkIn,
                    "checkOut": checkOut,
                    "roomId": room.id
                }
            })
        return jsonify(properties)


def add_room_to_db(data):
    room = Room(None, data["floor"], data["beds"], data["guestNum"], data["price"])
    with sqlite3.connect('mod15.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM 'table_rooms' "
                       "WHERE floor = ? AND beds = ? AND guestNum = ? AND price = ?",
                       (room.floor, room.beds, room.guestNum, room.price))
        if cursor.fetchone()[0] > 1:
            return "Is room is already exists", 409
        cursor.execute("""INSERT INTO table_rooms (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)""",
                       (room.floor, room.beds, room.guestNum, room.price))
        return jsonify({"id": room.id})


def add_order_to_db(data):
    checkIn = datetime.datetime.strptime(str(data["bookingDates"]["checkIn"]), "%Y%m%d")
    checkOut = datetime.datetime.strptime(str(data["bookingDates"]["checkOut"]), "%Y%m%d")
    order = Order(None, checkIn, checkOut, data["firstName"], data["lastName"], data["roomId"])
    if check_order(order):
        return Response(status=409)

    with sqlite3.connect('mod15.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO table_bookings "
                       "(checkIn, checkOut, firstName, lastName, roomId) VALUES (?, ?, ?, ?, ?)",
                       (order.checkIn, order.checkOut, order.firstName, order.lastName, order.roomId))
        return jsonify({"roomId": order.roomId})


def check_order(order: Order):
    with sqlite3.connect('mod15.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM `table_bookings` WHERE checkIn >= ? AND checkIn <= ? AND roomId = ?",
                       (order.checkIn, order.checkOut, order.roomId))
        orders = [Order(*row) for row in cursor.fetchall()]
        return orders
