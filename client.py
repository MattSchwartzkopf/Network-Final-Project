import asyncio
import json
import argparse
from socket import socketpair

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.message = ""
        self.loop = loop
        self.username = ''
        self.username_count = 1
        self.data = ''
        self.name = ""

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        AsyncClient.get_username(self)
        username_json = {"USERNAME" : str(self.name)}
        
        if username_json['USERNAME'] > "":
            transport.write(username_json['USERNAME'].encode())
            transport.write('USERNAME'.encode())
        
        
        print('Data sent: {!r}'.format(username_json))

    def data_received(self, data):
        receive = data.decode()
        print("Recveived: ", data)
        if receive == 'USERNAME_ACCEPTED':
            print("Received", receive)
            return(asyncio.async(handle_user_input(self.loop)))
        print('Data received: {!r}'.format(data.decode()))

    def get_username(self):
        self.username = input("Enter username: ")
        self.name = self.username
        self.username_count += 1
        self.username+= " has joined the chat!"
        return self.username

@asyncio.coroutine
def handle_user_input(loop):
    """reads from stdin in separate threadif user
        inputs 'quit' stops the event loop
        otherwise just echos user input"""
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        if message == "quit":
            loop.stop()
            return
        else:
            return(message)
    print(message)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=9000,
                        help='TCP port (default 9000)')
    
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()

    # Gets the user input for first use
    #group1 = asyncio.gather(*[handle_user_input(loop)])
    #all_groups = asyncio.gather(group1)
    #results = loop.run_until_complete(all_groups)
   # message = str(results[0])
    

    coro =  loop.create_connection(lambda: AsyncClient(loop),
                                  args.host, args.p)
    loop.run_until_complete(coro)
    try:
        asyncio.async(handle_user_input(loop))
        loop.run_forever()
    except:
         loop.close()





