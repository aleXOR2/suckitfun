Usage
============

1. Start server

```sh
$ /multiconn_selectors_server.py  127.0.0.1 65432 
```

1. Start client

```sh
$ ./multiconn_selectors_client.py  127.0.0.1 65432 3
```

In this example client started with 3 multiplexed sockets