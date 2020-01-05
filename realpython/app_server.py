#!/usr/bin/env python3.6

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    conn.setblocking(False)
    print("accepted connection from", addr)
    message = libserver.Message(sel, conn, addr)
    events = selectors.EVENT_READ
    sel.register(conn, events, data=message)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket()
lsock.setblocking(False)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None) #  If timeout is None, the call will block until a monitored file object becomes ready.
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try: 
                    message.process_events(mask)
                except SystemError:
                    print("main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}"
                )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()