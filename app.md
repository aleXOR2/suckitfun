Usage
============

1. Start server

    ```sh
    $ ./app_server.py  127.0.0.1 65432
    ```

1. Start client

    ```sh
    $ ./app_client.py  127.0.0.1 65432 search morpheus
    ```

You can only specify search of following types of requests:

* search <value> - fetch the string matches the query value you'd like to get from hardcoded db
* searchpartial <value> - fetch all the database entries where the `value` member of
* getrandimg - save a rand img from a server location
* echo <value> - echo the `value` in binary format

All other queries are treated as non-existent and replied with:
`{'result': 'Error: invalid action "${query_name}".'}`

Examples
========

### Search request

In this example client asks server to execute search command with value 'morpheus' and return the response (or error):-)

Server console

```sh
$ ./app_server.py  127.0.0.1 65432
listening on ('127.0.0.1', 65432)
accepted connection from ('127.0.0.1', 47228)
received request {'action': 'search', 'value': 'morpheus'} from ('127.0.0.1', 47228)
sending b'\x00g{"byteorder": "little", "content-type": "text/json", "content-encoding": "utf-8", "content-length": 43}{"result": "Follow the white rabbit. \xf0\x9f\x90\xb0"}' to ('127.0.0.1', 47228)
closing connection to ('127.0.0.1', 47228)
```

Client console:

```sh
 ./app_client.py 127.0.0.1 65432 search morpheus
starting connection to ('127.0.0.1', 65432)
sending b'\x00g{"byteorder": "little", "content-type": "text/json", "content-encoding": "utf-8", "content-length": 41}{"action": "search", "value": "morpheus"}' to ('127.0.0.1', 65432)
cleaning buffer
received response {'result': 'Follow the white rabbit. 🐰'} from ('127.0.0.1', 65432)
got result: Follow the white rabbit. 🐰
closing connection to ('127.0.0.1', 65432)
```

### Non existing request

In case you specify not existing request (say get):

```sh
    ./app_client.py 127.0.0.1 65432 get money
    starting connection to ('127.0.0.1', 65432)
    sending b'\x00g{"byteorder": "little", "content-type": "text/json", "content-encoding": "utf-8", "content-length": 35}{"action": "get", "value": "money"}' to ('127.0.0.1', 65432)
    cleaning buffer
    received response {'result': 'Error: invalid action "get".'} from ('127.0.0.1', 65432)
    got result: Error: invalid action "get".
    closing connection to ('127.0.0.1', 65432)
```

### Echo request

This example depicts echo message (it uses binary format by default).
Server console - start server as usual
Client console:

```sh
    $ ./app_client.py 127.0.0.1 65432 echo "Privet Gandon"
    starting connection to ('127.0.0.1', 65432)
    sending b'\x00\x7f{"byteorder": "little", "content-type": "binary/custom-client-binary-type", "content-encoding": "binary", "content-length": 13}Privet Gandon' to ('127.0.0.1', 65432)
    cleaning buffer
    received binary/custom-server-binary-type response from ('127.0.0.1', 65432)
    got response: b"Echoing message with length=13: b'Privet Gandon'"
    closing connection to ('127.0.0.1', 65432)
```

### Getrandimg request

Server console:

```sh
$ ./app_server.py  127.0.0.1 65432
listening on ('127.0.0.1', 65432)
accepted connection from ('127.0.0.1', 46746)
received request {'action': 'getrandimg'} from ('127.0.0.1', 46746)
sending b'\x00k{"byteorder": "little", "content-type": "image/jpeg", "content-encoding": "binary", "content-length": 2995}\xff\xd8\xff...' to ('127.0.0.1', 46746)
closing connection to ('127.0.0.1', 46746)
```

Client console:

```sh
$ ./app_client.py 127.0.0.1 65432 getrandimg
starting connection to ('127.0.0.1', 65432)
sending b'\x00g{"byteorder": "little", "content-type": "text/json", "content-encoding": "utf-8", "content-length": 24}{"action": "getrandimg"}' to ('127.0.0.1', 65432)
cleaning buffer
received image and stored at /tmp/tmp09lvvtum.jpg
closing connection to ('127.0.0.1', 65432)
```

After that you can copy link to the image and paste in into any image viewer or browser addressbar