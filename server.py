import asyncio

class AsyncServer(asyncio.Protocol):
    def __init__(self):
        self.USERS_JOINED = []
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        #print('Close the client socket')
       # self.transport.close()
        
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
                
@asyncio.coroutine
def handle_conversation():
    temp_history = []
    count = 0
    reader, writer = yield from asyncio.open_connection('localhost', 1060,
                                                        loop=loop)
        
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    
    while True:
        data = b''
        while not data.endswith(b'?'):
            more_data = yield from reader.read(4096)
            if not more_data:
                if data:
                    print('Client {} sent {!r} but then closed'
                          .format(address, data))
                else:
                    print('Client {} closed socket normally'.format(address))
                return
            data += more_data
        writer.write(data)


        
loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(AsyncServer, 'localhost', 1060)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    handle_conversation()
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()



'''

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



'''
