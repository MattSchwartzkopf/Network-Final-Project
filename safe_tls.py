"""simple_server

simple server to demo async_client
"""


import socket
import time
import random

counter = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 9000))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    print("Accepted connection from {}".format(addr))
    while True:
        conn.sendall(str(counter).encode("ascii"))
        time.sleep(3 * random.random())
        counter += 1
