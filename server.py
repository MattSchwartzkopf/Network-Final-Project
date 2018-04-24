import asyncio
import socket
import time
import random
import argparse

@asyncio.coroutine
def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''
        while not data.endswith(b'?'):
            more_data = yield from reader.read(4096)
            print(more_data)
            if not more_data:
                if data:
                    print('Client {} sent {!r} but then closed'
                          .format(address, data))
                    return
            data += more_data
            answer  = ""
        writer.write(answer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Safe TLS client and server')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('port', type=int, help='TCP port number')
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, args.host, args.port)
    print('Listening at {}'.format((args.host, args.port)))
    server = loop.run_until_complete(coro)
    
    
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
