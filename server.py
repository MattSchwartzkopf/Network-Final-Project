import asyncio
import json
import struct

USER_LIST = []
send_back = ''
MESSAGES = []
STORED_DATA = []

class AsyncServer(asyncio.Protocol):
    def __init__(self):
        #self.USER_LIST
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
        new_data = self.data
    
        #print('Close the client socket')
       # self.transport.close()
        
    def store_chat_history(self, history):
        with open('chat_history.txt', 'a') as file:
            for word in history:
                file.write("\n" + str(word))
            file.close()
        
    def load_chat_history(self):
        print("OLD CHAT HISTORY ")
        i = 0
        test = []
        new = []
        
        with open('chat_history.txt', 'r') as file:
            # Store all data
            if file.mode == 'r':
                test.append(file.read().splitlines())
                
            # Split data into 4
            r = 3
            for i in range(len(test[0])):
                new.append(test[0][i])
                if i > 0 and i % r == 0 or i == len(test[0]):
                    MESSAGES.append(new)
                    new = []
                    r += 4
            #print(MESSAGES)
        return(MESSAGES)
    
    def send_user_acception(self, message):
        message2 = self.load_chat_history()
        MESSAGES = message2
        
        # Formats all messages to send
        #print(message)
        formatter = json.loads(message[4:])
        
        username = formatter['USERNAME'][0:]
        USER_LIST.append(username)
        sender = json.dumps({'USERNAME_ACCEPTED' : True, "INFO" : "Welcome", 'USER_LIST' : USER_LIST, 'MESSAGES' : MESSAGES}).encode()
        length = struct.pack("!I", len(sender))
        self.transport.write(length)
        self.transport.write(sender)
        print("\nSender: ", sender)
        self.user_joined(username)
        self.count += 1
        
    def send_new_message(self, message):
        # Formats all messages to send
        formatter = json.loads(message[4:])

        # Send message
        username = formatter['MESSAGES'][0][0]
        dest = formatter['MESSAGES'][0][1]
        timestamp = formatter['MESSAGES'][0][2]
        message = formatter['MESSAGES'][0][3]
        MESSAGES = [username, dest, timestamp, message]
        self.store_chat_history(MESSAGES)
        sender = json.dumps({'MESSAGES' : [MESSAGES]}).encode()
        length = struct.pack("!I", len(sender))
        self.transport.write(length)
        self.transport.write(sender)

    def user_joined(self, message):
        joined = json.dumps({'USERS_JOINED' : message}).encode()
        length = struct.pack("!I", len(joined))
        self.transport.write(length)
        self.transport.write(joined)

@asyncio.coroutine
def handle_conversation(self, message):
    reader, writer = yield from asyncio.open_connection('localhost', 1060, loop=loop)
    formatter = json.loads(message[4:])
        
    if self.count == 0:
        address = writer.get_extra_info('peername')
        print('Accepted connection from {}'.format(address))
        print(self.connection_from)
        self.count += 1
        runner = 0
    
    # Build USERNAME stuff
    if formatter.__contains__('USERNAME') and self.count == 1:
        self.send_user_acception(message)

    if formatter.__contains__('MESSAGES') and self.count > 1:
        self.send_new_message(message)

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


