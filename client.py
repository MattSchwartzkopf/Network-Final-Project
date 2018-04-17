import asyncio

class AsyncClient(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.name = ""
        self.USERNAMES = []
        self.username_count = 1
        
    def connection_made(self, transport):
        transport.write(self.message.encode())
        print(AsyncClient.get_username(self))
        test = asyncio.async(handle_user_input(self.loop))
      
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def get_username(self):
        name = input("Enter username: ")
        self.USERNAMES.append({'Usernames' : {name : self.username_count}})
        self.username_count += 1
        name += " has joined the chat!"
        print("List: ", self.USERNAMES[0])
        return name

@asyncio.coroutine
def handle_user_input(loop):
    """reads from stdin in separate threadif user
        inputs 'quit' stops the event loop
        otherwise just echos user input"""
    while True:
        message = yield from loop.run_in_executor(None, input, "> ")
        return message
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





