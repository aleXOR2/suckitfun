### Description

Demo of fixed length socket IPC (Inter Proces Comunication)


### Use

1. First start server console

```sh
$ ./fixed_length_message_client_server.py 5005 receive

```

2. then start client on client console:
```sh
$ ./fixed_length_message_client_server.py 5005 send   
2019-12-14 20:56:20,353 - Sending completed
2019-12-14 20:56:20,854 - Sending completed
2019-12-14 20:56:21,355 - Sending completed
2019-12-14 20:56:21,856 - Sending completed
2019-12-14 20:56:22,356 - Sending completed
2019-12-14 20:56:22,857 - Sending completed
2019-12-14 20:56:23,358 - closing socket
```

Server shows connection established by client and provides its adres:
```sh
2019-12-14 20:56:20,353 - Connected by 127.0.0.1:57556
```

After 5 sec server shoud read aul mesages from the socket:
```sh
2019-12-14 20:56:20,353 - Connected by 127.0.0.1:575562019-12-14 20:56:25,356 - Receiving chunk with size 31
2019-12-14 20:56:25,356 - Received chunk b'Pale grew thy cheek and cold, C'
2019-12-14 20:56:25,356 - Receiving chunk with size 31
2019-12-14 20:56:25,356 - Received chunk b'older thy kiss; Truly that hour'
2019-12-14 20:56:25,356 - Receiving chunk with size 31
2019-12-14 20:56:25,356 - Received chunk b' foretold Sorrow to this.......'
2019-12-14 20:56:25,356 - Receiving chunk with size 2
2019-12-14 20:56:25,356 - Received chunk b'..'
2019-12-14 20:56:25,357 - data received: Pale grew thy cheek and cold, Colder thy kiss; Truly that hour foretold Sorrow to this.........
```

Server would not close socket until you interupt the proces (CTRL + C):

```sh
q^C2019-12-14 20:56:38,849 - caught keyboard interrupt, exiting
2019-12-14 20:56:38,849 - closing socket
```
