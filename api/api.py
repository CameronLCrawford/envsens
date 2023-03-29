from flask import Flask, request, jsonify, make_response
from tinyflux import TinyFlux, TimeQuery, Point, MeasurementQuery
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from json import dumps
import time
from socket import socket, AF_UNIX, SOCK_STREAM
from pickle import loads

# Connect to database server
sock = socket(AF_UNIX, SOCK_STREAM)
server_address = 'database/db_read_sock'
sock.connect(server_address)

app = Flask(__name__)
cors = CORS(app) # Access control

# Endpoints
TEMP_MR = '/temp/most-recent'
TEMP_TEN_MINS = '/temp/past-hour'

@app.get(TEMP_MR)
def temp_mr():
    sock.sendall(b'past-hour')
    data_raw_pickled = sock.recv(20000) # Approx. max data for one hour
    data_raw = loads(data_raw_pickled)
    if len(data_raw) == 0:
        return make_response({'message': 'no recent data'}, 406)
    else:
        return str(data_raw[-1].fields['temp'])


@app.get(TEMP_TEN_MINS)
def temp_ten_mins():
    sock.sendall(b'past-hour')
    data_raw_pickled = sock.recv(20000)  # Approx. max data for one hour
    data_raw = loads(data_raw_pickled)
    data_clean = [(datetime.isoformat(point.time), point.fields["temp"]) for point in data_raw]
    return data_clean

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)