import asyncio
import socket
import time
import random
import json

class AsyncClient (asyncio.Protocol):

    def __init__(self):
        self.json_user_list = {}
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        string = ""
        string2 = ""
        
        for char in message:
            if char == 'U':
                break
            else:
                string += char
        print("\n", 'Data received: {!r}'.format(string))
        
        if message.__contains__('USERNAME'):
            # read until "has"
            for char in message:
                if char == " ":
                    break
                else:
                    string2 += char
                    
            #print('Send: {!r}'.format("USERNAME_ACCEPTED"))
            self.json_user_list['USER_LIST']  = []
            self.json_user_list['USER_LIST'].append(string2)
            print("USER LIST: ", self.json_user_list)
            data = "USERNAME_ACCEPTED"
            self.transport.write(data.encode())    
        
            

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(AsyncClient, 'localhost', 1060)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()
# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


