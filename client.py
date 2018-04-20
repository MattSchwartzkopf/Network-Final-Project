import asyncio
import json
import argparse
import socket
import struct
import sys

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.message = ''
        self.loop = loop
        self.username = ''
        self.data = []
        self.transport = None
        self.count = 0
        
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.get_username()
        print('here1')
        
    def get_username(self):
        self.username = input("Enter username: ")
        self.send_data()
        print('here2')
        
    def send_data(self):
        username_json = json.dumps({"USERNAME" : self.username}).encode()
        length = struct.pack("!I", len(username_json))
        self.transport.write(length)
        self.transport.write(username_json)
        print('Data sent: {!r}'.format(username_json))
        print('here3')
        
    def data_received(self, data):
        self.data = data
        
        print('Data received: {!r}'.format(data))
        #message = asyncio.async(handle_user_input(self.loop))
        print('here5')        
      
@asyncio.coroutine
def handle_user_input(loop):
    reader, writer = yield from asyncio.open_connection('csi235.site', 9000, loop=loop)
    
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        print('here7')
        print("idk")
        writer.write(message.encode())
        if message == "quit":
            loop.stop()
            return
        else:
            #AsyncClient.send_message(message)
            break


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
    asyncio.async(handle_user_input(loop))
    try:
        asyncio.async(handle_user_input(loop))
        loop.run_forever()
    except:
        loop.stop()


















