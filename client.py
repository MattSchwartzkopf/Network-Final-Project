import asyncio
import json

class AsyncClient(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.username = ''
        self.username_count = 1
        self.data = ''

    def connection_made(self, transport):
        AsyncClient.get_username(self)
        string = {'data': [{ 'name' : self.username, 'message' : self.message }]}
        username_json = {'USERNAME' : self.username}
        if username_json['USERNAME'] > "":
            print(username_json['USERNAME'])
            transport.write(username_json['USERNAME'].encode())
            transport.write('USERNAME'.encode())
        
        
        print('Data sent: {!r}'.format(username_json))

    def data_received(self, data):
        receive = data.decode()
        if receive == 'USERNAME_ACCEPTED':
            print(receive)
            return(asyncio.async(handle_user_input(self.loop)))
        print('Data received: {!r}'.format(data.decode()))

    def get_username(self):
        self.username = input("Enter username: ")
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
        return(message)
        break
        if message == "quit":
            loop.stop()
            return
    print(message)
    
loop = asyncio.get_event_loop()

# Gets the user input for first use
group1 = asyncio.gather(*[handle_user_input(loop)])
all_groups = asyncio.gather(group1)
results = loop.run_until_complete(all_groups)
message = str(results[0])

coro =  loop.create_connection(lambda: AsyncClient(message, loop),
                              'localhost', 1060)
loop.run_until_complete(coro)
try:
    asyncio.async(handle_user_input(loop))
    loop.run_forever()
except:
     loop.close()





