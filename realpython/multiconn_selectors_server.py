#!/usr/bin/env python3
import logging
import sys
import socket
import selectors
import types
from time import time


TIMEOUT = 15 # sec

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


sel = selectors.DefaultSelector() # on Unix it is select.select - it is blocking as it waits for socket ready for I/O


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    conn.setblocking(False)
    logger.info("accepted connection from %s" % repr(addr))
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")  # SimpleNamespace is  just like Object but permits dict valus initialization
    events_mask = selectors.EVENT_READ | selectors.EVENT_WRITE  # creating events mask for both read and write events ?
    sel.register(conn, events_mask, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # bitwise and - &
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            logger.info("closing connection to %s" % repr(data.addr))
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            logger.info("echoing %s to %s" % (repr(data.outb), data.addr))
            sent = sock.send(data.outb)  # returns the number of B sent https://docs.python.org/3/library/socket.html?highlight=socket%20send#socket.socket.send
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.setblocking(False)
lsock.listen()
print("listening on", (host, port))
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=TIMEOUT)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
