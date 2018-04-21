import asyncio
import json
import argparse
import socket
import struct
import time
import calendar
import sys

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.username = ''
        self.count = 0
    
    def connection_made(self, transport):
        # Prints connection to server
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        
        def get_username(self):
            # Gets username from user
            self.username = input("Enter username: ")
        
        def send_data(self):
            
            if self.count == 0:
                # Build JSON message
                username_json = json.dumps({"USERNAME" : self.username}).encode()
                # Pack and send message lenth first
                length = struct.pack("!I", len(username_json))
                transport.write(length)
                # Send message
                transport.write(username_json)
                print('Data sent: {!r}'.format(username_json))
                self.count += 1
            
            if self.count > 0:
                # Gets message from handle_user_input
                queue = asyncio.Queue()
                message = sys.stdin.readline()
                asyncio.async(queue.put(message))
                # Sets time
                timestamp = calendar.timegm(time.gmtime())
                # Build JSON message
                lists = [self.username, 'ALL', timestamp, message]
                message2 = json.dumps({'MESSAGES' : lists}).encode()
                print(message2)
                # Send message length first
                length = struct.pack("!I", len(message2))
                transport.write(length)
                # Send full message
                transport.write(message2)
        
        # Calls functions accordingly
        get_username(self)
        send_data(self)

    def data_received(self, data):
        # Prints any and all received data
        print('Data received: {!r}'.format(data.decode()))

@asyncio.coroutine
def handle_user_input(loop):
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        if message == "quit":
            loop.stop()
            return

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=9000,
                        help='TCP port (default 9000)')
        
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    client = AsyncClient(loop)
    coro =  loop.create_connection(lambda: client,
                                   args.host, args.p)

    loop.run_until_complete(coro)

    try:
        asyncio.async(handle_user_input(loop))
        loop.run_forever()
    except:
        loop.stop()


















