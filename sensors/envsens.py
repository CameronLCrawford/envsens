from time import sleep
from datetime import datetime
import board
import DHT22
import os
from tinyflux import TinyFlux, Point
from socket import socket, AF_UNIX, SOCK_STREAM
from pickle import dumps

# 20 seconds between each recording
POLL_DELAY = 20

# 'board.D18' refers to GPIO pin on RPI4B
dht = DHT22.DHT22(board.D18)

devices = [dht]

# Connect to database server
sock = socket(AF_UNIX, SOCK_STREAM)
server_address = 'database/db_write_sock'
sock.connect(server_address)

while True:

    for device in devices:
        device_name = device.name
        response = device.poll()
        if response == -1:
            raise Exception("Device '{}' down!".format(device_name))
        point = Point(measurement=device_name, 
                        time=datetime.now(), 
                        tags={"device": device_name}, 
                        fields=response)
        pickled_point = dumps(point)
        sock.sendall(pickled_point)
        sleep(POLL_DELAY)
