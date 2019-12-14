"""
My interpretation of https://docs.python.org/3/howto/sockets.html
"""

import socket
import time
import sys
import random
import logging


MSGS = [
      'When we two parted; In silence and tears, Half broken-hearted To sever for years...............',
      'Pale grew thy cheek and cold, Colder thy kiss; Truly that hour foretold Sorrow to this.........',
      'The dew of the morning Sank chill on my brow - It felt like the warning Of what I feel now.....',
      'Thy vows are all broken, And light is thy fame; I hear thy name spoken, And share in its shame.'
      ]  # Lord Byron ‘When We Two Parted’ exzerpt
MSGS = [msg.encode('ascii') for msg in MSGS]
MSGLEN = 95 # bytes = 95 ascii symbols

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket()
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("nothing has been sent")
            totalsent = totalsent + sent
        logger.info('Sending completed')

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        conn, addr = my_socket.sock.accept()
        logger.info('Connected by %s:%d' % (addr))
        with conn:
            while bytes_recd < MSGLEN:
                buf = min(MSGLEN - bytes_recd, int(MSGLEN / 3))
                logging.info('Receiving chunk with size %d' % buf)
                chunk = conn.recv(buf)
                logger.info('Received chunk %s' % chunk)
                if chunk == b'':
                    raise RuntimeError("empty message received")
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<port> <action>")
    sys.exit(1)

port = int(sys.argv[1])
action = sys.argv[2]
my_socket = MySocket()

try:
    if action == 'send':
        my_socket.connect('127.0.0.1', port)
        deadline = time.time() + 3
        while time.time() < deadline:
            try:
                my_socket.mysend(random.choice(MSGS))
                time.sleep(0.5)
            except socket.timeout:
                logger.error('socket timeout error on send')
                break
    elif action == 'receive':
        my_socket.sock.bind(('127.0.0.1', port))
        my_socket.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.sock.listen()
        while True:
            try:
                time.sleep(5)
                received_data = my_socket.myreceive().decode('ascii')
                logger.info('data received: %s' % received_data)
                time.sleep(1)
            except socket.timeout:
                 logger.error('socket timeout error on receive')
                 break
except KeyboardInterrupt:
     logger.info("caught keyboard interrupt, exiting")
finally:
    logger.info('closing socket')
    my_socket.sock.close()

    