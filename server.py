import asyncio
import json
import struct

class AsyncServer(asyncio.Protocol):
    def __init__(self):
        self.USER_LIST = []
        self.transport = None
        self.data = ''
        self.count = 0
        self.connection_from = ''
        
    def connection_made(self, transport):
        if self.transport == None:
            peername = transport.get_extra_info('peername')
            self.connection_from = 'Connection from {}'.format(peername)
            #print('Connection from {}'.format(peername))
            self.transport = transport

    def data_received(self, data):
        message = data.decode()
        self.data += message
        asyncio.async(handle_conversation(self, message))
        print('Data server received: {!r}'.format(message))
        

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
def handle_conversation(self, message):
    temp_history = []
    reader, writer = yield from asyncio.open_connection('localhost', 1060, loop=loop)
    
    # Formats all messages to send
    formatter = json.loads(message[4:])
    username = formatter['USERNAME'][0:]
    
    if self.count == 0:
        address = writer.get_extra_info('peername')
        print('Accepted connection from {}'.format(address))
        print(self.connection_from)
        self.count += 1
        runner = 0
        
    if formatter.__contains__('USERNAME'):
        print(self.USER_LIST)
        for user in self.USER_LIST:
            if user == username:
                print("Found!")
                runner += 1
                break
        if runner == 1:
            print("found!")
        else:
            print("Nope!")
            print(username)
            self.USER_LIST.append(str(username))
            
        
    if formatter.__contains__('MESSAGES'):
        send_back = json.dumps({'MESSAGES' : message}).encode()
        print("Send back: ", send_back)
        
    while True:
        data = b''
        more_data = yield from reader.read(4096)
        print("MORE_DATA: ", more_data)
        if not more_data:
            if data:
                print('Client {} sent {!r} but then closed'
                      .format(address, data))
            else:
                print('Client {} closed socket normally'.format(address))
            return
        data += more_data
    writer.write(data)


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(AsyncServer, 'localhost', 1060)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except:
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
