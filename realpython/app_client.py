#!/usr/bin/env python3.6

import sys
import socket
import selectors
import traceback

import libclient

sel = selectors.DefaultSelector()


def create_request(action, value):
    if action == "echo":
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(value, encoding="utf-8"),
        )
    elif action == "getrandimg":
        return dict(
            type="text/json",
            encoding="utf-8",
            content={'action': 'getrandimg'}
        )
    else:
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket()
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

if __name__ == '__main__':

    if len(sys.argv) != 5:
        is_getrandimg_query = (sys.argv[3] == "getrandimg")
        if not is_getrandimg_query:
            sys.exit(f'usage: {sys.argv[0]} <host> <port> <action> <value>')
        sys.argv.insert(4, None) # fllling req'd args with dummy values
    
    host, port = sys.argv[1], int(sys.argv[2])
    action, value = sys.argv[3], sys.argv[4]
    request = create_request(action, value)
    start_connection(host, port, request)
    
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events: # key is a selector with events aggregation of read and write, mask is either read or write (what is ready)
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()
