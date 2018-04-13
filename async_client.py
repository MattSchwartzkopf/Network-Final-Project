"""async_client

Champlain College CSI-235, Spring 2018
Prof. Josh Auerbach

Bare bones example of asynchronously receiving 
data from server and user input from stdin
"""

import asyncio


class AsyncClient(asyncio.Protocol):

    def __init__(self, message, loop):
            self.message = message
            self.loop = loop

    def connection_made(self, transport):
        self.message = input("Name: ")
        string = (b'User Joined: ' + self.message.encode())
        #message = handle_user_input(transport)
        print("message: ", self.message.encode())
        transport.write(string)
        print('Data sent: {!r}'.format(self.message))
        
    def data_received(self, data):
        """simply prints any data that is received"""
        print("received: ", data)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

        
@asyncio.coroutine
def handle_user_input(loop):
    """reads from stdin in separate thread
    
    if user inputs 'quit' stops the event loop
    otherwise just echos user input
    """
    while True:
        message = yield from loop.run_in_executor(None, input)
        if message == "quit":
            loop.stop()
            return
        print(message)

if __name__ == '__main__':
       loop = asyncio.get_event_loop()
       message = 'Temp'
       coro = loop.create_connection(lambda: AsyncClient(message, loop), "localhost", 1060)
       while True:
           loop.run_until_complete(coro)
       
       try:
           loop.run_forever()
       except:
           loop.close() 



