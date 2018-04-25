import asyncio
import socket
import time
import random
import argparse
import json
import sys

class AsyncServer(asyncio.Protocol):
    def __init__(self, loop):
        self.USERS_JOINED = []
        
    def store_chat_history(history):
        with open('chat_history.txt', 'a') as file:
            for word in history:
                print("TESTTTTTT: ", word[6:])
                file.write(str(word[6:]))
                file.write("\n")
            file.close()
        
    def load_chat_history():
        print("OLD CHAT HISTORY ")
        with open('chat_history.txt', 'r') as file:
            if file.read() == '':
                print('None \n')
            else:
                print("\n") 
                print(file.read())

    def user_joined(username):
        new_user = json.dumps({'USERS_JOINED' : username})
        print('')
    
@asyncio.coroutine
def handle_conversation(reader, writer):
    temp_history = []
    count = 0
    
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
        
    while True:
        if count == 0:
            AsyncServer.load_chat_history()
            count += 1
        
        data = b''
        while not data.endswith(b'~'):
            received = yield from reader.read(4096)
            temp_history.append(received)
            json_string = json.loads(received[4:])

            # Loads username
            if json_string.__contains__('USERNAME') :
                #AsyncServer.user_joined(json_string['USERNAME'][0:])
                username = json_string['USERNAME'][0]
                new_user = {'USERS_JOINED' : username}
                sender = json.dumps(new_user).encode()
                
                print(sender)
                writer.write(sender)

            # Loads USERS_JOINED
            
            # Loads USERS_LEFT

            # Stores Messages
            
            
            
            if not received:
                if data:
                    print('Client {} sent {!r} but then closed'.format(address, data))
                    AsyncServer.store_chat_history(temp_history)
                    return
            data += received
        writer.write(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Safe TLS client and server')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('port', type=int, help='TCP port number')
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, args.host, args.port)
    print('Listening at {}'.format((args.host, args.port)))
    server = loop.run_until_complete(coro)
    
    
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
