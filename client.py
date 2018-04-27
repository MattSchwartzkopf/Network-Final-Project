"""
    Author: Matthew Schwartzkopf , Timothy Feraco, Paul Igo
    Class   : CSI-235
    Assignment: Final Project
    Date Assigned: April 12, 2018
    Due Date: April 26, 2018  11:59pm

    Description:
        This code is a TCP/TLS server for a simple chat.

        Champlain College CSI-235, Spring 2018
        and modified by Matthew Schwartzkopf, Timothy Feraco, Paul Igo.
"""

import asyncio
import json
import argparse
import struct
import time
import calendar
import sys
import socket, ssl

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.username = ''
        self.count = 0
        self.transport = None
        self.data = ''
        self.new_data = ''
        self.length = 0
        self.run= 0
        self.run_once = 0

     # Gets and prints connection to server
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.get_username()

    # Gets username from user
    def get_username(self):
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
        print(message)
        test = json.loads(message[4:])
        
        # Loads all message history
        for i in range(len(test['MESSAGES'])):
            print("", test['MESSAGES'][i][0] + ": ", test['MESSAGES'][i][3])
            self.count += 1
        self.run += 1

    # Prints all new messages
    def messages(self, message):
        new = ''
        # strips broken code from front of 'message'
        if message.__contains__('USERS_') or message.__contains__('JOINED') or message.__contains__('LEFT'):
            counter = 0
            for char in message:
                if counter > 1:
                    new += char
                if char == '{' or char == '}':
                    counter += 1
            test = json.loads(new[4:])
        else:
            test = json.loads(message[4:])
            
        # Prints message properly
        print(test['MESSAGES'][0][0] +": ", test['MESSAGES'][0][3])

    # Prints all new messages received/sent to server
    def print_new_messages(self, data):
        # Prints all new emssages
        if self.run > 0:
            self.new_data += data.decode('ISO-8859-1')
            if self.new_data.__contains__(']]}') and self.new_data.__contains__('MESSAGES'):
                self.messages(self.new_data)
                self.new_data = ''
            if self.new_data.__contains__('USERS_JOINED'):
                joined = json.loads(self.new_data[4:])
                self.new_data = ''
                print("User joined: ", joined['USERS_JOINED'][0])
            if self.new_data.__contains__('USERS_LEFT'):
                left = json.loads(self.new_data[4:])
                self.new_data = ''
                print("User left: ", left['USERS_LEFT'][0])
                

    def grab_server_messages(self, data):
        # Stores all messages from server
        while data:
            self.length += len(data)
            for char in data.decode('ISO-8859-1'):
                self.data += char
                self.run += 1
            break

    # Prints all stored server messages
    def print_server_messages(self):
        if self.data.__contains__(']]}') and self.count == 1:
            if len(self.data) == self.length:
                self.handle_chat(self.data)

    def data_received(self, data):
        # Grabs all stored messages from server
        self.grab_server_messages(data)

        # Prints all new messages
        if self.run_once > 0:
            self.print_new_messages(data)
        self.run_once += 1
        
        # Once all messages are received,
        # Print to console
        self.print_server_messages()

# Loop to continuously send messages to server from user input
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
    parser.add_argument('port', metavar='port', type=int, default=1060,
                        help='TCP port (default 9000)')
        
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    client = AsyncClient(loop)
    coro =  loop.create_connection(lambda: client,
                                   args.host, args.port)
    loop.run_until_complete(coro)

    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=None)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((args.host, args.port))
    print('Connected to host {!r} and port {}'.format(args.host, args.port))

    try:
        loop.run_forever()        
    except:
        loop.stop()








