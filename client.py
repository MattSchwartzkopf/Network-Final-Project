import asyncio
import json
import argparse
import struct
import time
import calendar
import sys

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.username = ''
        self.count = 0
        self.transport = None
        self.loop = loop
        self.data = ''
        self.new_data = ''
        self.length = 0
        self.run= 0
        
    def connection_made(self, transport):
        self.transport = transport
        # Prints connection to server
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.get_username()
         
    def get_username(self):
        # Gets username from user
        self.username = input("Enter username: ")
        self.send_username_data()
    
    # Sends user's username to server
    def send_username_data(self):
        # Build JSON message
        username_json = json.dumps({"USERNAME" : self.username}).encode()
        # Pack and send message lenth first
        length = struct.pack("!I", len(username_json))
        self.transport.write(length)
        # Send message
        self.transport.write(username_json)
        self.count += 1
        # Start looping sending messages
        asyncio.async(handle_user_input(self))

    # Prints all messages stored in server history
    def handle_chat(self, message):
        test = json.loads(message[4:])
        
        # Loads all message history
        for i in range(len(test['MESSAGES'])):
            print("", test['MESSAGES'][i][0] + ": ", test['MESSAGES'][i][3])
            self.count += 1
        self.run += 1

    # Prints all new messages
    def messages(self, message):
        
        if message.__contains__('USERS_'):
            print("ERROR")
        test = json.loads(message[4:])
        print(test['MESSAGES'][0][0] +": ", test['MESSAGES'][0][3])

    def print_new_messages(self, data):
        # Prints all new emssages
        if self.run > 0:
            self.new_data += data.decode('ISO-8859-1')
            if self.new_data.__contains__(']]}') and self.new_data.__contains__('MESSAGES'):
                self.messages(self.new_data)
                self.new_data = ''
            if self.new_data.__contains__('USERS_'):
                self.new_data = ''

    def grab_server_messages(self, data):
        # Stores all messages from server
        while data:
            self.length += len(data)
            for char in data.decode('ISO-8859-1'):
                self.data += char
                self.run += 1
            break
    def print_server_messages(self):
        if self.data.__contains__(']]}') and self.count == 1:
            if len(self.data) == self.length:
                self.handle_chat(self.data)

    def data_received(self, data):

        # Grabs all stored messages from server
        self.grab_server_messages(data)

        # Prints all new messages
        self.print_new_messages(data)
    
        # Once all messages are received,
        # Print to console
        self.print_server_messages()
                
@asyncio.coroutine
def handle_user_input(self):
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        # Sets time
        timestamp = calendar.timegm(time.gmtime())
        # Build JSON message
        lists = [self.username, 'ALL', timestamp, message]
        message_to_send = json.dumps({'MESSAGES' : [lists]}).encode()
        # Send message length first
        length = struct.pack("!I", len(message_to_send))
        self.transport.write(length)
        # Send full message
        self.transport.write(message_to_send)
        
        if message == "quit":
            loop.stop()
            return

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Async Client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 9000)')
        
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    client = AsyncClient(loop)
    coro =  loop.create_connection(lambda: client,
                                   args.host, args.p)
    loop.run_until_complete(coro)

    try:
        loop.run_forever()        
    except:
        loop.stop()








