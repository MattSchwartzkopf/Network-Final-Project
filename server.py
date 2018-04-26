import asyncio
import json
import struct

USER_LIST = []
send_back = ''
MESSAGES = []

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
                print("TESTTTTTT: ", word[6:])
                file.write(str(word[6:]) + " ")
            file.close()
        
    def load_chat_history(self):
        print("OLD CHAT HISTORY ")
        with open('chat_history.txt', 'r') as file:
            if file.mode == 'r':
                for line in file:
                    MESSAGES.append(line)
                print(MESSAGES)
        return(MESSAGES)
                
@asyncio.coroutine
def handle_conversation(self, message):
    temp_history = []
    reader, writer = yield from asyncio.open_connection('localhost', 1060, loop=loop)
    
    # Formats all messages to send
    #print(message)
    formatter = json.loads(message[4:])
    
    if self.count == 0:
        address = writer.get_extra_info('peername')
        print('Accepted connection from {}'.format(address))
        print(self.connection_from)
        self.count += 1
        runner = 0
    
    # Build USERNAME stuff
    if formatter.__contains__('USERNAME') and self.count == 1:
        MESSAGES = self.load_chat_history()
        username = formatter['USERNAME'][0:]
        USER_LIST.append(username)
        sender = json.dumps({'USERNAME_ACCEPTED' : True, "INFO" : "Welcome", 'USER_LIST' : USER_LIST, 'MESSAGES' : [MESSAGES]}).encode()
        length = struct.pack("!I", len(sender))
        #send = length + sender
        self.transport.write(length)
        self.transport.write(sender)
        print("Sent: ", sender)

    
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


