import asyncio
import json
import argparse

class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.message = ''
        self.loop = loop
        self.username = ''
        self.data = ''
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.get_username()

    def get_username(self):
        self.username = input("Enter username: ")
        self.send_data()

    def send_data(self):
        username_json = json.dumps({"USERNAME" : self.username})    
        self.transport.write(username_json.encode())
        print('Data sent: {!r}'.format(username_json.encode()))
        
    def data_received(self, data):
        print("here")
        receive = data.decode()
        if receive == 'USERNAME_ACCEPTED':
            print("Received", receive)
            return(asyncio.async(handle_user_input(self.loop)))
        print('Data received: {!r}'.format(data.decode()))
    

@asyncio.coroutine
def handle_user_input(loop):
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
    client = AsyncClient(loop)
    coro =  loop.create_connection(lambda: client,
                                  args.host, args.p)
    
    loop.run_until_complete(coro)
    #asyncio.async(handle_user_input(loop))
    try:
        loop.run_forever()
    except:
        loop.stop()


















