from socket import socket, AF_UNIX, SOCK_STREAM
from threading import Thread, Lock
from tinyflux import TinyFlux, TimeQuery
from datetime import datetime, timedelta
import os
from pickle import dumps, loads

DB_PATH = 'database/db.csv'
WRITE_SOCKET_PATH = 'database/db_write_sock'
READ_SOCKET_PATH = 'database/db_read_sock'

# Singleton represents a TinyFlux DB that has a lock so can be
# handled by multiple threads safely
class DB:
    def __init__(self, db_path):
        self.db = TinyFlux(db_path)
        self.db_lock = Lock()

    def insert(self, Point):
        with self.db_lock:
            self.db.insert(Point)

    def search(self, query):
        # 'query' is a string because TimeQuery object can't be pickled
        # and API only makes a small number of well-defined distinct searches
        if query == b'past-hour':
            Time = TimeQuery()
            past_hour = datetime.now() - timedelta(minutes=60)
            query = Time > past_hour
        with self.db_lock:
            result = self.db.search(query)
            return result

def handle_db_write():
    if os.path.exists(WRITE_SOCKET_PATH):
        os.remove(WRITE_SOCKET_PATH)
    with socket(AF_UNIX, SOCK_STREAM) as sock:
        sock.bind(WRITE_SOCKET_PATH)
        sock.listen()
        connection, client = sock.accept()
        while True:
            data = connection.recv(1024)
            if not data:
                break
            point = loads(data)
            db.insert(point)
    os.remove(WRITE_SOCKET_PATH) 

def handle_db_read():
    if os.path.exists(READ_SOCKET_PATH):
        os.remove(READ_SOCKET_PATH)
    with socket(AF_UNIX, SOCK_STREAM) as sock:
        sock.bind(READ_SOCKET_PATH)
        sock.listen()
        connection, client = sock.accept()
        while True:
            data = connection.recv(1024)
            if not data:
                break
            search_response = db.search(data)
            connection.sendall(dumps(search_response))
    os.remove(READ_SOCKET_PATH) 

if __name__ == '__main__':
    db = DB(DB_PATH)
    # Initialise two threads that handle writing and reading to/from
    # db, respectively. NB there is a lock on the db to prevent collisions
    writer = Thread(target=handle_db_write)
    reader = Thread(target=handle_db_read)
    writer.start()
    reader.start()
