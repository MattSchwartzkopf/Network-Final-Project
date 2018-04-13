"""async_client

Champlain College CSI-235, Spring 2018
Prof. Josh Auerbach

Bare bones example of asynchronously receiving 
data from server and user input from stdin
"""

import asyncio


class AsyncClient(asyncio.Protocol):

    def __init__(self):
        self.name = ""
        
    def data_received(self, data):
        """simply prints any data that is received"""

        # 'data' is already being grabbed from the server,
        # then output to client
        print("received: ", data)
        

@asyncio.coroutine
def handle_user_input(self, loop):
    """reads from stdin in separate thread
    
    if user inputs 'quit' stops the event loop
    otherwise just echos user input
    """
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        output = (self.name + ": " + message)    
        if message > " ":
            print(output)
        if message == "quit":
            loop.stop()
            return
        #print(message)

@asyncio.coroutine
def user_join(self, loop):
    """ has the user enter username and join server"""
    self.name = input("Enter username: ")
    print(self.name, " has joined the chat!")
    asyncio.async(get_name(self.name))

@asyncio.coroutine
def get_name(name):
    return name

if __name__ == '__main__':
    # Counter for user_join
    counter = 0

    loop = asyncio.get_event_loop()
    client = AsyncClient()
    coro = loop.create_connection(lambda: client, "localhost", 9000)

    #name = asyncio.async(get_name(""))
    
    # For user_join function
    if(counter == 0):
        asyncio.async(user_join(loop, coro))
        counter += 1

    loop.run_until_complete(coro)

    # Start a task which reads from standard input
    asyncio.async(handle_user_input(loop, loop))
    
    try:
        loop.run_forever()
    finally:
        loop.close()   
